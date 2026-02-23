# Remediation Plan for P1 (Conflict Resolution Ambiguity) and P2 (Condition Identifier Vocabulary)

Target file (canonical): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
Path note: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`,
`.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` are all symlinks to
`../.agents/skills`; fixes only need to be made to the single canonical file.

Source: `docs/.tmp/report_p1_p2_gap_analysis.md`

## 0. Purpose and scope of this document

### 0.1 Purpose

This document defines a concrete remediation plan to resolve the two issues identified in
`docs/.tmp/report_p1_p2_gap_analysis.md`:

- **P1 (Critical)**: The conflict between `interpretation.priority` and
  `precedence_and_conflict.conflict_policy.MUST_vs_MUST`, which leaves the behavior of a
  runner indeterminate when two MUST rules with different numeric priorities in the same
  layer collide.
- **P2 (High)**: The self-violation of the `compound_conditions` MUST requirement, where
  condition identifiers used in rule `conditions` arrays are either (a) not defined in
  `definitions` at all, or (b) use a different token form (space-separated) than the
  `definitions` keys (hyphen-separated).

### 0.2 Non-goals

- Concrete file edits to AI directive files are out of scope. This document specifies
  *what* to change, *why*, and the acceptance criteria, but does not perform the edits.
- Issues outside P1 and P2 (e.g., the MUST NOT-focused section issue addressed in
  `plan.final.ascii.md`) are not in scope.
- Rollout to files other than the authoring skill is not in scope.

### 0.3 Definitions

- **authoring skill**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`.
- **rule record**: A structured record with exactly the fields: `id`, `layer`, `priority`,
  `statement`, `conditions`, `exceptions`, `verification`.
- **runner**: The execution environment that applies or verifies compliance with AI
  directive files.
- **condition identifier**: A string token used in a rule record's `conditions` array,
  which `interpretation.compound_conditions` requires to be defined in the file or in
  `definitions`.
- **compound condition**: A condition entry of the form `"A and B"` (literal ` and `
  separator), per `interpretation.compound_conditions`.

### 0.4 Constraints on this plan

- All proposed changes MUST preserve the existing rule-record schema
  (`id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`).
- All proposed changes MUST result in YAML that parses successfully with a
  standard-compliant YAML parser.
- Changes MUST NOT alter the intent or semantics of existing rules unless explicitly
  stated as part of the fix.
- The plan MUST be self-contained: all necessary context is included within this document
  and the referenced gap analysis report.

---

## 1. P1: Conflict Resolution Ambiguity

### 1.1 Problem summary

Two sections of the SKILL.md provide contradictory instructions to a runner when two MUST
rules in the same layer have different numeric priority values:

| Section                          | Instruction                                       |
| -------------------------------- | ------------------------------------------------- |
| `interpretation.priority`        | Higher numeric priority wins within the same layer |
| `conflict_policy.MUST_vs_MUST`   | Halt or request clarification unconditionally      |

A runner cannot follow both instructions simultaneously when, for example, rule A
(L2, priority 98) and rule B (L2, priority 95) conflict: `interpretation.priority` says
rule A wins, but `MUST_vs_MUST` says to halt.

The root cause is that `MUST_vs_MUST` does not specify the precondition under which it
applies, namely that it should apply only *after* layer and priority resolution have been
attempted and have failed to break the tie.

### 1.2 Proposed change

#### Change P1-A: Narrow the applicability of `MUST_vs_MUST`

Rewrite the `precedence_and_conflict.conflict_policy.MUST_vs_MUST` value to explicitly
state that halting applies only when layer and priority cannot resolve the conflict.

**Current text:**

```yaml
MUST_vs_MUST: "Halt or request clarification; MUST NOT silently choose one."
```

**Proposed text:**

```yaml
MUST_vs_MUST: "When two MUST rules conflict and have the same layer and the same
  priority, halt or request clarification; MUST NOT silently choose one. When layer
  differs, the rule with higher-precedence layer wins. When layer is the same but
  priority differs, the rule with higher numeric priority wins."
```

#### Change P1-B: Add a clarifying note to `interpretation.priority`

Add a forward reference from `interpretation.priority` to `conflict_policy` so the
relationship between the two sections is explicit.

