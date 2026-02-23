# Policy on a Dedicated MUST NOT Section and Authoring Skill Improvement Plan (r3 Integrated Version)

Created on: 2026-02-23  
Base documents: `must-not-section-policy-and-remediation-plan-r2.md`, `plan.codex.md`, `plan.composer.md`, `plan.gpt.md`, `plan.opus.md`  
Target file (canonical): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`  
Path note: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`,  
`.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` are all symbolic links to `../.agents/skills`,  
and therefore there is only one canonical file under `.agents/skills/`.  
Any modification only needs to be made to this single file.  
Status: Integrated plan (no concrete file changes)

---

## 0. Purpose and Premises of This Document

### 0.1 Purpose

This document is an integrated response to the following proposition:

1. In AI directive files, is placing a dedicated section near the beginning of the file that collects only MUST NOT statements established by research results or by common/mechanistic norms?
2. If so, what strength of application leads to the best effect?
3. How should we improve the current state where the authoring skill does not satisfy meta-circularity?

### 0.2 Integration Method

The r2 core plan and four agent reviews (Codex / Composer / GPT / Opus) were
comprehensively examined to extract consensus points, resolve conflicts, and fill gaps.

The primary contributions from each agent plan are summarized below:

| Agent    | Primary Contribution                                                                                                                                                                                                                                  |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT      | Warning against over-assertive language around what is "established"; identifying the need to make Medium-strength "main predicate" judgment machine-verifiable; proposing explicit judgment procedures (decision rules)                            |
| Codex    | Policy to bound evidentiary wording to "strong practical best practice"; raising synchronization concerns between `.agents` and other paths; proposing explicit fields such as `statement_modal`; proposing additional verification methods (`must-not-locality-validation`, `one-modal-per-rule-validation`) |
| Opus     | Integrating a rebuttal based on Semantic Gravity Wells (arXiv 2601.08070, 2026); consistency analysis with prior implementation (previous branch commit); proposing an affirmative obligation form for A-2 statement: "MUST be classified as explanatory" |
| Composer | Pointing out schema deficiencies in rule A-1 (`exceptions` / `verification` missing); explicitly incorporating Phase 2 (moving prohibitions earlier) into the execution plan; presenting a future option to make `definitions.tier-separation` normatively prohibitive; concluding no further confirmation is required for `prohibitions.override` |

### 0.3 Non-goals

- Exact citation-level validation of individual papers on LLM attention characteristics is not an acceptance criterion of this plan.
- Repository-wide rollout to all AI directive files is not mandatory in this plan (candidate for a separate task).
- Concrete file edits to AI directive files are out of scope for this plan.

### 0.4 Definitions

Terms in this document are defined as follows:

