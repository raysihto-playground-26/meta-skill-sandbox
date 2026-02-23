# Plan r2: Integrated Remediation Plan for P1 and P2

Target file (canonical): .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md

Path note: .cursor/skills/, .github/skills/, .claude/skills/, .agent/skills/,
.gemini/skills/, .opencode/skills/, .windsurf/skills/ are all symlinks to
../.agents/skills; fixes only need to be made to the single canonical file.

Source documents:

- docs/.tmp/report_p1_p2_gap_analysis.md (gap analysis)
- docs/.tmp/plan-r1.en.claude.md
- docs/.tmp/plan-r1.en.codex.md
- docs/.tmp/plan-r1.en.copilot.md
- docs/.tmp/plan-r1.en.cursor.md
- docs/.tmp/plan-r1.en.gpt.md (adopted selectively; see Section 0.4)


## 0. Purpose, scope, and constraints

### 0.1 Purpose

This document is an integrated (rev 2) remediation plan for the two issues
identified in docs/.tmp/report_p1_p2_gap_analysis.md:

| ID | Issue                                                    | Severity |
|----|----------------------------------------------------------|----------|
| P1 | interpretation.priority vs MUST_vs_MUST contradiction    | Critical |
| P2 | Condition identifier vocabulary undefined + token form   | High     |

This plan synthesizes the best elements from five r1 plans, using the four
specification-modification plans (Claude, Codex, Copilot, Cursor) as the
primary base. Items agreed upon by all four plans are marked as MUST
(unanimous). Elements from plan-r1.en.gpt.md are adopted selectively where
they do not contradict the specification-modification approach (see Section 0.4).

### 0.2 Scope

- In scope: changes to the YAML content of SKILL.md that resolve P1 and P2.
- Out of scope: changes to file structure (frontmatter, fenced block layout),
  changes to other AI directive files, linter/tooling implementation, rollout
  to other files.

### 0.3 Definitions

- authoring skill: .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md.
- rule record: a structured record with exactly the fields: id, layer, priority,
  statement, conditions, exceptions, verification.
- runner: the execution environment (including AI agents) that applies or
  verifies compliance with AI directive files.
- condition identifier: a string token used in a rule record's conditions
  array, which interpretation.compound_conditions requires to be defined in
  the file or in definitions.
- compound condition: a condition entry of the form "A and B" (literal
  space-and-space separator), per interpretation.compound_conditions.

### 0.4 Source plan contributions and exclusions

Base plans (specification-modification approach):

| Plan    | Key contribution adopted in this plan                      |
|---------|------------------------------------------------------------|
| Claude  | failure_states_and_degradation cross-reference for P1;     |
|         | affected-rules inventory for P2; interaction risk with     |
|         | plan.final.ascii.md                                        |
| Codex   | Phase 0 baseline inventory as prerequisite; Phase 3        |
|         | verification alignment as independent step; exit           |
|         | conditions per phase                                       |
| Copilot | Safety argument (undefined identifiers are safe to         |
|         | rename); P1-B classified as clarity improvement            |
| Cursor  | Concise stepwise structure; choice-point framing           |

Selectively adopted from GPT (non-contradictory with specification-modification):

| Element                  | Adopted as                                       |
|--------------------------|--------------------------------------------------|
| P1 verification fixtures | Mental-trace test scenarios for P1 acceptance    |

Excluded from GPT:

| Element                       | Reason for exclusion                             |
|-------------------------------|--------------------------------------------------|
| Runner/linter-only approach   | Misaligned with the requirement to fix SKILL.md  |
| Alias resolution mechanism    | Contradicts the goal of exact-match identifiers  |
| Reserved triggers concept     | Defers the problem instead of resolving it       |

### 0.5 Design priorities (from the task constraints)

1. AI agent correct interpretation is the primary goal; human readability is
   not a priority.
2. Perfect formal consistency is not required if intent is unambiguously
   interpretable by AI agents.
3. Mechanical verification means verification that an AI agent can perform
   during contextual analysis of the file, not human-operated scripts.
4. Minimum change for maximum effect: minimize the number of affected rules
   and sections while resolving both P1 and P2 fully.

### 0.6 Constraints on this plan