**Current text:**

```yaml
priority: "Each rule has layer (L0-L4) and priority (numeric); L0 has highest
  precedence, and within the same layer, higher priority number wins. See
  precedence_and_conflict for details."
```

**Proposed text:**

```yaml
priority: "Each rule has layer (L0-L4) and priority (numeric); L0 has highest
  precedence, and within the same layer, higher priority number wins. When two
  rules share the same layer and the same priority, conflict_policy applies. See
  precedence_and_conflict for details."
```

### 1.3 Design rationale

1. **Deterministic resolution**: After the change, the runner follows a strict cascade:
   (a) compare layer, (b) compare priority, (c) apply conflict policy. At no point are
   two instructions in conflict.
2. **Minimal change**: Only two string values are rewritten. No new keys, no structural
   changes, no rule records added or removed.
3. **Backward compatibility**: The existing behavior for same-layer-same-priority
   conflicts (halt) is preserved. The change only *narrows* the applicability of halting to
   exclude cases already resolvable by priority.
4. **Consistency with `failure_states_and_degradation`**: The `rule-conflict` failure
   state already says "Apply precedence_and_conflict; if unresolved MUST halt or request
   clarification", which aligns with the proposed cascade. Change P1-A brings
   `conflict_policy.MUST_vs_MUST` into alignment with this existing guidance.

### 1.4 Conflict resolution cascade (post-fix)

The following cascade is deterministic and resolves every possible two-rule conflict:

```
Step 1: Compare layers.
  - If layers differ: rule with higher-precedence layer (lower index) wins.
  - If layers are the same: proceed to Step 2.

Step 2: Compare numeric priority.
  - If priorities differ: rule with higher numeric priority wins.
  - If priorities are equal: proceed to Step 3.

Step 3: Apply conflict_policy.
  - MUST vs MUST (same layer, same priority): Halt or request clarification.
  - MUST vs SHOULD: MUST wins.
  - prohibition vs other: Prohibition wins.
```

### 1.5 Acceptance criteria for P1

| ID     | Criterion                                                                    |
| ------ | ---------------------------------------------------------------------------- |
| P1-AC1 | `conflict_policy.MUST_vs_MUST` explicitly states it applies only when layer  |
|        | and priority are equal.                                                      |
| P1-AC2 | `interpretation.priority` references `conflict_policy` for the equal-        |
|        | priority case.                                                               |
| P1-AC3 | No logical contradiction exists between `interpretation.priority` and        |
|        | `conflict_policy.MUST_vs_MUST` for any combination of layer and priority.    |
| P1-AC4 | The YAML parses successfully with a standard-compliant YAML parser.          |
| P1-AC5 | The `failure_states_and_degradation.failure_states` entry for `rule-conflict` |
|        | remains consistent with the updated conflict_policy.                         |

---

## 2. P2: Condition Identifier Vocabulary

### 2.1 Problem summary

`interpretation.compound_conditions` states (MUST):

> "such identifiers MUST be defined in this file or in definitions."

However, the file violates its own requirement in two ways:

**Problem A -- Undefined identifiers**: The following identifiers are used in `conditions`
arrays throughout the file but have no entry in `definitions`:

| Identifier                                              | Usage context                 |
| ------------------------------------------------------- | ----------------------------- |
| `creating AI directive file`                            | Most rules' conditions        |
| `editing AI directive file`                             | Most rules' conditions        |
| `creating AI directive file that contains YAML block`   | yaml-include-* rules          |
| `editing AI directive file that contains YAML block`    | yaml-include-* rules          |
| `scope high-stakes`                                     | tier-separation rules         |
| `scope multi-constraint`                                | tier-separation rules         |
| `scope long-form reasoning`                             | tier-separation rules         |

**Problem B -- Token form mismatch**: The scope identifiers in `definitions` use hyphen
separation (e.g., `scope-high-stakes`), but the `conditions` arrays use space separation
(e.g., `scope high-stakes`). Since these are distinct YAML string values, a runner or
linter performing string comparison would fail to match them.

### 2.2 Proposed changes

#### Change P2-A: Add missing condition identifiers to `definitions`

