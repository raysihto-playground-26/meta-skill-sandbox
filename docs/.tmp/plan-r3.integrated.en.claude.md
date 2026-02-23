# MUST NOT Consolidated Section Policy and Authoring Skill Remediation Plan (r3 Integrated Edition)

Created: 2026-02-23
Foundation documents: `must-not-section-policy-and-remediation-plan-r2.md`, `plan.codex.md`, `plan.composer.md`, `plan.gpt.md`, `plan.opus.md`
Target file (entity): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
Path note: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`,
`.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` are all symbolic links to `../.agents/skills`,
so the entity is a single file under `.agents/skills/`. Modifications need only be applied to this one file.
Status: Integrated plan (no concrete file changes)

---

## 0. Purpose and Premises of This Document

### 0.1 Purpose

This document is an integrated response to the following propositions:

1. In AI directive files, is placing MUST NOT rules in an independent dedicated section near the beginning of the file
   established as a research finding or a recognized norm/convention based on underlying mechanisms?
2. If it is established, to what degree of strength should it be applied for maximum effectiveness?
3. Given that the authoring skill currently does not satisfy meta-circularity, what policy should guide its remediation?

### 0.2 Method of Integration

The r2 base plan and four agent reviews (Codex / Composer / GPT / Opus) were
comprehensively examined, extracting points of agreement, resolving disagreements, and supplementing gaps.

The major contributions of each agent plan are summarized below:

| Agent    | Major Contributions                                                                                                                                                                                                                                                                                                                                 |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT      | Warning against the assertion strength of "established"; pointing out the need to make the Medium-strength "main predicate" determination machine-verifiable; proposing explicit documentation of the determination procedure (decision rules)                                                                                                      |
| Codex    | Policy of tempering evidence expressions to "strong practical best practice"; raising the synchronization issue between `.agents` and other paths; concept of introducing explicit fields such as `statement_modal`; proposing additional verification methods (`must-not-locality-validation`, `one-modal-per-rule-validation`)                    |
| Opus     | Integration of Semantic Gravity Wells (arXiv 2601.08070, 2026) as a counterargument; consistency analysis with prior implementation (previous branch commit); proposal to formulate the A-2 statement as a positive obligation: "MUST be classified as explanatory"                                                                                 |
| Composer | Pointing out rule A-1 schema deficiencies (`exceptions` / `verification` missing); explicit incorporation of Phase 2 (moving prohibitions to the beginning) into the implementation plan; presenting the future option of normative prohibition for `definitions.tier-separation`; confirming that `prohibitions.override` requires no verification |

### 0.3 Non-Goals

- Precise citation verification of individual papers on LLM attention characteristics is not an acceptance criterion for this plan.
- Rollout to all AI directive files is not mandatory in this plan (candidate for a separate task).
- Concrete file changes to AI directive files are outside the scope of this plan.

### 0.4 Terminology

Terms used in this document are defined as follows:

- **AI directive files**: Markdown files under `.agents/skills/` (composed of YAML frontmatter + a single fenced YAML block).
- **authoring skill**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`. The meta-skill that defines the format, structure, and rules of AI directive files.
- **rule record**: A structured record having `id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, and `verification`.
- **meta-circular**: The state in which the authoring skill itself complies with all rules that it defines.
- **deontic operator**: The primary obligation or prohibition RFC modal identified from the `statement` field by the determination procedure described below.

---

## 1. Effectiveness of a MUST NOT Consolidated Section: Research Evidence and Design-Theoretic Norms

### 1.1 LLM Context Processing and the "Lost-in-the-Middle" Phenomenon

Large language models (LLMs) do not process information uniformly within long contexts.
Prior research (Liu et al. 2023, among others) demonstrates the **"lost-in-the-middle"** phenomenon,
in which information at the beginning and end of a prompt is activated significantly more strongly
than information in the middle.

This nonlinear attention distribution has direct implications for the design of AI directive files:

- **Prohibitions (MUST NOT) carry high failure costs**: Once a prohibition violation occurs during generation, it is difficult to retract.
- **Prohibitions buried in the middle suffer lower compliance rates**: Prohibitions placed in the middle of long instructions are more likely to be forgotten or ignored compared to those at the beginning or end.

### 1.2 Empirical Findings from Instruction Hierarchy Research

OpenAI's "Instruction Hierarchy" research (Wallace et al. 2024) and
Anthropic's findings on Constitutional AI support the following:

- Constraints are most likely to be complied with when they are explicit, independent, and placed early.
- When constraints are embedded within other content, model attention diminishes and compliance rates tend to decline.
- A design that gathers prohibition categories in one place and presents them early
  **can be reasonably inferred** to have the effect of activating prohibitions before generation begins.

**Important limitations** (GPT, Opus consensus):

- Research at OpenReview 2025 found that even with system/user prompt separation,
  stable establishment of instruction hierarchy failed, and models showed a tendency to ignore priority designations for constraint types.
- "Retention in working-memory equivalent" is not a directly demonstrated conclusion but is positioned as a reasonable inference.
- Enforceability depends not on "research assertions" but on designs that can be mechanically verified by a runner/linter (GPT).

### 1.3 Semantic Gravity Wells: Reverse Activation Risk of Negative Constraints (Important Counterargument)

Semantic Gravity Wells (arXiv 2601.08070, 2026) is a study that identified the
mechanism by which negative constraints fail in LLMs, and it has direct implications for MUST NOT
consolidated section design (raised by Opus, integrated in r2):

- **Priming Failure (87.5% of violations)**: The very act of explicitly mentioning the prohibited target
  activates rather than suppresses it. By writing "must not do X,"
  the model strongly recalls X.
- **Override Failure (12.5% of violations)**: Later FFN layers generate positive contributions
  (+0.39) toward prohibition tokens, overriding the earlier suppression signal with approximately 4x strength.
- **Asymmetry of suppression**: Successful suppression yields a 22.8 percentage-point probability reduction,
  while failure yields only 5.2 percentage points (4.4x asymmetry).

**Implications for design (all agents consensus)**:

- Simply "lining up" MUST NOT items in a consolidated section risks
  repeatedly activating prohibited targets through the priming effect.
- **Placement strategy is an auxiliary means of improving compliance rates, not a guarantee;
  post-hoc verification through verification methods is the true means of ensuring compliance.**
- Strong/Strict strength levels (expanding the number of MUST NOT records) may increase priming risk.

### 1.4 Perspectives from Normative Theory and Specification Design Theory

In the design practices of legislation, technical specifications (RFCs, legal provisions, security policies, etc.),
prohibitions are also placed as independent clauses/sections at the front:

- RFC 2119 defines MUST NOT as a normative keyword on par with MUST, requiring structural clarity in specification documents.
- In security policies, placing prohibitions at the beginning is standard as a "deny-by-default" principle.

### 1.5 Conclusion: Assessment of Establishment

| Perspective                                                            | Degree of Establishment | Notes                                                                                                                           |
| ---------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Empirical evidence of LLM attention mechanisms (lost-in-the-middle)    | High                    | Reproduced across multiple independent studies                                                                                  |
| Early placement of prohibitions auxiliarily improves compliance rates  | Medium                  | Not directly demonstrated but a reasonable inference; Semantic Gravity Wells show counterevidence exists                        |
| Explicitation benefits of MUST NOT consolidated placement              | High                    | Established in specification design theory and legislative design theory; however, auxiliary rather than guaranteed             |
| Reverse activation risk from explicit mention of MUST NOT              | High                    | Semantic Gravity Wells (2026): priming failure 87.5%                                                                            |
| Combination of structuring (dedicated section) + post-hoc verification | High                    | Placement alone is insufficient; assurance through verification is essential                                                    |
| Optimal point for "how early to place"                                 | Medium                  | Near the beginning is preferable but quantitative optimum is undetermined; reverse activation possibility also to be considered |

**Overall assessment (integrated conclusion based on all-agent consensus)**:

The design of consolidating MUST NOT rules into an independent dedicated section near the beginning of the file
is **supported as a reasonable design practice** based on LLM processing characteristics, specification design theory, and empirical research.

However, the following qualifications are essential:

1. "Consolidating placement improves compliance rates" does not hold simply (counterargument from Semantic Gravity Wells).
2. It should be evaluated as **"reasonably established as a combined approach of a structured dedicated section + post-hoc verification"**. The effect of placement alone is not established.
3. It is appropriate to position this not as an "established theorem" or "conventional wisdom based on mechanisms,"
   but as **a high-confidence design practice grounded in LLM positional-dependency characteristics + specification design clarity + verification tractability** (GPT, Codex consensus).

---

## 2. Selection of Application Strength

### 2.1 Strength Levels

| Strength Level | Description                                                                                                                                                                                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Weak**       | SHOULD be in a dedicated section. Exceptions are broadly permitted.                                                                                                                                                                                                                      |
| **Medium**     | Normative MUST NOT (those whose "deontic operator" of the rule record's `statement` field is MUST NOT) are all placed in `prohibitions`. Explanatory MUST NOT (those in fields outside rule records, and those in `statement` where the deontic operator is not MUST NOT) are permitted. |
| **Strong**     | Any MUST NOT contained in the `statement` field of any rule record is moved to `prohibitions` regardless of section.                                                                                                                                                                     |
| **Strict**     | The text MUST NOT is prohibited from appearing outside the `prohibitions` section anywhere in the entire file.                                                                                                                                                                           |

### 2.2 Recommended Strength and Rationale (All-Agent Consensus)

**Recommended strength: Medium (applied as MUST)**

Rationale:

- As the rules `explanatory-must-not-permitted` / `explanatory-must-not-for-clarity` indicate,
  the occurrence of the phrase MUST NOT and the occurrence of a "normative prohibition" are distinct.
- MUST NOT appearing in fields such as interpretation, definitions, failure_states_and_degradation, etc.
  is explanatory, and elevating these to `prohibitions` would:
  - Necessitate applying the rule record schema to explanatory text, causing file structure bloat.
  - Blur the boundary of "what is normative," making compliance verification more difficult instead.
- From the findings of Semantic Gravity Wells, Strong/Strict may expand the number of MUST NOT records,
  increasing priming risk.
- The lost-in-the-middle mitigation effect is largely achieved at Medium, so the
  additional benefit of Strong/Strict is small.

### 2.3 Operational Definition of Medium Strength: Deontic Operator Determination Procedure

To resolve the "non-determinism of main-predicate determination" raised by GPT and Codex,
the syntactic determination procedure introduced in r2 is also adopted in this plan.

**Definition of deontic operator**:

Scan the `statement` field from left to right; the first RFC modal
(MUST NOT / MUST / SHOULD NOT / SHOULD / MAY) determined to "count" is the deontic operator.

**Conditions for "not counting (explanatory)"** (if any of the following are met):

1. Appears as a token enclosed in single or double quotes (e.g., `'MUST NOT'`).
2. An occurrence where it is explicitly indicated as a mention of the phrase, such as "the phrase MUST NOT" or "phrase MUST NOT."
3. An occurrence appearing as part of an enumeration of RFC keywords (e.g., `(MUST, MUST NOT, SHOULD, ...)`).
4. An occurrence appearing as an explanation within parentheses (e.g., `All normative prohibitions (MUST NOT) MUST ...`).
5. An occurrence appearing as part of an example following "e.g." or "for example."

**Conditions for "counting (normative)"**: Occurrences that do not fall under any of the above "not counting" conditions.

**Rule for Medium strength**:

> A rule record whose `statement` deontic operator is **MUST NOT**
> MUST be placed in `prohibitions.items`.
> Rule records whose deontic operator is other than MUST NOT, and MUST NOT appearing in
> fields outside rule records (description, behavior, degradation, verification, etc.),
> are treated as explanatory use and do not require movement to `prohibitions`.

### 2.4 Limitations and Future Outlook of the Determination Procedure

**Current limitations** (GPT, Codex noted):

- The above determination procedure is clear for humans, but complete machine verification may
  require natural language analysis beyond regular expressions in some cases.
- Full alignment with `verification-machine-checkable` as advocated by the authoring skill itself
  is currently deferred to "future linter implementation."

**Future improvement candidates** (Codex proposal):

- Introduce an explicit field such as `statement_modal` (`MUST`, `MUST_NOT`, `SHOULD`, etc.)
  into rule records, structurally avoiding ambiguous determination of `statement` text.
- Implement the determination procedure as a linter to improve the satisfaction of `verification-machine-checkable`.

---

## 3. Identification of Meta-Circular Non-Compliance in the Current Authoring Skill

### 3.1 Investigation Method

All rules containing MUST NOT in their `statement` field were enumerated across the entire SKILL.md,
and the deontic operator determination procedure (Section 2.3) was applied.

### 3.2 Confirmed Violations (All-Agent Consensus)

#### Violation 1: Placement of `explanatory-must-not-permitted`

| Item               | Value                                                                                                                                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Rule ID            | `explanatory-must-not-permitted`                                                                                                                                                                                                     |
| Containing section | `authoring_obligations`                                                                                                                                                                                                              |
| statement          | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."` |
| Deontic operator   | MUST NOT ("MUST NOT be treated" is the first "counting" modal upon scanning)                                                                                                                                                         |
| Violation detail   | Deontic operator is MUST NOT but the rule is not placed in the `prohibitions` section                                                                                                                                                |
| Reference rule     | `prohibitions-dedicated-section`                                                                                                                                                                                                     |