- All proposed changes MUST preserve the existing rule-record schema (id,
  layer, priority, statement, conditions, exceptions, verification).
- All proposed changes MUST result in YAML that parses successfully with a
  standard-compliant YAML parser.
- Changes MUST NOT alter the intent or semantics of existing rules unless
  explicitly stated as part of the fix.
- Concrete change code (YAML snippets, diffs) MUST NOT appear in this plan.
  Identifier names and keywords MAY be mentioned.
- This plan MUST be self-contained.
- AI directive files MUST NOT be modified as part of creating this plan.

---

## 1. P1: Conflict Resolution Ambiguity

### 1.1 Problem summary (from gap analysis)

Two sections of SKILL.md provide contradictory instructions when two MUST
rules in the same layer have different numeric priority values:

- interpretation.priority states: within the same layer, higher numeric
  priority wins.
- precedence_and_conflict.conflict_policy.MUST_vs_MUST states: halt or
  request clarification unconditionally.

A runner cannot follow both simultaneously when, for example, rule A
(L2, priority 98) and rule B (L2, priority 95) conflict.

Root cause: MUST_vs_MUST does not specify the precondition under which it
applies, namely that it should apply only after layer and priority resolution
have been attempted and failed to break the tie.

### 1.2 Unanimous resolution (MUST -- all 4 plans agree)

Establish a deterministic three-step conflict resolution cascade:

Step 1 -- Compare layers.
  If layers differ: rule with higher-precedence layer (lower index in
  layer_order) wins.
  If layers are the same: proceed to Step 2.

Step 2 -- Compare numeric priority.
  If priorities differ: rule with higher numeric priority wins.
  If priorities are equal: proceed to Step 3.

Step 3 -- Apply conflict_policy.
  MUST vs MUST (same layer, same priority): halt or request clarification.
  MUST vs SHOULD: MUST wins.
  Prohibition vs other: prohibition wins.

This cascade is deterministic and resolves every possible two-rule conflict.

### 1.3 Required changes

#### Change P1-A: Narrow the applicability of MUST_vs_MUST (MUST)

Rewrite the value of precedence_and_conflict.conflict_policy.MUST_vs_MUST to
explicitly state:

- It applies only when layer and priority are both equal.
- When layer differs, layer precedence resolves the conflict.
- When layer is the same but priority differs, numeric priority resolves it.

The existing halt/clarification behavior for the same-layer-same-priority
case MUST be preserved.

Affected section: precedence_and_conflict.conflict_policy.MUST_vs_MUST
(1 string value rewrite).

#### Change P1-B: Add forward reference to conflict_policy in interpretation.priority (MUST)

Add language to interpretation.priority stating that conflict_policy applies
when layer and priority are both equal. The existing phrase "See
precedence_and_conflict for details" already provides a forward reference;
the addition clarifies the boundary between priority resolution and
conflict_policy.

Affected section: interpretation.priority (1 string value rewrite).

Note: Copilot classified this as "optional, for clarity." However, all four
plans propose this change, and it eliminates a potential ambiguity for AI
agents reading the two sections independently. Per the unanimity rule, it is
included as MUST.

### 1.4 Cross-reference: failure_states_and_degradation (from Claude)

The failure_states_and_degradation.failure_states entry for rule-conflict
already states: "Apply precedence_and_conflict; if unresolved MUST halt or
request clarification." This aligns with the proposed cascade (halt occurs
only when precedence_and_conflict cannot resolve). No change is needed to
failure_states_and_degradation; however, the implementer MUST verify that
the post-fix wording of conflict_policy.MUST_vs_MUST remains consistent
with this entry.

### 1.5 P1 verification (MUST)