Add the following entries to the `definitions` section:

```yaml
creating-ai-directive-file:
  description: "Trigger condition: the agent is creating a new AI directive file."
  canonical-terms: ["creating AI directive file"]
editing-ai-directive-file:
  description: "Trigger condition: the agent is editing an existing AI directive file."
  canonical-terms: ["editing AI directive file"]
creating-ai-directive-file-that-contains-yaml-block:
  description: "Trigger condition: the agent is creating a new AI directive file
    that contains a YAML block."
  canonical-terms: ["creating AI directive file that contains YAML block"]
editing-ai-directive-file-that-contains-yaml-block:
  description: "Trigger condition: the agent is editing an existing AI directive file
    that contains a YAML block."
  canonical-terms: ["editing AI directive file that contains YAML block"]
```

#### Change P2-B: Standardize scope identifier tokens in `conditions` arrays

Normalize all scope identifier tokens in `conditions` arrays to match the hyphen-separated
keys already present in `definitions`. This affects the four tier-separation rules
(`tier-separation-when-applicable`, `tier-separation-define-scope-format-stopping`,
`tier-separation-bounded-iteration`, `tier-separation-objective-vs-subjective`).

**Current pattern** (in each tier-separation rule):

```yaml
conditions:
  [
    "creating AI directive file and scope high-stakes",
    "editing AI directive file and scope high-stakes",
    "creating AI directive file and scope multi-constraint",
    "editing AI directive file and scope multi-constraint",
    "creating AI directive file and scope long-form reasoning",
    "editing AI directive file and scope long-form reasoning",
  ]
```

**Proposed pattern** (in each tier-separation rule):

```yaml
conditions:
  [
    "creating-ai-directive-file and scope-high-stakes",
    "editing-ai-directive-file and scope-high-stakes",
    "creating-ai-directive-file and scope-multi-constraint",
    "editing-ai-directive-file and scope-multi-constraint",
    "creating-ai-directive-file and scope-long-form-reasoning",
    "editing-ai-directive-file and scope-long-form-reasoning",
  ]
```

#### Change P2-C: Normalize all remaining condition identifiers

Update all non-tier-separation rules to use the hyphen-separated identifier form.

**Current form** (used in most rules):

```yaml
conditions: ["creating AI directive file", "editing AI directive file"]
```

**Proposed form:**

```yaml
conditions: ["creating-ai-directive-file", "editing-ai-directive-file"]
```

**Current form** (used in yaml-include-* rules):

```yaml
conditions:
  ["creating AI directive file that contains YAML block",
   "editing AI directive file that contains YAML block"]
```

**Proposed form:**

```yaml
conditions:
  ["creating-ai-directive-file-that-contains-yaml-block",
   "editing-ai-directive-file-that-contains-yaml-block"]
```

#### Change P2-D: Add a convention statement for identifier token form

Add a statement in `interpretation` (or in `definitions` preamble) that declares the
canonical token form for condition identifiers, making future inconsistencies preventable.

**Proposed addition** (as a new key under `interpretation`):

```yaml
condition_identifiers: "Condition identifiers in conditions arrays MUST use
  hyphen-separated lowercase form matching the corresponding definitions key.
  When a compound condition uses the 'A and B' form, both A and B MUST be
  hyphen-separated identifiers defined in definitions."
```

### 2.3 Design rationale

1. **Self-compliance**: After the changes, every identifier in every `conditions` array
   has a corresponding entry in `definitions`. The `compound_conditions` MUST requirement
   is satisfied.
2. **Machine-verifiable**: A linter can extract all condition identifiers (splitting
   compound conditions on ` and `), then check each token against `definitions` keys.
   The hyphen-separated canonical form guarantees exact string matching.
3. **Minimal semantic change**: No rule's meaning changes. The identifiers are renamed
   to a canonical form, and descriptions are added, but the set of applicable conditions
   remains identical.
4. **Consistency with existing style**: The `definitions` section already uses
   hyphen-separated keys (`scope-high-stakes`, `scope-multi-constraint`, etc.). The
   proposed changes extend this convention to all identifiers.

### 2.4 Affected rules inventory

The following is a complete list of rules that use condition identifiers requiring changes.

