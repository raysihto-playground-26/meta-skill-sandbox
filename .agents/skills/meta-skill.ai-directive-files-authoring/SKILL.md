---
name: "meta-skill.ai-directive-files-authoring"
description: >
  Mandatory format and authoring rules for AI directive files (frontmatter, single YAML block, no prose).
  Apply when creating or editing any SKILL.md or .md under .agents/skills/ or .*/skills/*/;
  or when the user creates, writes, or authors a new skill.
  All AI directive files in this repository MUST conform to this format.
---

```yaml
interpretation:
  binding: "All normative content in this block is subject to the following semantics."
  unknown_keys: "Keys not defined in this file or in the rule-record schema are ignored by compliant consumers; MUST NOT carry normative obligation."
  unspecified_behavior: "Situations not covered by an explicit rule or exception are unspecified; agents MUST NOT assume behavior and MUST treat as out-of-scope or request clarification."
  precedence: "Governed by precedence_and_conflict; layer and priority on each rule determine conflict resolution."
  closed_world: "Only rules and definitions in this file are in force; no implicit import of other directive files unless explicitly referenced by id or link."
  constraints: "Rules with conditions other than 'always' apply only when those conditions match; exceptions subtract from applicability."
  compound_conditions: "A condition entry may be a single trigger identifier or a compound of the form 'A and B' (literal space, and, space), meaning both A and B apply; such identifiers MUST be defined in this file or in definitions."
  error_handling: "Parse or structure errors invalidate the directive until corrected; verification methods define validity."
  priority: "Each rule has layer (L0–L4) and priority (numeric); L0 has highest precedence, and within the same layer, higher priority number wins. See precedence_and_conflict for details."

precedence_and_conflict:
  layer_order: ["L0", "L1", "L2", "L3", "L4"]
  meaning: "Lower index has higher precedence; L0 overrides L1–L4 when in conflict."
  conflict_policy:
    MUST_vs_MUST: "Halt or request clarification; MUST NOT silently choose one."
    MUST_vs_SHOULD: "MUST wins; SHOULD yields."
    prohibition_vs_other: "Prohibitions (prohibitions section) override all other rules."

failure_states_and_degradation:
  premise: "Instruction adherence is probabilistic; the following apply when compliance cannot be assumed."
  failure_states:
    - id: "missing-info"
      description: "Required inputs or context are absent"
      behavior: "MUST NOT invent (see no-invent); MUST output explicit uncertainty and list required inputs (see state-uncertainty-when-missing)."
    - id: "rule-conflict"
      description: "Two or more rules conflict for the same situation"
      behavior: "Apply precedence_and_conflict; if unresolved MUST halt or request clarification."
    - id: "validation-tool-unavailable"
      description: "Schema validation or linter cannot be run"
      behavior: "Degrade to manual review; document that post-hoc verification was not machine-applied."
  degradation: "When the model does not comply, the runner MUST NOT assume success; verification methods remain the authority for file validity."

definitions:
  ai-directives:
    description: "Declarative configuration directives that govern AI behavior and capabilities"
    canonical-terms: ["AI directives", "AI directive files"]
  ai-directive-files:
    description: "Markdown files (.md) under .*/skills/ that contain AI directives"
    file-extensions: [".md"]
    directory-locations: [".*/skills/"]
  runner:
    description: "The execution environment, toolchain, or system component that runs the model and applies or verifies compliance with AI directive files."
    canonical-terms: ["runner", "execution environment", "agent runner"]
  tier-separation:
    description: >
      An execution discipline that structures work into discrete tiers (tier 0, tier 1, …) where
      tier N MUST be fully executed, then frozen and validated (no further edits), before
      beginning execution of tier N+1. When a rule requires tier separation, the agent MUST NOT
      interleave content from multiple tiers and MUST treat each tier as a distinct, sequential
      phase: execute tier N, freeze, validate, then proceed to tier N+1.
  scope-high-stakes:
    description: "Context or output where errors have serious consequences (e.g. safety, compliance, legal)."
  scope-multi-constraint:
    description: "Context where many rules or constraints must be satisfied together."
  scope-long-form-reasoning:
    description: "Context involving extended analysis, multi-step reasoning, or long-form generation."

