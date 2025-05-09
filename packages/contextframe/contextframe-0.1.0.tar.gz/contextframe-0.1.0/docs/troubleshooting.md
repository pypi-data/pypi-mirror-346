# Troubleshooting

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Inserts are slow | No vector index, small batch inserts | Use `FrameDataset.create_vector_index()` and batch `add_many()` |
| "Dataset not found" when opening | Path typo or `.lance` directory missing | Verify path, run `FrameDataset.create()` first |
| "Concurrent write detected" on S3 | Multiple writers, no commit lock | Use DynamoDB manifest store or external `commit_lock` |
| "Arrow version mismatch" | Mixed binary wheels of Arrow | `pip uninstall pyarrow` then reinstall all deps with same Arrow version |
| Windows shows `PathTooLongError` | Long dataset paths exceed 260 char | Enable long-path support or shorten path |

If the table doesn't cover your issue, search the FAQ or open an issue on GitHub.
