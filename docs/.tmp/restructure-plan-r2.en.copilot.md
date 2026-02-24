# Restructuring Plan R2: Making Formal-Consistency-Only Review Comments Structurally Unjust

## 0. Essential Prerequisite (Foundation of This Plan)

Before any structural analysis, the following design axiom must be stated explicitly.
This is the concept that was missing from R1 and that grounds all reasoning in this plan.

### 0.1 The Core Design Axiom

  "Converge the design toward delivering ONLY the most critical instructions to the AI
  reliably, at minimum cost (minimum context)."

The goal is NOT completeness (zero misreading, full coverage). The practical optimum,
assuming non-determinism as a premise, is:

  - Suppress context bloat so that important instructions are NOT crowded out ("skipped")
  - Never drop "the absolute must-haves"

This is "effectiveness optimization" -- optimizing for the probability that AI follows
the most important instructions, not for formal perfection.

### 0.2 Structured Design Philosophy

The following hierarchy governs evaluation of any change to SKILL.md:

  Layer 1 -- Top-level goal:
    Instructions reach the AI correctly (= as intended) and are executed.

  Layer 2 -- Foundational premise:
    LLMs are non-deterministic. Targeting completeness therefore has poor
    cost-effectiveness. "Zero misread in all cases" is not an achievable or useful goal.

  Layer 3 -- Practical goals:
    (a) Instruction density: hold high-importance instructions in the minimal set
        (increase instruction density).
    (b) S/N ratio: do not scatter attention resources with redundant explanations or
        self-evident supplements (raise S/N).

  Layer 4 -- Balance condition:
    - Too short: critical instructions are omitted  --> NG
    - Too bloated for formal consistency/completeness: attention is diverted --> NG
    The target is: "minimum enforcement" + "minimum volume" aimed at the zone where
    failure probability is lowest.

### 0.3 Implications of the Axiom

(a) Completeness is not the goal.
    Since LLMs are non-deterministic, expanding the directive to cover every edge case
    causes context bloat, which buries critical instructions and raises failure probability.

(b) Effectiveness is the sole evaluation axis.
    A proposed change is evaluated not by "does it improve formal completeness?" but by
    "does it raise the probability that the AI correctly executes critical instructions?"

(c) Instruction compression as Attention optimization.
    An AI agent's attention resources are finite. Spending them on self-evident definitions
    or formal meta-rules is equivalent to stealing Attention from critical instructions.

(d) Practical optimum under non-determinism.
    The correct question is not "how can we guarantee correct transmission?" but "how can
    we minimize the failure probability?" A design that chases formal guarantee inflates
    context and worsens the answer to the correct question.

### 0.4 One-Line Tags for This Design Philosophy

  - "Maximize the stable transmission of the most critical instructions with minimal context"
  - "Practical optimum of instruction design, assuming non-determinism"
  - "Instruction compression as Attention resource optimization"
  - "Effectiveness maximization, not completeness"

---

## 1. Context and Motivation

### 1.1 The Triggering Review Comment

Review comment `discussion_r2841492177` on PR #10 argues that SKILL.md is internally
self-violating because:

- `interpretation.condition_identifiers` requires every condition identifier used in
  `conditions` arrays to match a `definitions` key by exact string equality (MUST).
- The identifier "always" is used in the `conditions` of nine or more rules, but no
  `always` entry exists under `definitions`.
- Therefore, a runner or linter implementing `condition_identifiers` literally would
  reject critical L0 rules such as `no-prose`, `no-invent`, and `frontmatter-required`.

### 1.2 Why This Comment Can Currently Be Made

The comment is formally valid given the current structure of SKILL.md because:

1. The `condition_identifiers` rule contains no explicit carve-out for self-evident
   sentinel values such as "always".
2. The `constraints` key does reference "always" as special, but that carve-out is not
   surfaced inside `condition_identifiers` where the MUST requirement lives.
3. Most importantly, SKILL.md contains no explicit statement of the design axiom in
   Section 0. Without that axiom, a reviewer applying formal-consistency analysis has no
   structural basis to be told their critique is out-of-scope.

### 1.3 Why the Comment Should Be Structurally Unjust

Applying the design axiom from Section 0:

- Adding "always" to `definitions` would create a token-consuming entry with zero
  disambiguation value ("always" carries no ambiguity requiring a definition).
- This is a pure Attention tax: it takes resources away from critical instructions
  and directs them to a self-evident definition.
- It sets a precedent that every self-evident English universal must be defined,
  accelerating definitions bloat and worsening instruction density.
- Each such entry moves the design further from "minimum context" and further from
  "failure probability minimization" -- directly against the top-level goal.

A SKILL.md that explicitly declares the Section 0 design axiom gives any reader a
structural basis to reject the comment: it demands formal completeness at the direct
cost of the file's stated primary design objective.

---

## 2. Problem Statement

