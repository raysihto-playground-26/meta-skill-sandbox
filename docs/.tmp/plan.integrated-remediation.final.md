# Integrated Remediation Plan (Final): P1 and P2 Gap Resolution

This document consolidates four R1 remediation plans into a single
integrated plan to resolve the two issues identified in the gap analysis
report (docs/.tmp/report_p1_p2_gap_analysis.md).

Target file: .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md

---

## 0. Purpose, Scope, and Constraints

### 0.1 Purpose

Resolve two internal consistency issues in the authoring meta-skill:

| ID  | Issue                                                      | Severity |
| --- | ---------------------------------------------------------- | -------- |
| P1  | interpretation.priority vs MUST_vs_MUST contradiction      | Critical |
| P2  | Condition identifier vocabulary undefined + token mismatch | High     |

P1 causes indeterminate runner behavior when two MUST rules with different
numeric priorities in the same layer collide. P2 is a self-violation of
the compound_conditions MUST requirement, where condition identifiers are
either absent from definitions or use a different token form.

### 0.2 Target File

.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md

Path note: .cursor/skills/, .github/skills/, .claude/skills/,
.agent/skills/, .gemini/skills/, .opencode/skills/, .windsurf/skills/
are all symlinks to ../.agents/skills/. Only the single canonical file
under .agents/skills/ requires modification.

### 0.3 Scope

In scope:

- Changes to YAML string values within the fenced YAML code block of
  SKILL.md that resolve P1 and P2.
- Addition of new definition entries to the definitions section.
- Optional addition of a convention key to the interpretation section.

Out of scope:

- Changes to file structure (frontmatter layout, fenced block structure).
- Changes to other AI directive files.
- Runner or linter implementation.
- New normative rules or prohibitions.
- Rollout to files other than the authoring skill.

### 0.4 Constraints

C1: All changes MUST modify SKILL.md directly. Runner-side or linter-side
workarounds that leave the directive file internally inconsistent are
excluded. (All 4 primary plans agree on this approach; the gpt plan's
runner-only strategy is excluded.)
C2: All changes MUST result in YAML parseable by a standard-compliant
YAML parser.
C3: All changes MUST preserve the existing rule-record schema (id, layer,
priority, statement, conditions, exceptions, verification).
C4: Changes MUST NOT alter the semantic intent or applicability of
existing rules.
C5: The number of affected fields should be minimized while ensuring P1
and P2 are fully resolved.
C6: This plan does not show concrete changed YAML. Keywords, identifiers,
and field names may be referenced.
C5: Condition identifiers MUST be canonical kebab-case (hyphen-separated lowercase). Space-containing identifiers MUST NOT be used in either definitions keys or conditions tokens.
C6: Alias, synonym, normalization, or heuristic matching MUST NOT be introduced. Condition resolution MUST be performed by exact key match only.
C7: P2 remediation MUST apply the minimum set of textual edits required to satisfy C5–C6 (i.e., only the condition tokens and definitions entries that are currently non-canonical or unresolved are changed). Canonical, already-resolved identifiers remain untouched.

### 0.5 Definitions

Terms used throughout this document:

- authoring skill: the file
  .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md.
- rule record: a structured YAML record with exactly the fields: id,
  layer, priority, statement, conditions, exceptions, verification.
- runner: the execution environment that applies or verifies compliance
  with AI directive files.
- condition identifier: a string token used in a rule record's conditions
  array that identifies when the rule applies.
- compound condition: a condition entry of the form "A and B" (literal
  space-and-space separator), per interpretation.compound_conditions.

---

## 1. Source Plans and Consensus Analysis

### 1.1 Source Plans

| Plan    | Source file             | Approach              |
| ------- | ----------------------- | --------------------- |
| claude  | plan-r1.en.claude.md    | SKILL.md modification |
| codex   | plan-r1.en.codex.md     | SKILL.md modification |
| copilot | plan-r1.en.copilot.md   | SKILL.md modification |
| cursor  | plan-r1.en.cursor.md    | SKILL.md modification |
| gpt     | plan-r1.en.gpt.md (ref) | Runner/linter only    |

The gpt plan proposes runner/linter-side behavior without modifying the
directive file. This approach is excluded per constraint C1. However,
specific compatible ideas from the gpt plan are selectively incorporated
where noted (tagged G-n).

### 1.2 Unanimous Agreements (MUST)

