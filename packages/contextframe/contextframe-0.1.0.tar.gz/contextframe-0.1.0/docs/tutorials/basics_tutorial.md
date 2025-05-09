# Basics Tutorial

A hands-on walk-through of the core ContextFrame workflow.  Follow along in a fresh Python session.

> **Prerequisites** – `pip install contextframe` and make sure you ran the Quick Start.

---

## 1. Set-up a working dataset

```python
from pathlib import Path
from contextframe import FrameRecord, FrameDataset

dataset = Path("my_docs.lance")
FrameDataset.create(dataset, overwrite=True)
```

## 2. Create your first record

```python
first = FrameRecord.create(
    title="ContextFrame Tutorial",
    content=(
        "ContextFrame stores documents as *frames* backed by the Lance\n"
        "columnar format.  This is the first one."
    ),
    author="You",
    tags=["docs", "tutorial"],
)
first.save(dataset)
```

## 3. Bulk-append more records

```python
records = [
    FrameRecord.create(title=f"Doc {i}", content=f"Content {i}") for i in range(3)
]
FrameDataset.open(dataset).add_many(records)
```

## 4. Similarity search

```python
import numpy as np
from contextframe import FrameDataset

ds = FrameDataset.open(dataset)
query_vec = np.zeros(1536, dtype=np.float32)  # Replace with a real embedding
nearest = ds.nearest(query_vec, k=2)
for r in nearest:
    print(r.title, r.uuid)
```

## 5. Full-text search

```python
hits = ds.full_text_search("ContextFrame", k=10)
print([h.title for h in hits])
```

## 6. Update a record in-place

```python
first.tags.append("updated")
first.content += "\nUpdated content."  # mutate in memory
FrameDataset.open(dataset).update_record(first)
```

## 7. Basic versioning via CLI

```bash
# Create a snapshot
contextframe version create my_docs.lance -d "Added three docs"  -a "You"

# List versions
contextframe version list my_docs.lance

# Roll back to version 0
contextframe version rollback my_docs.lance 0
```

---

Next steps:  
• See the **Schema Cheatsheet** for column-level mapping.  
• Checkout the **FastAPI Vector Search** recipe for a web-ready endpoint. 