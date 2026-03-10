---
name: "tmp-file-rules"
description: >-
  Rules for naming and storing temporary files under docs/.tmp/.
  MUST trigger whenever the AI Agent creates any temporary file, is asked to
  save output, write a summary, or produce any artifact intended for
  docs/.tmp/. Trigger whenever the user asks to "save", "output", "write",
  "create a file", "make a note", or uses any phrasing that implies producing
  a temporary file. When in doubt, prefer triggering.
---

```yaml
interpretation:
  precedence: explicit_priority_field
  priority_direction: higher_wins
  assumption: closed_world
  conflict: ask

globs:
  - "docs/.tmp/**/*"

rules:
  - id: file_path
    level: MUST
    priority: 100
    statement: >-
      Temporary files MUST be stored at
      docs/.tmp/YYYYMM/YYYYMMDDhhmmJST-summary-in-kebab-case.ext
      relative to the repository root, where YYYYMM and YYYYMMDDhhmm
      represent the current date-time in JST (UTC+9), and
      summary-in-kebab-case is a concise kebab-case description of the content.

  - id: record_prompt
    level: MUST
    priority: 90
    statement: >-
      When the prompting request is retrievable, it MUST be recorded in the
      temporary file (e.g., at the top of the file).

  - id: language_explicit
    level: MUST
    priority: 85
    statement: >-
      When an explicit language instruction is given, the temporary file
      MUST be written in that language.
    conditions: explicit_language_instruction_given

  - id: language_default
    level: MUST
    priority: 80
    statement: >-
      When no explicit language instruction is given, the temporary file
      MUST be written in the same language as the prompting request.

  - id: apply_skills
    level: MUST
    priority: 75
    statement: >-
      Applicable skills and rules MUST be applied when writing the temporary
      file content (e.g., apply Japanese style guidelines when writing in
      Japanese).
```