The following items are agreed upon by all four primary plans and are
therefore designated MUST in this integrated plan.

P1 -- Conflict Resolution Ambiguity:

- U-P1-1: The conflict between interpretation.priority and MUST_vs_MUST
  MUST be resolved by narrowing the applicability of MUST_vs_MUST.
- U-P1-2: A deterministic three-step conflict resolution cascade MUST be
  established: (1) layer precedence, (2) numeric priority, (3) conflict
  policy only when both layer and priority are equal.
- U-P1-3: The MUST_vs_MUST value MUST explicitly state it applies only
  when layer and priority are equal.
- U-P1-4: interpretation.priority MUST be aligned to reference
  conflict_policy as the fallback for the equal-priority case.
- U-P1-5: Only string value rewrites are required; no structural changes,
  no new rules, no new keys.

P2 -- Condition Identifier Vocabulary:

- U-P2-1: All condition identifiers used in conditions arrays MUST be
  defined in the definitions section.
- U-P2-2: The token form used in conditions and the key form in
  definitions MUST be identical (exact string match).
- U-P2-3: The canonical token form MUST be hyphen-separated lowercase,
  consistent with existing definitions keys (e.g., scope-high-stakes,
  ai-directive-files).
- U-P2-4: Missing trigger identifiers MUST be added to definitions.
- U-P2-5: Scope identifiers in conditions arrays MUST be normalized to
  match the existing hyphenated definitions keys.
- U-P2-6: All compound conditions MUST decompose into tokens that each
  resolve to a definitions key.
- U-P2-7: No rule's semantic applicability MUST be altered by the
  identifier normalization.

### 1.3 Majority Agreements (SHOULD)

- M-1: A convention statement for condition identifier format SHOULD be
  added to the interpretation section to prevent future regressions.
  (claude proposes explicitly; copilot and codex implicitly support via
  verification alignment requirements.)
- M-2: Tier-separated execution SHOULD be applied during implementation.
  (claude, codex, copilot include tier separation; cursor uses simpler
  phasing.)
- M-3: A complete inventory of all affected condition identifiers SHOULD
  be maintained during implementation to prevent omissions.
  (claude, codex, copilot.)

### 1.4 Selectively Incorporated from gpt Plan

- G-1: The three-step conflict resolution cascade (section 2.3) adopts
  the algorithmic specification style from the gpt plan, which describes
  the procedure as a step-by-step decision sequence suitable for
  deterministic implementation. This is compatible with C1 because the
  algorithm describes what SKILL.md should express.
- G-2: The concept of verifying the cascade against concrete example cases
  (gpt plan section 2) is incorporated into the verification strategy
  (section 5.1).

---

## 2. P1: Conflict Resolution Ambiguity

### 2.1 Problem Summary

Two sections of SKILL.md contradict each other:

- interpretation.priority (line 24) states that within the same layer,
  the rule with higher numeric priority wins.
- precedence_and_conflict.conflict_policy.MUST_vs_MUST (line 30) states
  unconditionally: halt or request clarification.

When two MUST rules in the same layer have different priorities (e.g., L2
priority 98 vs L2 priority 95), the runner receives contradictory
instructions. This is P1 (Critical) in the gap analysis.

Root cause: MUST_vs_MUST does not specify that it applies only after
layer and priority resolution have failed to break the tie.

### 2.2 Resolution (MUST -- Unanimous)

Per U-P1-1 through U-P1-5:

(a) Rewrite MUST_vs_MUST to explicitly state it applies only when both
layer and priority are equal.
(b) Rewrite interpretation.priority to include a forward reference to
conflict_policy for the equal-priority case.

### 2.3 Three-Step Conflict Resolution Cascade

After the fix, SKILL.md MUST express the following deterministic cascade
(per U-P1-2, incorporating G-1):

Step 1 -- Layer comparison:
If two conflicting rules have different layers, the rule in the
higher-precedence layer (lower index in layer_order) wins.
If layers are the same, proceed to Step 2.

Step 2 -- Numeric priority comparison:
If two conflicting rules in the same layer have different numeric
priorities, the rule with the higher numeric priority wins.
If priorities are also equal, proceed to Step 3.

Step 3 -- Conflict policy:
If two conflicting rules have the same layer and same priority:

- MUST vs MUST: Halt or request clarification.
- MUST vs SHOULD: MUST wins.
- Prohibition vs other: Prohibition wins
  (governed by the prohibitions override statement).

This cascade is exhaustive: every two-rule conflict reaches exactly one
deterministic outcome.

### 2.4 Changes Required

| ID   | Target field                                         | Type          |
| ---- | ---------------------------------------------------- | ------------- |
| P1-A | precedence_and_conflict.conflict_policy.MUST_vs_MUST | Rewrite value |
| P1-B | interpretation.priority                              | Rewrite value |

Total affected fields: 2 string values.
No new keys. No new rules. No structural changes.

### 2.5 Design Rationale

1. Deterministic resolution: the runner follows a strict cascade with no
   point of contradictory instructions.
2. Minimal change: only two string values are rewritten.
3. Backward compatibility: the halt behavior for same-layer-same-priority
   conflicts is preserved; the change only narrows its applicability.
4. Consistency with failure_states_and_degradation: the rule-conflict
   failure state already says "Apply precedence_and_conflict; if
   unresolved MUST halt or request clarification", which aligns with
   the proposed cascade.

### 2.6 Acceptance Criteria

| ID     | Criterion                                                  |
| ------ | ---------------------------------------------------------- |
| P1-AC1 | MUST_vs_MUST explicitly states it applies only when layer  |
|        | and priority are equal.                                    |
| P1-AC2 | interpretation.priority references conflict_policy for the |
|        | equal-priority case.                                       |
| P1-AC3 | No logical contradiction exists between interpretation     |
|        | .priority and MUST_vs_MUST for any combination of layer    |
|        | and priority values.                                       |
| P1-AC4 | The failure_states_and_degradation entry for rule-conflict |
|        | remains consistent with the updated cascade.               |
| P1-AC5 | YAML parses successfully.                                  |

---

## 3. P2: Condition Identifier Vocabulary

### 3.1 Problem Summary

interpretation.compound_conditions (line 22) requires (MUST) that all
condition identifiers be defined in the file or in definitions. The file
violates this requirement in two ways:

Problem A -- Undefined identifiers:
Seven identifier strings used in conditions arrays have no entry in
definitions:

| Identifier                                          | Usage context          |
| --------------------------------------------------- | ---------------------- |
| creating AI directive file                          | Most rules' conditions |
| editing AI directive file                           | Most rules' conditions |
| creating AI directive file that contains YAML block | yaml-include-\* rules  |
| editing AI directive file that contains YAML block  | yaml-include-\* rules  |
| scope high-stakes                                   | tier-separation rules  |
| scope multi-constraint                              | tier-separation rules  |
| scope long-form reasoning                           | tier-separation rules  |

Problem B -- Token form mismatch:
Definitions uses hyphenated keys (scope-high-stakes, scope-multi-constraint,
scope-long-form-reasoning) while conditions uses space-separated strings
(scope high-stakes, scope multi-constraint, scope long-form reasoning).
These are distinct YAML strings; mechanical matching fails.

### 3.2 Resolution (MUST -- Unanimous)

Per U-P2-1 through U-P2-7, with the additional constraints C5–C7:

(a) Add (or rename, if necessary) `definitions` entries so that every condition identifier used anywhere in the file is defined as a canonical kebab-case key (hyphen-separated lowercase).
(b) Update `conditions` tokens only where needed so that every identifier token is canonical kebab-case and matches a `definitions` key by exact string equality.
(c) Do not introduce aliases, alternate spellings, normalization layers, or heuristic matching. Condition resolution is exact-match only.
(d) Preserve the existing compound condition grammar, including the literal separator `" and "` per the `compound_conditions` requirement.

### 3.3 Changes Required

| ID   | Target                      | Type           | Affected count |
| ---- | --------------------------- | -------------- | -------------- |
| P2-A | definitions section         | Add entries    | 4 new entries  |
| P2-B | conditions across all rules | Rewrite values | 44 rules       |

P2-A -- Add definitions for the following identifiers:

- creating-ai-directive-file
- editing-ai-directive-file
- creating-ai-directive-file-that-contains-yaml-block
- editing-ai-directive-file-that-contains-yaml-block

These MUST use hyphen-separated lowercase keys, consistent with the
existing definitions convention (e.g., scope-high-stakes,
ai-directive-files, tier-separation).