prohibitions:
  override: "Every rule in this section overrides all rules in format_obligations, content_obligations, and authoring_obligations. This section override takes precedence over layer and priority; a prohibition in this section overrides any rule in those sections regardless of layer or priority value."
  items:
    - id: "no-prose"
      layer: L0
      priority: 100
      statement: "MUST NOT include narrative text, prose, or non-YAML content outside the frontmatter and the single fenced YAML code block."
      conditions: ["always"]
      exceptions: ["none"]
      verification: "no-prose-validation asserts remainder after removing frontmatter and fenced block is exclusively whitespace."
    - id: "no-invent"
      layer: L0
      priority: 100
      statement: "MUST NOT invent missing facts, sources, citations, requirements, or constraints."
      conditions: ["always"]
      exceptions: ["none"]
      verification: "Output does not assert or invent missing facts, sources, citations, requirements, or constraints."
    - id: "no-ambiguous-modals"
      layer: L2
      priority: 90
      statement: "MUST NOT use ambiguous modals (e.g. try to, when appropriate) without explicit definition."
      conditions: ["creating AI directive file", "editing AI directive file"]
      exceptions: ["none"]
      verification: "No ambiguous modal in rule or constraint content without definition."
    - id: "no-rely-on-model-verify"
      layer: L2
      priority: 95
      statement: "MUST NOT rely on instructions that ask the model to verify all rules after completing the task."
      conditions: ["creating AI directive file", "editing AI directive file"]
      exceptions: ["none"]
      verification: "No instruction asks model to verify all rules after task."
    - id: "no-ambiguous-modals-in-yaml"
      layer: L2
      priority: 92
      statement: "MUST NOT use ambiguous modals in YAML block output."
      conditions:
        ["creating AI directive file that contains YAML block", "editing AI directive file that contains YAML block"]
      exceptions: ["none"]
      verification: "YAML block contains no ambiguous modals."
    - id: "no-duplicate-rules"
      layer: L2
      priority: 90
      statement: "MUST NOT duplicate the same rule across multiple files without reference by id or link."
      conditions: ["creating AI directive file", "editing AI directive file"]
      exceptions: ["none"]
      verification: "No identical normative statement in two files without reference by id or link."
    - id: "no-prose-only-carrier"
      layer: L2
      priority: 100
      statement: "MUST NOT use prose-only or chapter-style as the primary carrier of normative rules."
      conditions: ["creating AI directive file", "editing AI directive file"]
      exceptions: ["none"]
      verification: "Normative rules are in structured records; prose is not the primary carrier."
    - id: "no-rely-on-prior-state"
      layer: L2
      priority: 95
      statement: "MUST NOT rely on implicit prior conversation state or assume persistence of constraints across invocations."
      conditions: ["creating AI directive file", "editing AI directive file"]
      exceptions: ["none"]
      verification: "No reference to prior turn or persistent state; constraints stated in full."

format_obligations:
  - id: "frontmatter-required"
    layer: L0
    priority: 100
    statement: "Every AI directive file MUST begin with a YAML frontmatter block enclosed by triple-dash delimiters."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "structure-validation asserts file starts with triple-dash line and frontmatter between first and second triple-dash."
  - id: "single-yaml-block"
    layer: L0
    priority: 100
    statement: "Every AI directive file MUST contain exactly one fenced YAML code block after the frontmatter."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "structure-validation asserts exactly one fenced YAML code block in the remainder after frontmatter."
  - id: "whitespace-only-separators"
    layer: L0
    priority: 100
    statement: "Only whitespace (newlines, spaces) MUST appear between the frontmatter closing delimiter and the fenced YAML code block opening delimiter."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "structure-validation confirms no non-whitespace content between frontmatter closing delimiter and code fence opening."

content_obligations:
  - id: "declarative-deterministic-definitional"
    layer: L2
    priority: 95
    statement: "All YAML content MUST be declarative, deterministic, and definitional in structure."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "YAML block contains only key-value and list structures; no procedural or narrative content."
  - id: "structured-english"
    layer: L2
    priority: 95
    statement: "All YAML string values expressing rules or specifications MUST use structured English."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "Human or tool review; string values use normative or enumerative English, not vague prose."
  - id: "standard-parseable"
    layer: L2
    priority: 95
    statement: "All YAML content MUST be parseable by any standard-compliant YAML parser without errors."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "yaml-parse-validation parses frontmatter and fenced block with standard YAML parser; both succeed."