- **AI directive files**: Markdown files under `.agents/skills/` (YAML frontmatter + a single fenced YAML block).
- **authoring skill**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`, a meta-skill that defines the format, structure, and rules of AI directive files.
- **rule record**: A structured record with `id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`.
- **meta-circular**: A state in which the authoring skill itself complies with every rule it defines.
- **deontic operator**: The principal RFC modal expressing obligation/prohibition of a rule, identified from the `statement` field by the judgment procedure defined later.

---

## 1. Effectiveness of a Dedicated MUST NOT Section: Research Basis and Normative Design Principles

### 1.1 LLM Context Processing and the "Lost-in-the-Middle" Phenomenon

Large language models (LLMs) do not process information in long contexts uniformly.
Prior studies (e.g., Liu et al. 2023) describe the **"lost-in-the-middle"** phenomenon:
information at the beginning and end of a prompt is significantly more activated than information in the middle.

This nonlinear attention distribution has direct implications for AI directive file design:

- **Prohibitions (MUST NOT) carry high failure cost**: once violated during generation, rollback is difficult.
- **If prohibitions are buried in the middle, compliance declines**: in long instructions, prohibitions placed in the middle are more likely to be forgotten or ignored than those at the start/end.

### 1.2 Empirical Findings on Instruction Hierarchy

Findings from OpenAI's "Instruction Hierarchy" work (Wallace et al. 2024) and
Anthropic's Constitutional AI support the following:

- Constraints are most likely to be followed when explicit, independent, and presented early.
- When constraints are embedded in other content, model attention weakens, and compliance tends to drop.
- A design that groups prohibition categories in one place and presents them early is **reasonably inferred** to help activate prohibitions before generation begins.

**Important limitations** (GPT/Opus consensus):

- OpenReview 2025 work shows that even with system/user prompt separation,
  stable establishment of instruction hierarchy can fail, and models tend to ignore priority annotations for constraint types.
- "Retention in a working-memory-like store" is not a directly proven conclusion and should be treated as a reasonable inference.
- Enforceability should rely not on "research-level assertions" but on designs that can be mechanically validated by runner/linter (GPT).

### 1.3 Semantic Gravity Wells: Reverse Activation Risk of Negative Constraints (Critical Counterevidence)

Semantic Gravity Wells (arXiv 2601.08070, 2026) identifies mechanisms by which negative constraints fail in LLMs and has direct implications for dedicated MUST NOT section design
(highlighted by Opus and integrated in r2):

- **Priming Failure (87.5% of violations)**: explicitly mentioning a prohibited target can activate it rather than suppress it. Saying "do not do X" can strongly evoke X.
- **Override Failure (12.5% of violations)**: later FFN layers produce positive contributions to prohibited tokens
  (+0.39), overriding earlier suppression signals with roughly 4x strength.
- **Suppression asymmetry**: success reduces probability by 22.8 points, while failure increases by only 5.2 points (4.4x asymmetry).

**Design implications** (consensus across all agents):

- Merely "listing" MUST NOTs in a dedicated section can repeatedly activate prohibited targets through a priming effect.
- **Placement strategy is a supporting measure for compliance improvement, not a guarantee;
  post-hoc verification methods are the true compliance guarantee mechanism.**
- Strong/Strict intensities (expansion of MUST NOT records) may increase priming risk.

### 1.4 Perspectives from Normative Theory and Specification Design

In design practice for laws and technical specifications (RFCs, statutory texts, security policies, etc.),
prohibitions are often front-loaded as independent clauses/sections:

- RFC 2119 defines MUST NOT as a normative keyword equal in status to MUST and demands structural clarity in specification documents.
- In security policy design, placing prohibitions first under a "deny-by-default" principle is standard.

### 1.5 Conclusion: Assessment of Degree of Establishment

| Perspective                                                            | Degree | Notes                                                                               |
| ---------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------- |
| Empirical evidence for LLM attention mechanism (lost-in-the-middle)    | High   | Reproduced across multiple independent studies                                      |
| Early placement of prohibitions as an auxiliary compliance enhancer    | Medium | Reasonable inference rather than direct proof; Semantic Gravity Wells provides counterevidence |
| Explicitness benefit of dedicated MUST NOT concentration               | High   | Established in specification/legal design theory; auxiliary, not a guarantee       |
| Reverse activation risk from explicit MUST NOT mention                 | High   | Semantic Gravity Wells (2026): priming failure 87.5%                               |
| Combination of structuring (dedicated section) + post-hoc verification | High   | Placement alone is insufficient; verification is required                           |
| Optimal point for "how early to place"                                | Medium | Early placement is preferred, but quantitative optimum is unresolved; reverse activation risk must also be considered |

**Overall assessment (integrated conclusion based on all-agent consensus):**

Concentrating MUST NOT statements into an independent dedicated section near the beginning of a file
is **supported as a reasonable design practice** based on LLM processing characteristics,
specification design theory, and empirical research.

However, the following limits are essential:

1. "Concentrated placement increases compliance" does not hold as a simple rule (counterevidence from Semantic Gravity Wells).
2. It should be evaluated as **reasonably established only as a combined approach of
   "structured dedicated section + post-hoc verification."**
   Effect from placement alone is not established.
3. It should be positioned not as an "established theorem" or "mechanistic common sense,"
   but as a **high-confidence design practice grounded in LLM positional dependence,
   structural clarity in specification design, and ease of verification** (GPT/Codex consensus).

---

## 2. Choosing Application Strength

### 2.1 Strength Levels

| Strength level | Description                                                                                                                                                                                                                                              |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Weak**       | SHOULD be in a dedicated section. Broad exceptions are allowed.                                                                                                                                                                                         |
| **Medium**     | All normative MUST NOT records (where the deontic operator of a rule record's `statement` field is MUST NOT) are placed in `prohibitions`. Explanatory MUST NOT usage is allowed (outside rule-record fields, and in `statement` where the deontic operator is not MUST NOT). |
| **Strong**     | Any MUST NOT appearing in any rule record's `statement` field is moved into `prohibitions` regardless of section.                                                                                                                                      |
| **Strict**     | MUST NOT text is prohibited anywhere outside the `prohibitions` section across the entire file.                                                                                                                                                        |

### 2.2 Recommended Strength and Rationale (all-agent consensus)

**Recommended strength: Medium (applied as MUST)**

Reasons:

- As shown by `explanatory-must-not-permitted` / `explanatory-must-not-for-clarity`,
  occurrence of the phrase MUST NOT and occurrence of a normative prohibition must be distinguished.
- MUST NOT occurrences in fields such as interpretation, definitions, and failure_states_and_degradation
  are explanatory, and elevating them into `prohibitions` would:
  - require applying a rule-record schema to explanatory prose, inflating file structure;
  - blur boundaries of what is normative, making compliance verification harder.
- Based on Semantic Gravity Wells, Strong/Strict can inflate MUST NOT records and may increase priming risk.
- Most lost-in-the-middle mitigation can be achieved at Medium strength, so incremental benefit from Strong/Strict is small.

### 2.3 Operational Definition of Medium Strength: Deontic-Operator Judgment Procedure

To resolve GPT/Codex concerns about non-determinism in "main predicate" judgment,
this plan adopts the syntactic judgment procedure introduced in r2.

**Definition of deontic operator**:

Scan the `statement` field from left to right, and take the first RFC modal
(MUST NOT / MUST / SHOULD NOT / SHOULD / MAY) that is judged to "count"
as the deontic operator.

**Conditions for "does not count (explanatory)"** (if any of the following apply):

1. It appears as a token enclosed in single or double quotes (e.g., `'MUST NOT'`).
2. It is explicitly a phrase mention, such as "the phrase MUST NOT" or "phrase MUST NOT."
3. It appears as part of an RFC keyword listing (e.g., `(MUST, MUST NOT, SHOULD, ...)`).
4. It appears as explanatory parenthetical text (e.g., `All normative prohibitions (MUST NOT) MUST ...`).
5. It appears as part of an example following "e.g." or "for example."

**Condition for "counts (normative)"**:
Any occurrence not falling under "does not count."

**Medium-strength rule**:

> Any rule record whose deontic operator in `statement` is **MUST NOT**
> MUST be placed in `prohibitions.items`.
> Rule records whose deontic operator is not MUST NOT, and MUST NOT occurrences
> in non-rule-record fields (`description`, `behavior`, `degradation`, `verification`, etc.),
> are treated as explanatory usage and do not require moving into `prohibitions`.

### 2.4 Limits of the Judgment Procedure and Future Outlook

**Current limits** (as pointed out by GPT/Codex):

- The above procedure is clear for humans, but fully mechanical verification may require
  natural language analysis beyond regular expressions in some cases.
- Full consistency with `verification-machine-checkable` claimed by the authoring skill itself
  is currently deferred to future linting.

**Future improvement candidates** (Codex proposal):

- Add an explicit field such as `statement_modal` (`MUST`, `MUST_NOT`, `SHOULD`, etc.)
  to rule records, as a structural solution that avoids ambiguous parsing of `statement` text.
- Implement the judgment procedure as a linter to improve conformance to `verification-machine-checkable`.

---

## 3. Identifying Current Meta-Circular Non-compliance in the Authoring Skill

### 3.1 Investigation Method

Across the full SKILL.md, rules containing MUST NOT in the `statement` field were enumerated,
and the deontic-operator judgment procedure (Section 2.3) was applied.

### 3.2 Confirmed Violations (all-agent consensus)

#### Violation 1: Placement of `explanatory-must-not-permitted`

| Item             | Value                                                                                                                                                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rule ID          | `explanatory-must-not-permitted`                                                                                                                                                                                                         |
| Current section  | `authoring_obligations`                                                                                                                                                                                                                  |
| statement        | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."` |
| Deontic operator | MUST NOT (`"MUST NOT be treated"` is the first "counting" modal in left-to-right scan)                                                                                                                                                 |
| Violation        | Deontic operator is MUST NOT, but the rule is not placed in `prohibitions`                                                                                                                                                              |
| Reference rule   | `prohibitions-dedicated-section`                                                                                                                                                                                                         |

