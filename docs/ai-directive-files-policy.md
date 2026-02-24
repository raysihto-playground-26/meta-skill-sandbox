# AI Directive Files Policy

This document is the canonical policy for AI directive files in this repository.
It optimizes for: maximize instruction adherence stability with minimal context.

This guide intentionally does not pursue "complete coverage" or "zero ambiguity"
through exhaustive definitions and checklists. It prioritizes practical
robustness under LLM non-determinism.

## Essence (non-negotiable direction)

"Design toward a system where only the highest-impact instructions are
transmitted reliably, at minimal cost (minimal context)."

Therefore:

- Prefer constraint density over completeness.
- Reduce context bloat to reduce "skipping important instructions".
- Do not lose the "must not miss" constraints.

Human readability and maintainability are secondary objectives.
Do not increase context size for readability unless it reduces the probability of instruction failure.

**Lean and mean is the default:** omit anything that is obvious or safely implicit, but do not omit anything whose absence would predictably cause failures.

## Status and Precedence

This document is the golden policy for AI directive files in this repository.
All other documents are advisory references unless this policy explicitly adopts specific parts.
If any guidance conflicts, this policy wins.
When trade-offs are unclear, prefer the option that maximizes adherence stability with minimal context, preserving non-negotiable constraints.

## Scope

This guide applies to:

- AI directive files (instruction files intended to constrain model behavior).
- How we structure, compress, and validate instructions for reliability.

This guide does not prescribe:

- A universal taxonomy for every project.
- Exhaustive definitions for obvious words.
- A mandatory, verbose "verify everything" doctrine.

## The core mental model

- LLMs are probabilistic. "Perfect compliance" is not the goal.
- Treat the model as a candidate generator, not a governor.
- Reliability comes from structure, prioritization, and external validation when
  worth the cost.

## Canonical structure for AI directive files (MUST)

AI directive files MUST follow this exact structure:

1. YAML frontmatter
2. A single YAML code block
3. Nothing else (no prose, no extra code blocks)

Example skeleton:

````markdown
---
name: example-directive
description: An example directive file with the canonical structure.
---

```yaml
interpretation:
  unknown_keys: ignore
  unspecified_behavior: forbidden
  extrapolation: forbidden
  precedence: explicit_priority_field

rules:
  - xxx
```
````

Rationale:

- The file becomes a compact, parseable "contract" for both humans and models.
- It prevents accidental dilution by narrative text.

## Interpretation contract placement (MUST)

Some references recommend placing a binding interpretation contract as prose
before the YAML block.

This repository MUST NOT do that, because AI directive files MUST contain no
prose outside frontmatter and the single YAML block.

Therefore:

- Any binding interpretation contract MUST be encoded inside the YAML block,
  typically under `interpretation:` keys (closed-world, precedence, and
  extrapolation rules).

## Priority and conflict handling (MUST)

Directive rule systems MUST define:

- A stable precedence order for rule layers (or an equivalent mechanism).
- A deterministic conflict policy with a safe failure mode.

Default policy (recommended):

- Higher layer wins.
- Within a layer, higher priority wins.
- If still tied, the more specific rule wins.
- If a true conflict remains between non-negotiable rules, halt (or request
  clarification). Do not guess.

## Conditions and exceptions (MUST, with an important anti-pattern)

Rules MUST have computable boundaries:

- Use explicit condition triggers (enumerations), not prose.
- Exceptions are first-class and must be explicit.

Anti-pattern to avoid:

- Do not use `conditions: always`.

Instead:

- For unconditional rules, omit `conditions` entirely.
- Only add `conditions` when there is a real trigger that matters.

This prevents "definition bloat" where obvious terms must be defined just
because they appear as condition values.

## Definitions policy (MUST)

- Define only non-obvious terms that materially change interpretation.
- Do not define words that are universally understood in this context (example:
  do not define "always", "generally", "usually" by default).

If a word must be defined, prefer:

- A short operational meaning
- A minimal boundary (what it includes / excludes)
- A single example when helpful

## Verification and testing (SHOULD, but scoped)

Do not rely on "final comprehensive rule checking" inside the same LLM call as
the primary enforcement mechanism.

