# Restructuring Plan R3: Policy-Grounded Remediation of `conditions: always` and Related Violations

## 0. Policy Authority Declaration

### 0.1 Governing Policy

This plan is grounded in `docs/ai-directive-files-policy.md`, the canonical (golden) policy for AI
directive files in this repository. Where R2 derived its proposals from an abstract "design axiom,"
this plan derives all proposals from explicit policy text. Policy wins over any prior plan.

Key policy statements governing this plan:

Conditions and exceptions (MUST):
"Anti-pattern to avoid: Do not use `conditions: always`."
"For unconditional rules, omit `conditions` entirely."
"Only add `conditions` when there is a real trigger that matters."
"This prevents 'definition bloat' where obvious terms must be defined just because
they appear as condition values."

Definitions policy (MUST):
"Define only non-obvious terms that materially change interpretation."
"Do not define words that are universally understood in this context (example: do not
define 'always', 'generally', 'usually' by default)."

Verification and testing (SHOULD):
"Do not rely on 'final comprehensive rule checking' inside the same LLM call as the
primary enforcement mechanism."
"Prefer: Externalize validation (programmatic checks, schema validation, or a separate
validation pass) when the constraint is important and cheaply checkable."

Essence (non-negotiable direction):
"Design toward a system where only the highest-impact instructions are transmitted
reliably, at minimal cost (minimal context)."
"Prefer constraint density over completeness."

### 0.2 Direction Change from R2

R2 proposed:
(a) Preserving `conditions: always` in SKILL.md (no removal).
(b) Adding an `inference_reserved_sentinels` mechanism to exempt "always" from the
`condition_identifiers` exact-match requirement.
(c) Adding a `design_axiom` top-level key to SKILL.md to declare non-determinism premise.
(d) Adding a `non_determinism_premise` key under `interpretation`.

All four are withdrawn in R3 for the following policy-grounded reasons:

(a) withdrawn: Preserving `conditions: always` is preserving a MUST violation.
Policy explicitly names it as an anti-pattern to avoid.
(b) withdrawn: A sentinel carve-out adds tokens and does not fix the root cause (P3-M2).
It is incompatible with the policy direction: "Prefer constraint density over completeness."
(c) withdrawn: The policy is already the canonical declaration of the design philosophy.
Re-declaring it inside SKILL.md is token overhead with zero disambiguation value.
"Lean and mean is the default: omit anything that is obvious or safely implicit."
(d) withdrawn: The non-determinism premise is already stated in SKILL.md's own
`failure_states_and_degradation.premise` ("Instruction adherence is probabilistic").
Duplication is a violation of DRY and adds context noise.

---

## 1. Problem Statement in Policy Vocabulary

| ID    | Category       | Problem                                                                  | Policy Basis                                             |
| ----- | -------------- | ------------------------------------------------------------------------ | -------------------------------------------------------- |
| P3-M2 | MUST violation | `rule-record-schema` mandates `conditions` as a required field, forcing  | "Conditions and exceptions (MUST)":                      |
|       |                | unconditional rules to use `conditions: always`                          | "For unconditional rules, omit `conditions` entirely"    |
| P3-M1 | MUST violation | `conditions: always` is used in many rules (no-prose, no-invent, etc.)   | "Anti-pattern to avoid: Do not use `conditions: always`" |
| P3-S1 | SHOULD gap     | Verification in some rules relies on same-generation self-check phrasing | "Do not rely on 'final comprehensive rule checking'      |
|       |                | without explicit externalization                                         | inside the same LLM call as the primary mechanism"       |

Note on P3-M1 and P3-M2 causality: P3-M2 causes P3-M1. The `rule-record-schema` mandates
`conditions` as a required field (P3-M2), which forces the anti-pattern `conditions: always`
(P3-M1). Fixing P3-M2 is therefore a prerequisite for fixing P3-M1.