#### Secondary Issue: Compound Predicates of `explanatory-must-not-permitted`

| Item                                   | Value                                                                                                                                                                                                                                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rule ID                                | `explanatory-must-not-permitted`                                                                                                                                                                                                                                              |
| Issue detail                           | Two predicates coexist: "is allowed" (permission) and "MUST NOT be treated" (prohibition)                                                                                                                                                                                     |
| Reference rule                         | `one-obligation-per-rule`                                                                                                                                                                                                                                                     |
| Interpretation and integrated judgment | If "is allowed" is read as equivalent to MAY, it could formally be interpreted as only one MUST NOT predicate; however, the ambiguity of "is allowed" itself goes against the spirit of `no-ambiguous-modals`, so splitting is desirable (r2, GPT, Codex, Composer consensus) |

### 3.3 Confirmed Non-Violations (Cases Where `statement` Contains MUST NOT but It Is Not the Deontic Operator)

| Rule ID                            | Section                 | Form of MUST NOT occurrence                                                      | Deontic operator | Determination     |
| ---------------------------------- | ----------------------- | -------------------------------------------------------------------------------- | ---------------- | ----------------- |
| `explanatory-must-not-for-clarity` | `authoring_obligations` | Appears as an example with "e.g. listing RFC keywords." Main operator is SHOULD. | SHOULD           | **Non-violation** |
| `use-normative-keywords`           | `authoring_obligations` | Part of RFC keywords enumeration `(MUST, MUST NOT, ...)`. Main operator is MUST. | MUST             | **Non-violation** |
| `prohibitions-dedicated-section`   | `authoring_obligations` | Appears as parenthetical explanation `(MUST NOT)`. Main operator is MUST.        | MUST             | **Non-violation** |
| `define-conflict-policy`           | `authoring_obligations` | Appears within an example (`e.g. MUST vs MUST: halt`). Main operator is MUST.    | MUST             | **Non-violation** |

