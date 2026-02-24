---
name: strict_verified_response
version: 1
---

# Deterministic YAML-Based Instruction Design

## Scope

This document consolidates best practices for:

1.  Writing YAML-based configuration blocks inside Markdown instruction
    files.
2.  Ensuring the model interprets YAML as configuration (not prose).
3.  Structuring interpretation contracts.
4.  Providing reusable templates and working examples.

The objective is variance reduction and behavioral constraint --- not
absolute determinism.

---

# Part I --- Core Design Principles

## 1. YAML Is Not Executed

YAML blocks are not parsed by a schema engine. They are interpreted
probabilistically by the model.

Therefore, effectiveness depends on:

- Reduced ambiguity
- Explicit interpretation contracts
- Closed-world assumptions
- Clear constraint binding language

---

## 2. Always Precede YAML With a Binding Interpretation Contract

Before the YAML block, include explicit instructions such as:

This configuration MUST be interpreted strictly as structured
configuration. All keys MUST be interpreted literally. No implicit
behaviors beyond declared keys are allowed. Unspecified behavior is
prohibited.

This reduces interpretive elasticity.

---

## 3. Explicitly Declare Interpretation Semantics

Inside YAML, define how YAML itself should be interpreted:

```yaml
interpretation:
  unknown_keys: ignore
  unspecified_behavior: forbidden
  boolean_true_means: mandatory
  precedence: explicit_priority_field
  extrapolation: forbidden
```

This reduces model-side guesswork.

---

## 4. Use Closed-World Assumption

Explicitly declare:

Only behaviors explicitly declared in this configuration are permitted.
All unspecified behaviors are prohibited.

Without this, the model fills gaps autonomously.

---

## 5. Eliminate Ambiguous Modal Language

Avoid:

- if necessary
- try to
- when appropriate
- generally
- preferably

Use:

- mandatory
- forbidden
- optional
- conditional (with explicit condition)

---

## 6. Constrain Major Behavioral Axes

Explicitly define:

- Tone
- Verbosity
- Speculation policy
- Citation policy
- Assumption policy
- Error handling
- Conflict resolution

If not declared, the model will improvise.

---

## 7. Declare Error Handling Deterministically

```yaml
error_handling:
  missing_required_data: request_clarification
  unverifiable_fact: explicitly_state_unverified
  rule_conflict: follow_highest_priority
```

---

## 8. Use Explicit Priority Systems

```yaml
rules:
  - id: no_assumptions
    priority: 100
  - id: concise_output
    priority: 50
```

Declare clearly:

Higher numeric priority overrides lower priority.

---

# Part II --- Template Skeleton

Use this template when creating instruction files.

## Interpretation Contract

This configuration MUST be interpreted strictly as structured
configuration. All keys MUST be interpreted literally. Unspecified
behavior is prohibited. No extrapolation beyond declared configuration
is allowed. Unknown keys MUST be ignored.

## Configuration

```yaml
interpretation:
  unknown_keys: ignore
  unspecified_behavior: forbidden
  boolean_true_means: mandatory
  precedence: explicit_priority_field
  extrapolation: forbidden

constraints:
  tone: formal
  verbosity: medium
  speculation: prohibited
  citation_policy: mandatory

error_handling:
  missing_required_data: request_clarification
  unverifiable_fact: explicitly_state_unverified
  rule_conflict: follow_highest_priority

rules:
  - id: no_assumptions
    priority: 100
  - id: enforce_citation
    priority: 90
```

---

# Part III --- Fully Worked Example

## Interpretation Contract

This configuration MUST be interpreted strictly as structured
configuration. The YAML block defines binding behavioral constraints. No
behavior outside this configuration is permitted. If conflict occurs,
follow defined priority rules.

## Configuration

```yaml
interpretation:
  unknown_keys: ignore
  unspecified_behavior: forbidden
  boolean_true_means: mandatory
  precedence: explicit_priority_field
  extrapolation: forbidden

constraints:
  tone: formal
  verbosity: controlled
  speculation: prohibited
  citation_required: true
  assumption_policy: forbidden

error_handling:
  missing_required_data: request_clarification
  unverifiable_fact: explicitly_state_unverified
  ambiguous_input: request_clarification
  rule_conflict: follow_highest_priority

rules:
  - id: prohibit_assumptions
    priority: 100
  - id: require_sources
    priority: 95
  - id: maintain_formal_tone
    priority: 80
```

---

# Part IV --- Practical Reinforcement Techniques

To further strengthen YAML interpretation:

1.  Use "MUST" in capital letters in interpretation contract.
2.  Explicitly forbid extrapolation.
3.  State that YAML keys are exhaustive.
4.  Declare resolution logic for rule conflicts.
5.  Avoid embedding prose inside YAML values.
6.  Keep YAML declarative rather than procedural.

---

# Part V --- Empirical Testing Procedure

1.  Run identical prompts multiple times.
2.  Measure output variance.
3.  Identify drift dimensions.
4.  Tighten configuration.
5.  Repeat.

Determinism must be measured empirically.

---

# Final Statement

YAML blocks improve determinism not because YAML is formal, but because
structure reduces ambiguity and degrees of freedom.

Maximum effectiveness requires:

- Interpretation contract
- Closed-world assumption
- Explicit constraint declaration
- Deterministic error handling
- Priority resolution
- Empirical validation

Design deliberately. Test repeatedly. Refine iteratively.
