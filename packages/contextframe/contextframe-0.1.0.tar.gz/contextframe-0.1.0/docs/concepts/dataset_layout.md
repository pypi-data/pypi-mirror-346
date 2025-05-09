---
title: "Lance Dataset Anatomy"
summary: "What lives inside a *.lance* directory and how ContextFrame uses it."
---

## Anatomy of a Lance Dataset

A **ContextFrame** dataset *is* a [Lance](https://lancedb.github.io/lance/index.html) dataset.  Every time you call
`FrameRecord.save()` or `FrameDataset.create()` the library writes a directory
ending in `.lance/` that follows the exact layout defined by the Lance format
specification.

```text
my_dataset.lance/
├── data/                 # immutable data fragments  ( *.lance files )
│   ├── 000000.lance
│   ├── 000001.lance
│   └── …
├── _versions/            # one manifest per dataset *version*
│   ├── 000000.manifest
│   ├── 000001.manifest
│   └── …
├── _indices/             # vector / bitmap index directories
│   └── UUID-1234…/index.idx
└── _deletions/           # tombstone files for logical deletes
    └── 000003.arrow
```

The high-level helper methods offered by ContextFrame take care of *all*
updates – you should **never edit these files manually**.

## Key components

| Directory / File          | Purpose                                                                                           | When is it written?                                             |
|---------------------------|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| `data/*.lance`            | Actual columnar data of one *fragment*                                                             | Whenever you append new frames                                  |
| `_versions/*.manifest`    | Immutable snapshot that lists fragments, schema & indices                                          | On *every* mutating operation (insert, delete, `create_index`)   |
| `_indices/*/index.idx`    | Vector- or scalar-bitmap index files                                                               | When you call `FrameDataset.create_vector_index()` …            |
| `_deletions/*.{arrow,bin}`| Tombstones containing row-ids of logically deleted rows                                            | When you call `FrameDataset.delete_record()` or `Dataset.delete` |

### Row-ID vs UUID

Lance can assign a 64-bit *row-id* to each row (feature flag
`move_stable_row_ids`).  ContextFrame already stores a **semantic** `uuid`
column which is under *your* control and never changes.

| Column        | Stability                               | Typical Use                                    |
|---------------|-----------------------------------------|------------------------------------------------|
| `uuid`        | Stable for the lifetime of the record   | Primary key for application-level references   |
| `__rowid__`   | Stable across compaction, **may change on `update()`** | Internal use by Lance indices          |

ContextFrame does **not** rely on Lance row-ids and therefore does *not* enable
this feature by default.  If you need it, call `Dataset.enable_row_ids()`
before your first insert and be aware of the extra storage bytes.

### Compaction & Optimise

Logical deletes create tombstone files which are consulted during scans.  Over
 time they accumulate and can slow down certain workloads.  Run

```python
from contextframe import FrameDataset

FrameDataset.open("my_dataset.lance")._native.optimize()
```

to *compact* the dataset: Lance rewrites fragments (without the deleted rows),
removes the old fragments + tombstones and writes a new manifest.

> **Tip** – Compaction is *optional*.  If you only delete occasionally you can
> ignore it.  For heavy update/delete workloads schedule it as a maintenance
> task.

### Indices and Zero-Copy Versioning

Creating or replacing a vector or scalar index never rewrites the data files.
Instead Lance places the index under `_indices/` and writes a fresh manifest
that references it – the perfect showcase of *zero-copy* design.

If you pass `replace=False` to any `create_*_index` helper and an index for that
column already exists Lance will raise an error to protect you from accidental
work loss.

---

## Takeaways for ContextFrame users

1. A `.lance` directory is **self-contained** – copy the whole folder and you
   have the complete dataset, all versions included.
2. **Everything** you do through the high-level API results in a new manifest
   version, giving you free "time-travel".
3. Use `_native.optimize()` (or the upcoming convenience wrapper) to clean up
   after massive deletes.
4. Keep your `uuid` as the authoritative identifier; treat Lance row-ids as an
   implementation detail unless you have a special use-case.

Continue to [How a Frame maps to Lance columns](frame_storage.md) to see the
exact column-level mapping.
