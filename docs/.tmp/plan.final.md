# Policy for a MUST NOT–Focused Section and an Authoring Skill Remediation Plan (r3 Integrated Version)

Target file (canonical): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`  
Path note: `.cursor/skills/`, `.github/skills/`, `.claude/skills/`, `.agent/skills/`, `.gemini/skills/`, `.opencode/skills/`, `.windsurf/skills/` are all symlinks to `../.agents/skills`, and the only canonical file is the single file under `.agents/skills/`. Fixes only need to be made to this one file.

profile:

- Apply the MUST NOT–focused section policy with **Medium strength** (normative MUST NOT rules consolidated in `prohibitions.items`; explanatory/illustrative MUST NOTs remain non-normative and are kept out of `prohibitions.items`).
- Treat “MUST NOT consolidation” as a **high-confidence design practice** rather than an established theorem; pair it with objective verification methods.

## 0. Purpose and assumptions of this document

### 0.1 Purpose

This document is an integrated answer to the following propositions:

1. In AI directive files, is placing an independent section near the beginning of the file that collects only MUST NOTs established as research-backed or mechanism-level common knowledge / norms?
2. If it is established, what strength of application most effectively improves outcomes?
3. Given the current state where the authoring skill does not satisfy meta-circularity, what policy should we adopt to improve the situation?

### 0.2 Method of integration

This document comprehensively examined the r2 main plan and four agent reviews (Codex / Composer / GPT / Opus), then extracted points of agreement, resolved conflicts, and filled gaps.

The main contributions of each agent plan are summarized below:

| Agent    | Main contribution(s)                                                                                                                                                                                                                                                                                              |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GPT      | Warning about the strength of the “it is established” assertion; pointing out the need to make the Medium-strength “main predicate” determination mechanically checkable; proposing explicit decision procedures (decision rules)                                                                                 |
| Codex    | Policy to constrain evidentiary language to “strong practical best practice”; raising the `.agents` vs other-path synchronization issue; concept of introducing explicit fields such as `statement_modal`; proposing added verification methods (`must-not-locality-validation`, `one-modal-per-rule-validation`) |
| Opus     | Integrating Semantic Gravity Wells (arXiv 2601.08070, 2026) as a counterpoint; analyzing consistency with prior implementation (previous branch commit); proposing a positive obligation form for A-2 as “MUST be classified as explanatory”                                                                      |
| Composer | Noting the schema deficiency in rule A-1 (`exceptions` / `verification` missing); explicitly incorporating Phase 2 (moving prohibitions earlier) into the execution plan; future option to make `definitions.tier-separation` a normative prohibition; “no need to re-check” judgment for `prohibitions.override` |

### 0.3 Non-goals

- Do not make precise citation verification of individual papers about LLM attention characteristics an acceptance condition for this plan.
- Do not require rollout to all AI directive files as part of this plan (candidate for a separate task).
- Concrete file changes to AI directive files are out of scope for this plan.

### 0.4 Definitions

Terms in this document are defined as follows:

- **AI directive files**: Markdown files under `.agents/skills/` (YAML frontmatter + single fenced YAML block structure).
- **authoring skill**: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`. A meta-skill that defines the format, structure, and rules of AI directive files.
- **rule record**: A structured record with `id`, `layer`, `priority`, `statement`, `conditions`, `exceptions`, `verification`.
- **meta-circular**: A state where the authoring skill complies with all rules that it defines, within the authoring skill itself.
- **deontic operator (normative operator)**: The primary obligation/prohibition RFC modal of a rule, identified from the `statement` field by the decision procedure described later.

## 1. Effectiveness of a MUST NOT–focused section: research grounds and design norms

### 1.1 LLM context processing and the “lost-in-the-middle” phenomenon

Large language models (LLMs) do not process information uniformly across long contexts. In the **“lost-in-the-middle”** phenomenon shown by prior work (e.g., Liu et al. 2023), information at the beginning and the end of a prompt is activated significantly more strongly than information in the middle.

This non-linear attention distribution has direct implications for AI directive file design:

- **Prohibitions (MUST NOT) have high failure cost**: once a prohibition is violated mid-generation, it is difficult to undo.
- **If prohibitions are buried in the middle, adherence decreases**: prohibitions placed in the middle of long instructions are more likely to be forgotten or ignored than those near the beginning/end.

### 1.2 Empirical findings on instruction hierarchy

OpenAI’s “Instruction Hierarchy” research (Wallace et al. 2024) and insights from Anthropic’s Constitutional AI support the following:

- Constraints are most likely to be followed when they are explicit, independent, and presented early.
- When constraints are embedded within other content, model attention thins and compliance tends to decrease.
- A design that collects prohibition categories in one place and presents them early can be **reasonably inferred** to make it easier to activate prohibitions before generation begins.

**Important limitations** (GPT, Opus agreement):

- OpenReview 2025 research shows that even with system/user prompt separation, stable establishment of an instruction hierarchy can fail, and models may ignore priority specifications for constraint types.
- “Retention equivalent to working memory” is not a directly demonstrated conclusion and should be positioned as a reasonable inference.
- The binding force is not a “research assertion”; it depends on designs that can be mechanically validated by runners/linters (GPT).

### 1.3 Semantic Gravity Wells: inverse-activation risk of negative constraints (a key counterpoint)

Semantic Gravity Wells (arXiv 2601.08070, 2026) identifies mechanisms by which negative constraints fail in LLMs and has direct implications for MUST NOT–focused section design (pointed out by Opus; integrated into r2):

- **Priming Failure (87.5% of violations)**: merely mentioning the prohibited target explicitly activates it rather than suppressing it. Writing “do not do X” causes the model to strongly recall X.
- **Override Failure (12.5% of violations)**: later FFN layers generate a positive contribution (+0.39) toward prohibited tokens and override earlier suppression signals by about 4× strength.
- **Asymmetry of suppression**: in success cases, probability decreases by 22.8 points; in failure cases, it decreases by only 5.2 points (4.4× asymmetry).

**Design implications (all-agent agreement)**:

- Simply “listing” MUST NOTs in a focused section can repeatedly activate prohibited targets via the priming effect.
- **Placement strategy is an auxiliary means of improving adherence, not a guarantee; ex post verification via verification methods is the true means of guaranteeing compliance.**
- Strong/Strict strength (inflating MUST NOT records) may increase priming risk.

### 1.4 Perspective from norm theory and specification design

In design practices for laws and technical specifications (RFCs, statutes, security policies, etc.), prohibitions are also front-loaded as independent clauses/sections:

- RFC 2119 defines MUST NOT as a normative keyword on par with MUST and requires structural clarity in specification documents.
- In security policies, placing prohibitions up front is standard under the “deny-by-default” principle.

### 1.5 Conclusion: assessment of “establishedness”

| Perspective                                                        | Strength | Note                                                                                                 |
| ------------------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------- |
| Empirical evidence of LLM attention mechanics (lost-in-the-middle) | High     | Replicated across multiple independent studies                                                       |
| Early placement of prohibitions auxiliary-improves compliance      | Medium   | Reasonable inference, not direct proof; Semantic Gravity Wells shows a counterpoint exists           |
| Explicitness benefit of a dedicated MUST NOT section               | High     | Established in specification/legal design; but auxiliary, not a guarantee                            |
| Inverse-activation risk from explicit MUST NOT mention             | High     | Semantic Gravity Wells (2026): priming failure 87.5%                                                 |
| Combining structure (dedicated section) + ex post verification     | High     | Must be backed by verification, not placement alone                                                  |
| The optimal point for “how early” to place it                      | Medium   | Early is desirable but quantitative optimum is unsettled; inverse activation is also a consideration |

**Overall assessment (integrated conclusion based on all-agent agreement)**:

Designing a dedicated section near the beginning of the file that aggregates MUST NOTs is **supported as a reasonable design practice** by LLM processing characteristics, specification design theory, and empirical research.

However, the following constraints are essential:

1. “Aggregating placement increases compliance” does not hold in a simple form (counterpoint from Semantic Gravity Wells).
2. It should be evaluated as **reasonably established only as a combined approach of “a structured dedicated section + ex post verification (verification)”**. The effect of placement alone is not established.
3. It is appropriate to position it not as an “established theorem” or “mechanism-level common knowledge”, but as a **high-confidence design practice grounded in position-dependent properties of LLMs + clarity in specification design + ease of verification** (GPT, Codex agreement).

## 2. Choosing the application strength

### 2.1 Strength levels

| Strength level | Content                                                                                                                                                                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Weak**       | SHOULD be in a dedicated section. Exceptions are broadly permitted.                                                                                                                                                                                       |
| **Medium**     | All normative MUST NOTs (those whose deontic operator in the `statement` field of a rule record is MUST NOT) must be placed in `prohibitions`. Explanatory MUST NOTs (outside rule records, or where the deontic operator is not MUST NOT) are permitted. |
| **Strong**     | Any MUST NOT included in the `statement` field of any rule record is moved into `prohibitions`, regardless of section.                                                                                                                                    |
| **Strict**     | Prohibit the text MUST NOT from appearing anywhere in the file outside the `prohibitions` section.                                                                                                                                                        |

