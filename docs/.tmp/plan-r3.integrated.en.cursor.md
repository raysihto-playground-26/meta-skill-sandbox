# MUST NOT Dedicated Section Policy and Authoring Skill Remediation Plan (r3 Integrated Edition)

Created: 2026-02-23
Target file (canonical): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
Path note: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`, `.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` are all symbolic links to `../.agents/skills`; the canonical instance is the single file under `.agents/skills/`. Any modification applies to this one file.
Status: Integrated plan (no concrete file changes)

---

## 0. Purpose and Premises of This Document

### 0.1 Purpose

This document provides an integrated response to the following propositions:

1. In AI directive files, is placing a dedicated section that collects only MUST NOT items near the beginning of the file established as a research finding or as a mechanistic convention/norm?
2. If so, at what strength of application does it yield the greatest effect?
3. Given that the authoring skill currently does not satisfy meta-circularity, what policy should guide remediation?

### 0.2 Integration Method

The r2 core plan and four agent reviews (Codex / Composer / GPT / Opus) were comprehensively verified; points of agreement were extracted, conflicts resolved, and gaps filled.

Major contributions from each agent plan are summarized below:

| Agent   | Major Contributions                                                                                                                                                                                                                          |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT     | Caution on the strength of asserting "established"; need for Medium-strength "primary predicate" determination to be machine-verifiable; proposal to formalize the determination procedure (decision rules).                                   |
| Codex   | Policy to keep justification wording as "strong practical best practice"; raising the `.agents` vs. other-path synchronization issue; proposal for explicit fields such as `statement_modal`; proposals for additional verification methods (`must-not-locality-validation`, `one-modal-per-rule-validation`). |
| Opus    | Integration of Semantic Gravity Wells (arXiv 2601.08070, 2026) as a counterargument; consistency analysis with prior implementation (previous branch commit); proposal for A-2 statement as affirmative obligation "MUST be classified as explanatory".                                                     |
| Composer| Identification of A-1 rule schema gaps (missing `exceptions` / `verification`); explicit inclusion of Phase 2 (moving prohibitions earlier) in the implementation plan; future option for normative prohibition of `definitions.tier-separation`; determination that `prohibitions.override` requires no further confirmation. |

### 0.3 Non-Purposes

- Accurate citation verification of individual papers on LLM attention properties is not a prerequisite for accepting this plan.
- Horizontal application to all AI directive files is not required by this plan (candidate for a separate task).
- Concrete changes to AI directive files are out of scope for this plan.

### 0.4 Term Definitions

Terms used in this document are defined as follows:

- **AI directive files**: Markdown files under `.agents/skills/` (YAML frontmatter + single fenced YAML block structure).
- **authoring skill**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`. The meta-skill that defines the format, structure, and rules for AI directive files.
- **rule record**: A structured record with `id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`.
- **meta-circular**: The state in which the authoring skill itself complies with all rules it defines.
- **deontic operator**: The RFC modal that is identified from the `statement` field by the determination procedure below and represents the rule's primary obligation or prohibition.

---

## 1. Validity of the MUST NOT Dedicated Section: Research Evidence and Design Norms

### 1.1 LLM Context Processing and the "Lost-in-the-Middle" Phenomenon

Large language models (LLMs) do not process information in long contexts uniformly. Prior work (e.g., Liu et al. 2023) demonstrates the **"lost-in-the-middle"** phenomenon: information at the beginning and end of a prompt is activated significantly more strongly than information in the middle.

This nonlinear attention distribution has direct implications for design of AI directive files:

- **Prohibitions (MUST NOT) have high failure cost**: If a prohibition is violated during generation, correction is difficult.
- **Prohibitions buried in the middle lose compliance**: Prohibitions placed in the middle of a long context are more likely to be forgotten or ignored than those at the beginning or end.

### 1.2 Empirical Findings on Instruction Hierarchy

OpenAI's "Instruction Hierarchy" work (Wallace et al. 2024) and Anthropic's Constitutional AI findings support:

- Constraints are most likely to be followed when they are explicit, independent, and placed early.
- When constraints are embedded in other content, model attention is diluted and compliance tends to drop.
- Collecting prohibition categories in one place and presenting them early is **reasonably inferred** to help activate prohibitions before generation begins.

