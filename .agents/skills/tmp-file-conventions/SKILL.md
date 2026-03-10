---
name: "tmp-file-conventions"
description: >-
  Rules for file names and storage locations when the AI agent creates temporary files,
  scripts, or intermediate outputs. Trigger whenever creating, writing, referencing, or
  discussing temporary files or helper scripts -- including casual variants ("temp file",
  "scratch file", "write a script to ..."). When in doubt, apply these rules.
---

```yaml
interpretation:
  precedence: explicit_priority_field
  priority_direction: higher_wins
  assumption: closed_world
  conflict: ask

rules:
  - id: storage_location
    level: MUST
    priority: 100
    statement: >-
      All temporary files MUST be created under /tmp. Creating temporary files
      inside the repository directory is forbidden.
    forbidden:
      - creating temporary files in the repository root or any repository subdirectory

  - id: subdirectory_grouping
    level: SHOULD
    priority: 80
    statement: >-
      Temporary files SHOULD be grouped in a dedicated subdirectory under /tmp
      (e.g., /tmp/<task-slug>/) to avoid collisions with other processes.

  - id: descriptive_names
    level: MUST
    priority: 90
    statement: >-
      Temporary file names MUST be descriptive and reflect their purpose.
    forbidden:
      - generic names such as tmp, test, out, file, temp, or single-character names
```