authoring_obligations:
  - id: "design-assume-probabilistic"
    layer: L2
    priority: 98
    statement: "Design MUST assume instruction adherence is probabilistic, not guaranteed."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "No instruction assumes perfect compliance."
  - id: "design-define-failure-states"
    layer: L2
    priority: 98
    statement: "Design MUST define failure states and degradation behavior (e.g. missing info, conflict, tool unavailable) so that the system does not rely on the premise that the model will always comply."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Output includes explicit failure states or degradation policy."
  - id: "compliance-verifiable-after-generation"
    layer: L2
    priority: 98
    statement: "AI directive files MUST be written so that compliance can be verified after generation."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Structure allows post-hoc validation by the runner."
  - id: "rules-enumerable"
    layer: L2
    priority: 98
    statement: "Rules MUST be enumerable."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Rules are in structured records; enumerable by id or list."
  - id: "verification-machine-checkable"
    layer: L2
    priority: 98
    statement: "Verification criteria MUST be machine-checkable where possible."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Verification field or method is specified; steps are machine-executable where possible."
  - id: "structure-support-schema"
    layer: L2
    priority: 98
    statement: "Structure MUST support schema validation or linter so that post-hoc validation can be applied by the runner."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Structure allows schema or linter to run."
  - id: "content-invocation-scoped"
    layer: L2
    priority: 95
    statement: "Content MUST be written for invocation-scoped use."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Content is self-contained per invocation."
  - id: "constraints-self-contained"
    layer: L2
    priority: 95
    statement: "Constraints and obligations MUST be self-contained and re-injectable per call."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Constraints and obligations are stated in full."
  - id: "description-includes-trigger-conditions"
    layer: L2
    priority: 92
    statement: "The frontmatter description MUST state when the skill applies (trigger conditions), so that the runner or user can invoke the skill only in matching situations (e.g. 'Apply when ...', 'Use when ...', or equivalent)."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Frontmatter has a description field; description contains trigger-condition phrasing (e.g. Apply when, Use when, or explicit enumeration of when to apply); human or pattern check."
  - id: "frontmatter-description-present"
    layer: L2
    priority: 92
    statement: "The frontmatter description MUST be present."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Frontmatter contains a description field."
  - id: "frontmatter-description-non-empty"
    layer: L2
    priority: 92
    statement: "The frontmatter description MUST be non-empty."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Description value is not null, not blank, and not only whitespace."
  - id: "frontmatter-description-length-bounds"
    layer: L2
    priority: 92
    statement: "The frontmatter description MUST be between 1 and 1024 characters in length."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Description length is >= 1 and <= 1024 characters."
  - id: "frontmatter-description-states-what"
    layer: L2
    priority: 92
    statement: "The frontmatter description MUST state what the skill does."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Description text explains the skill's purpose or behavior (what it does); human or pattern check."
  - id: "frontmatter-description-keywords"
    layer: L2
    priority: 92
    statement: "The frontmatter description SHOULD include keywords that help agents identify relevant tasks."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Description contains domain-relevant or task-relevant keywords; human or pattern check."
  - id: "frontmatter-description-folded-multiline"
    layer: L2
    priority: 88
    statement: "When the frontmatter description is multiline, it MUST use YAML folded block scalar (>)."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "When description spans multiple source lines, it uses folded style (description: >)."
  - id: "frontmatter-description-folded-multiline-guidelines"
    layer: L2
    priority: 87
    statement: "For multiline frontmatter descriptions, each line SHOULD be around 100 characters and at most about 120 as a guideline; line breaks SHOULD occur at meaning boundaries (for example, at the end of a sentence or clause) where possible."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "When description spans multiple source lines, approximate line length and break positions are checked by a human or tool as guidelines."
  - id: "rule-record-schema"
    layer: L2
    priority: 100
    statement: "Every normative rule MUST be represented as a structured record that conforms to the rule-record schema, defined as having exactly the following fields: id, layer, priority, statement, conditions, exceptions, verification; this single schema requirement is mandatory so that priority computation, conflict resolution, and automated lint are possible."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Each rule record is checked for conformance to the rule-record schema by verifying that it has exactly the fields id, layer, priority, statement, conditions, exceptions, verification."
  - id: "define-precedence-order"
    layer: L2
    priority: 95
    statement: "Global precedence order (e.g. L0 through L4) MUST be defined."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Document or file set contains explicit precedence order or reference thereto."
  - id: "define-conflict-policy"
    layer: L2
    priority: 95
    statement: "A deterministic conflict policy MUST be defined (e.g. MUST vs MUST: halt or request clarification; MUST vs SHOULD: MUST wins; prohibitions override other rules)."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Document or file set contains explicit conflict policy or reference thereto."
  - id: "one-obligation-per-rule"
    layer: L2
    priority: 95
    statement: "Every enforceable rule MUST be one obligation per rule."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Each rule has exactly one MUST or one MUST NOT predicate."
  - id: "verification-criterion-per-must"
    layer: L2
    priority: 95
    statement: "Every obligation and every prohibition MUST have a verification criterion."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Each rule has a verification field or criterion."
  - id: "explanatory-must-not-permitted"
    layer: L2
    priority: 92
    statement: "When describing interpretation, semantics, or verification (as opposed to primary normative statement fields), descriptive use of the phrase MUST NOT is allowed and MUST NOT be treated as additional enforceable prohibitions."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Descriptive uses of MUST NOT in interpretation, semantics, or verification text are retained and are not modeled or enforced as separate prohibition rules."
  - id: "explanatory-must-not-for-clarity"
    layer: L2
    priority: 92
    statement: "Explanatory or descriptive use of the phrase MUST NOT (e.g. listing RFC keywords, describing conflict policy or verification scope) SHOULD be used for clarity where doing so improves understanding."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Guidance text, examples, and templates favor including explanatory uses of MUST NOT to improve clarity when ambiguity is possible."
  - id: "use-normative-keywords"
    layer: L2
    priority: 90
    statement: "RFC-style normative keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) MUST be used as defined."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Normative terms used explicitly in rules and constraints."
  - id: "state-uncertainty-when-missing"
    layer: L0
    priority: 100
    statement: "When information is missing, MUST state uncertainty explicitly and list required inputs."
    conditions: ["always"]
    exceptions: ["none"]
    verification: "For any missing info, output includes explicit uncertainty statement and checklist of required inputs."
  - id: "conditions-exceptions-enumerated"
    layer: L2
    priority: 90
    statement: "Conditions and exceptions MUST be explicit enumerations (e.g. OR-separated triggers), not prose."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Conditions and exceptions are enumerations or defined terms, not free-form prose."
  - id: "prohibitions-dedicated-section"
    layer: L2
    priority: 95
    statement: "All normative prohibitions (MUST NOT) MUST be in a dedicated section."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "All MUST NOT rules appear in a dedicated section."
  - id: "prohibitions-override"
    layer: L2
    priority: 95
    statement: "Prohibitions MUST override all other rules."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Override of other rules by prohibitions is stated."
  - id: "compliance-externalized"
    layer: L2
    priority: 95
    statement: "Compliance MUST be externalized (schema validation, linter, explicit enumeration, or protocol-based generate-validate-correct cycle)."
    conditions: ["creating AI directive file", "editing AI directive file"]
    exceptions: ["none"]
    verification: "Validation is structural or external; not model self-verify after task."
  - id: "yaml-include-interpretation-semantics"
    layer: L2
    priority: 92
    statement: "When the file contains a YAML block, the YAML MUST include interpretation semantics (e.g. unknown_keys, unspecified_behavior, precedence)."
    conditions:
      ["creating AI directive file that contains YAML block", "editing AI directive file that contains YAML block"]
    exceptions: ["none"]
    verification: "YAML contains interpretation semantics keys (e.g. interpretation.unknown_keys, interpretation.unspecified_behavior, interpretation.precedence)."
  - id: "yaml-include-closed-world-statement"
    layer: L2
    priority: 92
    statement: "When the file contains a YAML block, the YAML MUST include a closed-world statement."
    conditions:
      ["creating AI directive file that contains YAML block", "editing AI directive file that contains YAML block"]
    exceptions: ["none"]
    verification: "YAML defines a closed_world statement or equivalent closed-world semantics."
  - id: "yaml-include-constraints"
    layer: L2
    priority: 92
    statement: "When the file contains a YAML block, the YAML MUST include constraints on rule applicability."
    conditions:
      ["creating AI directive file that contains YAML block", "editing AI directive file that contains YAML block"]
    exceptions: ["none"]
    verification: "YAML defines constraints that govern when rules apply."
  - id: "yaml-include-error-handling"
    layer: L2
    priority: 92
    statement: "When the file contains a YAML block, the YAML MUST include error_handling semantics."
    conditions:
      ["creating AI directive file that contains YAML block", "editing AI directive file that contains YAML block"]
    exceptions: ["none"]
    verification: "YAML defines error_handling semantics for parse or structure errors."
  - id: "yaml-include-rule-priority"
    layer: L2
    priority: 92
    statement: "When the file contains a YAML block, the YAML MUST define explicit priority on rules (e.g. layer and numeric priority)."
    conditions:
      ["creating AI directive file that contains YAML block", "editing AI directive file that contains YAML block"]
    exceptions: ["none"]
    verification: "YAML defines explicit priority attributes on rules (e.g. layer and numeric priority)."
  - id: "tier-separation-when-applicable"
    layer: L2
    priority: 85
    statement: "When the scope is high-stakes OR multi-constraint OR long-form reasoning (e.g. high-trust review, complex spec analysis), tier separation MUST be applied."
    conditions:
      [
        "creating AI directive file and scope high-stakes",
        "editing AI directive file and scope high-stakes",
        "creating AI directive file and scope multi-constraint",
        "editing AI directive file and scope multi-constraint",
        "creating AI directive file and scope long-form reasoning",
        "editing AI directive file and scope long-form reasoning",
      ]
    exceptions: ["none"]
    verification: "When applicable, output states that tier separation is applied."
  - id: "tier-separation-define-scope-format-stopping"
    layer: L2
    priority: 85
    statement: "When tier separation is applied, per-tier scope, output format, and stopping condition MUST be defined."
    conditions:
      [
        "creating AI directive file and scope high-stakes",
        "editing AI directive file and scope high-stakes",
        "creating AI directive file and scope multi-constraint",
        "editing AI directive file and scope multi-constraint",
        "creating AI directive file and scope long-form reasoning",
        "editing AI directive file and scope long-form reasoning",
      ]
    exceptions: ["none"]
    verification: "When applicable, output defines per-tier scope, output format, and stopping condition."
  - id: "tier-separation-bounded-iteration"
    layer: L2
    priority: 85
    statement: "When tier separation is applied, bounded iteration MUST be used (e.g. execute tier N, freeze, validate, then tier N+1; on inconsistency return to responsible tier)."
    conditions:
      [
        "creating AI directive file and scope high-stakes",
        "editing AI directive file and scope high-stakes",
        "creating AI directive file and scope multi-constraint",
        "editing AI directive file and scope multi-constraint",
        "creating AI directive file and scope long-form reasoning",
        "editing AI directive file and scope long-form reasoning",
      ]
    exceptions: ["none"]
    verification: "When applicable, output states bounded iteration (e.g. tier N, freeze, validate, tier N+1)."
  - id: "tier-separation-objective-vs-subjective"
    layer: L2
    priority: 85
    statement: "When tier separation is applied, objective validation tiers MUST be separated from subjective improvement tiers."
    conditions:
      [
        "creating AI directive file and scope high-stakes",
        "editing AI directive file and scope high-stakes",
        "creating AI directive file and scope multi-constraint",
        "editing AI directive file and scope multi-constraint",
        "creating AI directive file and scope long-form reasoning",
        "editing AI directive file and scope long-form reasoning",
      ]
    exceptions: ["none"]
    verification: "When applicable, output separates objective validation tiers from subjective improvement tiers."