**Important limitations** (GPT, Opus agreement):

- A 2025 OpenReview study shows that even with system/user prompt separation, instruction hierarchy can fail to stabilize reliably, and models tend to ignore priority specifications for constraint types.
- "Retention in working-memory equivalent" is not a directly empirically demonstrated conclusion; it should be positioned as a reasonable inference.
- Enforcement strength relies on design that is machine-verifiable by runner/linter, not on "research assertion" (GPT).

### 1.3 Semantic Gravity Wells: Inverse Activation Risk for Negation Constraints (Important Counterargument)

Semantic Gravity Wells (arXiv 2601.08070, 2026) identifies mechanisms by which negation constraints fail in LLMs and has direct implications for MUST NOT dedicated section design (Opus; integrated in r2):

- **Priming Failure (87.5% of violations)**: Explicitly mentioning the prohibited target itself activates it rather than suppressing it. Stating "MUST NOT do X" causes the model to strongly recall X.
- **Override Failure (12.5% of violations)**: Later FFN layers produce positive contribution (+0.39) to prohibited tokens, overwriting earlier suppression signals by roughly four times.
- **Asymmetry of suppression**: On success, probability decreases by 22.8 points; on failure, by only 5.2 points (4.4× asymmetry).

**Design implications (all agent agreement)**:

- Merely listing MUST NOT items in a dedicated section risks repeatedly activating prohibited targets via priming.
- **Placement strategy is a supplementary means to improve compliance, not a guarantee; post-hoc verification via verification methods is the true compliance guarantee.**
- Strong/Strict strength (expansion of MUST NOT records) may increase priming risk.

### 1.4 Normative and Specification Design Perspectives

In legal and technical specification design (RFCs, legal provisions, security policies, etc.), prohibitions are also placed as independent articles or sections in advance:

- RFC 2119 defines MUST NOT as a normative keyword on par with MUST and requires structural clarity in specification documents.
- In security policy, placing prohibitions first is standard as the "deny-by-default" principle.

### 1.5 Conclusion: Assessment of Establishment

| Perspective                                 | Establishment | Notes                                                                 |
| ------------------------------------------- | ------------- | --------------------------------------------------------------------- |
| LLM attention mechanism (lost-in-middle)    | High          | Reproduced in multiple independent studies                            |
| Early placement of prohibitions aids compliance | Medium     | Reasonable inference, not direct evidence; Semantic Gravity Wells shows counter evidence |
| Benefit of explicit MUST NOT dedicated placement | High      | Established in specification/legal design; supplementary, not guarantor |
| Inverse activation risk from explicit MUST NOT mention | High | Semantic Gravity Wells (2026): priming failure 87.5%                  |
| Combination of structure (dedicated section) + post-hoc verification | High | Verification must complement placement, not placement alone            |
| Optimal placement for "how early"            | Medium        | Near the beginning is preferred; quantitative optimum is not fixed; inverse activation also considered |

**Overall assessment (integrated conclusion from all agent agreement)**:

Designing a dedicated section that collects MUST NOT items near the beginning of the file is **supported as a reasonable design practice** from LLM processing characteristics, specification design theory, and empirical research.

The following limitations are essential:

1. "Concentrated placement alone improves compliance" does not hold in simple form (Semantic Gravity Wells counterargument).
2. It should be evaluated as **reasonably established as a combined approach of "structured dedicated section + post-hoc verification."** Placement-only effect is not established.
3. It should be positioned as a **high-confidence design practice based on LLM position-dependent effects + specification clarity + verifiability**, not as an "established theorem" or "mechanistic convention" (GPT, Codex agreement).

---

## 2. Choice of Application Strength

### 2.1 Strength Levels

| Strength Level | Content                                                                                                                                                                                                                                      |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Weak**       | SHOULD be in a dedicated section. Exceptions are broadly permitted.                                                                                                                                                                           |
| **Medium**     | All normative MUST NOT (rule records whose `statement` field deontic operator is MUST NOT) MUST be in `prohibitions`. Explanatory MUST NOT (outside rule record fields, and MUST NOT in `statement` where the deontic operator is not MUST NOT) is permitted. |
| **Strong**     | Must NOT in the `statement` field of any rule record MUST be moved to `prohibitions` regardless of section.                                                                                                                                  |
| **Strict**     | Prohibits any occurrence of MUST NOT text outside the `prohibitions` section anywhere in the file.                                                                                                                                             |