### 2.2 Recommended strength and rationale (all-agent agreement)

**Recommended strength: Medium (apply as MUST)**

Rationale:

- As shown by both `explanatory-must-not-permitted` and `explanatory-must-not-for-clarity`, the appearance of the phrase MUST NOT and the appearance of a “normative prohibition” must be distinguished.
- MUST NOTs inside fields such as interpretation, definitions, and failure_states_and_degradation are explanatory, and pulling these up into `prohibitions` would:
  - require applying the rule-record schema to explanatory prose, inflating file structure;
  - blur the boundary of what is normative, making compliance verification harder.
- From Semantic Gravity Wells, Strong/Strict can inflate MUST NOT records and may increase priming risk.
- Since Medium achieves most of the lost-in-the-middle mitigation effect, the marginal benefit of Strong/Strict is small.

### 2.3 Operational definition for Medium: decision procedure for determining the deontic operator

To eliminate the “non-determinism of main predicate determination” pointed out by GPT/Codex, this plan adopts the syntactic decision procedure introduced in r2.

**Definition of the deontic operator (normative operator)**:

Scan the `statement` field from the left and treat the first RFC modal (MUST NOT / MUST / SHOULD NOT / SHOULD / MAY) that is judged to “count” as the deontic operator.

**Conditions for “does not count (explanatory)”** (if any of the following hold):

1. Appears as a token surrounded by single or double quotes (e.g., `'MUST NOT'`).
2. Appears in a form explicitly indicating phrase-mention, such as “the phrase MUST NOT”, “phrase MUST NOT”.
3. Appears as part of an enumeration of RFC keywords (e.g., `(MUST, MUST NOT, SHOULD, ...)`).
4. Appears as a parenthetical explanatory note (e.g., `All normative prohibitions (MUST NOT) MUST ...`).
5. Appears as part of an example following “e.g.” / “for example”.

**Condition for “counts (normative)”**: any occurrence that does not meet the above “does not count” conditions.

**Medium-strength rule**:

> Rule records whose deontic operator in `statement` is **MUST NOT** must be placed in `prohibitions.items` (MUST).
> Rule records whose deontic operator is not MUST NOT, and MUST NOT occurrences in fields outside rule records
> (description, behavior, degradation, verification, etc.), are treated as explanatory use and do not require moving to `prohibitions`.

### 2.4 Limits of the procedure and future outlook

**Current limits** (GPT, Codex):

- The procedure is clear to humans, but fully mechanical validation may require natural-language analysis beyond regular expressions.
- Full alignment with the authoring skill’s `verification-machine-checkable` is, at present, left to “future linting”.

**Future improvement candidates** (Codex):

- Introduce an explicit field such as `statement_modal` (e.g., `MUST`, `MUST_NOT`, `SHOULD`) into rule records to structurally avoid ambiguous judgments from `statement` text.
- Implement the procedure as a linter to improve satisfaction of `verification-machine-checkable`.

## 3. Identifying meta-circular non-compliance in the current authoring skill

### 3.1 Investigation method

Enumerate rules whose `statement` field contains MUST NOT across the entire SKILL.md, and apply the deontic-operator decision procedure (Section 2.3).

### 3.2 Confirmed violation (all-agent agreement)

#### Violation 1: placement of `explanatory-must-not-permitted`

| Item             | Value                                                                                                                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Rule ID          | `explanatory-must-not-permitted`                                                                                                                                                                                                     |
| Section          | `authoring_obligations`                                                                                                                                                                                                              |
| statement        | `"When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."` |
| Deontic operator | MUST NOT (because “MUST NOT be treated” is the first “counting” modal during scanning)                                                                                                                                               |
| Violation        | Deontic operator is MUST NOT, but it is not placed in the `prohibitions` section                                                                                                                                                     |
| Reference rule   | `prohibitions-dedicated-section`                                                                                                                                                                                                     |

#### Secondary issue: compound predicate in `explanatory-must-not-permitted`

