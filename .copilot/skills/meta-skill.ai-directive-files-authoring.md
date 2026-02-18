---
name: "meta-skill.ai-directive-files-authoring"
description: "Skill for authoring AI directive files; defines mandatory standards, norms, and format specifications that all AI directive files must conform to"
version: "1.0.0"
globs:
  - ".copilot/skills/**/*.md"
  - ".copilot/skills/**/*.mdc"
  - ".copilot/rules/**/*.md"
  - ".copilot/rules/**/*.mdc"
  - ".copilot/agents/**/*.md"
  - ".copilot/agents/**/*.mdc"
---

```yaml
definitions:
  ai-directives:
    description: "Declarative configuration directives that govern AI behavior and capabilities"
    canonical-terms:
      - "AI directives"
      - "AI directive files"
  ai-directive-files:
    description: "Markdown files (.md, .mdc) located under .copilot/skills/, .copilot/rules/, or .copilot/agents/ directories that contain AI directives"
    file-extensions:
      - ".md"
      - ".mdc"
    directory-locations:
      - ".copilot/skills/"
      - ".copilot/rules/"
      - ".copilot/agents/"

rules:
  format:
    - id: "frontmatter-required"
      requirement: "Every AI directive file MUST begin with a YAML frontmatter block enclosed by triple-dash delimiters"
    - id: "single-yaml-block"
      requirement: "Every AI directive file MUST contain exactly one fenced YAML code block after the frontmatter"
    - id: "no-prose"
      requirement: "No narrative text, prose, or non-YAML content is permitted outside the frontmatter and the single fenced YAML code block"
    - id: "whitespace-only-separators"
      requirement: "Only whitespace characters (newlines, spaces) are permitted between the frontmatter closing delimiter and the fenced YAML code block opening delimiter"
  content:
    - id: "declarative-deterministic-definitional"
      requirement: "All YAML content MUST be declarative, deterministic, and definitional in structure"
    - id: "structured-english"
      requirement: "All YAML string values expressing rules or specifications MUST use structured English"
    - id: "standard-parseable"
      requirement: "All YAML content MUST be parseable by any standard compliant YAML parser without errors"

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
    assertion: "The file meta-skill.ai-directive-files-authoring.md is itself an AI directive file and MUST strictly conform to every rule it defines"
```