### 2.2 Recommended Strength and Rationale (All Agent Agreement)

**Recommended strength: Medium (applied as MUST)**

Reasons:

- As indicated by `explanatory-must-not-permitted` and `explanatory-must-not-for-clarity`, the occurrence of the phrase MUST NOT and the occurrence of "normative prohibition" are distinguished.
- MUST NOT in fields such as interpretation, definitions, failure_states_and_degradation is explanatory; moving these to `prohibitions` would:
  - Require applying the rule-record schema to explanatory text, inflating file structure.
  - Blur the boundary of "what is normative," making compliance harder to verify.
- From Semantic Gravity Wells, Strong/Strict may expand MUST NOT records and increase priming risk.
- Lost-in-the-middle mitigation is largely achieved at Medium; additional benefit from Strong/Strict is small.

### 2.3 Operational Definition of Medium Strength: Deontic Operator Determination Procedure

To resolve the "primary predicate indeterminacy" noted by GPT and Codex, the syntactic determination procedure introduced in r2 is adopted in this plan.

**Definition of deontic operator**:

Scan the `statement` field left to right; the first RFC modal (MUST NOT / MUST / SHOULD NOT / SHOULD / MAY) that is "counted" is the deontic operator.

**"Not counted" (explanatory) conditions** (any of the following):

1. It appears as a token enclosed in single or double quotes (e.g., `'MUST NOT'`).
2. It appears as an explicit mention of the phrase itself (e.g., "the phrase MUST NOT", "phrase MUST NOT").
3. It appears as an enumeration of RFC keywords (e.g., `(MUST, MUST NOT, SHOULD, ...)`).
4. It appears in parenthetical explanation (e.g., `All normative prohibitions (MUST NOT) MUST ...`).
5. It appears as part of an example following "e.g." or "for example".

**"Counted" (normative) condition**: Occurrences that do not fall under "not counted" above.

**Medium-strength rule**:

> A rule record whose deontic operator in `statement` is **MUST NOT** MUST be placed in `prohibitions.items`.
> Rule records whose deontic operator is not MUST NOT, and MUST NOT appearing in fields outside rule records (description, behavior, degradation, verification, etc.), are treated as explanatory and do not require placement in `prohibitions`.

### 2.4 Limitations of the Determination Procedure and Future Outlook

**Current limitations** (GPT, Codex):

- The determination procedure above is clear for humans but may require natural-language parsing beyond regex for full machine verification.
- Full alignment with the authoring skill's own `verification-machine-checkable` is left to "future lint implementation" for now.

**Future improvement candidates** (Codex proposal):

- Introduce an explicit field such as `statement_modal` (e.g., `MUST`, `MUST_NOT`, `SHOULD`) on rule records to avoid ambiguous determination from `statement` text.
- Implement the determination procedure as a linter to improve compliance with `verification-machine-checkable`.

---

## 3. Identification of Meta-Circular Non-Compliance in the Current Authoring Skill

### 3.1 Survey Method

All rules in SKILL.md whose `statement` field contains MUST NOT were enumerated, and the deontic operator determination procedure (Section 2.3) was applied.

### 3.2 Confirmed Violations (All Agent Agreement)

#### Violation 1: Placement of `explanatory-must-not-permitted`

| Item           | Value                                                                                                                                                                                                                                        |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rule ID        | `explanatory-must-not-permitted`                                                                                                                                                                                                              |
| Section        | `authoring_obligations`                                                                                                                                                                                                                       |
| statement      | "When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."               |
| Deontic operator | MUST NOT ("MUST NOT be treated" is the first "counted" modal in the scan)                                                                                                                                                                   |
| Violation      | Deontic operator is MUST NOT but the rule is not placed in the `prohibitions` section                                                                                                                                                         |
| Reference rule | `prohibitions-dedicated-section`                                                                                                                                                                                                               |

