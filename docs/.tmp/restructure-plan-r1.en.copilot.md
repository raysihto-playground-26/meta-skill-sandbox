# Restructuring Plan R1: Making Formal-Consistency-Only Review Comments Structurally Unjust

## 0. Context and Motivation

### 0.1 The Triggering Review Comment

Review comment `discussion_r2841492177` on PR #10 argues that the SKILL.md is
internally self-violating because:

- `interpretation.condition_identifiers` requires every condition identifier used
  in `conditions` arrays to match a `definitions` key by exact string equality (MUST).
- The identifier `"always"` is used in the `conditions` of nine or more rules, but
  no `always` entry exists under `definitions`.
- Therefore, a runner or linter implementing `condition_identifiers` literally would
  reject critical L0 rules such as `no-prose`, `no-invent`, and `frontmatter-required`.

### 0.2 Why This Comment Can Currently Be Made

The comment is formally valid *given the current structure* of SKILL.md because:

1. The `condition_identifiers` rule contains no explicit carve-out for self-evident
   sentinel values such as `"always"`.
2. The `constraints` key does reference `"always"` as special
   (`"Rules with conditions other than 'always' apply only when those conditions
   match"`), but this carve-out is not surfaced inside `condition_identifiers` where
   the MUST requirement lives.
3. Most importantly, SKILL.md contains no explicit statement that inference efficiency
   is the PRIMARY design goal and that formal consistency is explicitly subordinate.
   Without such a declaration, a reviewer applying formal-consistency analysis has no
   structural basis to be told their critique is out-of-scope.

### 0.3 Why the Comment Should Be Structurally Unjust

The purpose of SKILL.md is to maximize the quality of AI agent instruction
interpretation.  Token efficiency and signal-to-noise ratio (S/N ratio) are the
primary evaluation axes (see report_pr10_formal-consistency-priority_structural-problem.md).

Requiring `"always"` to appear in `definitions` would:

- Add a token-consuming entry that carries zero disambiguation value (the word
  "always" is universally understood and requires no definition).
- Set a precedent that every self-evident English sentinel (`"never"`, `"always"`,
  etc.) must be defined, accelerating definitions bloat.
- Shift AI agent attention from rule content toward a definitional dictionary,
  degrading S/N ratio (see "Lost in the Middle", Liu et al. 2023).

A design that explicitly declares inference efficiency as the primary goal -- and
that explicitly documents `"always"` and similar sentinels as inference-reserved
identifiers exempt from the definitions requirement -- would make the comment
structurally unjust: the comment would be asking for formal completeness at the
direct cost of the file's stated primary design goal.

---

## 1. Problem Statement

| ID  | Problem                                                          | Impact                                                          |
| --- | ---------------------------------------------------------------- | --------------------------------------------------------------- |
| R1a | No explicit primary-goal declaration in SKILL.md                 | Formal-consistency critiques have no structural counter-basis   |
| R1b | `condition_identifiers` has no sentinel carve-out                | `"always"` is technically non-compliant with its own MUST rule  |
| R1c | Tradeoff between formal consistency and inference efficiency is  | Reviewers can apply formal-consistency analysis without limit   |
|     | implicit, not structurally documented                            |                                                                 |

---

## 2. Proposed Structural Changes to SKILL.md

This plan proposes the following changes to the YAML block of
`.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`.
The canonical file is under `.agents/skills/`; all other paths
(`.cursor/skills/`, `.github/skills/`, etc.) are symlinks pointing there.

All changes are to the YAML content only.  No changes to frontmatter structure,
fenced-block structure, or other files are required.

### Change A: Add an Explicit `design_goal` Section

**Location**: New top-level key in the YAML block, placed immediately after
`interpretation` (before `precedence_and_conflict`).

**Purpose**: Declare inference efficiency as the primary design goal and formal
consistency as explicitly secondary.  This provides a structural foundation for
rejecting critiques that optimize for formal consistency at the cost of
inference efficiency.

**Proposed content (illustrative)**:

```
design_goal:
  primary: "Maximize inference efficiency: minimize token count, maximize signal-to-noise
    ratio, and keep AI agent attention on rule content rather than meta-structure."
  secondary: "Maintain formal consistency only insofar as it does not degrade
    inference efficiency or introduce unnecessary token overhead."
  tradeoff_policy: "When formal consistency and inference efficiency conflict,
    inference efficiency takes precedence.  A review comment that demands formal
    completeness at the direct cost of token efficiency or S/N ratio is out-of-scope
    for evaluation of this file."
```

**Effect**: Gives any reader (human reviewer or AI runner) a declared top-level
design axiom.  A comment such as discussion_r2841492177 -- which demands that a
zero-disambiguation-value sentinel be added to `definitions` -- now runs directly
against the `tradeoff_policy` and can be rejected on structural grounds.

### Change B: Introduce `inference_reserved_sentinels` Under `interpretation`

**Location**: New key inside the existing `interpretation` block, adjacent to
`condition_identifiers` and `constraints`.

**Purpose**: Explicitly enumerate self-evident, universally-understood sentinel
identifiers that are exempt from the `definitions` exact-match requirement,
and document *why* they are exempt (inference efficiency).

**Proposed content (illustrative)**:

```
inference_reserved_sentinels:
  rationale: "The following identifiers carry universally understood semantics
    that require no definitional disambiguation.  Adding them to definitions
    would incur token overhead with zero S/N benefit, violating the primary
    design goal (see design_goal).  They are therefore exempt from the
    condition_identifiers exact-match requirement."
  identifiers: ["always", "never"]
  semantics:
    always: "The rule applies unconditionally, regardless of any other context."
    never: "The rule never applies; it is effectively disabled."
```

