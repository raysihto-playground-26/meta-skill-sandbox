---
name: "std-meta-skill.ai-directive-files-authoring"
description: "Defines mandatory format for AI directive files (frontmatter + single YAML block, no prose). Apply when creating or editing any SKILL.md or .md under .agents/skills/, or any .*/skills/*/ path; or when the user creates, writes, or authors a new skill in this repository. All skill files in this repo must conform to this format."
globs:
  - ".*/skills/*/*.md"
---

```yaml
definitions:
  ai-directives:
    description: "Declarative configuration directives that govern AI behavior and capabilities"
    canonical-terms:
      - "AI directives"
      - "AI directive files"
  ai-directive-files:
    description: "Markdown files (.md) located under .*/skills/ directories that contain AI directives"
    file-extensions:
      - ".md"
    directory-locations:
      - ".*/skills/"

rules:
  format:
    - id: "frontmatter-required"
      layer: L0
      priority: 100
      statement: "Every AI directive file MUST begin with a YAML frontmatter block enclosed by triple-dash delimiters"
      conditions: always
      exceptions: none
      verification: "Structure-validation asserts file starts with triple-dash line and a frontmatter block between first and second triple-dash"
    - id: "single-yaml-block"
      layer: L0
      priority: 100
      statement: "Every AI directive file MUST contain exactly one fenced YAML code block after the frontmatter"
      conditions: always
      exceptions: none
      verification: "Structure-validation asserts exactly one fenced YAML code block exists in the remainder after frontmatter"
    - id: "no-prose"
      layer: L0
      priority: 100
      statement: "No narrative text, prose, or non-YAML content is permitted outside the frontmatter and the single fenced YAML code block"
      conditions: always
      exceptions: none
      verification: "No-prose-validation asserts remaining content after removing frontmatter and fenced block is exclusively whitespace"
    - id: "whitespace-only-separators"
      layer: L0
      priority: 100
      statement: "Only whitespace characters (newlines, spaces) are permitted between the frontmatter closing delimiter and the fenced YAML code block opening delimiter"
      conditions: always
      exceptions: none
      verification: "Structure-validation confirms no non-whitespace content between frontmatter closing delimiter and code fence opening"
  content:
    - id: "declarative-deterministic-definitional"
      layer: L2
      priority: 95
      statement: "All YAML content MUST be declarative, deterministic, and definitional in structure"
      conditions: always
      exceptions: none
      verification: "YAML block contains only key-value and list structures; no procedural or narrative content"
    - id: "structured-english"
      layer: L2
      priority: 95
      statement: "All YAML string values expressing rules or specifications MUST use structured English"
      conditions: always
      exceptions: none
      verification: "Human or tool review; string values use normative or enumerative English, not vague prose"
    - id: "standard-parseable"
      layer: L2
      priority: 95
      statement: "All YAML content MUST be parseable by any standard compliant YAML parser without errors"
      conditions: always
      exceptions: none
      verification: "Yaml-parse-validation extracts frontmatter and fenced block and parses both with standard YAML parser; both succeed"

verification:
  methods:
    - id: "structure-validation"
      description: "Verify file structure conforms to format rules"
      steps:
        - "Read the entire file content as plain text"
        - "Assert the file starts with the frontmatter opening delimiter (triple-dash line)"
        - "Extract the frontmatter block between the first and second triple-dash delimiters"
        - "Scan the remainder of the file for fenced YAML code blocks"
        - "Assert exactly one fenced YAML code block exists in the remainder"
        - "Assert no non-whitespace content exists outside the frontmatter and the fenced YAML code block"
    - id: "yaml-parse-validation"
      description: "Verify all YAML content is parseable by a standard YAML parser"
      steps:
        - "Extract the frontmatter YAML content (between triple-dash delimiters)"
        - "Parse it with a standard YAML parser and assert success"
        - "Extract the fenced YAML code block content (between code fence delimiters)"
        - "Parse it with a standard YAML parser and assert success"
    - id: "no-prose-validation"
      description: "Verify the complete absence of narrative prose"
      steps:
        - "Remove the frontmatter block (including delimiters) from the file content"
        - "Remove the fenced YAML code block (including delimiters) from the file content"
        - "Assert the remaining content consists exclusively of whitespace characters"
  self-validation:
    description: "This AI directive file MUST pass all verification methods defined herein"
    meta-circular: true
    assertion: "The file .*/skills/std-meta-skill.ai-directive-files-authoring/SKILL.md is itself an AI directive file and MUST strictly conform to every rule it defines"

authoring_musts:
  - id: "probabilistic-compliance-premise"
    layer: L2
    priority: 98
    statement: "Design MUST assume instruction adherence is probabilistic, not guaranteed; MUST define failure states and degradation behavior (e.g. missing info, conflict, tool unavailable) so that the system does not rely on the premise that the model will always comply"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Output includes explicit failure states or degradation policy; no instruction assumes perfect compliance"
  - id: "post-hoc-verifiable-design"
    layer: L2
    priority: 98
    statement: "AI directive files MUST be written so that compliance can be verified after generation; rules MUST be enumerable, verification criteria MUST be machine-checkable where possible, and structure MUST support schema validation or linter so that post-hoc validation can be applied by the runner"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Rules are in structured records with verification field; structure allows schema or linter to run"
  - id: "invocation-scoped-writable"
    layer: L2
    priority: 95
    statement: "Content MUST be written for invocation-scoped use; constraints and obligations MUST be self-contained and re-injectable per call; MUST NOT rely on implicit prior conversation state or assume persistence of constraints across invocations"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Constraints and obligations are stated in full; no reference to prior turn or persistent state"
  - id: "rule-record-schema"
    layer: L2
    priority: 100
    statement: "Every normative rule MUST be a structured record with all of: id, layer, priority, statement, conditions, exceptions, verification; this full schema is mandatory so that priority computation, conflict resolution, and automated lint are possible; MUST NOT use prose-only or chapter-style as the primary carrier of normative rules"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Every rule record contains id, layer, priority, statement, conditions, exceptions, verification; no normative obligation only in prose"
  - id: "precedence-and-conflict"
    layer: L2
    priority: 95
    statement: "MUST define global precedence order (e.g. L0 through L4) and deterministic conflict policy; MUST vs MUST MUST halt or request clarification; MUST vs SHOULD MUST yield to MUST; prohibitions MUST override other rules"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Document or file set contains explicit precedence order and conflict policy or reference thereto"
  - id: "no-assumptions"
    layer: L0
    priority: 100
    statement: "MUST NOT invent missing facts, sources, citations, requirements, or constraints; when information is missing MUST state uncertainty explicitly and list required inputs"
    conditions: always
    exceptions: none
    verification: "For any missing info, output includes explicit uncertainty statement and checklist of required inputs"
  - id: "atomic-verifiable-rules"
    layer: L2
    priority: 95
    statement: "Every enforceable rule MUST be one obligation per rule; every MUST and MUST NOT MUST have a verification criterion"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Each rule has exactly one MUST or MUST NOT predicate and a verification field or criterion"
  - id: "normative-language"
    layer: L2
    priority: 90
    statement: "MUST use RFC-style normative keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY); MUST NOT use ambiguous modals (e.g. try to, when appropriate) without explicit definition"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "No ambiguous modal in rule or constraint content without definition; normative terms used explicitly"
  - id: "conditions-exceptions-enumerated"
    layer: L2
    priority: 90
    statement: "Conditions and exceptions MUST be explicit enumerations (e.g. OR-separated triggers), not prose"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "Conditions and exceptions are enumerations or defined terms, not free-form prose"
  - id: "prohibitions-isolated"
    layer: L2
    priority: 95
    statement: "All prohibitions (MUST NOT) MUST be in a dedicated section and MUST override all other rules"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "All MUST NOT rules appear in a dedicated section; override of other rules is stated"
  - id: "externalize-meta-control"
    layer: L2
    priority: 95
    statement: "MUST NOT rely on instructions that ask the model to verify all rules after completing the task; compliance MUST be externalized (schema validation, linter, explicit enumeration, or protocol-based generate-validate-correct cycle)"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "No instruction asks model to verify all rules after task; validation is structural or external"
  - id: "yaml-interpretation-when-yaml-output"
    layer: L2
    priority: 92
    statement: "When the created or edited AI directive file contains a YAML block, that output MUST be preceded by a binding interpretation contract and the YAML MUST include interpretation semantics (e.g. unknown_keys, unspecified_behavior, precedence), closed-world statement, constraints, error_handling, and explicit priority on rules; MUST NOT use ambiguous modals in that YAML"
    conditions: "when creating or editing AI directive files that contain a YAML block"
    exceptions: none
    verification: "Output has binding sentence before YAML; YAML contains interpretation, closed_world, constraints, error_handling, priority; no ambiguous modals"
  - id: "tier-separation-when-applicable"
    layer: L2
    priority: 85
    statement: "When the scope is high-stakes, multi-constraint, or long-form reasoning (e.g. high-trust review, complex spec analysis), tier separation MUST be applied: define per-tier scope, output format, and stopping condition; use bounded iteration (e.g. execute tier N, freeze, validate, then tier N+1; on inconsistency return to responsible tier); separate objective validation tiers from subjective improvement tiers"
    conditions: "when creating or editing AI directive files and scope is high-stakes OR multi-constraint OR long-form reasoning"
    exceptions: none
    verification: "When applicable, output defines per-tier scope, output format, stopping condition; bounded iteration and tier separation stated"
  - id: "no-duplicate-rules"
    layer: L2
    priority: 90
    statement: "MUST NOT duplicate the same rule across multiple files without reference by id or link"
    conditions: "when creating or editing AI directive files"
    exceptions: none
    verification: "No identical normative statement in two files without reference by id or link"
```