Prefer:

- Externalize validation (programmatic checks, schema validation, or a separate
  validation pass) when the constraint is important and cheaply checkable.
- Keep "self-check instructions" internal and minimal; do not require printing
  checklists unless requested.

Verification requirements SHOULD be applied selectively:

- MUST/MUST NOT rules at the highest layers or highest priority should have a
  concrete validation strategy.
- Lower-impact rules may omit verification to avoid expanding context.

## Instruction compression and invocation scope (SHOULD)

- Prefer a single canonical instruction set per invocation (merge determinism).
- Re-inject required constraints per invocation, especially across tool calls.
- Separate hard constraints from soft guidance:
  - hard constraints first, compact
  - soft context labeled as advisory and kept short

## Tier separation for reliability (MAY, when useful)

When tasks are complex or high-stakes, use tier separation:

- Tier 0: extract constraints and assumptions
- Tier 1: align to requirements and hard constraints
- Tier 2: assess risks and failure modes
- Tier 3: validate key constraints (external if possible)
- Tier 4: optimize and polish

Avoid over-fragmentation. Only add tiers when they reduce failure probability
more than they increase overhead.

## How this guide uses `docs/guides.sub/*.md` (normative mapping)

The files under `docs/guides.sub/` are reference materials. This file is the
canonical policy. The rules below define which parts are adopted.

### `ai-directive-files-best-practices.md`

Use:

- Priority order and conflict policy (Sections 0.1, 0.2).
- No-assumptions / missing-info behavior (Section 0.3, 5.3).
- Normative keywords discipline (Section 1.1) and atomic rules (Section 3).
- "Do not print checklists by default" (Section 6.2).

Do not adopt as mandatory defaults:

- Any template that uses `conditions: always`. Read it as "unconditional", and
  omit `conditions` entirely in this repository.
- Full per-rule verification fields for every rule (Section 6.1) as a blanket
  requirement. Apply selectively as described in this guide.
- Minimal test suite and traceability requirements (Sections 7.1, 7.2) as a
  blanket requirement. Use only when the cost is justified.
- Templates that embed YAML-like blocks inside prose-heavy Markdown (Section 9)
  when they violate this repository's canonical directive file structure.

### `deterministic-yaml-instruction-design.md`

Use:

- Closed-world assumption and "unspecified behavior is forbidden" (Section 4).
- Eliminate ambiguous modals (Section 5).
- Explicit error handling and explicit priority systems (Sections 7, 8).

Do not adopt as mandatory defaults:

- Any requirement to place a binding interpretation contract as prose before the
  YAML block. In this repository, the binding contract MUST be encoded inside
  the YAML block (see "Interpretation contract placement (MUST)").
- Empirical variance measurement loops (Part V) as a required process. Use only
  when drift is an observed problem and measurement cost is justified.

### `llm-instruction-robustness-workaround-audit-manual.md`

Use:

- Meta-assumption: perfect compliance is not the goal (Section 1).
- Instruction compression (Section 3).
- Invocation-scoped design (Section 4).
- Hard constraints vs soft context separation (Section 5).
- Post-hoc validation as the enforcement strategy (Section 2), but scoped by
  cost and importance.

Do not adopt as mandatory defaults:

- The scoring model and audit questionnaire format as a required deliverable.
- Bibliographic references as required in directive files.

### `llm-meta-control-instability.md`

Use:

- The core insight: "LLM is a generator, not a governor" (Sections 2-4).
- Mitigation strategy: externalize meta-control and use protocol-based
  iteration (Sections 5.1, 5.3).

Do not adopt as mandatory defaults:

- Any instruction pattern that depends on a single-pass "final comprehensive
  rule check" inside the same generation call.

### `tier-separation-iterative-processing.md`

Use:

- Tier separation as an optional reliability architecture (Sections 2-3, 6-9).
- Priority blocking and controlled feedback loops (Sections 7-8).
- Guidance to avoid over-fragmentation (Section 9).

Do not adopt as mandatory defaults:

- Domain examples and broad applicability claims (Sections 4-5) as normative
  rules for all projects.
