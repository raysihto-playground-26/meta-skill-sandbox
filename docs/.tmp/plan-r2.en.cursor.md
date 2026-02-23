# Integrated Remediation Plan R2: P1 and P2 for AI Directive Authoring Skill

Target file (canonical): `.agents/skills/meta-skill.ai-directive-files-authoring/SKILL.md`

Source: `docs/.tmp/report_p1_p2_gap_analysis.md`

Integrated from: plan-r1.en.claude.md, plan-r1.en.codex.md, plan-r1.en.copilot.md, plan-r1.en.cursor.md
(plan-r1.en.gpt.md excluded: it proposed runner-side fixes without editing SKILL.md; the requirement
demands remediation of the AI directive file itself.)

---

## 0. Purpose and scope

### 0.1 Purpose

This plan defines remediation for two issues in the gap analysis report:

| ID  | Issue                                      | Severity |
| --- | ------------------------------------------ | -------- |
| P1  | interpretation.priority vs MUST_vs_MUST    | Critical |
| P2  | Condition identifier vocabulary and tokens | High     |

All four source plans agree that SKILL.md must be modified; runner-only behavior changes do not
satisfy the requirement.

### 0.2 Scope

- In scope: changes to the YAML content of SKILL.md that resolve P1 and P2.
- Out of scope: concrete edits to AI directive files during this planning task; changes to other
  files; human-operated linter scripts.

### 0.3 Constraints

- No concrete change code; keywords and identifiers may be cited.
- Minimize the number of affected rule locations; maximize effect.
- AI agent parseability is paramount; human readability is secondary.
- Mechanical verification should be feasible during AI agent context parsing; human scripts are
  not assumed.
- Perfect textual consistency is secondary to correct intent interpretation by AI agents.

---

## 1. P1: Conflict Resolution Ambiguity (MUST)

### 1.1 Unanimous problem

All four source plans agree:

- interpretation.priority states: within the same layer, higher numeric priority wins.
- precedence_and_conflict.conflict_policy.MUST_vs_MUST states: halt or request clarification.
- For two MUST rules in the same layer with different priorities (e.g. L2/98 vs L2/95), these
  instructions contradict each other; the runner cannot behave deterministically.

### 1.2 Unanimous remediation (MUST)

All four plans prescribe the same resolution:

1. **Conflict resolution order**: (a) compare layer; (b) compare numeric priority; (c) apply
   conflict_policy only when both layer and priority are equal.
2. **MUST_vs_MUST applicability**: Narrow the applicability of MUST_vs_MUST so that halt/clarification
   applies only when two MUST rules have the same layer and the same priority. When layer differs,
   layer precedence resolves. When layer is equal but priority differs, higher numeric priority wins.
3. **interpretation.priority alignment**: Add or revise interpretation.priority to state that when
   layer and priority are both equal, conflict_policy applies. This establishes the boundary between
   priority resolution and conflict policy.

### 1.3 Target sections

- precedence_and_conflict.conflict_policy.MUST_vs_MUST
- interpretation.priority

### 1.4 Acceptance

- No contradiction exists between interpretation.priority and MUST_vs_MUST for any combination of
  layer and priority.
- For same layer, different priority: higher priority wins (no halt).
- For same layer, same priority: halt or request clarification.
- An AI agent parsing the file can trace a single deterministic cascade for any two-rule conflict.

---

## 2. P2: Condition Identifier Vocabulary (MUST)

### 2.1 Unanimous problem

All four source plans agree:

- interpretation.compound_conditions requires identifiers in conditions to be defined in the file
  or in definitions.
- Problem A: Identifiers such as "creating AI directive file", "editing AI directive file",
  "creating AI directive file that contains YAML block", "editing AI directive file that contains
  YAML block", and scope identifiers (e.g. "scope high-stakes") are used in conditions but not
  defined in definitions.
- Problem B: definitions uses hyphen-separated keys (e.g. scope-high-stakes); conditions use
  space-separated strings (e.g. "scope high-stakes"). These are distinct YAML values; mechanical
  lookup fails.