| Item                                   | Value                                                                                                                                                                                                                                                                               |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rule ID                                | `explanatory-must-not-permitted`                                                                                                                                                                                                                                                    |
| Issue                                  | Two predicates co-exist: “is allowed” (permission) and “MUST NOT be treated” (prohibition)                                                                                                                                                                                          |
| Reference rule                         | `one-obligation-per-rule`                                                                                                                                                                                                                                                           |
| Interpretation and integrated judgment | If “is allowed” is read as MAY-equivalent, it could be interpreted as formally having only one MUST NOT predicate; however, the ambiguity of “is allowed” itself conflicts with the spirit of `no-ambiguous-modals`, so splitting is desirable (r2, GPT, Codex, Composer agreement) |

### 3.3 Non-violation confirmation (cases where `statement` contains MUST NOT but the deontic operator is not MUST NOT)

| Rule ID                            | Section                 | Form of MUST NOT occurrence                                                      | Deontic operator | Judgment          |
| ---------------------------------- | ----------------------- | -------------------------------------------------------------------------------- | ---------------- | ----------------- |
| `explanatory-must-not-for-clarity` | `authoring_obligations` | Example as “e.g. listing RFC keywords”; main operator is SHOULD.                 | SHOULD           | **Non-violation** |
| `use-normative-keywords`           | `authoring_obligations` | Part of RFC keywords enumeration `(MUST, MUST NOT, ...)`; main operator is MUST. | MUST             | **Non-violation** |
| `prohibitions-dedicated-section`   | `authoring_obligations` | Appears as parenthetical note `(MUST NOT)`; main operator is MUST.               | MUST             | **Non-violation** |
| `define-conflict-policy`           | `authoring_obligations` | Appears in an example (`e.g. MUST vs MUST: halt`); main operator is MUST.        | MUST             | **Non-violation** |

### 3.4 MUST NOTs outside rule records (permitted as explanatory use)

The following MUST NOT occurrences appear outside the `statement` fields of rule records and fall within the permitted range defined by `explanatory-must-not-permitted`:

| Location                                                    | Field type                  |
| ----------------------------------------------------------- | --------------------------- |
| `interpretation.unknown_keys`                               | interpretation prose        |
| `interpretation.unspecified_behavior`                       | interpretation prose        |
| `precedence_and_conflict.conflict_policy.MUST_vs_MUST`      | conflict policy prose       |
| `failure_states_and_degradation.failure_states[0].behavior` | behavior prose              |
| `failure_states_and_degradation.degradation`                | degradation prose           |
| `definitions.tier-separation.description`                   | definition prose (see note) |
| verification of `one-obligation-per-rule`                   | verification field          |

**Note on `definitions.tier-separation.description`** (Composer):

The phrase “MUST NOT interleave” in this description effectively functions as a normative prohibition in contexts where tier-separation applies. Whether the definitions field is included in the permitted scope explicitly stated as “interpretation, semantics, or verification” by `explanatory-must-not-permitted` is not specified within SKILL.md.

**Policy in this plan**: proceed by treating the definitions field as included in the permitted scope (as explanatory use) for the current state. When fixing, explicitly add “definitions” to the statements of A-1 and A-2 to resolve this ambiguity. As a future candidate task, keep the option of adding an independent prohibition rule as `no-interleave-tiers` under prohibitions and referencing it from definitions.

## 4. Goal setting

### 4.1 Target state

**Definition of full meta-circular compliance** (all-agent agreement):

> A state where the authoring skill complies with all rules it defines within the authoring skill itself.
> Concretely: a state where the authoring skill itself satisfies the conditions required by `prohibitions-dedicated-section`, `one-obligation-per-rule`, and `no-ambiguous-modals`.

### 4.2 Compliance confirmation criteria

1. For all rule records outside `prohibitions.items`, the deontic operator of `statement` is not MUST NOT.
2. The permitted scope of “explanatory MUST NOT” defined by `explanatory-must-not-permitted` is applied consistently within the file.
3. The “one rule, one predicate” requirement of `one-obligation-per-rule` is satisfied for all rule records.
4. The YAML parses successfully with a standard parser.
5. All rule records conform to the rule-record schema (`id, layer, priority, statement, conditions, exceptions, verification`).

### 4.3 Secondary goals (GPT, Codex)

- **Machine-checkability**: aim for a state where “which items are prohibitions” can be determined via syntactic rules.
- **Recurrence prevention**: consider adding verification methods so meta-circular violations do not recur when new rules are added.

## 5. Remediation policy

### 5.1 Basic policy

**Minimum change, maximum consistency** principle (all-agent agreement): restore meta-circular compliance by refactoring the description of `explanatory-must-not-permitted` without changing existing structure, rule count, or intent.

