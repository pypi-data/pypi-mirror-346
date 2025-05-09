# Recipe – FastAPI Vector Search Endpoint

This snippet shows how to wrap the `FrameDataset.nearest()` helper in a **FastAPI** micro-service.

> **Why?**  Turn your ContextFrame dataset into a low-latency similarity-search API that any web or mobile client can call.

---

## 1. Install dependencies

```bash
pip install contextframe fastapi uvicorn[standard] numpy
```

## 2. Save `app.py`

```python
from pathlib import Path
from typing import List

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

from contextframe import FrameDataset

DATASET_PATH = Path("my_docs.lance")  # change to your dataset

# Load dataset once at start-up
DS = FrameDataset.open(DATASET_PATH)
VECTOR_DIM = DS._native.schema.field("vector").type.list_size

app = FastAPI(title="ContextFrame Vector Search")

class Query(BaseModel):
    vector: List[float]
    k: int = 5

    @validator("vector")
    def _check_dim(cls, v):  # noqa: N805 – Pydantic wants "cls"
        if len(v) != VECTOR_DIM:
            raise ValueError(f"Expected vector of length {VECTOR_DIM}")
        return v

@app.post("/search")
def search(q: Query):
    vec = np.array(q.vector, dtype=np.float32)
    try:
        neighbours = DS.nearest(vec, k=q.k)
    except Exception as exc:  # pragma: no cover – guard against runtime issues
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return [
        {
            "uuid": r.uuid,
            "title": r.title,
            "score": float(r.metadata.get("_distance", 0)),
        }
        for r in neighbours
    ]
```

## 3. Run the server

```bash
uvicorn app:app --reload
```

Then `POST /search` with JSON like

```json
{
  "vector": [0.0, 0.1, 0.2, …],
  "k": 3
}
```

to receive the top-k nearest documents.

---

### Production notes

* Consider creating a **vector index** (`FrameDataset.create_vector_index`) beforehand.
* Mount the dataset directory on a fast SSD or use a read-through cache for S3.
* Add auth & rate-limiting (fastapi-limiter, auth headers, etc.) as needed.
