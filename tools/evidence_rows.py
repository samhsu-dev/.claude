"""Data and context helpers for evidence.py. No command runs at import."""
import hashlib
import json
import re
import subprocess
import sys
from functools import cache
from pathlib import Path
from project_rules import arguments, fields, repository_root, rule_directory
HOST = ".codex" if Path(__file__).resolve().parents[1].name == ".codex" else ".claude"
KINDS = {"decision", "doc", "code", "history", "program", "corpus"}
QUOTED = {"decision", "doc", "code"}
def parameters(root=None):
    directory = rule_directory(repository_root(Path(root or Path.cwd()).resolve()), HOST)
    path = directory / "evidence.md"
    evidence = fields(path, "Evidence Kinds")
    reference = fields(path, "Reference Runtime")
    return {"evidence": {key.removeprefix("evidence."): value for key, value in evidence.items()},
            "reference": {"name": reference.get("reference.name"), "version": reference.get("reference.version"),
                          "command": arguments(reference, "reference.command"),
                          "version_command": arguments(reference, "reference.version_command")}}
def load(path, root=None):
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip():
            try:
                row = json.loads(line)
                bindings = parameters(root).get("evidence", {})
                legacy_kind = bindings.get("legacy_program_kind")
                if legacy_kind and row.get("kind") == legacy_kind:
                    row["kind"] = "program"
                    legacy_field = bindings.get("legacy_runtime_field")
                    if legacy_field and legacy_field in row:
                        row["runtime"] = row.pop(legacy_field)
                    row["version_command"] = parameters(root).get("reference", {}).get("version_command", [])
                rows.append(row)
            except json.JSONDecodeError as e:
                sys.exit(f"{path}:{n}: {e}")
    return rows
def problem(row):
    kind = row.get("kind")
    if kind not in KINDS:
        return f"kind {kind!r} not in {sorted(KINDS)}"
    for field in ("claim", "source"):
        if not row.get(field):
            return f"missing {field}"
        if not isinstance(row[field], str):
            return f"{field} is not a string"
    if kind in QUOTED and not row.get("quote"):
        return "missing quote"
    if kind in {"program", "history", "corpus"} and "value" not in row:
        return "missing value"
    return None
def source_path(row, root):
    raw = row["source"] if row["kind"] == "program" else re.sub(r":\d+(-\d+)?$", "", row["source"])
    path = Path(raw)
    return path if path.is_absolute() else root / path
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
@cache
def interpreter(command):
    try:
        out = subprocess.run(list(command), capture_output=True, text=True, check=False).stdout
    except (OSError, ValueError):
        return None
    return out.splitlines()[0] if out else None
def squash(text):
    return " ".join(text.split())
def stale(row, root):
    kind = row["kind"]
    if kind in QUOTED:
        path = source_path(row, root)
        return not path.is_file() or squash(row["quote"]) not in squash(path.read_text(errors="replace"))
    if kind == "program":
        moved = row.get("runtime") and row["runtime"] != interpreter(tuple(row.get("version_command", [])))
        return bool(moved) or sha(source_path(row, root)) != row.get("program_sha")
    return False
def same(a, b):
    fields = ("quote", "value", "runtime", "version_command", "program_sha")
    return all(a.get(field) == b.get(field) for field in fields)
def check(rows, root):
    for row in rows:
        if row.get("status") != "conflict":
            row["status"] = "stale" if stale(row, root) else "fresh"
def observed_hash(row, rows, root):
    if "program_sha" in row:
        return row["program_sha"]
    fields = ("kind", "source", "run", "quote", "value", "runtime", "version_command")
    previous = next((r for r in rows if all(r.get(f) == row.get(f) for f in fields)), None)
    return previous.get("program_sha") if previous is not None else sha(source_path(row, root))
def duplicate(row, rows, current):
    for previous in rows:
        if (previous["kind"], previous["source"]) != (row["kind"], row["source"]) or not same(previous, row):
            continue
        if row["status"] == "stale" or previous.get("status") == "fresh":
            return True
        if current and previous.get("status") == "conflict" and previous.get("conflicts") == current["id"]:
            return True
    return False