Note on `discussion_r2841492177`: The review comment is a valid observation of the symptom
produced by P3-M1 + P3-M2. However, the commenter's proposed fix (add "always" to `definitions`)
would violate the Definitions policy ("Do not define words that are universally understood in this
context"). The correct fix is Solution Class A below.

---

## 2. Desired Solution Class (Defined Before Proposed Changes)

The solution class is defined here, before the specific changes, to make the design intent clear
and allow independent evaluation of the direction before committing to specific text.

### Solution Class A (highest priority, MUST fix)

Fix root cause first. Make `conditions` optional in `rule-record-schema`, then remove
`conditions: always` from all unconditional rules.

Properties:

- Eliminates both P3-M2 (root) and P3-M1 (symptom) in two ordered steps.
- Net token effect: reduction (removes `conditions: ["always"]` lines from N rules).
- After Class A, "always" no longer appears in any `conditions` array; the conflict
  between `condition_identifiers` and `definitions` ceases to exist.
- Machine-verifiable: grep for `conditions: always` should return zero results.

### Solution Class B (consequential, maintain consistency)

Update affected interpretation keys for internal consistency after Class A is applied.

Properties:

- B-1: Amend `condition_identifiers` to clarify it applies only when `conditions` is present.
  This is a clarification, not a new rule; no new tokens beyond the amendment text.
- B-2: Amend the `constraints` field value (which currently references 'always' as a special
  value) to reflect that unconditional rules omit `conditions` rather than using 'always'.
- Net token effect: neutral to small reduction (clarification text replaces longer old text).

### Solution Class C (optional, SHOULD gap)

Externalize the verification strategy where currently ambiguous.

Properties:

- C-1: Add an explicit statement in `failure_states_and_degradation` or a dedicated authoring
  obligation that verification MUST be externalizable (runner-side or linter-side),
  and MUST NOT depend on same-generation self-check as the primary mechanism.
- Apply only to MUST-level authoring obligations; do not expand for lower-priority rules
  (per policy: "Verification requirements SHOULD be applied selectively").
- This is optional: apply only if the cost (token addition) is justified by the compliance
  improvement for the rules it covers.

---

## 3. Proposed Changes (Minimum-First Ordering)

Changes are ordered from minimum-impact to maximum-impact, following the policy direction
"maximize adherence stability with minimal context." Each step is independently reviewable.

### Step 1 (fixes P3-M2 -- root cause)

Target: `authoring_obligations` > `rule-record-schema`

Current statement (abbreviated):
"Every normative rule MUST be represented as a structured record ... having exactly the
following fields: id, layer, priority, statement, conditions, exceptions, verification"

Proposed amendment:
Replace "having exactly the following fields: id, layer, priority, statement, conditions,
exceptions, verification" with "having the following fields: id, layer, priority, statement,
conditions (omit for unconditional rules), exceptions, verification".

Rationale: Policy says "For unconditional rules, omit `conditions` entirely." Making
`conditions` optional in the schema directly enables the removal of `conditions: always`.

Expected token delta: +1 sentence fragment (small overhead, high compliance value for a MUST rule).

Verification: `rule-record-schema` no longer mandates `conditions` as required for all rules.
Machine-check: schema validator accepts rule records that omit `conditions`.

### Step 2 (fixes P3-M1 -- anti-pattern removal)

Target: All unconditional rules across `prohibitions`, `format_obligations`, and
`content_obligations` that currently carry `conditions: ["always"]`.

Affected rules (non-exhaustive list from current SKILL.md):

- no-prose, no-invent (prohibitions)
- frontmatter-required, single-yaml-block, whitespace-only-separators (format_obligations)
- declarative-deterministic-definitional, structured-english, standard-parseable (content_obligations)

Proposed change: Delete the `conditions` field from each of these rules.

Rationale: After Step 1 makes `conditions` optional, these unconditional rules can omit
`conditions` entirely, following the policy anti-pattern guidance.

Expected token delta: negative (removes one `conditions` line per affected rule; approximately
8 rules x 1 line = ~8 lines of YAML removed).

Verification: No rule in the file has `conditions: ["always"]` or `conditions: always`.
Machine-check: grep for "conditions:.\*always" returns zero matches.

### Step 3 (fixes B-1 -- internal consistency)

Target: `interpretation.condition_identifiers`

Current text (abbreviated):
"Condition identifiers in conditions arrays MUST use canonical kebab-case ... and MUST match
the corresponding definitions key by exact string equality."

Proposed amendment: Prepend "When `conditions` is present, ..." or equivalently add a
preceding sentence: "This rule applies only to rules that include a `conditions` field."

Rationale: After Step 2, "always" no longer appears in any `conditions` array. This amendment
makes explicit that `condition_identifiers` is vacuously satisfied for rules that omit
`conditions`, removing any ambiguity for future readers or linters.

Expected token delta: +1 short sentence (small; justified by clarification value for a MUST rule).

Verification: A linter implementing `condition_identifiers` correctly handles rules without
a `conditions` field and does not flag them as violations.

### Step 4 (fixes B-2 -- internal consistency)

Target: `interpretation.constraints`

Current text:
"Rules with conditions other than 'always' apply only when those conditions match;
exceptions subtract from applicability."

Proposed replacement:
"Rules that include a `conditions` field apply only when those conditions match;
rules without a `conditions` field apply unconditionally. Exceptions subtract from
applicability."

Rationale: After Step 2, the reference to 'always' as a sentinel value is obsolete and
misleading. This replacement reflects the new structure where unconditional rules simply
omit `conditions`.

Expected token delta: neutral (same length approximately).

Verification: `constraints` field text does not reference 'always'; human or pattern check.

### Step 5 (optional, fixes C-1 -- SHOULD gap)

Target: `failure_states_and_degradation` or new authoring obligation.

Proposed addition: Add an explicit note or authoring obligation that verification
criteria in rule records are intended for post-hoc (runner-side or linter-side) validation,
not for same-generation self-check.

Apply only if cost (added tokens) is justified by the importance of the rules it covers.
Omit this step if the existing `no-rely-on-model-verify` prohibition in `prohibitions` is
judged sufficient to address the SHOULD gap.

Expected token delta: small positive (1-2 sentences or 1 new rule record).

Verification: Authoring obligations or failure_states_and_degradation explicitly references
external validation; does not instruct the model to perform a final comprehensive self-check.

---

## 4. Implementation Order and Priority

| Step | Target                     | Problem Fixed  | Priority   | Token Delta |
| ---- | -------------------------- | -------------- | ---------- | ----------- |
| 1    | rule-record-schema         | P3-M2 (root)   | Highest    | Small +     |
| 2    | Unconditional rule records | P3-M1          | High       | ~8 lines -  |
| 3    | condition_identifiers      | B-1            | Medium     | Small +     |
| 4    | constraints                | B-2            | Medium     | Neutral     |
| 5    | verification strategy      | P3-S1 (SHOULD) | Low (opt.) | Small +     |

Steps 1 and 2 are the minimum viable fix. Steps 3 and 4 maintain internal consistency.
Step 5 is optional.

Do not implement Step 2 before Step 1; doing so would leave rules without `conditions` in
violation of the current `rule-record-schema` MUST requirement.

---

## 5. Verification Strategy (Policy-Aligned)

Per policy: "Prefer: Externalize validation ... when the constraint is important and cheaply
checkable."

Per `llm-meta-control-instability.md` Section 4: "An LLM is a generator, not a governor."

Therefore, each step is verified by an external check, not by instructing the model to
self-verify after generation:

Step 1: Schema validator accepts rule records without `conditions` field.
Step 2: `grep -r "conditions:.*always"` returns zero matches in SKILL.md.
Step 3: Linter passes rule records without `conditions`; does not flag them.
Step 4: Pattern check confirms `constraints` field contains no reference to 'always'.
Step 5 (if applied): Pattern check or human review confirms no same-generation self-check
instruction in verification fields.

Do not use "verify all rules after completing the task" as the primary verification mechanism
for this plan (per `no-rely-on-model-verify` prohibition in SKILL.md and policy SHOULD guidance).

---

## 6. Scope and Constraints

- In scope: Changes to the YAML block content within SKILL.md (Steps 1-5 as described).
- Out of scope: Changes to frontmatter structure, changes to other AI directive files,
  rollout to other skills, runner/linter implementation.
- Explicit constraint: During the plan-authoring scope, no changes are made to AI directive
  files. Changes described in Section 3 are proposals only; implementation is a separate task.
- No new top-level keys (design_axiom, non_determinism_premise, inference_reserved_sentinels)
  are added. These are withdrawn per Section 0.2.

---

## 7. Summary Checklist

- [ ] Step 1: Amend `rule-record-schema` to make `conditions` optional for unconditional rules.
- [ ] Step 2: Remove `conditions: ["always"]` from all unconditional rules.
- [ ] Step 3: Prepend scope qualifier to `condition_identifiers` (applies only when `conditions`
      is present).
- [ ] Step 4: Rewrite `constraints` to remove the 'always' sentinel reference.
- [ ] Step 5 (optional): Add external-validation preference to `failure_states_and_degradation`
      or authoring obligations.
- [ ] Verify Step 2: `grep -r "conditions:.*always"` returns zero matches in SKILL.md.
- [ ] Verify Step 3: Linter accepts rule records without `conditions` field.
- [ ] Verify Step 4: `constraints` field contains no reference to 'always'.
- [ ] Confirm: No new top-level meta-keys added (design_axiom etc. are withdrawn).
- [ ] Confirm: Net token delta is non-positive (reductions from Step 2 outweigh additions
      from Steps 1, 3, 4).
