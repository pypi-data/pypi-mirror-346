# Schema Cheatsheet

The table below is your **one-stop reference** for how `FrameRecord` properties and metadata keys map to physical columns inside a `.lance` dataset.

| API attribute / Metadata key | Lance column | Arrow type |
|------------------------------|--------------|------------|
| `uuid`                       | `uuid`       | `string`   |
| `content / text_content`     | `text_content` | `string` |
| `vector`                     | `vector`     | `fixed_size_list<float32>[1536]` |
| `metadata['title']`          | `title`      | `string` |
| `metadata['version']`        | `version`    | `string` |
| `metadata['author']`         | `author`     | `string` |
| `metadata['tags']`           | `tags`       | `list<string>` |
| `metadata['created_at']`     | `created_at` | `string` (YYYY-MM-DD) |
| `metadata['updated_at']`     | `updated_at` | `string` |
| `raw_data_type` (param)      | `raw_data_type` | `string` |
| `raw_data` (param)           | `raw_data`   | `large_binary` (blob) |
| `metadata['relationships']`  | `relationships` | `list<struct{…}>` |
| `metadata['custom_metadata']`| `custom_metadata` | `map<string,string>` |

> Need a field that's not listed?  Store it under `custom_metadata` or extend the dataset schema via `FrameDataset._native.replace_schema()`.

For deeper background on how Lance stores these columns on disk see the full **Frame Storage** concept page.
