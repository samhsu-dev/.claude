#!/usr/bin/env python3
"""PostToolUse hook for Write, Edit, and MultiEdit: reports
- a doc or rule file past its line limit (CLAUDE.md Documentation Naming, rules/meta/rulewriting.md),
- a forbidden term from the project's .claude/rules/communication/terminology.md in the written text,
- a glossary Source path that does not resolve (rules/docs/glossary.md),
- a URL, a directory path, or a line number in a glossary entry outside Source (rules/docs/glossary.md Entry).

The tool has already run; exit 2 shows stderr to Claude as a warning.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DOC_TYPES = re.compile(r"^(concept|model|design|spec|impl|glossary)(-[\w-]+)?\.md$")
TERMINOLOGY = Path(".claude/rules/communication/terminology.md")
CODE_SPAN = re.compile(r"`[^`\n]*`")
PATH_TOKEN = re.compile(r"`([^`\s]+(?:/|\.(?:kt|kts|md|ya?ml|json|php|py|ts|js|toml)))`")
MAX_REPORTED = 20
EXTERNAL_LOCATION = re.compile(
    r"https?://|\b[\w-]+(?:\.[\w-]+)*\.(?:com|org|io|net|dev|edu)/"            # URL
    r"|\.(?:c|h|cc|cpp|hpp|kt|java|scala|qll|py|ts|js|go|rs|ml|php|y)`?:\d+"   # file:line
    r"|`:\d+|(?<![\w])L\d+-L?\d+\b"                                          # bare line range
    r"|`[^`\s]*\w/[\w.][^`\s]*`")                                            # directory path


def line_limit(path):
    """Line limit for the file, or None when it has none."""
    if path.name == "SKILL.md":
        return 500
    if DOC_TYPES.match(path.name) or path.name == "CLAUDE.md" or "/.claude/rules/" in str(path):
        return 200
    return None


def written_text(tool_input):
    """The text the tool call added to the file."""
    if "content" in tool_input:
        return tool_input["content"]
    if "edits" in tool_input:
        return "\n".join(edit.get("new_string", "") for edit in tool_input["edits"])
    return tool_input.get("new_string", "")


def terminology_files(path):
    """Project terminology rules for the edited file: the session project, then each ancestor of the file."""
    roots = [Path(os.environ["CLAUDE_PROJECT_DIR"])] if os.environ.get("CLAUDE_PROJECT_DIR") else []
    roots += list(path.parents)
    found = []
    for root in roots:
        candidate = root / TERMINOLOGY
        if candidate.is_file() and not any(os.path.samefile(candidate, known) for known in found):
            found.append(candidate)
    return found


def forbidden_terms(rule_file):
    """Quoted words after `never` in each bullet of the Forbidden Substitutions section."""
    section = re.search(r"^## Forbidden Substitutions\n(.*?)(?=^## |\Z)", rule_file.read_text(), re.S | re.M)
    if not section:
        return []
    terms = []
    for bullet in re.findall(r"^- (.+)$", section.group(1), re.M):
        clause = re.search(r"\bnever\b(.*?)(?:\.\s|\.$|$)", bullet)
        if clause:
            terms += re.findall(r"\"([^\"]+)\"", clause.group(1))
    return terms


def term_pattern(term):
    """Whole-word match; lowercase ASCII terms match any case, other terms match exactly."""
    if not term.isascii():
        return re.compile(re.escape(term))
    flags = re.I if term.islower() else 0
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])", flags)


def term_hits(path, text):
    """Lines of the written text that use a forbidden term outside a code span."""
    hits = []
    for rule_file in terminology_files(path):
        if os.path.samefile(path, rule_file):
            continue
        for term in forbidden_terms(rule_file):
            pattern = term_pattern(term)
            for line in text.splitlines():
                if pattern.search(CODE_SPAN.sub("", line)):
                    hits.append(f'"{term}" ({rule_file}): {line.strip()[:120]}')
    return hits


def repo_root(directory):
    result = subprocess.run(["git", "-C", str(directory), "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True)
    return Path(result.stdout.strip()) if result.returncode == 0 else directory


def source_cells(lines):
    """Source text of each entry field and of each table Source column, with its line number."""
    column = None
    for number, line in enumerate(lines, 1):
        field = re.match(r"\s*- \*\*Source:\*\*(.*)", line)
        if field:
            yield number, field.group(1)
            continue
        if not line.startswith("|"):
            column = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if "Source" in cells:
            column = cells.index("Source")
        elif column is not None and column < len(cells) and not set(cells[column]) <= set("-: "):
            yield number, cells[column]


def external_locations(path):
    """Lines of a glossary entry file that hold a URL, a directory path, or a line number outside Source."""
    hits = []
    column = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if re.match(r"\s*- \*\*Source:\*\*", line):
            continue
        text = line
        if line.startswith("|"):
            cells = line.strip().strip("|").split("|")
            stripped = [cell.strip() for cell in cells]
            if "Source" in stripped:
                column = stripped.index("Source")
            elif column is not None and column < len(cells):
                cells[column] = ""
            text = "|".join(cells)
        else:
            column = None
        match = EXTERNAL_LOCATION.search(text)
        if match:
            hits.append(f"{path.name}:{number}: {match.group(0)}")
    return hits


def tracked_paths(root):
    """Paths git tracks under root, submodules included."""
    result = subprocess.run(["git", "-C", str(root), "ls-files", "--recurse-submodules"],
                            capture_output=True, text=True)
    return result.stdout.splitlines()


def resolves(token, bases, tracked):
    """A token resolves under a base, or names the tail of a tracked path (a file in a submodule)."""
    if any((base / token).exists() or any(base.glob(token)) for base in bases):
        return True
    tail = re.compile(r"(^|/)" + re.escape(token).replace(r"\*", "[^/]*") + ("" if token.endswith("/") else "$"))
    return any(tail.search(path) for path in tracked)


def unresolved_sources(path):
    """Source paths of a glossary file that resolve against none of: the routing file's prefix, the repo root, the file's directory."""
    routing = path.parent / "glossary.md"
    prefix = re.search(r"relative to `([^`]+)`", routing.read_text()) if routing.is_file() else None
    root = repo_root(path.parent)
    bases = ([root / prefix.group(1)] if prefix else []) + [root, path.parent]
    tracked = tracked_paths(root)
    missing = []
    for number, cell in source_cells(path.read_text().splitlines()):
        for token in PATH_TOKEN.findall(cell):
            if not resolves(token, bases, tracked):
                missing.append(f"{path.name}:{number}: `{token}`")
    return missing


def main():
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input", {})
    if not tool_input.get("file_path"):
        return
    path = Path(tool_input["file_path"])
    if not path.is_file():
        return
    warnings = []
    limit = line_limit(path)
    if limit is not None:
        count = len(path.read_text().splitlines())
        if count > limit:
            warnings.append(f"{path} has {count} lines; the limit is {limit}. Split it by concern.")
    hits = term_hits(path, written_text(tool_input))
    if hits:
        warnings.append("Forbidden term in written text (allowed only as an exception the rule names):\n  " + "\n  ".join(hits[:MAX_REPORTED]))
    if path.name.startswith("glossary") and path.suffix == ".md":
        missing = unresolved_sources(path)
        if missing:
            more = f"\n  ... {len(missing) - MAX_REPORTED} more" if len(missing) > MAX_REPORTED else ""
            warnings.append(f"{len(missing)} glossary Source paths do not resolve:\n  " + "\n  ".join(missing[:MAX_REPORTED]) + more)
        if path.name != "glossary.md" and not path.name.endswith(".todo.md"):
            located = external_locations(path)
            if located:
                more = f"\n  ... {len(located) - MAX_REPORTED} more" if len(located) > MAX_REPORTED else ""
                warnings.append(f"{len(located)} glossary lines cite a URL, path, or line number outside Source:\n  " + "\n  ".join(located[:MAX_REPORTED]) + more)
    if warnings:
        print("~/.claude/hooks/doc_check.py:\n- " + "\n- ".join(warnings), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
