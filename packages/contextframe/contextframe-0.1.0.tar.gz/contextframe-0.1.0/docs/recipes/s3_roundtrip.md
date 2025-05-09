# Recipe – S3 Round-Trip

Store and read a dataset on Amazon S3 (or any S3-compatible service) with **zero code changes** beyond the URI.

---

## 1. Environment & packages

```bash
export AWS_ACCESS_KEY_ID="<key>"
export AWS_SECRET_ACCESS_KEY="<secret>"
export AWS_REGION="us-east-1"

pip install contextframe
```

## 2. Write a dataset directly to S3

```python
from contextframe import FrameRecord

rec = FrameRecord.create(title="S3 Example", content="Stored on S3!")

S3_URI = "s3://my-bucket/cf_demo.lance"
rec.save(S3_URI, storage_options={"region": "us-east-1"})
```

## 3. Append from another process / machine

```python
from contextframe import FrameDataset, FrameRecord

new_doc = FrameRecord.create(title="Another doc", content="Hello from EC2")
FrameDataset.open(S3_URI, storage_options={"region": "us-east-1"}).add(new_doc)
```

## 4. List versions & cleanup

```bash
contextframe version list $S3_URI --json | jq
```

```python
from contextframe import FrameDataset
FrameDataset.open(S3_URI, storage_options={"region": "us-east-1"})._native.cleanup_old_versions(keep=5)
```

### Concurrency note

S3 lacks atomic renames.  For **multiple writers** use a DynamoDB manifest store (switch URI to `s3+ddb://…`) **or** pass an external `commit_lock`.
