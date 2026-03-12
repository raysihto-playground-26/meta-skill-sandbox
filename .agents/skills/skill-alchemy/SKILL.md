---
name: "skill-alchemy"
description: >-
  Mandatory requirements for AI directive files: A YAML-only format and authoring protocol (frontmatter and single YAML block) with zero prose.
  MUST trigger whenever the AI Agent creates, modifies, refactors, or touches any .md file in .agents/skills/*/ or .*/skills/*/ directories.
  Also trigger when the user mentions skills, directives, SKILL.md files, or asks to "make a skill", "write a directive", "add a rule", "edit the skill file", "fix the directive", or any phrasing that implies working with AI directive files.
  Trigger proactively -- undertriggering is a known failure mode. When in doubt, trigger.
---

```yaml
interpretation:
  unknown_keys: ignore
  assumption: closed_world
  extrapolation: forbidden
  precedence: explicit_priority_field
  priority_direction: higher_wins
  conflict: ask

globs:
  - ".*/skills/*/*.md"
  - ".*/skills/skill-alchemy/SKILL.md"

rules:
  - id: canonical_structure
    level: MUST
    priority: 100
    statement: >-
      Every AI directive file MUST consist of exactly frontmatter (--- delimited YAML)
      and exactly_one_yaml_block_body (single fenced YAML code block). Nothing else.
    forbidden:
      - prose outside frontmatter and exactly_one_yaml_block_body
      - multiple code blocks
      - content after the closing code fence

  - id: reference_exemplar
    level: MUST
    priority: 90
    statement: >-
      MUST model structure and style exclusively after skill-alchemy/SKILL.md.
      Resolve the glob .*/skills/skill-alchemy/SKILL.md to a concrete path,
      then re-read the resolved file in full.
    conditions: creating_new_ai_directive_file
    exceptions:
      - name, description, globs, and domain-specific rules are expected to differ
    includes:
      - interpretation_contract_placement
      - closed_world_interpretation
      - priority_and_conflict
      - globs_in_body
      - english_authoring_language
    forbidden:
      - using other existing directive files as structural or stylistic references
      - averaging or synthesizing patterns from multiple existing files
      - replicating body keys or fields from other sources without domain-specific failure-prevention justification
      - relying on cached or already-loaded content instead of re-reading the exemplar

  - id: description_trigger_proactive
    level: MUST
    priority: 90
    statement: >-
      The frontmatter description field MUST enumerate concrete trigger scenarios
      (file-path patterns, agent actions, user-intent phrases, or combinations thereof),
      a catch-all for unenumerated variants, and a proactive directive
      ("When in doubt, trigger" or equivalent).
    rationale: undertriggering is an empirically observed failure mode
    forbidden:
      - placing trigger conditions exclusively in the body
      - passive trigger language ("Can be used when..." vs "MUST trigger when...")
    examples:
      - weak: "Commits staged changes with an auto-generated message."
        strong: >-
          Commits staged changes with an auto-generated message.
          MUST trigger when user explicitly requests a commit via
          "commit", "please commit", or any phrasing
          that implies committing. Trigger proactively --
          undertriggering is a known failure mode. When in doubt, trigger.

  - id: confirm_triggers
    level: SHOULD
    priority: 85
    statement: >-
      Before drafting a new directive file, the agent SHOULD ask the user
      to specify or confirm the skill's trigger conditions --
      when, in what contexts, and on what user actions the skill should activate.
      If the runtime environment does not support interactive prompting,
      infer from available context and document assumptions in the output.
    conditions: creating_new_ai_directive_file
    rationale: >-
      trigger conditions are the highest-impact, hardest-to-infer aspect
      of a directive

  - id: condition_field_form
    level: MUST
    priority: 70
    statement: >-
      The conditions field, when present, MUST be an explicit enumeration of triggers -- not prose.
    forbidden:
      - prose-embedded conditions in statement text
      - "conditions: always"
      - conditions field on unconditional rules

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
      This file is itself an AI directive file.
      Any modification to this file MUST preserve compliance with all rules defined herein.

  - id: lean_and_mean
    level: MUST
    priority: 90
    statement: >-
      Omit anything obvious or safely implicit.
      Do not omit anything whose absence would predictably cause failures.
      Prefer constraint density over completeness.
    forbidden:
      - redundant rationale or definitions for self-evident terms
      - verbose statements where a concise form suffices
      - fields added purely for completeness with no failure-prevention value
```