### 3.4 MUST NOT Outside Rule Records (Permitted as Explanatory Use)

The following are MUST NOT occurrences appearing outside the `statement` field of rule records,
falling within the permissible scope defined by `explanatory-must-not-permitted`:

| Location                                                    | Field type                  |
| ----------------------------------------------------------- | --------------------------- |
| `interpretation.unknown_keys`                               | interpretation prose        |
| `interpretation.unspecified_behavior`                       | interpretation prose        |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST`      | conflict policy prose       |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose              |
| `failure_states_and_degradation.degradation`                | degradation prose           |
| `definitions.tier-separation.description`                   | definition prose (see note) |
| `one-obligation-per-rule` verification                      | verification field          |

**Note: Regarding `definitions.tier-separation.description`** (raised by Composer)

The "MUST NOT interleave" in this description functions as a substantively normative prohibition
in the context where tier-separation applies. Whether the definitions field is included in the
permissible scope explicitly stated by `explanatory-must-not-permitted`
("interpretation, semantics, or verification") is not specified within SKILL.md.

**Policy of this plan**: Proceed by including the definitions field within the permissible scope (treating it as explanatory use) for now.
Resolve this ambiguity by explicitly adding "definitions" to the statements of A-1 and A-2 during modification.
Future reorganization into an independent rule `no-interleave-tiers` in prohibitions, referenced from definitions,
is retained as a candidate for a separate task.

---

## 4. Goal Setting

### 4.1 Target State

**Definition of full meta-circular compliance** (all-agent consensus):

> The state in which the authoring skill itself complies with all rules that it defines.
> Specifically: the state in which the conditions required by `prohibitions-dedicated-section`,
> `one-obligation-per-rule`, and `no-ambiguous-modals` are met by the authoring skill itself.

### 4.2 Compliance Verification Criteria

1. In all rule records outside `prohibitions.items`,
   the deontic operator of the `statement` is not MUST NOT.
2. The permissible scope of "explanatory MUST NOT" as defined by `explanatory-must-not-permitted`
   is consistently applied within the file.
3. The "one obligation per rule" required by `one-obligation-per-rule`
   is satisfied in all rule records.
4. YAML can be parsed successfully by a standard parser.
5. All rule records conform to the rule record schema
   (id, layer, priority, statement, conditions, exceptions, verification).

### 4.3 Secondary Goals (GPT, Codex Proposals)

- **Machine verifiability**: Aim for a state where "which is a prohibition" can be determined by syntactic rules.
- **Recurrence prevention**: Consider adding verification methods to prevent meta-circular violations from recurring when new rules are added.

---

## 5. Remediation Policy

### 5.1 Basic Policy

**Minimum change, maximum consistency** principle (all-agent consensus):
Restore meta-circular compliance by refactoring the description of `explanatory-must-not-permitted`
without changing the existing structure, rule count, or intent.

### 5.2 Specific Change Policy

#### Change A: Split `explanatory-must-not-permitted`

Split the current single rule (with 2 predicates) into the following 2 rules.

**Post-split rule A-1 (append to end of `prohibitions.items`)**

```yaml
- id: "no-treat-explanatory-must-not-as-prohibition"
  layer: L2
  priority: 92
  statement: "MUST NOT treat descriptive uses of the phrase 'MUST NOT' in interpretation,
    semantics, definitions, or verification fields as additional enforceable prohibitions."
  conditions: ["creating AI directive file", "editing AI directive file"]
  exceptions: ["none"]
  verification: "No interpretation, semantics, definitions, or verification field treats
    descriptive MUST NOT as an enforceable prohibition; human or pattern check."
