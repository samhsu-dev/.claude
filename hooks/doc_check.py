#!/usr/bin/env python3
"""PostToolUse hook for Write, Edit, and MultiEdit: reports
- a doc or rule file past its line limit (CLAUDE.md Documentation Naming, rules/meta/rulewriting.md),
- a forbidden term from the native project's rules/project/terminology.md in the written text,
- a glossary Source path that does not resolve (rules/docs/glossary.md),
- a URL, a directory path, or a line number in a glossary entry outside Source and Example (rules/docs/glossary.md Entry),
- a glossary citation field without a bibliography key (rules/docs/glossary.md Entry),
- a citation key that the bibliography does not hold (rules/docs/bibliography.md),
- a repository document that names a path of the agent configuration (CLAUDE.md Documentation Naming).

The tool has already run; exit 2 shows stderr to Claude as a warning.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from doc_check_context import bibliography_path as bibliography_path, TERMINOLOGY as TERMINOLOGY, CODE_SPAN as CODE_SPAN, AGENT_CONFIG as AGENT_CONFIG, line_limit as line_limit, written_text as written_text, terminology_files as terminology_files, LOCAL_RECORD_DIRS as LOCAL_RECORD_DIRS, local_record as local_record, forbidden_terms as forbidden_terms, term_pattern as term_pattern, term_hits as term_hits
from doc_check_context import DOC_TYPES, HOST
PATH_TOKEN = re.compile(r"`([^`\s]+(?:/|\.(?:kt|kts|md|ya?ml|json|php|py|ts|js|toml)))`")
MAX_REPORTED = 20
CELL_SEPARATOR = re.compile(r"(?<!\\)\|")
BIBLIOGRAPHY = Path("docs/references.bib")
CITATION = re.compile(r"\[[^\[\]]*@[^\[\]]*\]")
CITATION_KEY = re.compile(r"(?<![\w@])-?@([\w][\w:.#$%&+?<>~/-]*\w|\w)")
CITATION_FIELDS = ("Reference", "Literature", "Tools")
EXTERNAL_LOCATION = re.compile(
    r"https?://|\b[\w-]+(?:\.[\w-]+)*\.(?:com|org|io|net|dev|edu)/"            # URL
    r"|\.(?:c|h|cc|cpp|hpp|kt|java|scala|qll|py|ts|js|go|rs|ml|php|y)`?:\d+"   # file:line
    r"|`:\d+|(?<![\w])L\d+-L?\d+\b"                                          # bare line range
    r"|`[^`\s]*\w/[\w.][^`\s]*`")                                            # directory path
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
        cells = [cell.strip() for cell in CELL_SEPARATOR.split(line.strip().strip("|"))]
        if "Source" in cells:
            column = cells.index("Source")
        elif column is not None and column < len(cells) and not set(cells[column]) <= set("-: "):
            yield number, cells[column]
def external_locations(path):
    """Lines of a glossary entry file that hold a URL, a directory path, or a line number outside Source and Example."""
    hits = []
    column = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if re.match(r"\s*- \*\*(?:Source|Example):\*\*", line):
            continue
        text = line
        if line.startswith("|"):
            cells = CELL_SEPARATOR.split(line.strip().strip("|"))
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
def keyless_citations(path):
    """Citation fields and citation table cells of a glossary entry file that hold no bibliography key."""
    hits = []
    columns = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        field = re.match(r"\s*- \*\*(" + "|".join(CITATION_FIELDS) + r"):\*\*(.*)", line)
        if field:
            if "[@" not in field.group(2) and not field.group(2).strip().startswith("none"):
                hits.append(f"{path.name}:{number}: {field.group(1)}")
            continue
        if not line.startswith("|"):
            columns = []
            continue
        cells = [cell.strip() for cell in CELL_SEPARATOR.split(line.strip().strip("|"))]
        if any(name in cells for name in CITATION_FIELDS):
            columns = [cells.index(name) for name in CITATION_FIELDS if name in cells]
        elif columns and not set("".join(cells)) <= set("-: "):
            for column in columns:
                if column < len(cells) and "[@" not in cells[column] and not cells[column].startswith("none"):
                    hits.append(f"{path.name}:{number}: {cells[0]}")
    return hits
def unresolved_citations(path):
    """Citation keys of a doc that the repository bibliography does not hold."""
    text = CODE_SPAN.sub("", path.read_text())
    cited = {key for citation in CITATION.findall(text) for key in CITATION_KEY.findall(citation)}
    if not cited:
        return []
    root = repo_root(path.parent)
    relative = bibliography_path(root)
    bibliography = root / relative
    if not bibliography.is_file():
        return [f"{path.name}: no {BIBLIOGRAPHY}"]
    held = set(re.findall(r"^@\w+\{([^,\s]+),", bibliography.read_text(), re.M))
    return [f"{path.name}: @{key}" for key in sorted(cited - held)]
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
    if path.suffix == ".md" and not local_record(path) and not {".claude", ".codex"}.intersection(path.parts):
        agent_paths = [f"{path.name}:{number}" for number, line in enumerate(path.read_text().splitlines(), 1)
                       if AGENT_CONFIG.search(line)]
        if agent_paths:
            warnings.append("A repository document names the agent configuration, which is not part of the repository:\n  "
                            + "\n  ".join(agent_paths[:MAX_REPORTED]))
    if DOC_TYPES.match(path.name):
        unresolved = unresolved_citations(path)
        if unresolved:
            warnings.append(f"{len(unresolved)} citation keys do not resolve:\n  " + "\n  ".join(unresolved[:MAX_REPORTED]))
    if path.name.startswith("glossary") and path.suffix == ".md":
        missing = unresolved_sources(path)
        if missing:
            more = f"\n  ... {len(missing) - MAX_REPORTED} more" if len(missing) > MAX_REPORTED else ""
            warnings.append(f"{len(missing)} glossary Source paths do not resolve:\n  " + "\n  ".join(missing[:MAX_REPORTED]) + more)
        if path.name != "glossary.md" and not local_record(path):
            located = external_locations(path)
            if located:
                more = f"\n  ... {len(located) - MAX_REPORTED} more" if len(located) > MAX_REPORTED else ""
                warnings.append(f"{len(located)} glossary lines cite a URL, path, or line number outside Source:\n  " + "\n  ".join(located[:MAX_REPORTED]) + more)
            keyless = keyless_citations(path)
            if keyless:
                more = f"\n  ... {len(keyless) - MAX_REPORTED} more" if len(keyless) > MAX_REPORTED else ""
                warnings.append(f"{len(keyless)} glossary citations hold no bibliography key:\n  " + "\n  ".join(keyless[:MAX_REPORTED]) + more)
    if warnings:
        print(f"~/{HOST}/hooks/doc_check.py:\n- " + "\n- ".join(warnings), file=sys.stderr)
        sys.exit(2)
if __name__ == "__main__":
    main()