| ID  | Problem                                                           | Impact                                                         |
| --- | ----------------------------------------------------------------- | -------------------------------------------------------------- |
| R2a | No explicit design axiom in SKILL.md                             | Comments chasing formal completeness have no structural rebuttal|
| R2b | No acknowledgment that LLMs are non-deterministic in the design   | Completeness-chasing is not rejected at the design level       |
| R2c | `condition_identifiers` has no sentinel carve-out                 | "always" is technically non-compliant with its own MUST rule   |
| R2d | Tradeoff between formal consistency and effectiveness is implicit | Reviewers can apply formal-consistency analysis without limit  |

---

## 3. Proposed Structural Changes to SKILL.md

The canonical file is `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`.
All other paths (`.cursor/skills/`, `.github/skills/`, etc.) are symlinks pointing there.

All changes are to the YAML content only. No changes to frontmatter structure, fenced-block
structure, or other files are required or permitted in this scope.

### Change A: Add an Explicit `design_axiom` Section

Location: New top-level key in the YAML block, placed before `interpretation`.

Purpose: Declare the Section 0 design philosophy as a first-class, machine-readable
design axiom. Establish that:
  (1) the top-level goal is effective transmission of critical instructions to AI;
  (2) LLM non-determinism is a foundational premise, not an afterthought;
  (3) effectiveness (failure probability minimization) is the primary evaluation axis;
  (4) formal consistency is explicitly subordinate to effectiveness.

Proposed content (illustrative):

  design_axiom:
    top_level_goal: "Instructions reach the AI correctly and are executed as intended."
    foundational_premise: "LLMs are non-deterministic; targeting completeness has poor
      cost-effectiveness and is not a useful design goal."
    primary_axis: "Maximize the stable transmission of the most critical instructions
      at minimum context cost. Evaluate every change by whether it lowers the probability
      that critical instructions are missed or ignored -- not by whether it improves
      formal completeness."
    practical_goals:
      instruction_density: "Hold high-importance instructions in the minimal set;
        do not dilute them with self-evident supplements."
      sn_ratio: "Do not scatter AI attention resources with redundant or trivial content;
        raise signal-to-noise ratio."
    balance_condition: "Omitting critical instructions is NG. Bloating context for formal
      consistency or completeness is also NG. Target: minimum enforcement + minimum volume
      in the zone where failure probability is lowest."
    tradeoff_policy: "When formal consistency and effectiveness conflict, effectiveness
      takes precedence. A change that improves formal completeness at the direct cost of
      instruction density, context size, or S/N ratio is out-of-scope for this file."

Effect: Every reader (human reviewer or AI runner) now has a declared design axiom before
encountering any rules. A comment such as `discussion_r2841492177` -- which demands a
zero-value definition entry -- now runs directly against `tradeoff_policy` and can be
rejected on structural grounds without requiring case-by-case argumentation.

### Change B: Add a `non_determinism_premise` Key Under `interpretation`

Location: New key inside the existing `interpretation` block, near the top.

Purpose: Make the non-determinism premise machine-readable and explicit at the
interpretation layer, so that any rule or definition that chases completeness is
immediately counterable by referencing this premise.

Proposed content (illustrative):

  non_determinism_premise: "LLM instruction adherence is probabilistic, not guaranteed.
    This file is not designed to achieve completeness or zero-misread; it is designed to
    minimize the probability that critical instructions are missed. Rules and definitions
    are included only when their inclusion lowers that probability. Rules or definitions
    whose primary effect is to satisfy formal consistency without reducing failure
    probability are contrary to this file's design intent."

Effect: Any formal-consistency-only demand (e.g., "add always to definitions") can be
evaluated against this key: does adding it lower failure probability? If not, it is
contrary to design intent.

### Change C: Introduce `inference_reserved_sentinels` Under `interpretation`

Location: New key inside the existing `interpretation` block, adjacent to
`condition_identifiers` and `constraints`.

Purpose: Explicitly enumerate self-evident, universally-understood sentinel identifiers
that are exempt from the `definitions` exact-match requirement, and document why they
are exempt (Attention cost, zero disambiguation value, design_axiom).

Proposed content (illustrative):

  inference_reserved_sentinels:
    rationale: "The following identifiers carry universally understood semantics that
      require no definitional disambiguation. Adding them to definitions would incur
      Attention cost with zero S/N benefit, violating design_axiom.tradeoff_policy.
      They are exempt from the condition_identifiers exact-match requirement."
    identifiers: ["always", "never"]
    semantics:
      always: "The rule applies unconditionally, regardless of any other context."
      never: "The rule never applies; it is effectively disabled."

Effect: "always" is now explicitly documented as an inference-reserved sentinel.
A linter that flags "always" as a missing `definitions` entry is incorrectly ignoring
`inference_reserved_sentinels`. The self-violation in `condition_identifiers` is
structurally eliminated without any `definitions` bloat.

