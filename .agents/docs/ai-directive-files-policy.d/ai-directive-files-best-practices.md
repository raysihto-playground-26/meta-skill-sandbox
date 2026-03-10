# Best Practices for AI Instruction File Sets

## Goal: Certainty First, Efficiency Second

### Core Axes: English x Spec-style x Structured x Atomic x Priority-defined

---

## 0. Non-negotiable Principles

### 0.1 Priority Order

- **MUST** define a global precedence order and keep it stable:
  - **L0 (Constitution / Safety / Prohibitions)**
  - **L1 (Role & Success Criteria)**
  - **L2 (Process & Verification)**
  - **L3 (Output Style)**
  - **L4 (Task Playbooks / Recipes)**

### 0.2 Conflict Policy

- **MUST** define deterministic conflict resolution:
  - **MUST vs MUST**: **MUST halt** (or request clarification) and **MUST NOT guess**
  - **MUST vs SHOULD**: MUST wins
  - **SHOULD vs SHOULD**: higher `priority` wins; if equal, more specific rule wins
- **MUST** define "specificity" tie-breaker (recommended):
  - Task-specific > domain-specific > general
  - Conditional rule > unconditional rule
  - Rule with explicit constraints > vague rule

### 0.3 No Assumptions

- **MUST NOT** invent missing facts, sources, citations, requirements, or constraints.
- If required information is missing, **MUST**:
  - state uncertainty explicitly, and
  - list missing inputs as a short, structured checklist.

---

## 1. Language & Style: English x Spec-style

### 1.0 Language

- **MUST** write all AI directive files in English.
- English maximizes interpretation stability across LLM architectures and training distributions.
- **MUST NOT** mix languages within a single directive file.

### 1.1 Normative Keywords

- **MUST** use RFC-style normative keywords consistently:
  - MUST / MUST NOT / SHOULD / SHOULD NOT / MAY
- **MUST NOT** use ambiguous modals (e.g., "try to", "as needed", "when appropriate") without a definition.

### 1.2 Spec-style Sentence Form

- **MUST** write rules using canonical patterns:
  - `MUST <verb phrase>.`
  - `IF <condition> THEN MUST <verb phrase>.`
  - `UNLESS <exception> THEN MUST <verb phrase>.`
- **SHOULD** keep each statement <= 1 sentence and <= 25 words.

### 1.3 Definitions

- **MUST** include a Definitions section for non-obvious terms:
  - "verified", "authoritative source", "uncertainty statement", "conflict", etc.
- **SHOULD** define measurable thresholds (counts, length caps, mandatory fields).

---

## 2. Structure: Structured-first

### 2.1 Rule Record Format

- **MUST** represent every enforceable rule as a structured record with fixed fields.

**Recommended minimal schema**

- `id` (stable, unique)
- `layer` (L0-L4)
- `priority` (P0/P1/P2 or high/normal/low)
- `statement` (single normative sentence)
- `conditions` (optional, explicit)
- `exceptions` (optional, explicit)
- `verification` (how to check compliance)
- `rationale` (brief, optional but recommended)
- `examples` (optional; keep minimal)

### 2.2 File Header Metadata

- **MUST** put the following at top of each file:
  - `Layer`, `Scope`

### 2.3 One Source of Truth

- **MUST** avoid duplicating the same rule across multiple files.
- If a lower layer needs it, **MUST** reference by `id` (do not rewrite).

---

## 3. Atomicity: One rule, one obligation

### 3.1 Atomic Rules

- **MUST** enforce "one rule, one obligation/prohibition".
- **MUST NOT** bundle multiple obligations in a single statement.

Bad:

- `MUST do A and B; if C then do D.`
  Good:
- `R-001: MUST do A.`
- `R-002: MUST do B.`
- `R-003: IF C THEN MUST do D.`

### 3.2 Orthogonality

- **SHOULD** split rules by concern:
  - content correctness vs style vs safety vs process
- **MUST** ensure a single failure maps to a small number of rule IDs.

---

## 4. Priority-defined: Explicit precedence at every level

### 4.1 Layer + Priority

