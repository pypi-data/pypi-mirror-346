# Recipe – Store & Retrieve Images as Blobs

Attach raw binary data (e.g. JPEGs) to a `FrameRecord` and stream it back without loading the whole file into memory.

---

## 1. Install deps

```bash
pip install contextframe pillow
```

## 2. Save an image

```python
from pathlib import Path
from contextframe import FrameRecord, FrameDataset, MimeTypes

img_path = Path("cat.jpg")
bytes_data = img_path.read_bytes()

rec = FrameRecord.create(
    title="Cute Cat",
    content="An image of a cute cat.",
    raw_data=bytes_data,
    raw_data_type=MimeTypes.IMAGE_JPEG,
)

DATASET = Path("images.lance")
FrameDataset.create(DATASET, overwrite=True)
rec.save(DATASET)
```

## 3. Retrieve & display lazily

```python
from PIL import Image
from contextframe import FrameDataset

ds = FrameDataset.open("images.lance")
row_idx = 0  # only one row in this toy example
blob_files = ds._native.take_blobs([row_idx], column="raw_data")
with Image.open(blob_files[0]) as img:
    img.show()
```

The image bytes are streamed directly from disk (or S3) only when `Image.open` reads them.

---

**Tip** – store metadata like *resolution*, *format*, or *camera* in normal scalar fields so you can filter quickly without touching the blob column.
