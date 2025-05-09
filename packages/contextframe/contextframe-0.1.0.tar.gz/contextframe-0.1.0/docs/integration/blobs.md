---
title: "Working with Blobs (Large Binary Data)"
summary: "Store and lazily retrieve images, audio, videos and any binary objects with ContextFrame."
---

## Storing Large Binary Objects

ContextFrame supports **multimodal workloads** – you can attach images, audio, video or arbitrary binary files to any `FrameRecord`.

Under the hood the library uses the [*Blob as Files* feature of Lance](https://lancedb.github.io/lance/blob.html) which turns a binary column into a **lazy, file-like object** – meaning you never have to load the entire object into memory unless you really want to.

## How it works

1. The canonical schema defines a `raw_data` column as `large_binary()` and marks it with `"lance-encoding:blob": "true"`.  This tells the Lance engine that the column should be stored as an external blob segment.
2. When you create a `FrameRecord` you can pass a byte buffer and a MIME-type:

    ```python
    from contextframe import FrameRecord, MimeTypes

    jpeg_bytes = open("cat.jpg", "rb").read()
    rec = FrameRecord.create(
        title="Cute Cat",
        content="An image of a cute cat.",
        raw_data=jpeg_bytes,
        raw_data_type=MimeTypes.IMAGE_JPEG,
    )
    rec.save("cat_collection.lance")
    ```

3. Later, instead of materialising the whole column you can retrieve a **streaming blob file**:

```python
from contextframe import FrameDataset
import av  # or PIL, ffmpeg, etc.

# Open (local or remote) dataset
cat_ds = FrameDataset.open("cat_collection.lance")

# Map UUID ➜ row index
tbl = cat_ds._native.to_table(columns=["uuid"])  # small & cheap
row_idx = tbl.column("uuid").to_pylist().index(rec.uuid)

blob_files = cat_ds._native.take_blobs([row_idx], column="raw_data")
with av.open(blob_files[0]) as container:
    # do your video/image decode without loading entire file
    ...
```

> **Tip** — You can slice videos, extract frames, stream audio chunks, etc. directly from the returned `BlobFile` object.

## Best practices

* **Use appropriate MIME types** (`raw_data_type`) so downstream consumers know how to decode the blob.
* Keep metadata (e.g. *duration*, *resolution*, *fps*) in the normal scalar columns for fast predicate push-down.
* Combine blobs with vector embeddings to enable multimodal similarity search.

## Frequently Asked Questions

### Is the blob column downloaded when I call `to_table()`?

No.  Only the metadata (offsets) is read.  The actual bytes are fetched lazily when you access the `BlobFile`.

### Does it work on object storage like S3 or GCS?

Yes.  Blob data is chunked and stored alongside the manifest files, honouring the same URI you pass to `FrameDataset.create` or `FrameRecord.save`.  All the concurrency/lock recommendations for S3 still apply.

### Can I have multiple blob columns?

Absolutely – just add additional `large_binary()` fields with the same blob metadata flag when defining a custom schema.