Note: scope-high-stakes, scope-multi-constraint, and
scope-long-form-reasoning already exist as definitions keys and do NOT
need new entries. They only need their corresponding conditions tokens
to be normalized.

P2-B -- Normalize conditions arrays using the following mapping:

| Current token (in conditions)                       | Normalized (definitions key)                        |
| --------------------------------------------------- | --------------------------------------------------- |
| creating AI directive file                          | creating-ai-directive-file                          |
| editing AI directive file                           | editing-ai-directive-file                           |
| creating AI directive file that contains YAML block | creating-ai-directive-file-that-contains-yaml-block |
| editing AI directive file that contains YAML block  | editing-ai-directive-file-that-contains-yaml-block  |
| scope high-stakes                                   | scope-high-stakes                                   |
| scope multi-constraint                              | scope-multi-constraint                              |
| scope long-form reasoning                           | scope-long-form-reasoning                           |

For compound conditions, both parts are normalized while preserving the
" and " separator. Example:
"creating AI directive file and scope high-stakes"
becomes "creating-ai-directive-file and scope-high-stakes".

### 3.4 Affected Rules Inventory

Rules with conditions ["creating AI directive file",
"editing AI directive file"] (34 rules):

- Prohibitions (6): no-ambiguous-modals, no-rely-on-model-verify,
  no-duplicate-rules, no-prose-only-carrier, no-rely-on-prior-state,
  no-treat-explanatory-must-not-as-prohibition
- Authoring obligations (28): design-assume-probabilistic,
  design-define-failure-states, compliance-verifiable-after-generation,
  rules-enumerable, verification-machine-checkable,
  structure-support-schema, content-invocation-scoped,
  constraints-self-contained, description-includes-trigger-conditions,
  frontmatter-description-present, frontmatter-description-non-empty,
  frontmatter-description-length-bounds,
  frontmatter-description-states-what,
  frontmatter-description-keywords,
  frontmatter-description-folded-multiline,
  frontmatter-description-folded-multiline-guidelines,
  rule-record-schema, define-precedence-order, define-conflict-policy,
  one-obligation-per-rule, verification-criterion-per-must,
  explanatory-must-not-permitted, explanatory-must-not-for-clarity,
  use-normative-keywords, conditions-exceptions-enumerated,
  prohibitions-dedicated-section, prohibitions-override,
  compliance-externalized

Rules with YAML-block conditions (6):

- Prohibitions (1): no-ambiguous-modals-in-yaml
- Authoring obligations (5): yaml-include-interpretation-semantics,
  yaml-include-closed-world-statement, yaml-include-constraints,
  yaml-include-error-handling, yaml-include-rule-priority

Rules with compound scope conditions (4):

- tier-separation-when-applicable,
  tier-separation-define-scope-format-stopping,
  tier-separation-bounded-iteration,
  tier-separation-objective-vs-subjective

Total: 44 rules require conditions value updates.

### 3.5 Change Volume and Minimization

The gap analysis indicates up to 44 rules may be impacted by condition-token remediation. Under C7 (minimum-change), only rules whose `conditions` arrays contain non-canonical tokens (non-kebab-case or otherwise mismatched against `definitions`) are edited. Rules whose tokens are already canonical and resolve by exact match are left untouched.

Where edits are required, the operation remains mechanical: apply an explicit, finite mapping table from legacy tokens to canonical kebab-case tokens, and ensure the corresponding `definitions` keys exist. No semantic reinterpretation of rule intent is performed; only the identifier surface form is corrected.

The alternative of avoiding `conditions` edits by adding space-containing quoted keys in `definitions` (copilot approach) is rejected because it violates C5 (single canonical identifier convention) and increases long-term drift risk by allowing two incompatible vocabularies to coexist.

### 3.6 Convention Statement (MUST -- per C5–C6)

A convention statement MUST be added to the `interpretation` section under a new key (e.g., `condition_identifiers`) declaring:

- Condition identifiers in `conditions` arrays MUST use canonical kebab-case (hyphen-separated lowercase) and MUST match the corresponding `definitions` key by exact string equality.
- `definitions` keys for condition identifiers MUST be canonical kebab-case; space-containing keys MUST NOT be introduced.
- No aliasing, synonym tables, normalization layers, or heuristic matching is permitted; resolution is exact-match only.
- In compound conditions of the form `"A and B"`, both `A` and `B` MUST be canonical kebab-case identifiers defined in `definitions`.

