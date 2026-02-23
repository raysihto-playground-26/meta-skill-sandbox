# Plan r1: Remediate P1 and P2 gaps (without editing AI directive files)

This plan is derived only from the following in-repo documents:

- docs/.tmp/report_p1_p2_gap_analysis.md
- .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md

Constraint: Concrete edits to AI directive files are not allowed in this iteration. Therefore, this plan focuses on runner/linter-side behavior so that evaluation and validation become deterministic even when the directive text is internally inconsistent.

## Problem statement (from the gap analysis report)

### P1: Conflict resolution ambiguity (MUST vs MUST)

As-is, two statements in the target directive are inconsistent:

- interpretation.priority says: within the same layer, higher numeric priority wins.
- precedence_and_conflict.conflict_policy.MUST_vs_MUST says: "Halt or request clarification; MUST NOT silently choose one."

Example (from the report): if two MUST rules in the same layer (e.g., L2) conflict and have different priorities (e.g., 98 vs 95), the runner cannot know whether to pick the higher priority rule or to halt.

To-be (from the report): make conflict resolution deterministic by separating:

1. Different layers: resolve by layer order (L0 > L1 > L2 > L3 > L4).
2. Same layer, different priority: resolve by numeric priority (higher wins).
3. Same layer and same priority: apply conflict policy (MUST vs MUST -> halt/request clarification).

### P2: Condition identifier vocabulary inconsistency (compound conditions)

interpretation.compound_conditions requires that each identifier used in a compound condition of the form "A and B" MUST be defined in the file or in definitions.

As-is issues called out by the report:

- Undefined identifiers are widely used in conditions, but do not exist in definitions:
  - "creating AI directive file"
  - "editing AI directive file"
  - "creating AI directive file that contains YAML block"
  - "editing AI directive file that contains YAML block"
- Tokenization mismatch:
  - conditions use space-separated identifiers like "scope high-stakes"
  - definitions use hyphenated keys like scope-high-stakes
  - These are distinct YAML strings, so mechanical lookup fails.

To-be (from the report): ensure all identifiers used in conditions are defined and mechanically matchable, so a runner/linter can validate conditions deterministically.

## Goals

- Make conflict resolution deterministic per the P1 to-be rules.
- Make compound condition identifier resolution deterministic and mechanically checkable per the P2 to-be requirements.
- Do not edit AI directive files in this iteration.

## Non-goals

- Refactoring or rewriting the AI directive file to remove the inconsistencies directly.
- Changing the semantics described in the gap analysis report.

## Plan overview

Implement and document runner/linter behavior that:

- Resolves rule conflicts deterministically using (layer, priority) as the primary decision key, and applies MUST-vs-MUST halting only when (layer, priority) are equal (P1).
- Validates and resolves condition identifiers in a deterministic way, including handling the known space-vs-hyphen mismatch for the scope identifiers, and handling the known "creating/editing ..." identifiers that appear in conditions but are not present as definition keys (P2).

## Detailed plan

### 1) Specify the deterministic resolver algorithm (P1)

Deliverable: a short, implementation-oriented specification (in code or docs) that states:

- Each rule has:
  - layer in {L0, L1, L2, L3, L4}
  - numeric priority
  - an RFC-style modal category (e.g., MUST)
- When multiple rules apply and conflict:
  - First, pick the rule(s) with the highest-precedence layer (lowest index in layer_order).
  - Within that layer, pick the rule(s) with the highest numeric priority.
  - If more than one conflicting rule remains after applying both layer and priority (tie on both):
    - Apply conflict_policy by modal pair.
    - For MUST vs MUST, halt or request clarification (do not silently choose).

Acceptance criteria:

- A runner implementing this algorithm is deterministic for the example in the report (same layer, different priority -> higher priority wins).
- MUST-vs-MUST halting is triggered only when (layer, priority) tie prevents resolution.

### 2) Implement conflict-resolution tests (P1)

Deliverable: a small set of tests or fixtures that cover:

- Different layers with conflicting rules (layer precedence decides).
- Same layer, different priorities (priority decides).
- Same layer and same priority with MUST vs MUST (halt path).

Acceptance criteria:

- All tests pass and demonstrate the intended decision points.
- The MUST-vs-MUST halt behavior is reachable only in the tie case.

### 3) Define a deterministic condition identifier resolution procedure (P2)

Deliverable: a specification for how the runner/linter resolves identifiers used in conditions:

- A condition entry is either:
  - a single identifier string, or
  - a compound string of the exact form "A and B" (literal space, "and", space).
- For compounds:
  - split into parts A and B and resolve each part independently.
- Resolution for an identifier token T:
  - First try exact match against known definition keys.
  - If not found, apply a deterministic alias rule for the known space-vs-hyphen mismatch:
    - If T begins with "scope " and contains spaces, also try replacing spaces with hyphens to match keys like scope-high-stakes.
  - If still not found, classify T as undefined and report it.

Note: The report also highlights identifiers used in conditions that are not present in definitions. Because directive-file edits are out of scope, this plan requires the runner/linter to treat these as a controlled set of known, reserved triggers for evaluation and validation (rather than silently accepting arbitrary undefined tokens).

Acceptance criteria:

- The three scope identifiers used with spaces in conditions can be resolved to the existing hyphenated definition keys deterministically:
  - "scope high-stakes" -> scope-high-stakes
  - "scope multi-constraint" -> scope-multi-constraint
  - "scope long-form reasoning" -> scope-long-form-reasoning
- The undefined identifiers called out by the report are surfaced explicitly (or handled only if they are in an explicit reserved-trigger list).

### 4) Implement condition vocabulary validation and reporting (P2)

Deliverable: linter/validator behavior that:

- Extracts all condition strings in the directive.
- For each condition:
  - if compound, split and resolve both parts
  - if single token, resolve it
- Produces a machine-readable report of:
  - unresolved identifiers
  - identifiers that resolved via alias (space->hyphen)
  - summary counts by category

Acceptance criteria:

- The linter produces a stable, deterministic report for the current file state.
- Space-vs-hyphen mismatches do not cause false "undefined" errors for the scope identifiers.
- Truly undefined identifiers (per the report list) are not silently ignored.

### 5) Document the runner/linter semantics and how they address P1/P2

Deliverable: documentation that:

- States the P1 deterministic conflict resolution order (layer, then priority, then policy only on ties).
- States the P2 identifier resolution and aliasing rules, including the scope space-vs-hyphen normalization.
- States what the runner/linter does when an identifier is undefined (error, warning, halt), and ensures this behavior is deterministic.

Acceptance criteria:

- A reader can understand, without external context, why P1 no longer produces ambiguous outcomes and why P2 identifiers are mechanically resolvable or explicitly reported.

## Risks and mitigations

- Risk: Introducing aliasing could mask genuine vocabulary drift.
  - Mitigation: Report when aliasing was applied; require explicit acceptance (e.g., fail CI in strict mode).
- Risk: Treating some identifiers as reserved triggers could conflict with a strict reading of "MUST be defined in this file or in definitions."
  - Mitigation: Limit reserved triggers to an explicit, audited list that exactly matches the identifiers cited in the gap analysis report; do not generalize.

## Definition of done

- Runner/linter behavior is deterministic for P1 and P2 as described above.
- The ambiguous MUST-vs-MUST behavior is eliminated for non-tie cases (P1).
- Condition identifier resolution is mechanically checkable and produces explicit, deterministic outputs for undefined or aliased identifiers (P2).
