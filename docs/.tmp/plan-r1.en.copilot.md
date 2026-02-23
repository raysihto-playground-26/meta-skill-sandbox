# Remediation Plan: P1 (Conflict Resolution Ambiguity) and P2 (Condition Identifier Vocabulary)

Target file (canonical): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
Path note: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`, `.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` are all symlinks to `../.agents/skills/`, and the only canonical file is the single file under `.agents/skills/`. Fixes only need to be made to this one file.

## 0. Purpose, scope, and assumptions

### 0.1 Purpose

This document is a remediation plan for the two issues identified in `docs/.tmp/report_p1_p2_gap_analysis.md`:

| ID  | Issue                                                      | Severity |
| --- | ---------------------------------------------------------- | -------- |
| P1  | `interpretation.priority` and `MUST_vs_MUST` contradiction | Critical |
| P2  | Condition identifier vocabulary undefined + token mismatch | High     |

The plan describes the changes required to bring the authoring skill into internal consistency, without changing its intent or the set of normative rules it enforces.

### 0.2 Scope

- **In scope**: changes to the YAML content of SKILL.md that resolve P1 and P2.
- **Out of scope**: changes to file structure (frontmatter, fenced block layout), changes to other AI directive files, linter/tooling implementation, and rollout to other files.

### 0.3 Definitions

Terms used in this plan:

- **SKILL.md**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`, the authoring meta-skill.
- **runner**: the execution environment that applies or verifies compliance with AI directive files.
- **rule record**: a structured record with fields `id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`.
- **condition identifier**: a string used in the `conditions` array of a rule record that identifies when the rule applies.
- **compound condition**: a condition of the form `"A and B"` (literal `<space>and<space>`), as specified by `interpretation.compound_conditions`.

### 0.4 Non-goals

- This plan does not aim to add new normative rules or prohibitions.
- This plan does not implement tooling (linter, schema validator) for the changes described.
- Concrete file changes to AI directive files are out of scope for this plan.

## 1. P1: Conflict Resolution Ambiguity

### 1.1 Problem statement

Two sections of SKILL.md specify conflicting behavior for resolving MUST-vs-MUST conflicts within the same layer:

**Source A** — `interpretation.priority` (L24):

```yaml
priority: "Each rule has layer (L0–L4) and priority (numeric); L0 has highest
  precedence, and within the same layer, higher priority number wins. See
  precedence_and_conflict for details."
```

This states that within the same layer, the rule with the higher numeric priority wins.

**Source B** — `precedence_and_conflict.conflict_policy.MUST_vs_MUST` (L30):

```yaml
MUST_vs_MUST: "Halt or request clarification; MUST NOT silently choose one."
```

This states that MUST-vs-MUST conflicts should unconditionally halt.

**Contradiction**: when two MUST rules in the same layer have different numeric priorities (e.g., L2/priority:98 vs L2/priority:95), Source A says priority:98 wins, but Source B says halt. The runner cannot determine which instruction to follow.

### 1.2 Target state

A deterministic three-step conflict resolution procedure:

1. **Different layers**: resolve by layer precedence order (L0 > L1 > L2 > L3 > L4).
2. **Same layer, different priority**: resolve by numeric priority (higher number wins).
3. **Same layer and same priority**: apply the conflict policy (MUST vs MUST → halt or request clarification; MUST vs SHOULD → MUST wins).

### 1.3 Remediation policy

#### Change P1-A: narrow the applicability of `MUST_vs_MUST`

Rewrite the `MUST_vs_MUST` value in `precedence_and_conflict.conflict_policy` to apply only when layer and priority are equal, making it consistent with `interpretation.priority`.

Current:

```yaml
MUST_vs_MUST: "Halt or request clarification; MUST NOT silently choose one."
```

Proposed:

```yaml
MUST_vs_MUST: "When layer and priority are equal, halt or request clarification;
  MUST NOT silently choose one. When layer differs, layer precedence resolves the
  conflict. When layer is equal but priority differs, higher numeric priority wins."
```

Design points:

- The three-step resolution is now fully explicit in `conflict_policy`.
- `interpretation.priority` and `MUST_vs_MUST` no longer contradict each other.
- The halt behavior is preserved for genuinely ambiguous cases (same layer, same priority).
- The "MUST NOT silently choose one" clause remains but is scoped to the equal-priority case.

#### Change P1-B: align `interpretation.priority` (optional, for clarity)

To reduce redundancy and ensure a single authoritative source, consider adding a forward reference in `interpretation.priority`:

Current:

```yaml
priority: "Each rule has layer (L0–L4) and priority (numeric); L0 has highest
  precedence, and within the same layer, higher priority number wins. See
  precedence_and_conflict for details."
```

Proposed:

```yaml
priority: "Each rule has layer (L0–L4) and priority (numeric); L0 has highest
  precedence, and within the same layer, higher priority number wins. When layer
  and priority are both equal, conflict_policy applies. See precedence_and_conflict
  for details."
```

Design points:

- Makes explicit that `conflict_policy` is the fallback, not the primary resolution mechanism.
- The phrase "See precedence_and_conflict for details" already exists; the addition clarifies the boundary.

