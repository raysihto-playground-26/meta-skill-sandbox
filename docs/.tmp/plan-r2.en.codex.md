# Integrated Plan R2 (rev2): Remediation of P1 and P2 for AI Directive Authoring Skill

## 0. Scope and hard constraints

Target file for follow-up implementation:
- .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md

Input basis used to build this integrated plan:
- docs/.tmp/report_p1_p2_gap_analysis.md
- docs/.tmp/plan-r1.en.claude.md
- docs/.tmp/plan-r1.en.codex.md
- docs/.tmp/plan-r1.en.copilot.md
- docs/.tmp/plan-r1.en.cursor.md
- docs/.tmp/plan-r1.en.gpt.md

Hard constraints for this planning artifact:
- This file is a plan only. It MUST NOT perform concrete edits.
- The follow-up implementation MUST edit SKILL.md to resolve P1 and P2.
- The plan MUST stay self-contained and use only repository-grounded facts from the inputs above.
- The plan MUST prioritize machine interpretation by AI agents over human-oriented prose style.
- The plan MUST minimize the number of impacted rules while maximizing closure of reported gaps.

## 1. Unified problem statement

P1 (critical):
- interpretation.priority says same-layer conflicts are resolved by higher numeric priority.
- precedence_and_conflict.conflict_policy.MUST_vs_MUST says halt or request clarification.
- Without a tie condition boundary, MUST-vs-MUST behavior is ambiguous for same-layer different-priority conflicts.

P2 (high):
- interpretation.compound_conditions requires identifiers in conditions to be defined in-file or in definitions.
- Conditions use identifiers that are missing from definitions.
- Conditions also use tokens that do not string-match existing definition keys (space form vs hyphen form).
- Result: deterministic machine resolution is not guaranteed.

## 2. Four-plan unanimous requirements (MUST)

The following were consistent across the four non-gpt r1 plans and are therefore mandatory:

1) P1 determinism MUST be explicit.
- Conflict resolution order MUST be:
  - layer precedence first,
  - numeric priority second,
  - conflict_policy only when still unresolved.
- MUST_vs_MUST halt behavior MUST be scoped to the unresolved tie case.

2) P2 vocabulary closure MUST be complete.
- Every identifier used in any conditions entry MUST be defined in an authoritative in-file registry.
- Compound conditions of the form "A and B" MUST resolve both A and B deterministically.

3) Token matching MUST be exact for machine use.
- Conditions tokens and authoritative identifiers MUST support exact machine matching in this revision.
- Space-vs-hyphen mismatch MUST be removed as an ambiguity source.

4) Validation MUST be machine oriented.
- Acceptance checks MUST be executable by an AI agent via contextual parsing steps, not dependent on human-only interpretation.

5) Scope control MUST be preserved.
- Changes MUST target P1 and P2 only.
- Unrelated rule semantics MUST NOT be changed.

## 3. Integrated strategy (best-of-five under constraints)

### 3.1 P1 remediation strategy (MUST)

MUST changes:
- Rewrite conflict_policy.MUST_vs_MUST intent so it applies only when layer and priority cannot resolve a conflict.
- Align interpretation.priority wording so precedence between priority resolution and conflict policy is explicit.

MUST preserve:
- Existing behavior for same-layer same-priority MUST-vs-MUST remains halt or clarification.
- Existing MUST_vs_SHOULD and prohibition override semantics remain unchanged.

Expected effect:
- A single deterministic decision path exists for all P1 conflict cases.

### 3.2 P2 remediation strategy (MUST with minimal-impact rule)

MUST outcomes:
- All currently used condition identifiers become defined and resolvable in-file.
- Compound condition decomposition yields only resolvable identifiers.
- Space-vs-hyphen mismatch no longer blocks machine resolution.

Minimum-impact execution rule:
- Select the canonical identifier set that resolves P2 while touching the fewest rule records.
- In this repository state, most conditions already use phrase-style tokens; therefore registry-side closure is the first-choice path unless it fails a mandatory acceptance criterion.