**Effect**: The `"always"` identifier is now explicitly documented as an
inference-reserved sentinel.  The `condition_identifiers` MUST requirement
applies to all other identifiers; `always` (and `never`) are explicitly
out-of-scope.  A linter or runner that flags `"always"` as a missing
`definitions` entry would be incorrectly ignoring `inference_reserved_sentinels`.

### Change C: Amend `condition_identifiers` to Reference the Sentinel Carve-Out

**Location**: `interpretation.condition_identifiers` (currently at approximately
line 24 of SKILL.md in PR #10).

**Current text (approximately)**:

```
condition_identifiers: "Condition identifiers in conditions arrays MUST use
  canonical kebab-case (hyphen-separated lowercase) and MUST match the
  corresponding definitions key by exact string equality.  No aliasing,
  synonym tables, normalization layers, or heuristic matching is permitted;
  resolution is exact-match only.  In compound conditions of the form
  'A and B', both A and B MUST be canonical kebab-case identifiers defined
  in definitions."
```

**Proposed amendment**: Add a closing sentence that explicitly points to the
sentinel carve-out:

```
  "Identifiers listed under inference_reserved_sentinels are exempt from
  this requirement; they are valid condition identifiers without a
  corresponding definitions entry."
```

**Effect**: The `condition_identifiers` rule is now internally consistent with
the use of `"always"`.  The self-violation identified by discussion_r2841492177
is structurally eliminated -- not by adding `"always"` to `definitions`
(which would hurt inference efficiency), but by making the exemption explicit
within the rule itself.

### Change D: (Optional) Add a `design_goal_conformance` Note to `prohibitions.override`

**Location**: `prohibitions.override` field.

**Purpose**: Reinforce that the `prohibitions` section is itself subject to the
`design_goal` hierarchy -- i.e., prohibition authoring must not sacrifice
inference efficiency for formal completeness.

**Effect**: Makes it explicit that even formal self-consistency requirements
(like the `condition_identifiers` MUST) are constrained by the `design_goal`,
providing a second structural anchor.

---

## 3. Why This Approach Is Superior to the Alternatives

### Alternative A: Add `always` to `definitions`

- Fixes the formal violation directly.
- BUT: Sets a precedent that every English sentinel needs a definition entry.
  Leads to definitions bloat, lower S/N ratio, and higher token cost.
- Does not address the root cause: the absence of an inference-efficiency-first
  design declaration means the same type of formal-consistency critique can
  be raised for any other self-evident term in the future.

### Alternative B: Relax `condition_identifiers` to Allow Free-Form Phrases

- Removes the MUST exact-match requirement entirely.
- BUT: Makes condition identifiers unverifiable by linters, reducing
  the machine-checkability of compliance (see `verification-machine-checkable`).

### This Plan (Changes A-C)

- Declares inference efficiency as the structural primary goal (Change A).
- Documents self-evident sentinels as explicitly exempt (Change B).
- Keeps the MUST exact-match for all non-sentinel identifiers (Change C).
- Eliminates the self-violation without token overhead.
- Makes the exemption machine-verifiable (check: is the identifier in
  `inference_reserved_sentinels.identifiers`?).
- Provides a durable structural foundation that makes future
  formal-consistency-only critiques structurally out-of-scope.

---

## 4. Verification that the Change Makes discussion_r2841492177 Unjust

After the changes in this plan are applied:

1. **R1a resolved**: `design_goal.tradeoff_policy` explicitly declares that
   formal-consistency demands that cost inference efficiency are out-of-scope.
   The comment can be rejected on this structural ground alone.

2. **R1b resolved**: `inference_reserved_sentinels` carves `"always"` out of
   the `condition_identifiers` MUST requirement.  A linter implementing
   `condition_identifiers` correctly would pass `"always"` as valid.
   The self-violation no longer exists.

3. **R1c resolved**: The tradeoff is now explicit and structural.  A reviewer
   raising the same class of critique -- "identifier X is used in conditions
   but not defined in definitions" -- must first demonstrate that X is not
   an inference-reserved sentinel AND that adding it to definitions would
   not harm inference efficiency.  The burden of proof shifts from the file
   maintainer to the formal-consistency critic.

---

## 5. Scope Constraints for This Plan

- **In scope**: Changes to the YAML block content within SKILL.md (new keys,
  amended values) as described in Section 2.
- **Out of scope**: Changes to frontmatter structure, changes to other AI
  directive files, runner/linter implementation, rollout to other skills.
- **Explicit constraint (from problem statement)**: During the plan-authoring
  scope, no changes are made to AI directive files.  Changes described in
  Section 2 are proposals only; implementation is a separate task.

---

## 6. Summary Checklist

- [ ] A.1: Add `design_goal` top-level key with `primary`, `secondary`,
       and `tradeoff_policy` fields.
- [ ] B.1: Add `interpretation.inference_reserved_sentinels` with `rationale`,
       `identifiers`, and `semantics` fields.
- [ ] C.1: Amend `interpretation.condition_identifiers` to add a trailing
       sentence referencing the sentinel exemption.
- [ ] D.1: (Optional) Amend `prohibitions.override` to note that prohibitions
       are also subject to the `design_goal` hierarchy.
- [ ] Verify: After changes, a linter that checks `condition_identifiers`
       must accept `"always"` as a valid condition identifier.
- [ ] Verify: After changes, a reviewer citing formal-consistency absence
       of `"always"` in `definitions` can be referred to
       `inference_reserved_sentinels` and `design_goal.tradeoff_policy`
       as the structural rebuttal.