### 1.4 Change size evaluation

| Change | Target                                                 | Scope of impact                   |
| ------ | ------------------------------------------------------ | --------------------------------- |
| P1-A   | `precedence_and_conflict.conflict_policy.MUST_vs_MUST` | rewrite 1 string value            |
| P1-B   | `interpretation.priority`                              | rewrite 1 string value (optional) |

### 1.5 Verification criteria

1. Reading `conflict_policy.MUST_vs_MUST` and `interpretation.priority` together produces a single, deterministic resolution procedure with no contradictions.
2. For two MUST rules in the same layer with different priorities, both sources agree that the higher priority wins.
3. For two MUST rules in the same layer with the same priority, both sources agree that the runner must halt or request clarification.
4. YAML parses successfully with a standard parser.

## 2. P2: Condition Identifier Vocabulary

### 2.1 Problem statement

`interpretation.compound_conditions` (L22) requires that all condition identifiers be defined:

```yaml
compound_conditions: "A condition entry may be a single trigger identifier or a
  compound of the form 'A and B' (literal space, and, space), meaning both A and B
  apply; such identifiers MUST be defined in this file or in definitions."
```

Two sub-problems exist:

#### Problem A: undefined identifiers

The following condition identifiers are used across rule records but are not defined in `definitions`:

| Identifier                                            | Usage                                  |
| ----------------------------------------------------- | -------------------------------------- |
| `creating AI directive file`                          | conditions of most authoring rules     |
| `editing AI directive file`                           | conditions of most authoring rules     |
| `creating AI directive file that contains YAML block` | conditions of yaml-include-\* rules    |
| `editing AI directive file that contains YAML block`  | conditions of yaml-include-\* rules    |
| `scope high-stakes`                                   | conditions of tier-separation-\* rules |
| `scope multi-constraint`                              | conditions of tier-separation-\* rules |
| `scope long-form reasoning`                           | conditions of tier-separation-\* rules |

#### Problem B: token format mismatch

The `definitions` section defines keys with hyphens (`scope-high-stakes`, `scope-multi-constraint`, `scope-long-form-reasoning`), but the `conditions` arrays in tier-separation rules use spaces (`scope high-stakes`, `scope multi-constraint`, `scope long-form reasoning`). These are distinct YAML strings and a machine-based resolver would fail to match them.

### 2.2 Target state

1. All condition identifiers used in `conditions` arrays across the file are defined in `definitions` (or an equivalent section).
2. The token form used in `conditions` and the key form used in `definitions` are identical.
3. A runner or linter can mechanically verify that every condition identifier resolves to a definition.

### 2.3 Remediation policy

Two approaches are viable. This plan recommends **Approach 1** (normalize conditions to match definitions) as the primary strategy, with Approach 2 as an alternative.

#### Approach 1 (recommended): add missing definitions + normalize token format in conditions

##### Change P2-A: add missing trigger identifiers to `definitions`

Add the following entries to the `definitions` section:

```yaml
creating-AI-directive-file:
  description: "Trigger condition: the agent is creating a new AI directive file."
editing-AI-directive-file:
  description: "Trigger condition: the agent is editing an existing AI directive file."
creating-AI-directive-file-that-contains-YAML-block:
  description: "Trigger condition: the agent is creating a new AI directive file
    that contains a YAML block."
editing-AI-directive-file-that-contains-YAML-block:
  description: "Trigger condition: the agent is editing an existing AI directive file
    that contains a YAML block."
```

Design points:

- Uses hyphen-delimited keys consistent with existing `definitions` style (e.g., `scope-high-stakes`).
- Descriptions are minimal and self-explanatory, following the existing pattern.

##### Change P2-B: normalize scope identifiers in `conditions` to match `definitions` keys

Replace all occurrences of space-separated scope identifiers in `conditions` arrays with their hyphen-delimited equivalents from `definitions`:

| Current (in conditions)     | Normalized (matching definitions key) |
| --------------------------- | ------------------------------------- |
| `scope high-stakes`         | `scope-high-stakes`                   |
| `scope multi-constraint`    | `scope-multi-constraint`              |
| `scope long-form reasoning` | `scope-long-form-reasoning`           |

This affects the `conditions` of the following rules:

- `tier-separation-when-applicable`
- `tier-separation-define-scope-format-stopping`
- `tier-separation-bounded-iteration`
- `tier-separation-objective-vs-subjective`

##### Change P2-C: normalize trigger identifiers in `conditions` to match new `definitions` keys

Replace all occurrences of space-separated trigger identifiers in `conditions` arrays with the hyphen-delimited keys added in Change P2-A:

| Current (in conditions)                               | Normalized                                            |
| ----------------------------------------------------- | ----------------------------------------------------- |
| `creating AI directive file`                          | `creating-AI-directive-file`                          |
| `editing AI directive file`                           | `editing-AI-directive-file`                           |
| `creating AI directive file that contains YAML block` | `creating-AI-directive-file-that-contains-YAML-block` |
| `editing AI directive file that contains YAML block`  | `editing-AI-directive-file-that-contains-YAML-block`  |

