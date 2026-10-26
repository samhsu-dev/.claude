#!/usr/bin/env python3
"""Task evidence file: merge the rows runs write, mark stale and conflicting rows, render them.

A task's working directory holds one subdirectory per run and the merged evidence file:

    <task-dir>/evidence-merged.jsonl   merged rows, written only by this tool
    <task-dir>/EVIDENCE.md             the same rows rendered for reading
    <task-dir>/<run>/evidence.jsonl    rows one run established, one JSON object per line

Row fields:
    kind    decision | doc | code | history | php | corpus
    claim   the fact in one sentence
    source  path:line or path:first-last (decision, doc, code), the program path (php),
            the command with its commit or corpus release (history, corpus)
    quote   decision, doc, code: the exact text at source
    value   php: complete stdout; history: the hits; corpus: the counts and the counting method
    php     php rows: the interpreter version line
    run     filled by merge from the run directory name when absent

Commands:
    evidence.py merge <task-dir> [--root DIR]   merge every <run>/evidence.jsonl, then check
    evidence.py check <task-dir> [--root DIR]   recompute stale marks
    evidence.py brief <task-dir>                print the instructions a run brief carries
Relative paths in source resolve against --root (default: the current directory).
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from functools import cache
from pathlib import Path

KINDS = {"decision", "doc", "code", "history", "php", "corpus"}
QUOTED = {"decision", "doc", "code"}
MERGED = "evidence-merged.jsonl"
RENDERED = "EVIDENCE.md"
RUN_FILE = "evidence.jsonl"


def load(path):
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
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
    if kind in QUOTED and not row.get("quote"):
        return "missing quote"
    if kind in {"php", "history", "corpus"} and "value" not in row:
        return "missing value"
    return None


def source_path(row, root):
    raw = row["source"] if row["kind"] == "php" else re.sub(r":\d+(-\d+)?$", "", row["source"])
    path = Path(raw)
    return path if path.is_absolute() else root / path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


@cache
def interpreter():
    try:
        out = subprocess.run(["php", "-v"], capture_output=True, text=True, check=False).stdout
    except OSError:
        return None
    return out.splitlines()[0] if out else None


def squash(text):
    return " ".join(text.split())


def stale(row, root):
    kind = row["kind"]
    if kind in QUOTED:
        path = source_path(row, root)
        return not path.is_file() or squash(row["quote"]) not in squash(path.read_text(errors="replace"))
    if kind == "php":
        moved = row.get("php") and row["php"] != interpreter()
        return bool(moved) or sha(source_path(row, root)) != row.get("program_sha")
    return False


def same(a, b):
    return a.get("quote") == b.get("quote") and a.get("value") == b.get("value")


def check(rows, root):
    for row in rows:
        if row.get("status") != "conflict":
            row["status"] = "stale" if stale(row, root) else "fresh"


def render(rows):
    out = ["# Evidence", "", "| ID | kind | status | claim | source | run |", "|---|---|---|---|---|---|"]
    for r in rows:
        claim = r["claim"].replace("|", "\\|")
        source = r["source"].replace("|", "\\|")
        status = r["status"] + (f" of {r['conflicts']}" if r.get("conflicts") else "")
        out.append(f"| {r['id']} | {r['kind']} | {status} | {claim} | `{source}` | {r['run']} |")
    for r in rows:
        body = r.get("quote") if r["kind"] in QUOTED else r.get("value")
        if body in (None, ""):
            continue
        out += ["", f"## {r['id']}", ""]
        if r.get("php"):
            out.append(f"Interpreter: {r['php']}")
            out.append("")
        out += ["```", str(body).rstrip("\n"), "```"]
    return "\n".join(out) + "\n"


def write(task, rows):
    (task / MERGED).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    (task / RENDERED).write_text(render(rows))


def merge(task, root):
    rows = load(task / MERGED)
    kept = {(r["kind"], r["source"]): r for r in rows if r.get("status") != "conflict"}
    added = dup = conflict = 0
    errors = []
    for run_file in sorted(task.glob(f"*/**/{RUN_FILE}")):
        run = str(run_file.parent.relative_to(task))
        for n, row in enumerate(load(run_file), 1):
            why = problem(row)
            if why:
                errors.append(f"{run_file}:{n}: {why}")
                continue
            row.setdefault("run", run)
            if row["kind"] == "php":
                row["program_sha"] = sha(source_path(row, root))
            key = (row["kind"], row["source"])
            if any(same(r, row) for r in rows if (r["kind"], r["source"]) == key):
                dup += 1
                continue
            old = kept.get(key)
            row["id"] = f"E{len(rows) + 1}"
            if old is not None:
                row["status"], row["conflicts"] = "conflict", old["id"]
                conflict += 1
            else:
                kept[(row["kind"], row["source"])] = row
                added += 1
            rows.append(row)
    check(rows, root)
    write(task, rows)
    staled = sum(r["status"] == "stale" for r in rows)
    print(f"rows {len(rows)} added {added} duplicate {dup} conflict {conflict} stale {staled}")
    for e in errors:
        print("rejected", e)
    return 1 if errors else 0


def brief(task):
    merged = (task / RENDERED).resolve()
    print(f"""Evidence: read {merged} before any search; cite its rows by ID and never repeat a search a fresh row records.
For each fact you establish that the file lacks, append one JSON object per line to {RUN_FILE} in your working directory:
  {{"kind": "doc|code|decision", "claim": "...", "source": "path:line", "quote": "exact text at that line"}}
  {{"kind": "php", "claim": "...", "source": "program path", "php": "php -v first line", "value": "complete stdout"}}
  {{"kind": "history|corpus", "claim": "...", "source": "command, with commit or corpus release", "value": "hits or counts, with the counting method"}}
Paths are relative to the integration worktree or absolute. Do not edit {MERGED} or {RENDERED}.""")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["merge", "check", "brief"])
    parser.add_argument("task", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    task = args.task.resolve()
    if not task.is_dir():
        sys.exit(f"{task}: no such task directory")
    if args.command == "merge":
        return merge(task, args.root.resolve())
    if args.command == "check":
        rows = load(task / MERGED)
        check(rows, args.root.resolve())
        write(task, rows)
        print(f"rows {len(rows)} stale {sum(r['status'] == 'stale' for r in rows)}")
        return 0
    return brief(task)


if __name__ == "__main__":
    sys.exit(main())
