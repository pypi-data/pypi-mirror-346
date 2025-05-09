# Frequently Asked Questions

## “ImportError: No module named _lance”

Install the Lance engine extras:

```bash
pip install contextframe
```

---

## “ValueError: Vector length X != embedding dimension 1536”

Your query or record vector must have the exact dimension configured for the dataset (default 1536).  Re-encode or pad/truncate the array.

---

## “Why is my `.lance` directory empty?”

You created a dataset but never inserted a record.  Call `record.save(path)` or `dataset.add(record)` after `FrameDataset.create()`.

---

## “How big can a blob be?”

Lance streams blobs in chunks.  Individual objects of **GBs** are fine; very large collections may benefit from object storage (S3/GCS/etc.).

---

## “How do I store datasets on S3?”

Just pass an `s3://…` URI to `FrameDataset.create()` / `FrameRecord.save()` and, if needed, a `storage_options` dict with your region or custom endpoint.

```python
FrameDataset.create("s3://my-bucket/cf.lance", storage_options={"region": "us-east-1"})
```

---

## “How do I clean up old versions?”

```python
FrameDataset.open("docs.lance")._native.cleanup_old_versions(keep=10)
```

This rewrites manifests to retain only the last 10 versions (irreversible).
