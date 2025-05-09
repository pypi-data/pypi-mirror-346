---
title: "Using Remote Object Storage"
summary: "Persist and access ContextFrame datasets on S3, GCS, Azure, or any Object Store supported by Lance."
---

## Using Remote Object Storage with ContextFrame

> **TL;DR** — A ContextFrame dataset is just a *Lance* dataset under the hood. Point it at `s3://…`, `gs://…`, or `az://…` **and your existing code keeps working**.  All that changes is the dataset URI (plus, if required, a credentials dictionary via `storage_options` or environment variables).

ContextFrame relies on the [Lance](https://lancedb.github.io/lance/index.html) columnar format for storage.  One of the nicest features of Lance is its **first-class support for object stores** such as:

* **Amazon S3** (and S3-compatible stores like MinIO or DigitalOcean Spaces)
* **Google Cloud Storage**
* **Azure Blob Storage**

This means you can keep all of your frames in durable and infinitely scalable cloud storage **without changing a single line of code**—just adjust the dataset URI.

Below you will find concrete, copy-paste ready examples for the three major providers.  Each example covers:

1. **Writing** a brand-new dataset (`FrameDataset.create` or `FrameRecord.save`).
2. **Opening** an existing dataset for reading or appending.

All snippets assume you have already installed the extra dependencies:

```bash
pip install contextframe
```

---

## 1. Amazon S3

### Credentials

Lance follows the [standard AWS environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html):

```bash
export AWS_ACCESS_KEY_ID="<your-access-key>"
export AWS_SECRET_ACCESS_KEY="<your-secret-key>"
export AWS_REGION="us-east-1"
```

You can also pass the values programmatically via `storage_options`.

### Creating a dataset on S3

```python
from contextframe import FrameRecord

record = FrameRecord.create(
    title="S3 Example",
    content="Stored on S3!",
    author="Alice",
)

s3_uri = "s3://my-bucket/demo_dataset.lance"

# The convenience helper automatically creates the dataset if it doesn't exist
record.save(s3_uri, storage_options={
    "region": "us-east-1",      # required for S3-compatible targets
    # "endpoint": "http://localhost:9000",  # uncomment for MinIO etc.
})
```

Behind the scenes `record.save(...)` translates to a call to `lance.write_dataset(..., storage_options=...)`.

### Opening an existing S3 dataset

```python
from contextframe import FrameDataset

ds = FrameDataset.open(
    "s3://my-bucket/demo_dataset.lance",
    storage_options={"region": "us-east-1"}
)
print(ds.count_by_filter("True"))  # total number of rows
```

> **Tip** — If you need advanced settings (timeouts, proxy, SSE-KMS, …) simply add the documented keys to the same `storage_options` dict.  Refer to the full [Lance object-store documentation](https://lancedb.github.io/lance/object_store.html).

---

## 2. Google Cloud Storage

```bash
export GOOGLE_SERVICE_ACCOUNT="/path/to/service_account.json"
```

```python
from contextframe import FrameDataset, FrameRecord

uri = "gs://my-gcs-bucket/cf_docs.lance"

# Write a new dataset
FrameDataset.create(uri, overwrite=True, storage_options={
    "service_account": "/path/to/service_account.json",
})

# Read it back
ds = FrameDataset.open(uri, storage_options={"service_account": "/path/to/service_account.json"})
```

---

## 3. Azure Blob Storage

```bash
export AZURE_STORAGE_ACCOUNT_NAME="myaccount"
export AZURE_STORAGE_ACCOUNT_KEY="<key>"
```

```python
from contextframe import FrameDataset

uri = "az://my-container/archive.lance"

# Create or open with explicit credentials
options = {"account_name": "myaccount", "account_key": "<key>"}
frame_ds = FrameDataset.create(uri, overwrite=True, storage_options=options)
```

---

## Atomic commits & concurrent writers

Most object stores guarantee **atomic commits** out-of-the-box, which means
two processes cannot corrupt a dataset by writing at the same time.  Lance (and
therefore ContextFrame) automatically benefits from this on:

* the **local file system**
* **Google Cloud Storage**
* **Azure Blob Storage**

### Why S3 is special

Amazon S3 lacks native atomic rename semantics, so concurrent writes **can**
lead to race conditions.  Lance offers **two complementary strategies** for
safe multi-writer scenarios:

#### 1. Custom `commit_lock` context manager

Provide your own distributed lock (Redis, Zookeeper, etc.) and pass it to
`lance.write_dataset` (indirectly used by `FrameDataset.create` and
`FrameRecord.save`).  A minimal example:

```python
from contextlib import contextmanager
import redis

@contextmanager
def commit_lock(version: int):
    lock = redis.Redis().lock("my-dataset-lock", timeout=60)
    lock.acquire()
    try:
        yield  # perform the write
    finally:
        lock.release()

# Usage (identical for FrameDataset.create, FrameRecord.save, etc.)
import lance, pyarrow as pa
# tbl = pa.Table.from_pandas(...)
lance.write_dataset(tbl, "s3://bucket/path/myset.lance", commit_lock=commit_lock)
```

All writers **must** use the same mechanism for Lance to detect conflicts.

#### 2. DynamoDB-based manifest store *(experimental)*

Skip the manual locking altogether and leverage a DynamoDB table by switching
the URI scheme to **`s3+ddb://`** and appending `?ddbTableName=<table>`:

```python
import lance

# The DynamoDB table must have a primary key `base_uri` (string) +
# a sort key `version` (number).
ds = lance.dataset(
    "s3+ddb://my-bucket/myset.lance?ddbTableName=contextframe_manifest"
)
```

This feature is considered *experimental* by the Lance team but works well for
many real-world workloads.

> 🔒 **Best practice** — If you only have a **single writer** (e.g. a batch
> job or CI pipeline) you can safely ignore this section.  For collaborative
> or streaming scenarios pick one of the two strategies above.

---

## Frequently Asked Questions

### Do I need to change anything else in my code?

No.  All higher-level helpers (`nearest`, `full_text_search`, collection helpers, …) work exactly the same way irrespective of where the dataset lives.

### Can I mix local and remote datasets?

Absolutely.  Each dataset URI is handled independently—store training data on S3, scratch data on local disk, and evaluation sets on GCS if you wish.

### How do I enable concurrent writes on S3?

Lance offers an *experimental* DynamoDB-based commit mechanism (see the upstream docs).  You can activate it by switching to the special `s3+ddb://` URI scheme and adding `?ddbTableName=<name>`.

---

## Next Steps

* Head back to the [Python API reference](python_api.md) for class-level details.
* Consult the official [Lance object store documentation](https://lancedb.github.io/lance/object_store.html) for advanced configuration options.
* Follow the [Quick-Start](../quickstart.md) guide to learn the basics of ContextFrame.