This affects the `conditions` of all rules in `prohibitions`, `authoring_obligations`, and the yaml-include-_ / tier-separation-_ rules.

Note: compound conditions (e.g., `"creating AI directive file and scope high-stakes"`) would become `"creating-AI-directive-file and scope-high-stakes"`, preserving the `" and "` separator as specified by `interpretation.compound_conditions`.

#### Approach 2 (alternative): add missing definitions using space-delimited keys + normalize definitions keys to match conditions

Instead of normalizing the conditions, normalize the definitions keys to use spaces. This would mean:

- Rename `scope-high-stakes` to `scope high-stakes` in definitions.
- Add new definition entries with space-delimited keys (e.g., `creating AI directive file`).

This approach has a downside: YAML keys with spaces require quoting, which is less conventional and harder to maintain. Therefore, **Approach 1 is recommended**.

### 2.4 Change size evaluation

| Change | Target                                | Scope of impact                                             |
| ------ | ------------------------------------- | ----------------------------------------------------------- |
| P2-A   | `definitions` section                 | add 4 new definition entries                                |
| P2-B   | `conditions` in tier-separation rules | rewrite scope identifiers in 4 rules (24 condition entries) |
| P2-C   | `conditions` across most rules        | rewrite trigger identifiers across ~30 rules                |

### 2.5 Verification criteria

1. Every identifier appearing in any `conditions` array (whether simple or as part of a compound `"A and B"`) has a corresponding key in `definitions`.
2. No space-vs-hyphen mismatch exists between `conditions` identifiers and `definitions` keys.
3. `compound_conditions`'s MUST requirement ("such identifiers MUST be defined in this file or in definitions") is satisfied.
4. YAML parses successfully with a standard parser.
5. No rule's semantic meaning is changed by the identifier renaming.

## 3. Execution plan

### 3.1 Phasing

Both P1 and P2 changes can be applied independently. However, since P2-C touches the `conditions` arrays of most rules (including those also affected by P2-B), it is recommended to apply P2 changes together as a single phase.

| Phase   | Changes          | Description                                    | Dependency |
| ------- | ---------------- | ---------------------------------------------- | ---------- |
| Phase 1 | P1-A, P1-B       | Resolve conflict resolution ambiguity          | None       |
| Phase 2 | P2-A, P2-B, P2-C | Resolve condition identifier vocabulary issues | None       |

### 3.2 Tier separation per phase

Each phase follows a tiered execution:

| Tier                                  | Content                                                                                                                          |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0 (pre-check)**                | Confirm the current state matches the As-Is described in the gap analysis report.                                                |
| **Tier 1 (apply changes)**            | Apply the changes described in this plan to SKILL.md.                                                                            |
| **Tier 2 (objective verification)**   | Run YAML parse validation, verify conflict resolution is deterministic (P1), verify all identifiers resolve to definitions (P2). |
| **Tier 3 (subjective quality check)** | Human review to confirm semantic intent is preserved and wording is clear.                                                       |

### 3.3 Acceptance criteria

#### Phase 1 (P1) acceptance

1. `interpretation.priority` and `precedence_and_conflict.conflict_policy.MUST_vs_MUST` produce a single, deterministic conflict resolution procedure.
2. For two MUST rules in the same layer with different priorities, the higher numeric priority wins (no halt).
3. For two MUST rules in the same layer with equal priority, the runner halts or requests clarification.
4. YAML parses successfully.

#### Phase 2 (P2) acceptance

1. Every condition identifier used in any rule's `conditions` has a matching key in `definitions`.
2. Token forms in `conditions` and `definitions` keys are identical (no space-vs-hyphen mismatch).
3. `compound_conditions`'s MUST requirement is satisfied.
4. No rule's semantic intent has changed.
5. YAML parses successfully.

## 4. Risks and considerations

| Risk                                                                                                | Mitigation                                                                                                |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| P2-C touches ~30 rules; risk of introducing typos                                                   | Mechanical find-and-replace; verify by extracting all condition identifiers and matching to definitions   |
| Hyphen-delimited trigger identifiers (P2-C) may reduce human readability                            | Consistent with existing definitions style; readability trade-off is acceptable for machine-verifiability |
| P1-A expands the `MUST_vs_MUST` string; risk of introducing new ambiguity                           | The three-step procedure is explicit and exhaustive; verification criteria check determinism              |
| Changes to `conditions` strings may affect runner behavior if the runner already uses these strings | Since the current identifiers are undefined, no compliant runner can rely on them; normalization is safe  |

## 5. Items for future consideration

1. **Schema or linter for condition identifier validation**: implement a tool that extracts all condition identifiers from rule records and verifies they exist in `definitions`.
2. **`MUST_vs_SHOULD` and `prohibition_vs_other` alignment**: after resolving `MUST_vs_MUST`, review whether the other conflict policy entries also need similar layer/priority scoping.
3. **`triggers` section**: as the number of trigger identifiers grows, consider introducing a dedicated `triggers` section separate from `definitions` for organizational clarity.
4. **Formal grammar for compound conditions**: define a BNF or similar grammar for condition strings to enable fully mechanical parsing and validation.