This is a single new key under `interpretation`, not a new rule record. It prevents future regressions where new identifiers are added in a non-canonical form or without a `definitions` entry.

### 3.7 Acceptance Criteria

| ID     | Criterion                                                |
| ------ | -------------------------------------------------------- |
| P2-AC1 | Every identifier token in any conditions array has a     |
|        | matching key in definitions.                             |
| P2-AC2 | All condition identifiers use hyphen-separated lowercase |
|        | form.                                                    |
| P2-AC3 | All compound conditions decompose into tokens that each  |
|        | match a definitions key.                                 |
| P2-AC4 | The compound_conditions MUST requirement is satisfied    |
|        | (no self-violation).                                     |
| P2-AC5 | No rule's applicability semantics are altered.           |
| P2-AC6 | YAML parses successfully.                                |

---

## 4. Execution Plan

### 4.1 Ordering

P1 and P2 are independent in terms of affected YAML keys. P1 is
classified as Critical and involves only 2 string rewrites; P2 is High
and involves a larger volume of changes. Applying P1 first is
recommended to resolve the higher-severity issue with minimal risk.

| Phase   | Changes          | Description                                                                              |
| ------- | ---------------- | ---------------------------------------------------------------------------------------- |
| Phase 0 | Inventory        | Extract all condition tokens; compute resolution status; produce mapping + impact report |
| Phase 1 | P1-A, P1-B       | Resolve conflict resolution ambiguity                                                    |
| Phase 2 | P2-A, P2-B, P2-C | Resolve condition identifier vocabulary (minimum-change per C7)                          |

### 4.2 Tier-Separated Execution (SHOULD -- per M-2)

Each phase SHOULD follow tiered execution with bounded iteration:

Phase 1 (P1):

| Tier | Scope                                          | Stopping condition                    |
| ---- | ---------------------------------------------- | ------------------------------------- |
| T0   | Confirm current text of MUST_vs_MUST and       | Both fields identified and match the  |
|      | interpretation.priority matches As-Is state    | As-Is described in the gap analysis   |
| T1   | Apply P1-A and P1-B rewrites                   | Both values rewritten per section 2.2 |
| T2   | Objective verification (P1-AC1 through P1-AC5) | All acceptance criteria pass          |

Phase 2 (P2):

| Tier | Scope                                            | Stopping condition                     |
| ---- | ------------------------------------------------ | -------------------------------------- |
| T0   | Build complete inventory of all condition        | All identifiers catalogued with        |
|      | identifiers and their current vs target forms    | current and target forms (per M-3)     |
| T1   | Apply P2-A (add definitions entries)             | All 4 new entries present              |
| T2   | Apply P2-B (normalize all conditions arrays)     | All 44 rules updated per mapping table |
| T3   | Apply P2-C (add convention statement) if adopted | Convention key present in interpret.   |
| T4   | Objective verification (P2-AC1 through P2-AC6)   | All acceptance criteria pass           |

---

## 5. Verification Strategy

Verification is designed for AI agent context analysis during
implementation. The agent performing the changes can execute these
checks as part of its reasoning process. External scripts run by humans
are not assumed.

### 5.1 P1 Verification

An AI agent implementing changes MUST verify:

(a) Read the updated MUST_vs_MUST and interpretation.priority values and
confirm the three-step cascade (section 2.3) is unambiguously
expressed by the combination of both fields.
(b) Trace the cascade for the example case from the gap analysis (L2
priority 98 vs L2 priority 95): confirm the outcome is deterministic
-- priority 98 wins, no halt. (Incorporates G-2.)
(c) Trace the cascade for the tie case (same layer, same priority):
confirm the outcome is halt or request clarification.
(d) Confirm failure_states_and_degradation.failure_states entry for
rule-conflict remains consistent with the updated cascade.
(e) Confirm YAML parses without errors.

### 5.2 P2 Verification

An AI agent implementing changes MUST verify:

(a) Enumerate all conditions values from all rule records in the file.
(b) For each condition entry: - If simple (no " and " separator): confirm it exists as a key in
definitions. - If compound ("A and B"): split on " and ", confirm both A and B
exist as keys in definitions.
(c) Confirm no space-vs-hyphen mismatches remain between conditions
tokens and definitions keys.
(d) Confirm all 4 new definitions entries are present and use
hyphen-separated lowercase keys.
(e) Confirm YAML parses without errors.