Required vocabulary coverage (identifiers explicitly called out by the report):
- creating AI directive file
- editing AI directive file
- creating AI directive file that contains YAML block
- editing AI directive file that contains YAML block
- scope high-stakes
- scope multi-constraint
- scope long-form reasoning

Mandatory governance additions:
- Add one authoritative condition identifier policy statement to interpretation so future additions are deterministic.
- Define explicit handling for any alias or alternate token forms if retained for compatibility.
- If aliases are retained, alias resolution MUST be finite, one-step, and deterministic.

Note on integrating the gpt plan:
- Runner-only remediation without SKILL.md edits is rejected.
- Only the gpt plan elements that improve deterministic machine verification are adopted, and only as support for SKILL.md-centered remediation.

## 4. Change budget and blast-radius control

Mandatory change classes:
- P1 text-level semantic alignment in interpretation and conflict policy keys.
- P2 identifier registry closure for all used tokens.
- P2 policy clarification for machine resolution of simple and compound conditions.

Blast-radius guardrails:
- Do not change layer values, numeric priorities, rule ids, or section topology unless required to satisfy P1 or P2 acceptance.
- Do not rewrite normative intent of unrelated prohibitions or obligations.
- Prefer registry and policy corrections over broad multi-rule rewrites when both satisfy all mandatory acceptance checks.

## 5. AI-agent executable verification plan (MUST)

The following checks are required and are designed for execution by an AI agent during context analysis:

P1 checks:
1) Trace three conflict cases and verify one outcome each:
   - different layer,
   - same layer different priority,
   - same layer same priority.
2) Confirm MUST_vs_MUST halt is reachable only in the unresolved tie case.
3) Confirm no text-level contradiction remains between interpretation.priority and conflict policy.

P2 checks:
1) Extract all conditions entries from all rule records.
2) For each entry:
   - if simple token, resolve directly against the authoritative identifier registry,
   - if "A and B", split on literal " and " and resolve both parts.
3) Verify zero unresolved tokens after applying the documented deterministic alias rule (if aliasing exists).
4) Confirm all report-listed problematic identifiers are now resolvable.
5) Confirm no space-vs-hyphen mismatch remains as an unresolved state.

Structural checks:
1) Confirm YAML remains parseable by standard YAML parsing.
2) Confirm rule-record schema shape remains intact.
3) Confirm no unintended edits outside P1/P2 target areas.

## 6. Acceptance criteria (MUST)

AC-P1-1:
- Conflict resolution is deterministic via layer, then priority, then conflict policy for unresolved ties.

AC-P1-2:
- MUST_vs_MUST applies only when layer and priority are both non-distinguishing.

AC-P1-3:
- interpretation.priority and conflict policy are mutually consistent for all layer/priority combinations.

AC-P2-1:
- Every identifier used by conditions is defined in-file in an authoritative registry.

AC-P2-2:
- Every compound condition resolves all component identifiers deterministically.

AC-P2-3:
- Previously reported undefined or mismatched identifiers are all resolvable.

AC-P2-4:
- Machine-executable validation steps can detect regressions in P1 and P2.

AC-SCOPE-1:
- The implementation modifies SKILL.md to fix P1/P2 and does not rely on runner-only workaround.

AC-SCOPE-2:
- Changes are minimal relative to affected rule count and preserve unrelated semantics.

## 7. Execution order (tiered)

Tier 0: Baseline capture
- Confirm current P1 contradiction and P2 unresolved vocabulary list from SKILL.md.

Tier 1: Apply P1 edits
- Apply conflict resolution wording alignment.

Tier 2: Validate P1
- Run P1 checks in Section 5.

Tier 3: Apply P2 edits
- Apply identifier registry closure and identifier policy updates using minimum-impact rule.

Tier 4: Validate P2
- Run P2 and structural checks in Section 5.

Tier 5: Final scope confirmation
- Confirm all acceptance criteria pass and no out-of-scope drift occurred.

## 8. Explicit non-adopted direction

The following direction is explicitly out of scope for follow-up implementation:
- Any plan that resolves P1/P2 only in runner or linter behavior while leaving SKILL.md uncorrected.

This integrated plan requires SKILL.md remediation as the primary and mandatory path.
