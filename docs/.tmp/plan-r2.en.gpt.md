Title: Plan R2 (rev2) - Integrated remediation plan for P1 and P2 in AI directive authoring skill

Inputs (in-repo, normative for this plan):

- docs/.tmp/report_p1_p2_gap_analysis.md
- docs/.tmp/plan-r1.en.claude.md
- docs/.tmp/plan-r1.en.codex.md
- docs/.tmp/plan-r1.en.copilot.md
- docs/.tmp/plan-r1.en.cursor.md
- Target file to change (canonical): .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md
  Note: other .\*/skills paths are symlinks to .agents/skills; change only the canonical file.

This document is a plan only. It MUST NOT include concrete edits, patches, or code for any AI directive file.
It is written to be interpreted by AI agents; human readability is not a primary objective.

# ================================================================ 0. Problem statement (self-contained summary of the gap report)

P1 (Critical): Conflict resolution ambiguity for MUST-vs-MUST

- As-is:
  - interpretation.priority states: within the same layer, higher numeric priority wins.
  - precedence_and_conflict.conflict_policy.MUST_vs_MUST states: halt or request clarification; MUST NOT silently choose one.
  - Therefore, two MUST rules in the same layer with different priorities yield contradictory instructions.
- To-be:
  - Deterministic cascade:
    - If layers differ: resolve by layer precedence order.
    - Else if priorities differ: resolve by numeric priority (higher wins).
    - Else (same layer and same priority): apply conflict policy; MUST-vs-MUST halts/requests clarification.

P2 (High): Condition identifier vocabulary is undefined and inconsistent

- As-is:
  - interpretation.compound_conditions requires: identifiers used in conditions (including A and B compounds) MUST be defined in this file or in definitions.
  - The file uses condition identifiers that are not defined in definitions (notably, creating/editing triggers and YAML-block variants).
  - The file uses space-tokenized scope identifiers in conditions while definitions use hyphen-tokenized keys; exact-match resolution fails.
- To-be:
  - Every condition identifier token used anywhere in conditions is defined and mechanically resolvable.
  - A runner/linter can deterministically validate conditions tokens against the authoritative registry.

=========================================================

1. # Global constraints and decision principles (R2 rules)

MUST (global):

- Fixes MUST be applied by changing .agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md (the directive), not by shifting responsibility entirely to runner/linter behavior.
- The resulting specification MUST be internally consistent for P1 and MUST be self-compliant for P2 (it must satisfy its own MUST requirements).
- The plan MUST minimize the number of touched rule records while maximizing the elimination of ambiguity and self-violation.
- Verification MUST prefer procedures executable during AI agent context analysis (parse, enumerate, compare, resolve) rather than relying on humans running external scripts.
- No change may require a consumer to guess unspecified behavior; tie-breaks and fallbacks MUST be explicit.

SHOULD (global):

- Prefer changes that rewrite as few YAML scalar values as possible, and add as few new keys as possible.
- Prefer deterministic, local checks (extract tokens, exact match, controlled normalization) over subjective review.

# ========================================================= 2. P1 remediation (Conflict resolution determinism)

2.1 MUST outcome (post-fix semantics)

- A deterministic conflict-resolution cascade MUST be unambiguous and complete:
  - Compare layer first (layer precedence order).
  - If same layer, compare numeric priority next.
  - Only if both layer and priority are equal, enter conflict_policy evaluation.
- MUST-vs-MUST halting MUST apply only in the tie case (same layer AND same priority).

  2.2 Minimal change strategy (impact minimization)

- MUST rewrite the text of precedence_and_conflict.conflict_policy.MUST_vs_MUST to scope halting to the tie case and to state how non-tie MUST-vs-MUST conflicts are resolved (layer, then priority).
- MUST rewrite the text of interpretation.priority to explicitly state that conflict policy is the fallback only for equal layer and equal priority (or otherwise remove any implication of contradictory authority).
- MUST NOT add new structural sections to achieve P1 (no new schema, no new rule records) unless strictly necessary; P1 can be fixed via scalar-text rewrites.

  2.3 P1 acceptance criteria (machine-checkable)

- P1-AC1: Reading interpretation.priority and conflict_policy together yields exactly one deterministic procedure (no contradictory branch) for:
  - different layer
  - same layer, different priority
  - same layer, same priority
- P1-AC2: For the example class (same layer, different priority, both MUST), the procedure selects the higher priority rule and does not halt.
- P1-AC3: For the tie case (same layer, same priority, both MUST), the procedure halts/requests clarification and does not silently choose.
- P1-AC4: YAML parsing of the fenced YAML block remains valid after the rewrite(s).

# ========================================================= 3. P2 remediation (Condition identifier vocabulary)

3.1 MUST outcome (post-fix semantics)

- Every condition identifier token used in any rule record conditions entry MUST be defined in exactly one authoritative registry in the file (definitions or an equivalent dedicated registry).
- Compound conditions of the form "A and B" MUST be mechanically decomposable into tokens A and B, and each token MUST resolve deterministically to a defined identifier.
- The specification MUST define one deterministic resolution rule for identifier tokens so that a runner/linter can validate conditions without ambiguity.

  3.2 Inventory: minimum required identifiers to address (from gap report)
  Undefined trigger identifiers currently used in conditions:

- creating AI directive file
- editing AI directive file
- creating AI directive file that contains YAML block
- editing AI directive file that contains YAML block

Space-tokenized scope identifiers currently used in compound conditions:

- scope high-stakes
- scope multi-constraint
- scope long-form reasoning

Hyphen-tokenized scope identifiers currently present as definitions keys:

- scope-high-stakes
- scope-multi-constraint
- scope-long-form-reasoning

  3.3 Integrated strategy (best effect per touched rules)

MUST (core):

- Introduce explicit definitions entries so that every identifier token listed in 3.2 is defined.
- Establish a single canonical token form for identifiers (recommended canonical target: the existing hyphen-tokenized definitions keys).
- Establish deterministic, explicit token resolution for conditions so that:
  - exact canonical tokens are accepted directly, and
  - any permitted non-canonical tokens (aliases) resolve to exactly one canonical identifier.

R2 choice to minimize change churn:

- MUST implement a low-churn fix first (add missing definitions and define controlled aliasing/normalization semantics), because it eliminates the self-violation without rewriting dozens of rule records.
- SHOULD perform a high-churn normalization later (rewrite all conditions entries to canonical tokens) only if it is necessary for downstream exact-string consumers or to retire aliasing.

  3.4 P2 change set (no-code description)

P2-A (MUST): Add missing trigger identifiers to the authoritative registry

- Add definitions entries for the four creating/editing triggers (including the YAML-block variants), so they are no longer undefined.
- Each trigger definition SHOULD include minimal semantics (what it means) and SHOULD support deterministic resolution from the condition token used in rule records.

P2-B (MUST): Make scope tokens resolvable without changing all rule records

- Ensure that the space-tokenized scope tokens used in conditions ("scope high-stakes", etc.) resolve deterministically to the existing hyphen-tokenized definitions keys (scope-high-stakes, etc.).
- The resolution mechanism MUST be explicit in the specification text (not implicit convention).
- The mechanism MUST be constrained to the known vocabulary (do not introduce a general heuristic that silently accepts arbitrary undefined tokens).

P2-C (SHOULD, optional hardening): Normalize conditions tokens to canonical form

- If and only if needed, rewrite rule-record conditions entries to use canonical tokens directly (for both trigger and scope tokens).
- This step is high-churn (touches many rule records) and SHOULD be deferred until after P2-A/P2-B are in place and validated.

P2-D (MUST): Add a machine-checkable convention statement

- Add one explicit statement under interpretation (or an equivalent already-defined semantics area) that declares:
  - the canonical token form
  - the deterministic resolution rule (exact match first; controlled aliasing/normalization next; otherwise unresolved)
  - how unresolved tokens are handled (error / invalid directive / halt), consistent with existing error_handling and verification methods

    3.5 P2 acceptance criteria (machine-checkable)

- P2-AC1: Every condition entry token in the entire file is either:
  - a canonical identifier token, or
  - an explicitly permitted alias that resolves to exactly one canonical identifier.
- P2-AC2: Every token produced by decomposing compound conditions on the literal separator " and " resolves deterministically.
- P2-AC3: The file no longer violates its own compound_conditions MUST requirement (no undefined identifier tokens under the defined resolution rule).
- P2-AC4: YAML parsing of the fenced YAML block remains valid after the changes.
- P2-AC5: The resolution rule is explicit enough that a runner/linter can implement it without guessing.

# ========================================================= 4. Execution order (phasing) and stopping conditions

MUST:

- Apply P1 before P2. Rationale: P1 is Critical and small; applying it first reduces risk.
- Use tier-separated, bounded execution: perform one phase, freeze, validate against acceptance criteria, then proceed.

Phase 1 (P1):

- Edit only the two scalar texts implicated by P1.
- Stop when P1-AC1..P1-AC4 all pass.

Phase 2 (P2 low-churn core: P2-A, P2-B, P2-D):

- Edit only the authoritative registry content and the interpretation-level resolution statement(s).
- Stop when P2-AC1..P2-AC5 all pass without rewriting rule-record conditions arrays.

Phase 3 (P2 high-churn optional: P2-C):

- Rewrite rule-record conditions arrays to canonical tokens, then re-run P2 acceptance criteria.
- Stop when aliasing/normalization is no longer required for any in-file token (optional end-state).

# ========================================================= 5. Verification procedures (AI-agent executable emphasis)

MUST provide these verification procedures as part of the implementation work (not in this plan file):

- YAML parse validation: parse frontmatter YAML and fenced YAML block YAML.
- P1 determinism check: confirm the cascade has exactly one branch for each of the three cases and that tie-handling matches P1 acceptance criteria.
- P2 vocabulary extraction:
  - Enumerate every conditions entry.
  - For each entry, if it contains the literal " and ", split into tokens; otherwise treat as single token.
  - Apply the specified resolution rule.
  - Confirm every token resolves; produce a deterministic report (counts, unresolved tokens, alias-resolved tokens).

SHOULD:

- Add or update verification method descriptions inside SKILL.md to reflect the P2 vocabulary check and the P1 cascade check, but only if doing so does not require adding many new rules.

# ========================================================= 6. Change impact minimization (explicit guidance)

MUST:

- Prefer updating a small number of scalar semantics fields and a small number of definitions entries over rewriting many rule records.
- Avoid changing rule-record ids, layers, priorities, or statements for P1/P2 remediation.
- Avoid broad refactors (new sections, new schemas) unless the acceptance criteria cannot be met otherwise.

SHOULD:

- When adding vocabulary entries, keep them minimal and non-overlapping; every alias must resolve to exactly one canonical identifier to avoid reintroducing ambiguity.

# ========================================================= 7. Definition of Done (R2)

Done when:

- P1-AC1..P1-AC4 pass.
- P2-AC1..P2-AC5 pass (at least for the low-churn core Phase 2).
- The number of touched rule records is minimized (ideally zero rule-record rewrites for Phase 2), while still eliminating P1 ambiguity and P2 self-violation.