### 5.2 Concrete remediation policy

#### Change A: split `explanatory-must-not-permitted`

Split the current single rule (two predicates) into the following two rules.

**Post-split rule A-1 (append to the end of `prohibitions.items`)**

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

- Explicitly include “definitions” in `statement` (resolves the ambiguity noted by Composer).
- Complete `exceptions` and `verification` (resolves the schema deficiency noted by Composer).
- The deontic operator is MUST NOT, and placement in `prohibitions.items` conforms to Medium strength.

**Post-split rule A-2 (remain in `authoring_obligations`; rewrite statement)**

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

- The deontic operator is MUST (“MUST be classified”), not MUST NOT. This makes placement outside `prohibitions` conform to Medium strength.
- The r1-proposed “does not constitute an enforceable prohibition” is rejected because it is a negative assertion that does not match any RFC-style normative keyword required by `use-normative-keywords` (Opus; fixed in r2).
- By making it “MUST be classified as explanatory” and cross-referencing `no-treat-explanatory-must-not-as-prohibition`, the rule is clarified as a positive obligation and compatibility with `use-normative-keywords` is maintained.
- Explicitly include “definitions” in the permitted scope.

#### Change B: confirm `explanatory-must-not-for-clarity` (no change)

No change is required because the deontic operator of `statement` is SHOULD and MUST NOT appears only as an example. After performing Change A, confirm consistency between the two rules.

#### Change C: reorder (included in Change A)

Complete by appending A-1 to the end of `prohibitions.items`.

### 5.3 Scope of `prohibitions.override` (confirmed; no change needed)

`prohibitions.override` explicitly overrides format_obligations / content_obligations / authoring_obligations. Even if `explanatory-must-not-permitted` remains in `authoring_obligations`, the new prohibition A-1 can override A-2 in authoring_obligations; however, the two are complementary and not contradictory. **No re-check is required on this point** (Composer confirmed; removed from unresolved items in r2).

### 5.4 Change size evaluation

| Change                     | Target                                                 | Scope of impact                             |
| -------------------------- | ------------------------------------------------------ | ------------------------------------------- |
| A-1: add new rule          | end of `prohibitions.items`                            | add 1 rule record                           |
| A-2: rewrite existing rule | `authoring_obligations.explanatory-must-not-permitted` | change statement + verification fields only |
| B: confirmation only       | none                                                   | no change                                   |

## 6. Final policy on application strength

**Apply Medium strength as MUST (enforced).**

Concrete application rules (see deontic-operator decision procedure in Section 2.3):

- For rule records whose deontic operator in `statement` is **MUST NOT**: must be placed in `prohibitions.items` (MUST).
- For rule records whose deontic operator is not MUST NOT: no move into `prohibitions` is required (MUST NOT occurrences by other means are permitted).
- For MUST NOTs in fields outside rule records: permitted (within the scope of `explanatory-must-not-permitted`).

**Reasons for not adopting Strict strength** (all-agent agreement):

- Moving all explanatory MUST NOTs into `prohibitions` would require promoting them into rule records, greatly inflating structure.
- From Semantic Gravity Wells, inflating MUST NOT records increases priming risk.
- Medium achieves most of the adherence benefit.

## 7. Execution plan

### 7.1 Phase 1: restore meta-circular compliance (the core of this task)

| Tier                                  | Content                                                                                                                                                               |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0 (structure check)**          | Enumerate all rule records in SKILL.md and update the confirmed-violation list in Sections 3.2–3.4 to the latest state.                                               |
| **Tier 1 (apply changes)**            | Apply Change A (add A-1 + rewrite A-2).                                                                                                                               |
| **Tier 2 (objective verification)**   | Run YAML parse validation, structure validation, compliance checks for `prohibitions-dedicated-section` and `one-obligation-per-rule`, and rule-record schema checks. |
| **Tier 3 (subjective quality check)** | Human review to confirm the post-change wording preserves intent.                                                                                                     |

### 7.2 Phase 2: move the `prohibitions` section earlier (separate task)

As auxiliary reinforcement for lost-in-the-middle mitigation, move the `prohibitions` section within the YAML block to immediately after `interpretation` and `precedence_and_conflict` (adopting the Composer proposal and explicitly making it a Phase).

- This is a large structural change and is treated as a separate task after Phase 1 completes.
- Based on Semantic Gravity Wells, evaluate the effect of moving as auxiliary; it is important to pair it with strengthened ex post verification (verification methods).