### 2.2 Unanimous remediation (MUST)

All four plans prescribe:

1. **Define all used identifiers**: Add entries to definitions for every identifier referenced in
   any conditions array. Required definitions include:
   - creating-ai-directive-file (or equivalent hyphen form)
   - editing-ai-directive-file
   - creating-ai-directive-file-that-contains-yaml-block
   - editing-ai-directive-file-that-contains-yaml-block
   - (scope-high-stakes, scope-multi-constraint, scope-long-form-reasoning already exist in
     definitions)

2. **Unify token form**: Use one canonical form so that the strings in conditions arrays exactly
   match the keys in definitions. The existing definitions use hyphen-separated lowercase keys.
   Normalize all conditions to use that form.

3. **Update all conditions arrays**: Replace every occurrence of space-separated identifiers with
   the corresponding hyphen-separated identifiers so that each token in conditions has an exact
   match in definitions.

### 2.3 Canonical identifier forms (keywords only)

Identifiers used in conditions must match definitions keys. Canonical forms (hyphen-separated):

- creating-ai-directive-file
- editing-ai-directive-file
- creating-ai-directive-file-that-contains-yaml-block
- editing-ai-directive-file-that-contains-yaml-block
- scope-high-stakes
- scope-multi-constraint
- scope-long-form-reasoning

Compound conditions retain the literal " and " separator between tokens; each token must be a
defined identifier.

### 2.4 Affected rule categories

- Rules using ["creating AI directive file", "editing AI directive file"]: most authoring rules
  in prohibitions and authoring_obligations.
- Rules using yaml-include conditions: no-ambiguous-modals-in-yaml, yaml-include-\* rules.
- Rules using compound conditions with scope: tier-separation-when-applicable,
  tier-separation-define-scope-format-stopping, tier-separation-bounded-iteration,
  tier-separation-objective-vs-subjective.

Minimize edits by batching identifier normalization across all conditions arrays in a single
logical phase.

### 2.5 Acceptance

- Every token in every conditions array has a matching key in definitions.
- No space-vs-hyphen mismatch between conditions and definitions.
- compound_conditions MUST requirement is satisfied (no self-violation).
- An AI agent parsing the file can verify each condition token against definitions by exact
  string match.
- No rule applicability semantics are altered.

---

## 3. Execution order

P1 before P2. P1 is Critical and touches two string values; P2 touches definitions and many
conditions arrays. Applying P1 first reduces risk and keeps changes ordered.

---

## 4. Verification (AI agent context parsing)

The following verification should be performable by an AI agent during context parsing of
SKILL.md:

1. **P1**: For any two rules with conflicting obligations, trace the cascade: layer comparison,
   then priority comparison, then conflict_policy. Confirm a single outcome.
2. **P2**: Extract all condition entries; for compound conditions, split on " and "; for each
   token, confirm a definitions key exists with exact match.
3. **Structure**: YAML parses successfully; rule records retain required fields (id, layer,
   priority, statement, conditions, exceptions, verification).

Human-operated scripts are not assumed. Verification is by logical inference during file
interpretation.

---

## 5. Summary of required changes

| Change | Target                            | Purpose                                        |
| ------ | --------------------------------- | ---------------------------------------------- |
| P1-A   | conflict_policy.MUST_vs_MUST      | Restrict applicability to equal layer+priority |
| P1-B   | interpretation.priority           | Reference conflict_policy for tie case         |
| P2-A   | definitions                       | Add four trigger identifier entries            |
| P2-B   | tier-separation rules' conditions | Normalize scope tokens to hyphen form          |
| P2-C   | All other rules' conditions       | Normalize trigger tokens to hyphen form        |

Total: 2 interpretation/precedence string updates (P1); 4 new definitions + conditions array
updates across affected rules (P2). A convention statement under interpretation (e.g.
condition_identifiers) stating that condition tokens MUST match definitions keys in hyphen form
is recommended for durability but is not required by unanimous agreement; include only if
consistent with minimal-change principle.
