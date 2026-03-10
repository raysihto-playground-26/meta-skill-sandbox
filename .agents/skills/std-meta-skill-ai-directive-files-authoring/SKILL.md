---
name: "std-meta-skill-ai-directive-files-authoring"
description: >-
  Mandatory requirements for AI directive files: A YAML-only format and authoring protocol (frontmatter and single YAML block) with zero prose.
  MUST trigger whenever the AI Agent creates, modifies, refactors, or touches any .md file in .agents/skills/*/ or .*/skills/*/ directories.
  Also trigger when the user mentions skills, directives, SKILL.md files, or asks to "make a skill", "write a directive", "add a rule", "edit the skill file", "fix the directive", or any phrasing that implies working with AI directive files.
  Trigger proactively -- undertriggering is a known failure mode. When in doubt, trigger.
---

```yaml
interpretation:
  precedence: explicit_priority_field
  priority_direction: higher_wins
  assumption: closed_world
  conflict: ask

globs:
  - ".*/skills/*/*.md"
  - ".agents/skills/std-meta-skill-ai-directive-files-authoring/SKILL.md"

rules:
  - id: canonical_structure
    level: MUST
    priority: 100
    statement: >-
      Every AI directive file MUST consist of exactly:
      (1) YAML frontmatter (--- delimited),
      (2) a single fenced YAML code block,
      (3) nothing else.
    forbidden:
      - prose outside frontmatter and the YAML code block
      - multiple code blocks
      - any content after the closing code fence

  - id: reference_exemplar
    level: MUST
    priority: 90
    statement: >-
      When creating a new AI directive file, the new file MUST model its
      structure and style exclusively after
      .agents/skills/std-meta-skill-ai-directive-files-authoring/SKILL.md
      and no other files.
    conditions: creating_new_ai_directive_file

  - id: description_trigger
    level: MUST
    priority: 90
    statement: >-
      The frontmatter description field MUST include trigger conditions:
      when and in what contexts the skill activates.
    forbidden:
      - placing trigger conditions exclusively in the body

  - id: description_pushy
    level: SHOULD
    priority: 85
    statement: >-
      The description SHOULD actively encourage triggering in relevant contexts.
    rationale: undertriggering is an empirically observed failure mode
    examples:
      - weak: "Commits staged changes with an auto-generated message."
        strong: >-
          Commits staged changes with an auto-generated message. Use this skill
          whenever the user asks to commit -- including casual variants
          ("commit", "please commit"). When in doubt, prefer triggering.

  - id: globs_match_target
    level: MUST
    priority: 75
    statement: >-
      globs MUST match the target files for the directive being defined.
    forbidden:
      - copying, reusing, or basing globs on the globs in this file
    conditions: directive_has_target_paths
    overrides: reference_exemplar

  - id: conditional_rule_form
    level: MUST
    priority: 70
    statement: >-
      Conditional rules MUST use explicit condition triggers
      (enumerations), not prose.
    forbidden:
      - prose-embedded conditions in statement text

  - id: unconditional_rule_form
    level: MUST
    priority: 70
    statement: >-
      Unconditional rules MUST omit the conditions field entirely.
    forbidden:
      - "conditions: always"

  - id: interpretation_contract_placement
    level: MUST
    priority: 80
    statement: >-
      Any binding interpretation contract MUST be encoded inside the YAML
      block, not as prose.

  - id: closed_world_interpretation
    level: MUST
    priority: 80
    statement: >-
      AI directive files MUST declare closed-world interpretation
      semantics in the interpretation section of the YAML block.
      Unspecified behavior MUST be forbidden. The model MUST NOT
      fill gaps autonomously beyond what is explicitly declared.

  - id: priority_and_conflict
    level: MUST
    priority: 80
    statement: >-
      Directive files MUST define a stable precedence mechanism and a
      deterministic conflict policy with a safe failure mode.

  - id: globs_in_body
    level: MUST
    priority: 60
    statement: >-
      The directive MUST declare a top-level globs key inside the YAML body block
      listing the paths it must auto-apply to.
    conditions: directive_has_target_paths

  - id: yaml_validity
    level: MUST
    priority: 80
    statement: >-
      Both the frontmatter and the YAML code block MUST be valid, parseable YAML.
    verification: prettier --check with default options

  - id: meta_circular_compliance
    level: MUST
    priority: 80
    statement: >-
      This file is itself an AI directive file. Any modification to this
      file MUST preserve compliance with all rules defined herein.

  - id: lean_and_mean
    level: MUST
    priority: 90
    statement: >-
      Omit anything obvious or safely implicit. Do not omit anything
      whose absence would predictably cause failures. Prefer constraint
      density over completeness.
    forbidden:
      - redundant rationale or definitions for self-evident terms
      - verbose statements where a concise form suffices
      - fields added purely for completeness with no failure-prevention value
```
