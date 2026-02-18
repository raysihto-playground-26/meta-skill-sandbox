#!/usr/bin/env python3
"""
Verification script for AI directive files.

Implements the verification methods defined in
skills/meta-skill.ai-directive-files-authoring.md.

Usage:
    python3 scripts/verify-ai-directive.py <file_path> [<file_path> ...]
"""

import re
import sys

import yaml


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def structure_validation(content: str) -> list[str]:
    """Verify file structure conforms to format rules (structure-validation)."""
    errors: list[str] = []

    # Assert the file starts with the frontmatter opening delimiter
    if not content.startswith("---"):
        errors.append("File does not start with frontmatter opening delimiter '---'")
        return errors

    # Extract frontmatter block between first and second '---'
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("File does not contain a complete frontmatter block (missing closing '---')")
        return errors

    remainder = parts[2]

    # Scan for fenced YAML code blocks in the remainder
    fence_pattern = re.compile(r"^```yaml\s*$", re.MULTILINE)
    close_pattern = re.compile(r"^```\s*$", re.MULTILINE)

    fence_opens = list(fence_pattern.finditer(remainder))
    if len(fence_opens) == 0:
        errors.append("No fenced YAML code block found after frontmatter")
        return errors
    if len(fence_opens) > 1:
        errors.append(f"Found {len(fence_opens)} fenced YAML code blocks; exactly one is required")
        return errors

    # Find the closing fence after the opening fence
    open_match = fence_opens[0]
    close_matches = [m for m in close_pattern.finditer(remainder) if m.start() > open_match.end()]
    if not close_matches:
        errors.append("Fenced YAML code block is not closed")
        return errors

    close_match = close_matches[0]

    # Assert no non-whitespace content outside frontmatter and fenced block
    before_fence = remainder[: open_match.start()]
    after_fence = remainder[close_match.end() :]

    if before_fence.strip():
        errors.append("Non-whitespace content found between frontmatter and fenced YAML code block")
    if after_fence.strip():
        errors.append("Non-whitespace content found after the fenced YAML code block")

    return errors


def yaml_parse_validation(content: str) -> list[str]:
    """Verify all YAML content is parseable (yaml-parse-validation)."""
    errors: list[str] = []

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Cannot extract frontmatter for YAML parsing")
        return errors

    frontmatter_yaml = parts[1]
    try:
        yaml.safe_load(frontmatter_yaml)
    except yaml.YAMLError as e:
        errors.append(f"Frontmatter YAML parse error: {e}")

    # Extract fenced YAML block content
    remainder = parts[2]
    fence_match = re.search(
        r"^```yaml\s*\n(.*?)^```\s*$", remainder, re.MULTILINE | re.DOTALL
    )
    if not fence_match:
        errors.append("Cannot extract fenced YAML code block for parsing")
        return errors

    block_yaml = fence_match.group(1)
    try:
        yaml.safe_load(block_yaml)
    except yaml.YAMLError as e:
        errors.append(f"Fenced YAML code block parse error: {e}")

    return errors


def no_prose_validation(content: str) -> list[str]:
    """Verify the complete absence of narrative prose (no-prose-validation)."""
    errors: list[str] = []

    # Remove frontmatter block (including delimiters)
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Cannot extract frontmatter for prose check")
        return errors

    remainder = parts[2]

    # Remove fenced YAML code block (including delimiters)
    cleaned = re.sub(
        r"^```yaml\s*\n.*?^```\s*$", "", remainder, count=1, flags=re.MULTILINE | re.DOTALL
    )

    if cleaned.strip():
        errors.append(f"Narrative prose detected outside permitted blocks: '{cleaned.strip()[:100]}'")

    return errors


def verify_file(path: str) -> bool:
    """Run all verification methods on a file. Returns True if valid."""
    content = read_file(path)

    all_errors: list[str] = []
    validations = [
        ("structure-validation", structure_validation),
        ("yaml-parse-validation", yaml_parse_validation),
        ("no-prose-validation", no_prose_validation),
    ]

    for name, fn in validations:
        errors = fn(content)
        if errors:
            for e in errors:
                all_errors.append(f"[{name}] {e}")

    if all_errors:
        print(f"FAIL: {path}")
        for e in all_errors:
            print(f"  - {e}")
        return False

    print(f"PASS: {path}")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_path> [<file_path> ...]", file=sys.stderr)
        return 1

    all_passed = True
    for path in sys.argv[1:]:
        if not verify_file(path):
            all_passed = False

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