#### Secondary issue: Compound predicate in `explanatory-must-not-permitted`

| Item                      | Value                                                                                                                                                                                                      |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rule ID                   | `explanatory-must-not-permitted`                                                                                                                                                                           |
| Issue                     | Two predicates coexist: `"is allowed"` (permission) and `"MUST NOT be treated"` (prohibition)                                                                                                             |
| Reference rule            | `one-obligation-per-rule`                                                                                                                                                                                  |
| Interpretation & decision | If `"is allowed"` is read as MAY-equivalent, one could interpret formal presence of only one MUST NOT predicate; however, ambiguity of `"is allowed"` itself conflicts with the spirit of `no-ambiguous-modals`, so splitting is preferable (r2/GPT/Codex/Composer consensus) |

### 3.3 Confirmed Non-violations (contains MUST NOT in `statement`, but not as deontic operator)

| Rule ID                            | Section                 | MUST NOT occurrence form                                                    | Deontic operator | Judgment          |
| ---------------------------------- | ----------------------- | --------------------------------------------------------------------------- | ---------------- | ----------------- |
| `explanatory-must-not-for-clarity` | `authoring_obligations` | Example usage as "e.g. listing RFC keywords"; main operator is SHOULD.      | SHOULD           | **No violation**  |
| `use-normative-keywords`           | `authoring_obligations` | Part of RFC keyword listing `(MUST, MUST NOT, ...)`; main operator is MUST. | MUST             | **No violation**  |
| `prohibitions-dedicated-section`   | `authoring_obligations` | Appears as parenthetical explanation `(MUST NOT)`; main operator is MUST.   | MUST             | **No violation**  |
| `define-conflict-policy`           | `authoring_obligations` | Appears in example (`e.g. MUST vs MUST: halt`); main operator is MUST.      | MUST             | **No violation**  |