#### Secondary issue: Compound predicate of `explanatory-must-not-permitted`

| Item           | Value                                                                                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Rule ID        | `explanatory-must-not-permitted`                                                                                                                                                                       |
| Issue          | Two predicates coexist: "is allowed" (permission) and "MUST NOT be treated" (prohibition)                                                                                                              |
| Reference rule | `one-obligation-per-rule`                                                                                                                                                                              |
| Interpretation and integrated judgment | Reading "is allowed" as MAY-equivalent could formally allow a single MUST NOT predicate; however, the ambiguity of "is allowed" itself conflicts with the spirit of `no-ambiguous-modals`, so splitting is desirable (r2, GPT, Codex, Composer agreement) |

### 3.3 Confirmed Non-Violations (Cases where `statement` contains MUST NOT but deontic operator is not MUST NOT)

| Rule ID                          | Section               | Form of MUST NOT occurrence                                                      | Deontic operator | Judgment       |
| -------------------------------- | --------------------- | -------------------------------------------------------------------------------- | ---------------- | -------------- |
| `explanatory-must-not-for-clarity` | `authoring_obligations` | As example "e.g. listing RFC keywords". Primary operator is SHOULD.               | SHOULD           | **Non-violation** |
| `use-normative-keywords`         | `authoring_obligations` | Part of RFC keywords enumeration `(MUST, MUST NOT, ...)`. Primary operator is MUST. | MUST             | **Non-violation** |
| `prohibitions-dedicated-section` | `authoring_obligations` | Appears in parenthetical explanation `(MUST NOT)`. Primary operator is MUST.     | MUST             | **Non-violation** |
| `define-conflict-policy`        | `authoring_obligations` | Appears in example (`e.g. MUST vs MUST: halt`). Primary operator is MUST.        | MUST             | **Non-violation** |

### 3.4 MUST NOT Outside Rule Records (Permitted as Explanatory Use)

The following MUST NOT occurrences are outside the `statement` field of rule records and fall within the permitted scope defined by `explanatory-must-not-permitted`:

| Location                                                        | Field type                 |
| --------------------------------------------------------------- | -------------------------- |
| `interpretation.unknown_keys`                                   | interpretation prose       |
| `interpretation.unspecified_behavior`                            | interpretation prose       |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST`          | conflict policy prose      |
| `failure_states_and_degradation.failure_states[0].behavior`      | behavior prose             |
| `failure_states_and_degradation.degradation`                     | degradation prose          |
| `definitions.tier-separation.description`                       | definition prose (see note) |
| `one-obligation-per-rule` verification                          | verification field         |

**Note on `definitions.tier-separation.description`** (Composer):

The "MUST NOT interleave" in this description functions as a de facto normative prohibition in contexts where tier-separation applies. Whether the definitions field is included in the permitted scope that `explanatory-must-not-permitted` explicitly defines as "interpretation, semantics, or verification" is not stated in SKILL.md.

**Plan policy**: For now, treat the definitions field as permitted (explanatory use). When modifying, add "definitions" explicitly to A-1 and A-2 statements to resolve this ambiguity. Future organization as an independent rule `no-interleave-tiers` in prohibitions with a reference from definitions is left as a candidate for a separate task.

---

## 4. Goal Setting

### 4.1 Target State

**Definition of full meta-circular compliance** (all agent agreement):

> The state in which the authoring skill itself complies with all rules it defines.
> Concretely: the authoring skill satisfies the conditions required by `prohibitions-dedicated-section`, `one-obligation-per-rule`, and `no-ambiguous-modals`.

### 4.2 Compliance Verification Criteria

1. Every rule record outside `prohibitions.items` has a deontic operator in `statement` that is not MUST NOT.
2. The permitted scope of "explanatory MUST NOT" defined by `explanatory-must-not-permitted` is applied consistently within the file.
3. The "one obligation per rule" required by `one-obligation-per-rule` is satisfied for all rule records.
4. YAML parses successfully with a standard parser.
5. All rule records conform to the rule-record schema (id, layer, priority, statement, conditions, exceptions, verification).

### 4.3 Secondary Goals (GPT, Codex proposal)

- **Machine verifiability**: Aim for a state where "which are prohibitions" can be determined by syntactic rules.
- **Recurrence prevention**: Consider adding verification methods so that meta-circular violations do not recur when new rules are added.

---

## 5. Remediation Policy

### 5.1 Basic Policy

**Minimum change, maximum consistency** principle (all agent agreement):

Restore meta-circular compliance by refactoring the wording of `explanatory-must-not-permitted` without changing existing structure, rules, or intent.

### 5.2 Concrete Change Policy

#### Change A: Split `explanatory-must-not-permitted`

Split the current single rule (two predicates) into the following two rules.

**Split rule A-1 (add to end of `prohibitions.items`)**

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

Design points:

- Include `definitions` explicitly in `statement` (resolve Composer ambiguity).
- Complete `exceptions` and `verification` (address Composer schema gaps).
- Deontic operator is MUST NOT; placement in `prohibitions.items` conforms to Medium strength.

**Split rule A-2 (retain in `authoring_obligations`, rewrite statement)**

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

Design points:

- Deontic operator is MUST ("MUST be classified"), not MUST NOT; placement outside `prohibitions` conforms to Medium strength.
- The r1 proposal "does not constitute an enforceable prohibition" is a negative assertion that does not match any RFC-style normative keyword required by `use-normative-keywords`; rejected (Opus; corrected in r2).
- "MUST be classified as explanatory" plus cross-reference to `no-treat-explanatory-must-not-as-prohibition` clarifies as an affirmative obligation and ensures consistency with `use-normative-keywords`.
- Include definitions explicitly in the permitted scope.

#### Change B: Confirm `explanatory-must-not-for-clarity` (no change)

Deontic operator is SHOULD; MUST NOT appears as an example. No change required. Confirm consistency of both rules after Change A.

#### Change C: Order adjustment (included in Change A)

Completed by adding A-1 to the end of `prohibitions.items`.

### 5.3 Scope of `prohibitions.override` (Confirmed, No Change)

`prohibitions.override` explicitly overrides format_obligations, content_obligations, and authoring_obligations. Even if `explanatory-must-not-permitted` remains in `authoring_obligations`, the new prohibition A-1 may override authoring_obligations A-2, but the two are complementary and not contradictory. **No further confirmation needed** (Composer confirmed; removed from open issues in r2).

### 5.4 Change Impact Assessment

| Change                    | Target                                                         | Scope                                      |
| ------------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| A-1: Add new rule         | End of `prohibitions.items`                                    | Add one rule record                        |
| A-2: Rewrite existing rule | `authoring_obligations.explanatory-must-not-permitted` | Change statement + verification fields only |
| B: Confirmation only      | None                                                           | No change                                  |

---

## 6. Final Policy on Application Strength

**Apply Medium strength as MUST (mandatory).**

Concrete application rules (see Section 2.3 deontic operator determination procedure):

- Rule records whose deontic operator in `statement` is **MUST NOT**: MUST be placed in `prohibitions.items`.
- Rule records whose deontic operator is not MUST NOT: Do not require placement in `prohibitions` (MUST NOT may appear elsewhere and is permitted).
- MUST NOT in fields outside rule records: Permitted (scope of `explanatory-must-not-permitted`).

**Reason for not adopting Strict strength** (all agent agreement):

- Moving all explanatory MUST NOT to `prohibitions` would require elevating them to rule records, greatly inflating structure.
- From Semantic Gravity Wells, expansion of MUST NOT records increases priming risk.
- Medium strength achieves most compliance benefit.

---

## 7. Implementation Plan

### 7.1 Phase 1: Restore Meta-Circular Compliance (Core of This Task)

| Tier                         | Content                                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0 (Structure verification)** | Enumerate all rule records in SKILL.md and update the violation list in Sections 3.2–3.4.                                                         |
| **Tier 1 (Change implementation)**  | Implement Change A (add A-1, rewrite A-2).                                                                                                        |
| **Tier 2 (Objective verification)** | YAML parse verification, structure verification, `prohibitions-dedicated-section` compliance, `one-obligation-per-rule` compliance, rule-record schema verification. |
| **Tier 3 (Subjective quality check)** | Human review to confirm that post-change wording preserves intent.                                                                               |

### 7.2 Phase 2: Move `prohibitions` Section Earlier (Separate Task)

As supplementary reinforcement for lost-in-the-middle mitigation, move the `prohibitions` section within the YAML block to immediately after `interpretation` and `precedence_and_conflict` (Composer proposal; adopted and explicitly Phase 2).

- This is a structural change; treat as a separate task after Phase 1 completion.
- From Semantic Gravity Wells, the effect of placement is supplementary; pairing with verification method strengthening is important.

### 7.3 Phase 3: Strengthen Verification Methods (Separate Task, Recommended)

Based on Codex proposal, consider adding the following verification methods:

| Verification method proposal       | Purpose                                                          |
| ---------------------------------- | ---------------------------------------------------------------- |
| `must-not-locality-validation`     | Verify no prohibition exists outside `prohibitions.items`         |
| `one-modal-per-rule-validation`    | Check one rule, one modal (prohibit compound predicates)          |

These are not required for Phase 1 acceptance but are effective for preventing recurrence of meta-circular violations.

### 7.4 Acceptance Criteria (Phase 1)

- No rule record outside `prohibitions.items` has a deontic operator in `statement` that is MUST NOT.
- YAML parses successfully with a standard parser.
- Rule-record schema (id, layer, priority, statement, conditions, exceptions, verification) is maintained for all rules.
- No semantic contradiction between `explanatory-must-not-permitted` and `no-treat-explanatory-must-not-as-prohibition`.

---

## 8. Major Changes from r2

| Change area                 | r2 wording                               | r3 (this document) revision                                                                                                                              | Basis                  |
| --------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| Establishment wording       | "Supported as reasonable practice"        | Limited to "position as high-confidence design practice"; explicitly not treating as "established theorem" or "mechanistic convention" (GPT, Codex)       | GPT, Codex             |
| Machine verifiability of determination procedure | Procedure defined but limits not stated | Explicitly state limits (full machine verification may require natural-language parsing); add future `statement_modal` field idea (GPT, Codex)       | GPT, Codex             |
| Definitions scope           | Implicitly permitted                     | Include "definitions" explicitly in A-1, A-2 statements to resolve ambiguity (Composer)                                                                  | Composer               |
| Verification method strengthening | Not mentioned                        | Add as Phase 3 consideration: `must-not-locality-validation` / `one-modal-per-rule-validation` (Codex)                                                    | Codex                  |
| Phase 2 positioning         | In implementation plan but separate task | Same separate-task treatment; explicitly number as Phase for better planning (Composer)                                                                   | Composer               |
| Agent contribution documentation | Mentioned in table as review basis   | Detail each agent's major contributions in Section 0.2; improve integration transparency (self-containment requirement for this plan)                       | Self-containment requirement |
| Term definitions           | Used implicitly in the body              | Consolidate term definitions in Section 0.4                                                                                                              | Self-containment requirement |

---

## 9. Open and Follow-Up Items

1. **Normative prohibition of `definitions.tier-separation`**:
   Currently permitted as explanatory use; future consideration: add `no-interleave-tiers` to prohibitions and reference from definitions in a separate task.

2. **Application to other AI directive files**:
   Currently only one skill file under `.agents/skills/` in this repository. When additional files exist, decide whether to apply the same Medium strength (including deontic operator determination). Alternatively, unify via reference (id/link) to the authoring skill.

3. **Concretizing Semantic Gravity Wells mitigation**:
   Consider adding specific guidelines for AI directive file style to reduce priming risk (e.g., "describe preferred state affirmatively instead of directly naming prohibited targets") as a separate task.

4. **Linting of deontic operator determination**:
   Implement the determination procedure in Section 2.3 as a machine-executable linter to improve compliance with `verification-machine-checkable`. Also consider Codex proposal for adding a `statement_modal` field.

5. **Guidelines for MUST NOT in explanatory text**:
   Consider whether to move toward "permit only when necessary (SHOULD NOT use routinely)" regarding Codex's point on side effects of "actively using MUST NOT in explanatory text." Currently `explanatory-must-not-for-clarity` recommends with SHOULD; whether to lower this recommendation strength is the issue.
