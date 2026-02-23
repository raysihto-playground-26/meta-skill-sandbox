# Plan r1: P1 and P2 Gap Remediation for AI Directive Authoring Skill

Target file:
- .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md

Primary source:
- docs/.tmp/report_p1_p2_gap_analysis.md

## 1. Purpose

This plan defines how to resolve the two reported gaps:
- P1: Conflict Resolution Ambiguity
- P2: Condition Identifier Vocabulary

The objective is to make conflict handling and condition matching deterministic and verifiable.

## 2. Scope and constraints

- This is a planning document only.
- Concrete edits to AI directive files are out of scope in this task.
- The plan content is based on the reported P1 and P2 findings and their As-Is, To-Be, and Gap definitions.
- The plan must remain self-contained.

## 3. Problem summary

### 3.1 P1: Conflict Resolution Ambiguity

As-Is:
- `interpretation.priority` states that within the same layer, higher numeric priority wins.
- `precedence_and_conflict.conflict_policy.MUST_vs_MUST` states: halt or request clarification, and must not silently choose one.
- For two MUST rules in the same layer with different priorities, these statements conflict.

To-Be:
1. Different layers: resolve by layer order.
2. Same layer, different priority: resolve by numeric priority.
3. Same layer, same priority: apply conflict policy (MUST vs MUST -> halt or request clarification).

Gap:
- The applicability condition of `MUST_vs_MUST` is not constrained to unresolved tie cases.
- The relationship between priority resolution and conflict policy is not explicit.

### 3.2 P2: Condition Identifier Vocabulary

As-Is:
- `interpretation.compound_conditions` requires identifiers in conditions to be defined in the file or in definitions.
- Multiple identifiers used in `conditions` are not defined.
- Token forms are inconsistent (space-separated identifiers in conditions vs hyphenated identifiers in definitions).

To-Be:
1. Every identifier used in conditions is defined.
2. Condition tokens and definition keys match in one canonical form.
3. Runner and linter can validate conditions against definitions deterministically.

Gap:
- Undefined identifiers violate the stated MUST requirement.
- Token mismatch prevents mechanical lookup and validation.

## 4. Remediation plan

### Phase 0: Baseline inventory

1. Enumerate all identifiers used in all `conditions` fields.
2. Enumerate all existing keys in `definitions` (or equivalent identifier registry section if adopted).
3. Build a one-to-one mapping table:
   - used identifier
   - defined identifier
   - status: exact match, alias only, or missing

Exit condition:
- A complete inventory exists for all condition identifiers.

### Phase 1: Resolve P1 determinism

1. Define one explicit decision order for conflicts:
   - layer comparison first
   - priority comparison second
   - conflict policy only when still unresolved
2. Constrain `MUST_vs_MUST` applicability to unresolved conflicts after layer and priority comparison.
3. Align `interpretation.priority` and `precedence_and_conflict.conflict_policy` wording so no contradictory behavior remains.

Exit condition:
- A single deterministic path exists for every rule conflict case.

### Phase 2: Resolve P2 identifier consistency

1. Define all currently used condition identifiers in one authoritative location (`definitions` or an equivalent dedicated section).
2. Select one canonical token form for identifiers and apply it consistently.
3. Update all `conditions` values so every token exactly matches a defined identifier.
4. Ensure each compound condition of the form `A and B` uses only defined identifiers for both A and B.

Exit condition:
- Every condition token is defined and exact-match resolvable.

### Phase 3: Verification alignment

1. Add or update verification steps so they can check:
   - identifier existence
   - exact token matching between conditions and definitions
   - compound part validity for `A and B`
2. Ensure the verification description remains deterministic and executable by runner or linter.

Exit condition:
- The file includes verification logic that can detect regressions for P1 and P2.

## 5. Acceptance criteria

- AC1: No contradiction remains between priority resolution and MUST-vs-MUST conflict handling.
- AC2: Conflict handling order is explicit and deterministic.
- AC3: All identifiers used by conditions are defined in the file.
- AC4: Condition tokens and definition keys use one canonical and exact-matchable form.
- AC5: Compound conditions are fully resolvable from defined identifiers.
- AC6: Verification can mechanically detect violations of AC1 through AC5.

## 6. Risks and controls

Risk 1:
- Partial normalization can leave mixed token forms.
Control:
- Use the inventory mapping from Phase 0 as mandatory completion evidence.

Risk 2:
- P1 wording can still be interpreted as dual authority.
Control:
- Keep one explicit conflict decision sequence and state when conflict policy is entered.

Risk 3:
- Future rule additions can reintroduce undefined identifiers.
Control:
- Keep identifier existence checks in verification methods.

## 7. Deliverable from this plan

- A follow-up implementation change set to the target file that applies Phases 1 to 3 and satisfies AC1 through AC6.