**Rules using `["creating AI directive file", "editing AI directive file"]`:**

- no-ambiguous-modals
- no-rely-on-model-verify
- no-duplicate-rules
- no-prose-only-carrier
- no-rely-on-prior-state
- no-treat-explanatory-must-not-as-prohibition
- design-assume-probabilistic
- design-define-failure-states
- compliance-verifiable-after-generation
- rules-enumerable
- verification-machine-checkable
- structure-support-schema
- content-invocation-scoped
- constraints-self-contained
- description-includes-trigger-conditions
- frontmatter-description-present
- frontmatter-description-non-empty
- frontmatter-description-length-bounds
- frontmatter-description-states-what
- frontmatter-description-keywords
- frontmatter-description-folded-multiline
- frontmatter-description-folded-multiline-guidelines
- rule-record-schema
- define-precedence-order
- define-conflict-policy
- one-obligation-per-rule
- verification-criterion-per-must
- explanatory-must-not-permitted
- explanatory-must-not-for-clarity
- use-normative-keywords
- conditions-exceptions-enumerated
- prohibitions-dedicated-section
- prohibitions-override
- compliance-externalized

**Rules using `["creating AI directive file that contains YAML block", ...]`:**

- no-ambiguous-modals-in-yaml
- yaml-include-interpretation-semantics
- yaml-include-closed-world-statement
- yaml-include-constraints
- yaml-include-error-handling
- yaml-include-rule-priority

**Rules using compound conditions with scope identifiers:**

- tier-separation-when-applicable
- tier-separation-define-scope-format-stopping
- tier-separation-bounded-iteration
- tier-separation-objective-vs-subjective

### 2.5 Acceptance criteria for P2

| ID     | Criterion                                                                    |
| ------ | ---------------------------------------------------------------------------- |
| P2-AC1 | Every identifier token used in any `conditions` array has a matching key in  |
|        | `definitions`.                                                               |
| P2-AC2 | All condition identifiers use hyphen-separated lowercase form.               |
| P2-AC3 | All compound conditions (containing ` and `) decompose into tokens that each |
|        | have a matching key in `definitions`.                                        |
| P2-AC4 | The `compound_conditions` MUST requirement is satisfied (no self-violation).  |
| P2-AC5 | No rule's applicability semantics are altered by the identifier rename.      |
| P2-AC6 | The YAML parses successfully with a standard-compliant YAML parser.          |
| P2-AC7 | A `condition_identifiers` convention statement exists in `interpretation`.    |

---

## 3. Execution plan

### 3.1 Ordering: P1 before P2

P1 and P2 are independent in terms of affected YAML keys. However, P1 is classified as
Critical and P2 as High, so P1 should be applied first. Additionally, P2 involves a larger
number of changes (touching nearly every rule record), so applying the smaller P1 change
first reduces merge conflict risk.

### 3.2 Tier-separated execution

Following the authoring skill's tier-separation principle, each phase uses bounded
iteration: execute the tier, freeze output, validate, then proceed.

#### Phase 1: Fix P1 (Conflict Resolution Ambiguity)

| Tier   | Scope                              | Output format       | Stopping condition                       |
| ------ | ---------------------------------- | ------------------- | ---------------------------------------- |
| Tier 0 | Confirm current text of the two    | Quoted current text  | Both sections identified and quoted      |
|        | target fields in SKILL.md          |                     |                                          |
| Tier 1 | Apply Changes P1-A and P1-B       | Updated YAML values | Both values rewritten per Section 1.2    |
| Tier 2 | Objective validation               | Pass/fail checklist | All P1-AC* criteria pass                 |
| Tier 3 | Subjective review                  | Human sign-off      | Wording preserves original intent        |

#### Phase 2: Fix P2 (Condition Identifier Vocabulary)