verification:
  methods:
    - id: "structure-validation"
      description: "Verify file structure conforms to format rules"
      steps:
        - "Read the entire file content as plain text"
        - "Assert the file starts with the frontmatter opening delimiter (triple-dash line)"
        - "Extract the frontmatter block between the first and second triple-dash delimiters"
        - "Scan the remainder for fenced YAML code blocks"
        - "Assert exactly one fenced YAML code block exists in the remainder"
        - "Assert no non-whitespace content exists outside the frontmatter and the fenced YAML code block"
    - id: "yaml-parse-validation"
      description: "Verify all YAML content is parseable by a standard YAML parser"
      steps:
        - "Extract the frontmatter YAML content (between triple-dash delimiters)"
        - "Parse with a standard YAML parser and assert success"
        - "Extract the fenced YAML code block content (between code fence delimiters)"
        - "Parse with a standard YAML parser and assert success"
    - id: "no-prose-validation"
      description: "Verify the complete absence of narrative prose"
      steps:
        - "Remove the frontmatter block (including delimiters) from the file content"
        - "Remove the fenced YAML code block (including delimiters) from the file content"
        - "Assert the remaining content consists exclusively of whitespace characters"
  self-validation:
    description: "This AI directive file MUST pass all verification methods defined herein."
    meta-circular: true
    assertion: "The file .*/skills/meta-skill.ai-directive-files-authoring/SKILL.md is itself an AI directive file and MUST strictly conform to every rule it defines."
```
