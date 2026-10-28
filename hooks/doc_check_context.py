"""Data and context helpers for doc_check.py. No command runs at import."""
import os
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from project_rules import fields, rule_directory
HOST = ".codex" if Path(__file__).resolve().parents[1].name == ".codex" else ".claude"
TERMINOLOGY = (Path(HOST) / "rules/project/terminology.md",)
VALUE_FILES = tuple(f".{host}/rules/project/terminology.md" for host in ("claude", "codex"))
DOC_TYPES = re.compile(r"^(concept|model|design|spec|impl|glossary)(-[\w-]+)?\.md$")
CODE_SPAN = re.compile(r"`[^`\n]*`")
AGENT_CONFIG = re.compile(r"(?<![\w.])~?/?\.(?:claude|codex)/")
def line_limit(path):
    """Line limit for the file, or None when it has none."""
    if path.name == "SKILL.md":
        return 500
    if DOC_TYPES.match(path.name) or path.name in {"CLAUDE.md", "AGENTS.md"} or any(f"/.{host}/rules/" in str(path) for host in ("claude", "codex")):
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
    roots = [Path(os.environ[name]) for name in ("CLAUDE_PROJECT_DIR", "CODEX_PROJECT_DIR") if os.environ.get(name)]
    roots += list(path.parents)
    found = []
    for root in roots:
        for relative in TERMINOLOGY:
            candidate = root / relative
            if candidate.is_file() and not any(os.path.samefile(candidate, known) for known in found):
                found.append(candidate)
    return found
LOCAL_RECORD_DIRS = {"decisions", "todo", "audit"}
def local_record(path):
    """A file of a local record directory, `docs/decisions/`, `docs/todo/` or `docs/audit/`, which is never committed."""
    return path.parent.name in LOCAL_RECORD_DIRS and path.parent.parent.name == "docs"
def forbidden_terms(rule_file):
    """Forbidden terms and their exemptions from the fixed markdown section."""
    values = fields(rule_file, "Forbidden Substitutions")
    terms = []
    for key, term in values.items():
        if ".forbidden." in key:
            prefix = key.split(".forbidden.")[0] + ".exemptions."
            terms.append((term, [text for name, text in values.items() if name.startswith(prefix)]))
    return terms

def bibliography_path(repository: Path) -> Path:
    values = fields(rule_directory(repository, HOST) / "bibliography.md", "Bibliography")
    return Path(values.get("bibliography.path", "docs/references.bib"))
def term_pattern(term):
    """Whole-word match; lowercase ASCII terms match any case, other terms match exactly."""
    if not term.isascii():
        return re.compile(re.escape(term))
    flags = re.I if term.islower() else 0
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])", flags)
def term_hits(path, text):
    """Lines of the written text that use a forbidden term outside a code span."""
    hits = []
    if any(path.match(value_file) for value_file in VALUE_FILES):
        return []
    for rule_file in terminology_files(path):
        for term, exempt in forbidden_terms(rule_file):
            pattern = term_pattern(term)
            masks = [term_pattern(phrase) for phrase in exempt]
            for line in text.splitlines():
                stripped = CODE_SPAN.sub("", line)
                for mask in masks:
                    stripped = mask.sub("", stripped)
                if pattern.search(stripped):
                    hits.append(f'"{term}" ({rule_file}): {line.strip()[:120]}')
    return hits
