---
title: "CLI – Working With Versions"
summary: "Every mutating command writes a new dataset version; learn the implications and tooling."
---

ContextFrame's command-line interface (`contextframe …`) wraps the same
high-level Python API that powers your scripts.  **All commands that change a
`.lance` dataset automatically create a new manifest version.**

| Command                                   | Resulting operation | Version written? |
|-------------------------------------------|---------------------|------------------|
| `contextframe create`                     | New dataset / row   | **Yes**          |
| `contextframe version create`             | Snapshot of current file | **Yes**      |
| `contextframe version rollback`           | Overwrite working copy with older snapshot | **Yes** (rollback itself) |
| `contextframe conflicts merge`            | 3-way merge + write | **Yes**          |
| `contextframe conflicts apply-resolution` | Apply manual resolution | **Yes**      |

### Inspecting versions

```bash
contextframe version list mydoc.lance
contextframe version show mydoc.lance 42
```

### Time-travel in Python

```python
from contextframe import FrameDataset

# Latest
ds = FrameDataset.open("mydoc.lance")
print(ds.versions())       # -> [0, 1, 2, 3]

# Historical view (read-only)
historical = ds.checkout(1)
print(historical.count_by_filter("True"))
```

### Garbage collection

Versions are cheap because Lance uses *zero-copy* manifests, but they are **not
free**.  If you keep thousands of versions you will eventually accumulate
obsolete fragments.  Run:

```python
FrameDataset.open("mydoc.lance")._native.cleanup_old_versions(keep=10)
```

to keep only the last 10 versions (**irreversible**).

> **Best practice** — Keep enough history for debugging / reproducibility, then
> schedule periodic clean-ups.