### 7.3 Phase 3: strengthen verification methods (separate task; recommended)

Based on the Codex proposal, consider adding the following verification methods:

| Candidate verification method   | Purpose                                                             |
| ------------------------------- | ------------------------------------------------------------------- |
| `must-not-locality-validation`  | Confirm that prohibitions do not exist outside `prohibitions.items` |
| `one-modal-per-rule-validation` | Check one rule, one modal (ban compound predicates)                 |

These are not acceptance conditions for Phase 1, but they are effective for preventing recurrence of meta-circular violations.

Optional follow-on acceptance criteria (Phase 2/3, if executed):

- Phase 2: `prohibitions` appears immediately after `interpretation` and `precedence_and_conflict` within the YAML block, without changing rule semantics.
- Phase 3: The verification methods chosen are documented and runnable (even if initially as a checklist), and failures are treated as plan regressions.

### 7.4 Acceptance criteria (Phase 1)

- For all rule records outside `prohibitions.items`, the deontic operator of `statement` is not MUST NOT.
- The YAML parses successfully with a standard parser.
- The rule-record schema (`id, layer, priority, statement, conditions, exceptions, verification`) is maintained for all rules.
- There is no semantic contradiction between `explanatory-must-not-permitted` and `no-treat-explanatory-must-not-as-prohibition`.

## 8. Unresolved / items for continued consideration

1. **Making `definitions.tier-separation` a normative prohibition**: treat it as permitted explanatory use for now, but keep as a future candidate task to add `no-interleave-tiers` under prohibitions and reference it from definitions.

2. **Rollout to other AI directive files**: in this repository there is currently only one skill file under `.agents/skills/`. If the number of files increases, decide whether to apply the same Medium strength (including the deontic-operator decision procedure) or unify via references (id/link) to the authoring skill.

3. **Concrete mitigation measures for Semantic Gravity Wells**: consider as a separate task adding specific guidelines for AI directive file writing style to reduce priming risk (e.g., “describe desired states positively instead of directly naming prohibited targets”).

4. **Linting the deontic-operator decision procedure**: implement the procedure in Section 2.3 as a mechanically executable linter to improve satisfaction of `verification-machine-checkable`. Consider the `statement_modal` field proposal alongside.

5. **Guidelines for using MUST NOT in explanatory prose**: regarding the side effects of actively using MUST NOT in explanatory text (Codex), consider whether to shift toward “permit only when necessary (SHOULD NOT habitual use)”. At present, `explanatory-must-not-for-clarity` recommends it with SHOULD, so lowering the strength of that recommendation is a discussion point.

## Addendum: Decision on “Unresolved / items for continued consideration” (Interim Hold)

To unblock adoption and avoid an extended “under review / not referencable” state, we are making an interim decision to **hold** the unresolved items and proceed with a stable, usable plan. The following choices define the current direction until a later review is explicitly scheduled.

### 1) Promote `definitions.tier-separation` to a normative prohibition?

**Decision:** Hold; **keep as explanatory only (no promotion)**.  
We will maintain the current placement and semantics: tier separation remains explanatory guidance and is not elevated into `prohibitions.items` at this time.

### 2) Scaling policy across additional AI directive files

**Decision:** Hold; choose **reference unification**: treat the **authoring skill as the single source of truth**.  
If/when additional directive files are introduced, they should reference the authoring skill rather than duplicating the full policy text, to minimize drift and ensure consistent enforcement posture.

### 3) “Semantic Gravity Wells” mitigations as concrete authoring guidelines

**Decision:** Hold; **defer**.  
We will not add additional prescriptive writing-style guidelines for this concern in the current iteration. This may be revisited after initial adoption, once we have evidence of recurring failure modes.

### 4) Make the deontic-operator classification procedure (Section 2.3) machine-checkable (linter)

**Decision:** Hold; pursue **staged introduction**, starting with **lightweight checks**.  
Initial verification should emphasize high-signal structural checks (e.g., locality and placement constraints for normative MUST NOT rules). More advanced semantic checks may be added later, based on observed needs and acceptable false-positive rates.

### 5) Policy for using MUST NOT in explanatory prose

**Decision:** Hold; **keep current stance (clarity first)**.  
We will continue to allow explanatory MUST NOT phrasing when it materially improves clarity, while relying on classification/placement rules to prevent such text from being treated as normative prohibitions.

**Note:** This addendum intentionally prioritizes “plan usability and referencability” over further debate. Any changes to these interim decisions should be made via an explicit revision and re-review of this section.
