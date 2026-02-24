# The Instability of Meta-Control in LLMs

## -- The Structural Difficulty of Self-Consistency and a Representative Case --

**Source of truth and translations**  
This document (the English version) is the source of truth. When changing the content, edit this English version. The Japanese version (`.ja.md`) is generated as a translation of this document (e.g. by AI). Do not edit the Japanese version directly; the Japanese version is maintained primarily by translating the English version after any updates.

---

## 1. Higher-Level Framing of the Problem

When using Large Language Models (LLMs), we often expect them to:

- Perform self-verification
- Guarantee global consistency of outputs
- Execute a final meta-check after completing a task
- Maintain a holistic view over all given constraints

However, these forms of meta-level control frequently behave inconsistently or incompletely.

This is not an accidental failure.

It is a structural limitation:

    An LLM does not function as a governor of its own reasoning process.

---

## 2. Structural Nature of the Problem

### 2.1 No Separation Between Object-Level and Meta-Level

In human reasoning, we can distinguish between:

- Object-level execution (doing the task)
- Meta-level evaluation (verifying the task)

In LLMs, both are produced by the same token-generation mechanism.

"Verification" is not an independent process.
It is merely another sequence of predicted tokens.

There is no separate control plane.

---

### 2.2 Absence of Explicit Execution Phases

LLMs do not have:

- A "finalization" phase
- A commit step
- A guaranteed post-processing stage
- A termination checkpoint

Instructions such as:

    "After completing the task, verify all rules"

do not create a new execution phase.
They remain contextual text within the same probabilistic generation process.

---

### 2.3 No Deterministic Coverage Guarantee

Formal completeness requires:

1. Exhaustive enumeration
2. Persistent tracking
3. Explicit comparison
4. Detection of omissions

LLMs lack a deterministic mechanism that guarantees such coverage.

They approximate coherence -- they do not enforce it.

---

## 3. Representative Case:

## "Final Comprehensive Rule Check"

A typical manifestation of this structural issue is the instruction:

    "After finishing the task, ensure that all rules have been applied."

Implicitly, this demands:

1. Perfect retention of the full rule set
2. Exhaustive comparison against the output
3. Detection of violations
4. Correction
5. Re-verification

But for an LLM:

- This is not a mandatory execution phase.
- It is not a separate validation process.
- It is not a rule engine.

Therefore, common outcomes include:

- The check is skipped.
- Only a subset of rules is reviewed.
- A declaration of verification is generated without substantive inspection.

The "final comprehensive rule check" is a representative symptom of meta-control instability.

---

## 4. The Core Insight

The issue is not:

- Weak prompting
- Carelessness by the model
- Insufficient emphasis

The issue is architectural:

    An LLM is a generator, not a governor.

It produces plausible continuations.
It does not enforce systemic guarantees.

---

## 5. General Mitigation Strategies

The solution is not to strengthen the command.

The solution is to redesign the control structure.

### 5.1 Externalize Meta-Control

- Separate generation and validation
- Use external rule engines
- Apply schema validation (e.g., JSON + schema checks)

---

### 5.2 Structuralize Meta-Processing

Replace abstract natural language instructions with:

- Explicit enumeration
- Structured output formats
- Deterministic evaluation fields (OK / NG flags)

---

### 5.3 Protocol-Based Iteration

Design explicit cycles:

1. Generate
2. Validate
3. Correct
4. Re-validate

Treat this as a system-level protocol rather than a single instruction.

---

## 6. Practical Design Principle

Shift the mental model:

    Do not expect self-contained consistency from the LLM.
    Treat the LLM as a candidate generator.
    Enforce consistency through structure and external mechanisms.

---

## 7. Conclusion

The instability of "final rule checking" is not a localized issue.

It is a specific instance of a broader structural limitation:

    The difficulty of enforcing meta-control within probabilistic generative systems.

Robustness is achieved not by stronger instructions,
but by better system design.

End of document.
