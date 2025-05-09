---
title: "How a Frame Maps to Lance Columns"
summary: "Column-by-column mapping between the ContextFrame schema and the underlying Lance dataset."
---

A **Frame** is stored as **one row** in a Lance dataset.  The table below shows
how each public attribute in `FrameRecord` corresponds to a concrete Arrow
field in the dataset (types are shown in Arrow notation).

| API attribute / Metadata key | Lance column | Arrow type | Notes |
|------------------------------|--------------|------------|-------|
| `uuid`                       | `uuid`       | `string`   | Mandatory primary key (universally unique) |
| `text_content` / `content`   | `text_content` | `string` | Full document body (Markdown, plain-text, …) |
| `vector`                     | `vector`     | `fixed_size_list<float32>[1536]` | Embedding; dimension configurable via `embed_dim` |
| `metadata['title']`          | `title`      | `string`   | Required |
| `metadata['version']`        | `version`    | `string`   | Semantic version string (e.g. `1.2.0`) |
| `metadata['context']`        | `context`    | `string`   | Free-form domain / model context |
| `metadata['uri']`            | `uri`        | `string`   | External canonical URI if any |
| `metadata['local_path']`     | `local_path` | `string`   | Original source file path |
| `metadata['cid']`            | `cid`        | `string`   | Content-addressable hash (IPFS CID, …) |
| `metadata['collection']`     | `collection` | `string`   | Logical collection name |
| `metadata['position']`       | `position`   | `int32`    | Positional index within collection |
| `metadata['author']`         | `author`     | `string`   | Primary author |
| `metadata['contributors']`   | `contributors` | `list<string>` | Additional contributors |
| `metadata['created_at']`     | `created_at` | `string`   | ISO-8601 date (`YYYY-MM-DD`) |
| `metadata['updated_at']`     | `updated_at` | `string`   | ISO-8601 date |
| `metadata['tags']`           | `tags`       | `list<string>` | Arbitrary keywords |
| `metadata['status']`         | `status`     | `string`   | `draft`, `published`, … |
| `metadata['source_file']`    | `source_file`| `string`   | Filename of the original artefact |
| `metadata['source_type']`    | `source_type`| `string`   | `pdf`, `html`, `image`, … |
| `metadata['source_url']`     | `source_url` | `string`   | HTTP URL if harvested from the web |
| `metadata['relationships']`  | `relationships` | `list<struct{…}>` | Contains parent/child/member-of links |
| `metadata['custom_metadata']`| `custom_metadata` | `map<string, string>` | **Extensible** key/value area – safe for schema evolution |
| `metadata['record_type']`    | `record_type`| `string`   | `document` \| `collection_header` |
| `raw_data_type` (param)      | `raw_data_type` | `string` | MIME type, only present if `raw_data` is set |
| `raw_data` (param)           | `raw_data`   | `large_binary` (Lance blob) | Raw bytes for images/audio/etc. |
| `metadata['collection_id']` | `collection_id` | `string` | Unique identifier for the collection |
| `metadata['collection_id_type']` | `collection_id_type` | `string` | `uuid` \| `uri` \| `cid` \| `string` |

### Why `custom_metadata` is evolution-friendly

If your application needs *per-project* or *per-experiment* keys simply add
them to the `custom_metadata` dict – **no schema change required**.  Lance
stores the map as a nested column so new keys coexist happily with existing
rows.  This keeps the *canonical* schema stable while still letting you attach
arbitrary metadata.

### Adding brand-new *columns*

When you need to promote an ad-hoc key to a first-class, search-optimised
column you **must** update `contextframe.schema.contextframe_schema.build_schema()`
and bump your dataset by writing a new manifest with the extended schema.  As
long as you *only add* columns older readers continue to function.

> **Rule of thumb** — Use `custom_metadata` for experimental keys.  Once you
> realise the field is widely used, formalise it in the schema and (optionally)
> backfill existing rows with a one-off `Dataset.merge()`.

### Reserved column names

The list above constitutes the *canonical* schema.  Do **not** add columns
starting with `_` (underscore) – Lance and Arrow reserve that namespace for
internal metadata.

---

**Next:** [Dataset Anatomy](dataset_layout.md) explains how these columns end up
on disk and how to maintain a healthy dataset over time.
