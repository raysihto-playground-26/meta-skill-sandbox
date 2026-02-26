---
name: "create-tmp-file"
description: >-
  Skill for creating new temporary files under docs/.tmp/ with the filename format
  YYYYMMDDhhmmJST_summary.ext (e.g., 202602270835JST_validation_report.md).
---

```yaml
interpretation:
  precedence: list_order
  assumption: closed_world

rules:
  - id: tmp_file_location
    level: MUST
    statement: >-
      All new temporary files MUST be created under docs/.tmp/.

  - id: tmp_file_naming
    level: MUST
    statement: >-
      Temporary file names MUST follow the format YYYYMMDDhhmmJST_summary.ext, where the timestamp
      prefix is obtained via `date '+%Y%m%d%H%M%Z'` and summary is a short description of the file content.
    example: "202602270835JST_validation_report.md"

  - id: tmp_dir_creation
    level: MUST
    statement: >-
      If docs/.tmp/ does not exist, it MUST be created before writing the file.
```