- **MUST** define precedence as:
  1. higher layer wins (L0 highest)
  2. within same layer, higher `priority` wins
  3. if tie, more specific wins
  4. if still tie, halt / request clarification

### 4.2 Prohibitions Isolation

- **MUST** keep all prohibitions in L0, in a dedicated "PROHIBITIONS" section.
- **MUST** ensure prohibitions override all other rules.

---

## 5. Conditions & Exceptions: Make boundaries computable

### 5.1 Conditions as Enumerations

- **MUST** specify conditions as explicit triggers, not prose.

Example:

- `conditions: user_requests_sources OR claim_is_time_sensitive OR high_stakes_domain`

### 5.2 Exceptions are first-class

- **MUST** define exceptions explicitly.
- **MUST NOT** imply exceptions via vague language ("unless necessary").

### 5.3 Degradation Policy

- **MUST** define fallback behavior:
  - missing info -> state uncertainty + list required inputs
  - conflict -> halt/clarify; do not guess
  - tool unavailable -> state limitation; provide bounded alternative only if permitted

---

## 6. Verification: Make compliance checkable

### 6.1 Rule-level Verification

- **MUST** include `verification` for every **MUST/MUST NOT** rule.
- Verification statements **SHOULD** be objective:
  - "Output includes X"
  - "Output does not contain Y"
  - "Output length <= N"
  - "Contains citations for each non-common factual claim"

### 6.2 Internal Self-check

- **MUST** require an internal pre-output compliance check against all applicable MUST/MUST NOT rules.
- **MUST NOT** print full checklists by default (unless requested); keep checks internal.

---

## 7. Testing: Evidence of certainty

### 7.1 Minimal Test Suite

- **MUST** maintain:
  - **Golden tests** (typical use)
  - **Adversarial tests** (prohibited requests, prompt injection)
  - **Missing-info tests** (forcing uncertainty behavior)
  - **Conflict tests** (contradictory instructions)

### 7.2 Traceability

- **MUST** map each test case to the rule IDs it validates.
- **SHOULD** track regressions by rule ID and date.

---

## 8. Efficiency (Second Priority): Reduce change cost without harming certainty

### 8.1 "Constitution + Recipes" Architecture

- **MUST** keep L0-L2 short, stable, and reviewable (the "Constitution").
- **SHOULD** put volatile, task-specific details into L4 playbooks.

### 8.2 Change Management

- **MUST** use stable rule IDs; never reuse IDs.
- **MUST** deprecate before removal:
  - `status: deprecated` -> later remove after tests updated
- **SHOULD** require PR template fields:
  - impacted rule IDs, rationale, tests updated, backward-compat notes

### 8.3 Linting / Automation

- **SHOULD** implement a simple linter that checks:
  - missing fields (id/layer/priority/statement/verification)
  - duplicate IDs
  - ambiguous words blacklist (e.g., "appropriate", "as needed")
  - multi-obligation statements (heuristic)
  - missing conflict policy reference

---

## 9. Practical Templates

### 9.1 File Template (Markdown)

- **MUST** follow this skeleton:

- Title
- Layer / Scope
- Definitions
- Priority & Conflict Policy (reference to L0)
- Rules (records)
- Exceptions (if not inline)
- Verification Notes

### 9.2 Rule Template (YAML-like block inside Markdown)

```yaml
id: R-L0-001
layer: L0
priority: P0
statement: MUST NOT assert unverified facts.
conditions: always
exceptions: none
verification: For any uncertain claim, output includes an explicit uncertainty statement.
rationale: Prevents hallucinated claims and preserves trust.
examples:
  - "I could not verify X from authoritative sources."
```

---

## 10. "Certainty-first" Checklist

- [ ] Global precedence + conflict policy is defined and referenced everywhere.
- [ ] Every MUST/MUST NOT rule is atomic and has verification criteria.
- [ ] Prohibitions are isolated in L0 and override all other layers.
- [ ] Conditions/exceptions are explicit enumerations, not prose.
- [ ] Missing-info behavior forbids guessing and requires explicit uncertainty.
- [ ] Minimal test suite exists and maps to rule IDs.
- [ ] Efficiency measures (DRY, recipes, lint) do not weaken the above.

---