The following verification MUST be performed after applying P1 changes.
These are mental-trace scenarios that an AI agent can evaluate by reading
the post-fix file (adopted from GPT's test-case concept):

Scenario 1 -- Different layers:
  Rule X at L0/priority 50 conflicts with Rule Y at L2/priority 100.
  Expected: Rule X wins (L0 has higher-precedence layer).
  Verify: interpretation.priority and conflict_policy both support this.

Scenario 2 -- Same layer, different priority:
  Rule X at L2/priority 98 conflicts with Rule Y at L2/priority 95.
  Expected: Rule X wins (higher numeric priority).
  Verify: interpretation.priority says higher priority wins.
  Verify: conflict_policy.MUST_vs_MUST does NOT trigger (priorities differ).

Scenario 3 -- Same layer, same priority:
  Rule X at L2/priority 95 (MUST) conflicts with Rule Y at L2/priority 95 (MUST).
  Expected: Halt or request clarification.
  Verify: conflict_policy.MUST_vs_MUST triggers (layer and priority are equal).

All three scenarios MUST produce a single deterministic outcome with no
contradiction between interpretation.priority and conflict_policy.

### 1.6 P1 change size

Total: 2 string value rewrites. No new keys, no structural changes, no rule
records added or removed.

---

## 2. P2: Condition Identifier Vocabulary

### 2.1 Problem summary (from gap analysis)

interpretation.compound_conditions requires (MUST) that condition identifiers
be defined in the file or in definitions. The file violates its own
requirement in two ways:

Problem A -- Undefined identifiers: The following identifiers are used in
conditions arrays but have no entry in definitions:

- creating AI directive file
- editing AI directive file
- creating AI directive file that contains YAML block
- editing AI directive file that contains YAML block
- scope high-stakes
- scope multi-constraint
- scope long-form reasoning

Problem B -- Token form mismatch: The scope identifiers in definitions use
hyphen separation (scope-high-stakes, scope-multi-constraint,
scope-long-form-reasoning), but conditions arrays use space separation
(scope high-stakes, scope multi-constraint, scope long-form reasoning).
These are distinct YAML string values.

### 2.2 Unanimous resolution (MUST -- all 4 plans agree)

1. Every identifier used in any conditions array MUST have a corresponding
   definition entry.
2. The token form used in conditions and the key used in definitions MUST
   be identical (exact string match).
3. The compound_conditions MUST requirement MUST be satisfied (no
   self-violation).

### 2.3 Minimum-change strategy

The four r1 plans all propose adding definitions and normalizing token form.
However, they differ in how many rules' conditions arrays must be rewritten.

The full-normalization approach (Claude, Copilot) rewrites conditions in
approximately 44 rules to use hyphen-separated form. This is comprehensive
but has a large blast radius.

This plan adopts a hybrid minimum-change strategy that achieves the same
outcome with far fewer rule changes:

Strategy: Split the problem into two groups and apply different solutions
to each, minimizing the total number of changes.

Group 1 -- Trigger identifiers (4 identifiers, approximately 38 rules):

  Identifiers: creating AI directive file, editing AI directive file,
  creating AI directive file that contains YAML block,
  editing AI directive file that contains YAML block.

  These appear in the conditions of approximately 38 rules. Rather than
  rewriting all 38 rules' conditions, add definitions for these identifiers
  using keys that exactly match the current conditions usage. This resolves
  Problem A for these identifiers without changing any conditions arrays.

  The definition keys will use the token form as currently written in
  conditions (space-separated, matching the existing usage). This means
  the YAML definition keys require quoting. While this produces a mixed
  key style in the definitions section (some hyphenated, some quoted
  space-separated), this is valid YAML and AI agents can interpret it
  correctly. Per Design Priority 2, perfect stylistic consistency is not
  required if intent is unambiguously interpretable.

  Safety argument (from Copilot): since these identifiers are currently
  undefined, no compliant runner can rely on their current form. Adding
  definitions that match the existing form creates no regression.

Group 2 -- Scope identifiers (3 identifiers, 4 rules):

  Identifiers: scope high-stakes, scope multi-constraint,
  scope long-form reasoning.

  These appear in the conditions of exactly 4 rules (the tier-separation
  rules). Definitions already exist using hyphenated keys (scope-high-stakes,
  scope-multi-constraint, scope-long-form-reasoning). Rather than adding
  duplicate definitions with space-separated keys, normalize the conditions
  to match the existing definitions.

  This requires changing the scope identifier tokens in the conditions
  arrays of 4 rules. Each of these 4 rules has 6 compound conditions
  containing scope identifiers.

### 2.4 Required changes

#### Change P2-A: Add trigger identifier definitions (MUST)

Add 4 new entries to the definitions section for the trigger identifiers
listed in Group 1. Each entry MUST include at minimum a description field.
The definition key for each entry MUST exactly match the token as it
currently appears in conditions arrays.

Identifiers to define:
- creating AI directive file
- editing AI directive file
- creating AI directive file that contains YAML block
- editing AI directive file that contains YAML block

Affected section: definitions (4 new entries added).

#### Change P2-B: Normalize scope identifiers in conditions (MUST)

In the conditions arrays of the 4 tier-separation rules, replace the
space-separated scope identifiers with the hyphen-separated form that
matches the existing definitions keys.

Mapping:
- scope high-stakes -> scope-high-stakes
- scope multi-constraint -> scope-multi-constraint
- scope long-form reasoning -> scope-long-form-reasoning

When these appear as part of a compound condition (e.g.,
"creating AI directive file and scope high-stakes"), only the scope
identifier portion after the " and " separator is changed. The trigger
identifier portion remains unchanged (it matches the new definitions
from P2-A).

Affected rules (4 total):
- tier-separation-when-applicable
- tier-separation-define-scope-format-stopping
- tier-separation-bounded-iteration
- tier-separation-objective-vs-subjective

### 2.5 Change size evaluation

| Change | Target                         | Rules affected | Entries changed        |
|--------|--------------------------------|----------------|------------------------|
| P2-A   | definitions section            | 0              | +4 new definitions     |
| P2-B   | tier-separation rules          | 4              | 24 condition strings   |
| Total  |                                | 4 rules        | 4 defs + 24 strings    |

Comparison with full-normalization approach:

| Approach              | Rules affected | Definition entries | Condition rewrites |
|-----------------------|----------------|--------------------|--------------------|
| Full normalization    | ~44            | +4                 | ~88                |
| Minimum-change hybrid | 4              | +4                 | 24                 |

The minimum-change hybrid achieves the same outcome (all identifiers defined
and exactly matchable) while affecting approximately 9% of the rules that
the full approach would touch.

### 2.6 P2 verification (MUST)

The following verification MUST be performed after applying P2 changes:

1. Extract every identifier token from every conditions array in the file.
   For compound conditions of the form "A and B", split on " and " and
   extract both A and B.

2. For each extracted identifier token, confirm that an entry with an
   exactly matching key exists in definitions.

3. Confirm that no space-vs-hyphen mismatch remains between any conditions
   identifier and its corresponding definitions key.

4. Confirm that compound_conditions's MUST requirement ("such identifiers
   MUST be defined in this file or in definitions") is satisfied for every
   conditions entry in the file.

5. Confirm that no rule's applicability semantics have changed as a result
   of the identifier changes.

An AI agent can perform this verification by reading the complete file and
tracing each conditions entry against the definitions section.

---

## 3. Interaction with plan.final.ascii.md (from Claude)

The changes in plan.final.ascii.md (MUST NOT section remediation) target
the statement and verification fields of specific rules in prohibitions
and authoring_obligations. The P1 and P2 changes in this plan target
different fields and sections:

- P1 changes: interpretation.priority and conflict_policy.MUST_vs_MUST
  (neither is touched by plan.final.ascii.md).
- P2-A changes: definitions section (not touched by plan.final.ascii.md).
- P2-B changes: conditions arrays of 4 tier-separation rules (not touched
  by plan.final.ascii.md).

There is no structural conflict between this plan and plan.final.ascii.md.
The order of application does not matter for correctness, but applying P1
first is recommended because it is classified as Critical while P2 is High.

---

## 4. Execution plan

### Phase 0: Baseline inventory (from Codex)

Before making any changes, build a complete inventory of all condition
identifiers used across all rule records in the file.

Steps:
1. Extract all conditions values from all rule records.
2. For compound conditions, split on " and " to extract individual tokens.
3. For each token, check whether it exists as a key in definitions.
4. Classify each token as: exact match, token-form mismatch only, or
   missing entirely.

Exit condition: a complete mapping exists for all condition identifiers,
confirming the As-Is state described in the gap analysis report.

### Phase 1: Fix P1 -- Conflict Resolution Ambiguity (MUST)

Apply Changes P1-A and P1-B.

Steps:
1. Confirm the current text of interpretation.priority and
   conflict_policy.MUST_vs_MUST matches the As-Is state in the gap
   analysis report.
2. Rewrite conflict_policy.MUST_vs_MUST per Change P1-A.
3. Rewrite interpretation.priority per Change P1-B.
4. Run verification scenarios (Section 1.5).
5. Verify that the rule-conflict entry in failure_states_and_degradation
   remains consistent (Section 1.4).

Exit condition: all three verification scenarios in Section 1.5 produce
deterministic, non-contradictory outcomes.

### Phase 2: Fix P2 -- Condition Identifier Vocabulary (MUST)

Apply Changes P2-A and P2-B.

Steps:
1. Add the 4 trigger identifier definitions (Change P2-A).
2. Normalize the scope identifiers in the 4 tier-separation rules'
   conditions (Change P2-B).
3. Run verification (Section 2.6).

Exit condition: every condition identifier in the file has an exactly
matching key in definitions; the compound_conditions MUST requirement is
satisfied.

### Phase 3: Verification alignment (from Codex)

After Phases 1 and 2, confirm that the file's own verification methods
can detect regressions for P1 and P2.

Steps:
1. Review the verification section in SKILL.md.
2. Confirm that condition-identifier resolution (P2) can be checked by
   the methods described in the file, or note if a verification method
   update is needed.
3. Confirm that conflict-resolution consistency (P1) can be checked by
   the methods described in the file, or note if a verification method
   update is needed.

Exit condition: the file includes or references verification logic
sufficient to detect regressions for both P1 and P2. If updates to
verification methods are needed, they are documented as follow-up items.

---

## 5. Acceptance criteria

### Unanimous (MUST -- all 4 base plans agree)

- AC1: No contradiction remains between interpretation.priority and
  conflict_policy.MUST_vs_MUST for any combination of layer and priority.
- AC2: The conflict resolution cascade (layer -> priority -> conflict_policy)
  is deterministic for every possible two-rule conflict.
- AC3: Every condition identifier used in any conditions array has a
  matching key in definitions with exact string equality.
- AC4: The compound_conditions MUST requirement is satisfied (no
  self-violation).
- AC5: No rule's applicability semantics are altered by the changes.
- AC6: The YAML parses successfully with a standard-compliant YAML parser.

### Additional

- AC7: The rule-conflict entry in failure_states_and_degradation remains
  consistent with the updated conflict_policy (from Claude).
- AC8: Verification scenarios in Section 1.5 all produce the expected
  deterministic outcome (from GPT).

---

## 6. Risks

| Risk                                                | Mitigation                                   |
|-----------------------------------------------------|----------------------------------------------|
| P1 rewording introduces new ambiguity               | Verification scenarios (Section 1.5) trace   |
|                                                     | three representative cases; AC1 and AC2      |
|                                                     | require no contradiction.                    |
| P2-B scope identifier normalization introduces      | Only 4 rules affected; each has exactly 6    |
| typos in the 4 tier-separation rules                | compound conditions with a known pattern.    |
| Mixed key styles in definitions (some hyphenated,   | Design Priority 2: perfect stylistic         |
| some space-separated) may confuse future authors    | consistency is not required if AI agents can  |
|                                                     | interpret intent correctly. A future          |
|                                                     | normalization pass may unify key styles.      |
| Interaction with plan.final.ascii.md changes        | No structural conflict (Section 3). P1/P2    |
|                                                     | target different fields and sections.         |
| Future rule additions may reintroduce undefined     | Phase 3 verification alignment ensures the   |
| condition identifiers (from Codex)                  | file's verification methods can detect this.  |

---

## 7. Summary of all proposed changes

| Change | Target section(s)                    | Type        | Rules affected |
|--------|--------------------------------------|-------------|----------------|
| P1-A   | conflict_policy.MUST_vs_MUST         | Rewrite     | 0 (meta)       |
| P1-B   | interpretation.priority              | Rewrite     | 0 (meta)       |
| P2-A   | definitions                          | Add entries | 0              |
| P2-B   | tier-separation rules' conditions    | Normalize   | 4              |

Total changes: 2 string value rewrites + 4 new definition entries +
24 condition string normalizations across 4 rules.

Total rules with modified conditions arrays: 4 (out of approximately 44).
