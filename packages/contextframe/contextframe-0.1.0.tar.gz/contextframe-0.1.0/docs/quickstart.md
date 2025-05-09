# ContextFrame Quick Start

This page takes you from **zero to query** in less than five minutes.

## 1 – Install the library

```bash
pip install contextframe
```

## 2 – Create an in-memory record

```python
from contextframe import FrameRecord

record = FrameRecord.create(
    title="Hello ContextFrame",
    content="Just a tiny example document…",
    author="Alice",
    tags=["example", "quickstart"],
)
```

## 3 – Persist it to a dataset

```python
from pathlib import Path
from contextframe import FrameDataset

DATASET = Path("demo.lance")

# Create an *empty* dataset (overwrites if it already exists)
FrameDataset.create(DATASET, overwrite=True)

# Append the record
record.save(DATASET)
```

At this point you have a self-contained **`demo.lance/`** directory on disk (or S3/GCS/Azure if you passed a cloud URI).

## 4 – Run a vector search

```python
import numpy as np
from contextframe import FrameDataset

query_vec = np.zeros(1536, dtype=np.float32)  # substitute a real embedding
results = FrameDataset.open(DATASET).nearest(query_vec, k=3)

for r in results:
    print(r.uuid, r.title)
```

## 5 – Inspect from the CLI

```bash
contextframe info demo.lance
```

Output:

```text
Title: Hello ContextFrame
Created: 2025-05-08
Metadata: 8 fields
Content: 1 lines, 5 words
```

That's it!  Head over to the **Basics Tutorial** next for a deeper walk-through.