```

Design rationale:

- Explicitly includes definitions in the `statement` (resolving the ambiguity raised by Composer).
- Completes `exceptions` and `verification` (resolving the schema deficiency raised by Composer).
- The deontic operator is MUST NOT, and placement in `prohibitions.items` conforms to Medium strength.

**Post-split rule A-2 (remains in `authoring_obligations`; statement rewritten)**

```yaml
- id: "explanatory-must-not-permitted"
  layer: L2
  priority: 92
  statement: "Descriptive use of the phrase MUST NOT in interpretation, semantics,
    definitions, or verification text (as opposed to primary normative statement fields)
    MUST be classified as explanatory; enforcement as a separate prohibition is governed
    by no-treat-explanatory-must-not-as-prohibition."
  conditions: ["creating AI directive file", "editing AI directive file"]
  exceptions: ["none"]
  verification: "Descriptive uses of MUST NOT in interpretation, semantics, definitions,
    or verification text are classified as explanatory and cross-reference
    no-treat-explanatory-must-not-as-prohibition for enforcement."
```

Design rationale:

- The deontic operator is MUST ("MUST be classified"), not MUST NOT.
  This makes placement outside the `prohibitions` section conform to Medium strength.
- The r1 proposal "does not constitute an enforceable prohibition" was rejected because
  it is a negative assertion that does not correspond to any of the RFC-style normative keywords
  required by `use-normative-keywords` (raised by Opus, corrected in r2).
- By using "MUST be classified as explanatory" + cross-reference to
  `no-treat-explanatory-must-not-as-prohibition`, the obligation is clarified as a positive one,
  ensuring consistency with `use-normative-keywords`.
- Explicitly includes definitions in the permissible scope.

#### Change B: Confirmation of `explanatory-must-not-for-clarity` (No Change)

The deontic operator of the `statement` is SHOULD, and MUST NOT appears as an example, so no change is needed.
After implementing Change A, confirm consistency between both rules.

#### Change C: Order Adjustment (Included in Change A)

Completed by appending A-1 to the end of `prohibitions.items`.

### 5.3 Scope of Application of `prohibitions.override` (Confirmed; No Change Needed)

`prohibitions.override` explicitly overrides format_obligations / content_obligations / authoring_obligations.
When `explanatory-must-not-permitted` remains in `authoring_obligations`, the new prohibition A-1
could override A-2 in authoring_obligations, but the two are complementary and do not conflict.
**This point requires no verification** (confirmed by Composer, removed from unresolved items in r2).

### 5.4 Assessment of Change Volume

| Change                     | Target                                                 | Scope of impact                                 |
| -------------------------- | ------------------------------------------------------ | ----------------------------------------------- |
| A-1: New rule addition     | End of `prohibitions.items`                            | Addition of 1 rule record                       |
| A-2: Existing rule rewrite | `authoring_obligations.explanatory-must-not-permitted` | Changes to statement + verification fields only |
| B: Confirmation only       | None                                                   | No change                                       |

---

## 6. Final Policy on Application Strength

**Medium strength is applied as MUST (mandatory).**

Specific application rules (refer to the deontic operator determination procedure in Section 2.3):

- Rule records whose `statement` deontic operator is **MUST NOT**:
  MUST be placed in `prohibitions.items`.
- Rule records whose `statement` deontic operator is other than MUST NOT:
  Do not require movement to `prohibitions` (permitted even if MUST NOT appears through other means).
- MUST NOT in fields outside rule records:
  Permitted (within the scope of applicability of `explanatory-must-not-permitted`).

**Reasons for not adopting Strict strength** (all-agent consensus):

- Moving all explanatory MUST NOT to `prohibitions` would require elevation to rule records, causing significant structural bloat.
- From the findings of Semantic Gravity Wells, expansion of MUST NOT records increases priming risk.
- Medium strength achieves most of the compliance benefit.

---

## 7. Implementation Plan

### 7.1 Phase 1: Restoring Meta-Circular Compliance (Core of This Task)

| Tier                                   | Content                                                                                                                                                                                                    |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0 (Structure confirmation)**    | Enumerate all rule records in SKILL.md and update the confirmed violation list from Sections 3.2–3.4 to the latest state.                                                                                  |
| **Tier 1 (Implement changes)**         | Implement Change A (add A-1 + rewrite A-2).                                                                                                                                                                |
| **Tier 2 (Objective verification)**    | Perform YAML parse verification, structure verification, `prohibitions-dedicated-section` compliance confirmation, `one-obligation-per-rule` compliance confirmation, and rule-record schema confirmation. |
| **Tier 3 (Subjective quality review)** | Confirm through human review that the post-change descriptions preserve the original intent.                                                                                                               |

### 7.2 Phase 2: Moving the `prohibitions` Section to the Beginning (Separate Task)

As an auxiliary strengthening of the lost-in-the-middle countermeasure, move the `prohibitions` section
within the YAML block to immediately after `interpretation` and `precedence_and_conflict`
(adopting Composer's proposal and making it explicit as a Phase).

- This is a major structural change and is treated as a separate task after Phase 1 completion.
- From the findings of Semantic Gravity Wells, the effect of the move is assessed as auxiliary.
  Combining it with strengthened post-hoc verification (verification methods) is important.

### 7.3 Phase 3: Strengthening Verification Methods (Separate Task; Recommended)

Based on Codex's proposal, consider adding the following verification methods:

| Candidate verification method   | Purpose                                                             |
| ------------------------------- | ------------------------------------------------------------------- |
| `must-not-locality-validation`  | Confirm that no prohibition exists outside `prohibitions.items`     |
| `one-modal-per-rule-validation` | Inspect for one modal per rule (prohibition of compound predicates) |

These are not acceptance criteria for Phase 1 but are effective for preventing recurrence of meta-circular violations.

### 7.4 Acceptance Criteria (Phase 1)

- In all rule records outside `prohibitions.items`, the deontic operator of the `statement` is not MUST NOT.
- YAML can be parsed successfully by a standard parser.
- The rule record schema (id, layer, priority, statement, conditions, exceptions, verification) is maintained for all rules.
- There is no semantic contradiction between `explanatory-must-not-permitted` and `no-treat-explanatory-must-not-as-prohibition`.

---

## 8. Major Changes from r2

| Change area                                      | r2 description                                                               | r3 (this document) revision                                                                                                                                                       | Basis                                     |
| ------------------------------------------------ | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Expression of establishment degree               | "Supported as a reasonable practice"                                         | Qualified to "positioned as a high-confidence design practice." Explicitly stated that it is not treated as an "established theorem" or "conventional wisdom based on mechanisms" | GPT, Codex                                |
| Machine verifiability of determination procedure | Defined the determination procedure but did not explicitly state limitations | Explicitly stated the limitation (complete machine verification may require natural language analysis in some cases) and added the future `statement_modal` field concept         | GPT, Codex                                |
| Permissible scope of definitions                 | Implicitly permitted                                                         | Explicitly included "definitions" in the statements of A-1 and A-2 to resolve ambiguity                                                                                           | Composer                                  |
| Verification method strengthening                | Not mentioned                                                                | Added `must-not-locality-validation` / `one-modal-per-rule-validation` as consideration items in Phase 3                                                                          | Codex                                     |
| Positioning of Phase 2                           | Included in implementation plan but treated as separate task                 | Similarly treated as separate task but explicitly numbered as a Phase to improve planning clarity                                                                                 | Composer                                  |
| Documentation of agent contributions             | Mentioned in tabular form as review evidence                                 | Detailed each agent's major contributions in Section 0.2 to improve integration transparency                                                                                      | Self-containment requirement of this plan |
| Terminology                                      | Used implicitly within the text                                              | Consolidated terminology definitions in Section 0.4                                                                                                                               | Self-containment requirement              |

---

## 9. Unresolved and Ongoing Consideration Items

1. **Normative prohibition of `definitions.tier-separation`**:
   Currently permitted as explanatory use; however, future reorganization into adding `no-interleave-tiers` to prohibitions
   and referencing it from definitions is retained as a candidate for a separate task.

2. **Rollout to other AI directive files**:
   In this repository, there is currently only one file under `.agents/skills/`.
   If files increase, a decision is needed on whether to apply the same Medium strength
   (including the deontic operator determination procedure) or to unify via reference (id/link) to the authoring skill.

3. **Concretization of Semantic Gravity Wells mitigation measures**:
   Adding specific guidelines to the writing style of AI directive files to reduce priming risk
   (e.g., "describe the desired state affirmatively instead of directly naming the prohibited target")
   is worth considering as a separate task.

4. **Linter implementation of deontic operator determination**:
   Implement the determination procedure from Section 2.3 as a machine-executable linter
   to improve the satisfaction of `verification-machine-checkable`.
   Consider also the `statement_modal` field introduction proposed by Codex.

5. **Guidelines for MUST NOT usage in explanatory text**:
   Regarding the "side effects of a policy that actively uses MUST NOT in explanatory text" raised by Codex,
   consider whether to lean toward "permitted only when necessary (SHOULD NOT as default)."
   Currently, `explanatory-must-not-for-clarity` recommends this at SHOULD level,
   so whether to lower the strength of this recommendation is the point of discussion.
