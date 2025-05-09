---
title: "Python API Reference"
summary: "Comprehensive reference for the ContextFrame Python package."
---

## ContextFrame Python API Reference

This page provides a **single-stop reference** for the public Python surface exposed by the `contextframe` package. It combines:

1. **Narrative explanations** and _getting-started_ snippets so you can be productive in minutes.
2. **Auto-generated API documentation** powered by [mkdocstrings](https://mkdocstrings.github.io/). All objects are kept perfectly in-sync with the code base—every parameter, return type, and example you see below is extracted directly from the source on every build.

> **Tip** — Use the sidebar on the right (or the page search) to jump to any class or function.

---

## Quick start

```python
from pathlib import Path
from contextframe import FrameRecord, FrameDataset

# 1) Create an in-memory record
record = FrameRecord.create(
    title="Example Document",
    content="Hello, ContextFrame!",
    author="Jane Doe",
    tags=["example", "tutorial"],
)

# 2) Persist it to a new dataset on disk (.lance directory)
dataset_path = Path("docs_demo.lance")
frame_ds = FrameDataset.create(dataset_path, overwrite=True)
frame_ds.add(record)

# 👉 **Cloud Storage?** Simply replace `docs_demo.lance` with an S3/GCS/Azure URI
# like `s3://my-bucket/docs_demo.lance` and pass `storage_options={...}`.
# See the [Object Storage guide](object_storage.md) for full details.

# 3) Run a similarity search (once you have embeddings)
# query_vec = your_encoder.embed("Hello world")
# neighbours = frame_ds.nearest(query_vec, k=5)
```

Everything in ContextFrame revolves around two **central abstractions**:

* [`FrameRecord`](#framerecord) — an in-memory object representing a single row/document.
* [`FrameDataset`](#framedataset) — a high-level wrapper on top of a Lance dataset directory that stores many records.

---

## Public Modules

### `contextframe.frame`

Below you find the **complete documentation** for the two key classes. Expand individual methods to see signatures, docstrings, parameter types, and usage examples.

#### `FrameRecord`

::: contextframe.FrameRecord
    handler: python
    options:
      members_order: source
      show_if_no_docstring: true
      show_source: false
      docstring_section_style: list

#### `FrameDataset`

::: contextframe.FrameDataset
    handler: python
    options:
      members_order: source
      show_if_no_docstring: true
      show_source: false
      docstring_section_style: list

---

## Helper Utilities

### `contextframe.helpers.metadata_utils`

The helper functions shown below are especially handy when you manipulate metadata outside the main classes.

::: contextframe.helpers.metadata_utils
    handler: python
    options:
      heading_level: 3
      filters: ["create_metadata", "create_relationship", "add_relationship_to_metadata", "validate_relationships"]