| Tier   | Scope                              | Output format       | Stopping condition                       |
| ------ | ---------------------------------- | ------------------- | ---------------------------------------- |
| Tier 0 | Inventory all condition identifiers| Table of identifiers| All identifiers catalogued               |
|        | across all rule records            | and their status    |                                          |
| Tier 1 | Apply Change P2-A (add definitions)| Updated definitions | All new entries added                    |
| Tier 2 | Apply Changes P2-B and P2-C       | Updated conditions  | All conditions arrays normalized         |
|        | (normalize conditions)             | arrays              |                                          |
| Tier 3 | Apply Change P2-D (add convention)| Updated interpret.  | Convention statement added               |
| Tier 4 | Objective validation               | Pass/fail checklist | All P2-AC* criteria pass                 |
| Tier 5 | Subjective review                  | Human sign-off      | Semantics preserved; wording clear       |

### 3.3 Verification methods

The following verification steps should be performed after each phase:

1. **YAML parse validation**: Parse both frontmatter and fenced YAML block with a
   standard YAML parser; both must succeed.
2. **Structure validation**: Confirm the file retains the required structure (frontmatter
   + single fenced YAML code block + whitespace-only separators).
3. **Rule-record schema check**: Confirm every rule record has exactly the fields `id`,
   `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`.
4. **Condition identifier resolution** (P2 only): Extract all `conditions` values, split
   compound conditions on ` and `, and confirm every resulting token exists as a key in
   `definitions`.
5. **Conflict resolution consistency** (P1 only): Trace the cascade (Section 1.4) for the
   example case (L2 priority 98 vs L2 priority 95) and confirm a single deterministic
   outcome.

---

## 4. Risk assessment

| Risk                                             | Likelihood | Impact | Mitigation                               |
| ------------------------------------------------ | ---------- | ------ | ---------------------------------------- |
| P1 rewording introduces a new ambiguity          | Low        | High   | Acceptance criterion P1-AC3 requires     |
|                                                  |            |        | no logical contradiction; cascade in     |
|                                                  |            |        | Section 1.4 is fully enumerated.         |
| P2 identifier rename breaks downstream tooling   | Low        | Medium | No known downstream consumers of         |
|                                                  |            |        | condition identifier strings at present. |
| P2 large number of condition changes introduces  | Medium     | Medium | Tier-separated execution with per-tier   |
| typos or omissions                               |            |        | validation. Full inventory in 2.4.       |
| Interaction with plan.final.ascii.md changes     | Low        | Low    | P1/P2 do not touch prohibitions or       |
|                                                  |            |        | authoring_obligations statement fields   |
|                                                  |            |        | targeted by that plan (except for the    |
|                                                  |            |        | conditions arrays, which that plan does  |
|                                                  |            |        | not modify).                             |

---

## 5. Summary of all proposed changes

| Change ID | Target section(s)                   | Type          | Description                              |
| --------- | ----------------------------------- | ------------- | ---------------------------------------- |
| P1-A      | precedence_and_conflict             | Rewrite value | Narrow MUST_vs_MUST to same-layer-same-  |
|           | .conflict_policy.MUST_vs_MUST       |               | priority case only; enumerate all cases  |
| P1-B      | interpretation.priority             | Rewrite value | Add forward reference to conflict_policy |
|           |                                     |               | for equal-priority case                  |
| P2-A      | definitions                         | Add entries   | Define 4 new condition identifiers       |
| P2-B      | tier-separation rules' conditions   | Rewrite value | Normalize scope tokens to hyphen form    |
| P2-C      | All other rules' conditions         | Rewrite value | Normalize trigger tokens to hyphen form  |
| P2-D      | interpretation                      | Add key       | Declare canonical token form convention  |

Total: 2 value rewrites (P1), 4 new definition entries + ~44 conditions array rewrites +
1 new interpretation key (P2).

---

## 6. Open items and future work

1. **Linter for condition identifier resolution**: Implement a tool that extracts all
   `conditions` values, splits on ` and `, and checks each token against `definitions`
   keys. This would automate P2-AC1 through P2-AC4.
2. **Linter for conflict resolution consistency**: Implement a tool that verifies no pair
   of rules at the same layer and priority have conflicting MUST statements without an
   explicit exception or documented resolution.
3. **Integration with plan.final.ascii.md**: If the changes from that plan (MUST NOT
   section remediation) are applied first, the P2-C changes (conditions normalization)
   should be applied to the post-fix file. The changes do not conflict structurally, but
   the order of application should be coordinated.