### 5.3 Cross-Cutting Verification

(a) Confirm the file structure remains valid: frontmatter block +
single fenced YAML code block + whitespace-only separators.
(b) Confirm all rule records retain exactly the fields: id, layer,
priority, statement, conditions, exceptions, verification.
(c) Confirm no rule's statement or verification field has been altered
(only conditions values and interpretation/conflict_policy strings
should change).

---

## 6. Risk Assessment

| Risk                                        | Likelihood | Impact | Mitigation                           |
| ------------------------------------------- | ---------- | ------ | ------------------------------------ |
| P1 rewording introduces new ambiguity       | Low        | High   | Cascade in 2.3 is fully enumerated;  |
|                                             |            |        | verification 5.1(b)(c) checks        |
|                                             |            |        | determinism against concrete cases.  |
| P2 large-scale conditions normalization     | Medium     | Medium | Mechanical 7-entry mapping table;    |
| introduces typos or omissions               |            |        | full inventory per M-3;              |
|                                             |            |        | verification 5.2 detects misses.     |
| Hyphenated identifiers differ from current  | Low        | Low    | Consistent with existing definitions |
| space-separated form in readability         |            |        | convention; AI agent interpretation  |
|                                             |            |        | is the priority (per plan context).  |
| Future rule additions reintroduce undefined | Medium     | Low    | Convention statement P2-C prevents   |
| identifiers                                 |            |        | regression; verification 5.2         |
|                                             |            |        | provides detection method.           |
| Interaction with other pending changes      | Low        | Low    | P1 and P2 changes do not touch rule  |
|                                             |            |        | statement or verification fields;    |
|                                             |            |        | conflict limited to conditions       |
|                                             |            |        | arrays which other plans do not      |
|                                             |            |        | modify.                              |

---

## 7. Summary of All Changes

### 7.1 Mandatory Changes (MUST)

| Change | Target                       | Type           | Description                         |
| ------ | ---------------------------- | -------------- | ----------------------------------- |
| P1-A   | conflict_policy.MUST_vs_MUST | Rewrite value  | Narrow to same-layer-same-priority  |
| P1-B   | interpretation.priority      | Rewrite value  | Add forward ref to conflict_policy  |
| P2-A   | definitions                  | Add entries    | 4 new trigger condition identifiers |
| P2-B   | conditions (across 44 rules) | Rewrite values | Normalize to hyphen-separated form  |

### 7.2 Recommended Change (SHOULD)

| Change | Target         | Type    | Description                      |
| ------ | -------------- | ------- | -------------------------------- |
| P2-C   | interpretation | Add key | condition_identifiers convention |

### 7.3 Totals

Mandatory: 2 value rewrites (P1) + 4 new definitions entries +
44 conditions array normalizations (P2) = 50 field-level changes.

Recommended: 1 new interpretation key.

Net new YAML keys: 4 (definitions) + 0-1 (interpretation).
Net new rule records: 0.
Structural changes: 0.

---

## 8. Provenance and Best-of Selection Summary

This section documents which ideas were adopted from each source plan.

From claude:

- Detailed acceptance criteria structure (adopted).
- Risk assessment with specific mitigations (adopted).
- P2-D convention statement concept (adopted as P2-C, SHOULD).
- Complete affected rules inventory (adopted as section 3.4).
- Tier-separated execution with per-tier tables (adopted as SHOULD).

From codex:

- Phased execution with explicit exit conditions (adopted).
- Verification alignment as a distinct concern (incorporated into
  section 5).
- Clean, concise acceptance criteria (adopted).

From copilot:

- Change size evaluation per change ID (adopted).
- Two-approach analysis for P2 with recommendation (analysis
  incorporated into section 3.5).
- Forward reference in interpretation.priority as a distinct change
  (adopted as P1-B, MUST per U-P1-4).
- Future consideration of triggers section and formal grammar for
  compound conditions (noted but not adopted for this revision).

From cursor:

- Concise problem statement format (adopted).
- Simple implementation order table (adopted in section 4.1).
- Focused success criteria (adopted).

From gpt (compatible parts only):

- Algorithmic specification style for the cascade (adopted as G-1,
  section 2.3).
- Test-case-style verification against concrete examples (adopted as
  G-2, section 5.1).
