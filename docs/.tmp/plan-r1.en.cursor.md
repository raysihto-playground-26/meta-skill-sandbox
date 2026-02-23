# Plan R1: Resolving P1 and P2 Gap Analysis Issues

This document is a remediation plan for the issues identified in
`docs/.tmp/report_p1_p2_gap_analysis.md`. The target file of the report is
`.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`.

---

## 1. Summary of Issues

The gap analysis report identifies two root causes of internal inconsistency
in the AI directive files authoring specification:

| ID  | Issue                                         | Severity | As-Is                          | To-Be                            |
|-----|-----------------------------------------------|----------|--------------------------------|----------------------------------|
| P1  | Priority resolution vs conflict policy clash | Critical | Conflict resolution undefined  | Deterministic resolution         |
| P2  | Condition identifier vocabulary + mismatch   | High     | MUST self-violation + no match | All identifiers defined, matchable |

---

## 2. P1: Conflict Resolution Ambiguity

### 2.1 Problem

Two specifications contradict each other:

- **interpretation.priority** (L24): Within the same layer, the rule with the
  higher numeric priority wins.

- **precedence_and_conflict.conflict_policy.MUST_vs_MUST** (L30): Halt or
  request clarification; MUST NOT silently choose one.

When two MUST rules in the same layer (e.g. L2) have different priorities
(e.g. 98 vs 95), the runner cannot determine whether to apply the higher
priority rule or halt. Resolution is non-deterministic.

### 2.2 Resolution Strategy

Clarify the applicability of each mechanism so they do not overlap:

1. **Layer differs**: Resolve by layer precedence (L0 > L1 > ... > L4).

2. **Same layer, different priority**: Resolve by numeric priority (higher wins).
   Conflict policy does not apply in this case.

3. **Same layer, same priority**: Apply conflict policy. For MUST vs MUST, halt
   or request clarification.

The specification must state explicitly that:

- Priority resolution (layer + numeric priority) takes precedence over conflict
  policy.

- MUST_vs_MUST applies only when layer and priority are equal and resolution
  by priority is impossible.

### 2.3 Required Specification Updates

- Revise `interpretation.priority` to state that conflict policy applies only
  when layer and priority are equal.

- Revise `precedence_and_conflict.conflict_policy.MUST_vs_MUST` to state that
  it applies when two MUST rules have identical layer and priority (or when
  priority resolution cannot distinguish them).

- Optionally add a stepwise conflict-resolution algorithm that runs:
  (1) layer order, (2) numeric priority, (3) conflict policy for ties.

---

## 3. P2: Condition Identifier Vocabulary

### 3.1 Problem

The specification requires (compound_conditions, L22) that identifiers in
conditions MUST be defined in the file or in definitions. The file violates
this requirement in two ways:

**Problem A: Undefined identifiers**

Identifiers used in `conditions` but not defined in `definitions`:

| Identifier                                      | Usage (example)                    | In definitions |
|------------------------------------------------|------------------------------------|----------------|
| creating AI directive file                     | Most rules' conditions             | No             |
| editing AI directive file                      | Most rules' conditions             | No             |
| scope high-stakes                              | tier-separation rules              | No             |
| scope multi-constraint                         | tier-separation rules              | No             |
| scope long-form reasoning                      | tier-separation rules              | No             |
| creating AI directive file that contains YAML block | yaml-include-* rules        | No             |
| editing AI directive file that contains YAML block  | yaml-include-* rules         | No             |

**Problem B: Token form mismatch**

Conditions use space-separated tokens (e.g. "scope high-stakes") while
definitions use hyphen-separated keys (e.g. "scope-high-stakes"). These are
different YAML strings; mechanical matching fails.

### 3.2 Resolution Strategy

1. **Define all trigger and scope identifiers** in `definitions` (or an
   equivalent section such as `triggers`).

2. **Unify token form** so that the strings used in `conditions` exactly match
   the keys in definitions. Choose one canonical form (e.g. hyphen-separated)
   and use it consistently.

### 3.3 Required Specification Updates

- Add definitions for:
  - creating AI directive file
  - editing AI directive file
  - creating AI directive file that contains YAML block
  - editing AI directive file that contains YAML block

- Align scope identifiers: either
  - (a) use hyphen form in conditions (scope-high-stakes, scope-multi-constraint,
    scope-long-form-reasoning) to match existing definitions, or
  - (b) add definitions for the space form and standardize on that form.

- Ensure every identifier used in any `conditions` array appears under
  `definitions` (or an equivalent) with the exact same string.

---

## 4. Implementation Order

| Step | Issue | Action                                          |
|------|-------|-------------------------------------------------|
| 1    | P1    | Resolve priority vs conflict_policy semantics   |
| 2    | P2    | Add missing trigger and scope definitions       |
| 3    | P2    | Unify token form across conditions and definitions |
| 4    | Both  | Validate that all conditions reference defined identifiers |
| 5    | Both  | Validate conflict resolution is deterministic    |

---

## 5. Success Criteria

- **P1**: No contradiction between interpretation.priority and MUST_vs_MUST.
  The runner can deterministically resolve conflicts using layer, then
  priority, then conflict policy for ties.

- **P2**: Every identifier in any `conditions` entry is defined in the file
  with an exact string match. A linter or runner can mechanically validate
  conditions against definitions.

---

## 6. References

Source document: `docs/.tmp/report_p1_p2_gap_analysis.md`

Target file: `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`