### Change D: Amend `condition_identifiers` to Reference the Sentinel Carve-Out

Location: `interpretation.condition_identifiers`.

Purpose: Add a trailing sentence so the MUST requirement explicitly excludes
inference-reserved sentinels. Eliminates the formal self-violation.

Proposed amendment: Append to the current text:

  "Identifiers listed under inference_reserved_sentinels are exempt from this requirement
  and are valid condition identifiers without a corresponding definitions entry."

Effect: `condition_identifiers` is now internally consistent with the use of "always".
The self-violation identified by `discussion_r2841492177` is structurally eliminated.

### Change E: (Optional) Amend `prohibitions.override` to Reference `design_axiom`

Location: `prohibitions.override` field.

Purpose: Reinforce that even the prohibitions section is subject to `design_axiom` -- i.e.,
prohibition authoring must not sacrifice instruction density for formal completeness.

---

## 4. Why This Approach Is Superior to the Alternatives

### Alternative A: Add `always` to `definitions`

- Fixes the formal violation directly.
- BUT: Zero disambiguation value; pure Attention tax.
- Sets a precedent for every self-evident English universal to need a definition.
- Does not address R2a or R2b; the same class of critique can be raised for any
  future self-evident term.

### Alternative B: Relax `condition_identifiers` to Allow Free-Form Phrases

- Removes the MUST exact-match requirement entirely.
- BUT: Makes condition identifiers unverifiable by linters; reduces machine-checkability.

### This Plan (Changes A-D)

- Declares the non-determinism premise and effectiveness-first axiom as machine-readable
  top-level keys (Changes A, B): addresses R2a and R2b.
- Documents self-evident sentinels as explicitly exempt with justification (Change C):
  addresses R2c without token overhead.
- Keeps the MUST exact-match for all non-sentinel identifiers (Change D).
- Eliminates the self-violation without any `definitions` bloat.
- Makes the exemption machine-verifiable.
- Provides a durable structural foundation that makes future formal-consistency-only
  critiques structurally out-of-scope.

---

## 5. Verification that the Changes Make `discussion_r2841492177` Unjust

After the changes in this plan are applied:

1. R2a resolved: `design_axiom.tradeoff_policy` explicitly declares that formal-
   consistency demands that cost effectiveness are out-of-scope. The comment can be
   rejected on this structural ground alone, without case-by-case argument.

2. R2b resolved: `interpretation.non_determinism_premise` explicitly states that rules
   and definitions are included only when their inclusion lowers failure probability.
   Adding "always" to `definitions` does not lower failure probability; it is therefore
   contrary to design intent by definition.

3. R2c resolved: `inference_reserved_sentinels` carves "always" out of the
   `condition_identifiers` MUST requirement. A linter implementing `condition_identifiers`
   correctly would pass "always" as valid. The self-violation no longer exists.

4. R2d resolved: The tradeoff is now explicit at multiple structural levels (design_axiom,
   non_determinism_premise, inference_reserved_sentinels). A reviewer raising the same
   class of critique must first demonstrate that the requested addition lowers failure
   probability and does not increase context cost. The burden of proof shifts structurally
   from the file maintainer to the formal-consistency critic.

---

## 6. Scope Constraints for This Plan

- In scope: Changes to the YAML block content within SKILL.md (new keys, amended values)
  as described in Section 3.
- Out of scope: Changes to frontmatter structure, changes to other AI directive files,
  runner/linter implementation, rollout to other skills.
- Explicit constraint: During the plan-authoring scope, no changes are made to AI
  directive files. Changes described in Section 3 are proposals only; implementation
  is a separate task.

---

## 7. Summary Checklist

- [ ] A.1: Add `design_axiom` top-level key with `top_level_goal`, `foundational_premise`,
       `primary_axis`, `practical_goals`, `balance_condition`, and `tradeoff_policy` fields.
- [ ] B.1: Add `interpretation.non_determinism_premise` making the LLM non-determinism
       assumption machine-readable.
- [ ] C.1: Add `interpretation.inference_reserved_sentinels` with `rationale`,
       `identifiers`, and `semantics` fields.
- [ ] D.1: Amend `interpretation.condition_identifiers` to add a trailing sentence
       referencing the sentinel exemption.
- [ ] E.1: (Optional) Amend `prohibitions.override` to note that prohibitions are also
       subject to `design_axiom`.
- [ ] Verify: A linter checking `condition_identifiers` must accept "always" as valid.
- [ ] Verify: A reviewer citing the absence of "always" in `definitions` can be referred
       to `inference_reserved_sentinels` (formal rebuttal) and `design_axiom.tradeoff_policy`
       plus `non_determinism_premise` (design-philosophy rebuttal).
- [ ] Verify: The new keys do not add token overhead that exceeds the S/N benefit they
       provide (they must themselves satisfy the design_axiom they declare).