### 3.4 MUST NOT outside rule records (allowed as explanatory usage)

The following MUST NOT occurrences appear outside a rule record's `statement` field
and fall within the allowed explanatory range defined by `explanatory-must-not-permitted`:

| Location                                                    | Field type                        |
| ----------------------------------------------------------- | --------------------------------- |
| `interpretation.unknown_keys`                               | interpretation prose              |
| `interpretation.unspecified_behavior`                       | interpretation prose              |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST`      | conflict policy prose             |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose                    |
| `failure_states_and_degradation.degradation`                | degradation prose                 |
| `definitions.tier-separation.description`                   | definition prose (see note)       |
| verification of `one-obligation-per-rule`                   | verification field                |

**Note on `definitions.tier-separation.description`** (Composer point):

The phrase "MUST NOT interleave" in this text effectively functions as
a normative prohibition in contexts where tier-separation applies.
Whether the definitions field is included in the allowed range explicitly stated by
`explanatory-must-not-permitted` ("interpretation, semantics, or verification")
is not specified within SKILL.md.

**Policy in this plan**: For now, proceed by treating the definitions field as included in
the allowed range (i.e., explanatory usage).
At remediation time, add "definitions" explicitly to statements A-1 and A-2
to remove this ambiguity.
Future refactoring to add an independent rule `no-interleave-tiers` under prohibitions
and reference it from definitions remains a candidate for a separate task.

---

## 4. Goal Setting

### 4.1 Target State

**Definition of full meta-circular compliance** (all-agent consensus):

> A state where the authoring skill itself complies with all rules it defines.  
> Specifically: the authoring skill itself satisfies conditions required by
> `prohibitions-dedicated-section`, `one-obligation-per-rule`, and `no-ambiguous-modals`.

### 4.2 Compliance Confirmation Criteria

1. In all rule records outside `prohibitions.items`,
   the deontic operator in `statement` is not MUST NOT.
2. The allowed scope of "explanatory MUST NOT" defined by `explanatory-must-not-permitted`
   is applied consistently within the file.
3. "One rule, one predicate" required by `one-obligation-per-rule`
   is satisfied in all rule records.
4. YAML can be parsed successfully by a standard parser.
5. All rule records conform to the rule-record schema
   (`id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`).

### 4.3 Secondary Goals (GPT/Codex proposals)

- **Machine verifiability**: Target a state where "which record is a prohibition" can be judged by syntactic rules.
- **Recurrence prevention**: Consider adding verification methods so meta-circular violations do not recur when new rules are added.

---

## 5. Remediation Policy

### 5.1 Basic Policy

Principle of **minimum change, maximum consistency** (all-agent consensus):
without changing existing structure, rule count, or intent,
restore meta-circular compliance by refactoring the description of
`explanatory-must-not-permitted`.

### 5.2 Concrete Change Policy

#### Change A: Split `explanatory-must-not-permitted`

Split the current single rule (two predicates) into the following two rules.

**Post-split Rule A-1 (add at the end of `prohibitions.items`)**

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

Design highlights:

- Explicitly include definitions in `statement` (resolving ambiguity flagged by Composer).
- Complete `exceptions` and `verification` (resolving schema gap flagged by Composer).
- The deontic operator is MUST NOT; placement in `prohibitions.items` conforms to Medium strength.

**Post-split Rule A-2 (remain in `authoring_obligations`, rewrite statement)**

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

Design highlights:

- Deontic operator is MUST ("MUST be classified"), not MUST NOT.
  Therefore placement outside `prohibitions` conforms to Medium strength.
- The r1-proposed phrase "does not constitute an enforceable prohibition"
  is a negative assertion that does not match RFC-style normative keywords
  required by `use-normative-keywords`, and is therefore rejected
  (Opus point, already fixed in r2).
- Using "MUST be classified as explanatory" + cross-reference to
  `no-treat-explanatory-must-not-as-prohibition` clarifies as an affirmative obligation
  and preserves consistency with `use-normative-keywords`.
- Explicitly include definitions in the allowed scope.

#### Change B: Confirm `explanatory-must-not-for-clarity` (no change)

Its deontic operator in `statement` is SHOULD, and MUST NOT appears as an example, so no change is needed.
After Change A, verify consistency between both rules.

#### Change C: Ordering adjustment (included in Change A)

Completed by adding A-1 to the end of `prohibitions.items`.

### 5.3 Scope of `prohibitions.override` (confirmed, no change required)

`prohibitions.override` explicitly overrides format_obligations / content_obligations / authoring_obligations.
Even when `explanatory-must-not-permitted` remains in `authoring_obligations`,
new prohibition A-1 may override authoring-obligation A-2, but both are complementary
and not contradictory. **No further confirmation is required on this point**
(already confirmed by Composer and removed from unresolved items in r2).

### 5.4 Change Volume Assessment

| Change                          | Target                                                    | Scope of impact                                 |
| ------------------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| A-1: Add new rule               | End of `prohibitions.items`                               | Add one rule record                             |
| A-2: Rewrite existing rule      | `authoring_obligations.explanatory-must-not-permitted`   | Modify only statement + verification fields     |
| B: Confirmation only            | None                                                      | No change                                       |

---

## 6. Final Policy on Application Strength

**Apply Medium strength as MUST (mandatory).**

Concrete application rules (see deontic-operator judgment procedure in Section 2.3):

- Rule records whose deontic operator in `statement` is **MUST NOT**:
  MUST be placed in `prohibitions.items`.
- Rule records whose deontic operator in `statement` is not MUST NOT:
  no move to `prohibitions` is required (MUST NOT appearing in other forms is allowed).
- MUST NOT in fields outside rule records:
  allowed (within scope of `explanatory-must-not-permitted`).

**Why Strict is not adopted** (all-agent consensus):

- Moving all explanatory MUST NOT into `prohibitions` would require elevating prose into rule records, causing major structural inflation.
- Based on Semantic Gravity Wells, inflating MUST NOT records may increase priming risk.
- Medium strength achieves most compliance effect.

---

## 7. Execution Plan

### 7.1 Phase 1: Restore meta-circular compliance (core of this task)

| Tier                            | Description                                                                                                                                    |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0 (structure check)**    | Enumerate all rule records in SKILL.md and refresh the confirmed-violation list in Sections 3.2-3.4.                                          |
| **Tier 1 (apply changes)**      | Apply Change A (add A-1 + rewrite A-2).                                                                                                       |
| **Tier 2 (objective validation)** | Run YAML parse validation, structural validation, `prohibitions-dedicated-section` compliance check, `one-obligation-per-rule` compliance check, and rule-record schema check. |
| **Tier 3 (subjective quality check)** | Human review to confirm post-change descriptions preserve intended meaning.                                                             |

### 7.2 Phase 2: Move `prohibitions` section earlier (separate task)

As an auxiliary enhancement against lost-in-the-middle, move the `prohibitions` section
within the YAML block to immediately after `interpretation` and `precedence_and_conflict`
(adopting Composer's proposal and making it explicit as a phase).

- This is a large structural change and should be handled as a separate task after Phase 1.
- Given Semantic Gravity Wells, impact from this relocation should be treated as auxiliary.
  It is important to combine with stronger post-hoc verification methods.

### 7.3 Phase 3: Strengthen verification methods (separate task, recommended)

Based on Codex's proposal, consider adding the following verification methods:

| Candidate verification method     | Purpose                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| `must-not-locality-validation`    | Verify prohibitions do not exist outside `prohibitions.items`    |
| `one-modal-per-rule-validation`   | Verify one-rule/one-modal (prohibit compound predicates)         |

These are not acceptance criteria for Phase 1, but are effective in preventing recurrence of meta-circular violations.

### 7.4 Acceptance Criteria (Phase 1)

- In all rule records outside `prohibitions.items`, the deontic operator in `statement` is not MUST NOT.
- YAML parses successfully with a standard parser.
- Rule-record schema (`id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`) is preserved across all rules.
- No semantic contradiction exists between `explanatory-must-not-permitted` and `no-treat-explanatory-must-not-as-prohibition`.

---

## 8. Major Changes from r2

| Change area                        | r2 wording                              | r3 (this document) revision                                                                                                 | Basis                    |
| ---------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Expression of establishment degree | "supported as a reasonable practice"    | Restricted to "positioned as a high-confidence design practice"; explicitly not treated as an "established theorem" or "mechanistic common sense" | GPT, Codex               |
| Machine verifiability of judgment procedure | Judgment procedure defined but limits not explicit | Explicitly states limits (some cases require natural language analysis for full machine validation) and adds future `statement_modal` field concept | GPT, Codex               |
| Allowed scope for definitions      | Implicitly allowed                       | Explicitly include "definitions" in A-1 and A-2 statements to remove ambiguity                                               | Composer                 |
| Verification-method strengthening  | Not mentioned                            | Add `must-not-locality-validation` / `one-modal-per-rule-validation` as Phase 3 consideration                              | Codex                    |
| Positioning of Phase 2             | Included in plan as separate task        | Also separate task, but explicitly numbered as a phase to improve planning clarity                                           | Composer                 |
| Explicit mention of agent contributions | Mentioned in table as review basis      | Section 0.2 details major contributions from each agent and improves integration transparency                                | Self-containment requirement of this plan |
| Definitions                         | Used implicitly in body                  | Consolidated in Section 0.4                                                                                                  | Self-containment requirement |

---

## 9. Unresolved / Ongoing Considerations

1. **Normative prohibition for `definitions.tier-separation`**:  
   Currently treated as allowed explanatory usage, but future task candidate remains to add
   `no-interleave-tiers` under prohibitions and reference it from definitions.

2. **Rollout to other AI directive files**:  
   This repository currently has only one skill file under `.agents/skills/`.
   If files increase, decide whether to apply the same Medium strength
   (including deontic-operator judgment procedure) or standardize on references (id/link) to the authoring skill.

3. **Concrete mitigations for Semantic Gravity Wells**:  
   As a writing style for AI directive files, adding concrete guidelines to reduce priming risk
   (e.g., describing desired states affirmatively instead of directly naming prohibited targets)
   is worth considering as a separate task.

4. **Linting deontic-operator judgment**:  
   Implement the Section 2.3 judgment procedure as a machine-executable linter
   to improve conformance with `verification-machine-checkable`.
   Also consider Codex's `statement_modal` field proposal.

5. **Guideline for MUST NOT usage in explanatory prose**:  
   Regarding Codex's concern about side effects of actively using MUST NOT in prose,
   consider whether to shift toward "allow only when necessary (SHOULD NOT habitual use)."
   Since current `explanatory-must-not-for-clarity` recommendation is SHOULD,
   whether to lower this recommendation strength remains an open point.
