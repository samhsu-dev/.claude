#!/usr/bin/env python3
"""Task evidence file: merge the rows runs write, mark stale and conflicting rows, render them.

A task's working directory holds one subdirectory per run and the merged evidence file:

    <task-dir>/evidence-merged.jsonl   merged rows, written only by this tool
    <task-dir>/EVIDENCE.md             the same rows rendered for reading
    <task-dir>/<run>/evidence.jsonl    rows one run established, one JSON object per line

Row fields:
    kind    decision | doc | code | history | program | corpus
    claim   the fact in one sentence
    source  path:line or path:first-last (decision, doc, code), the program path (program),
            the command with its commit or corpus release (history, corpus)
    quote   decision, doc, code: the exact text at source
    value   program: complete stdout; history: the hits; corpus: the counts and the counting method
    runtime program rows: the first line from version_command
    version_command  argv for the reference runtime version command\n    program_sha  program bytes at execution; merge reuses a known snapshot for legacy rows
    run     filled by merge from the run directory name when absent

Commands:
    evidence.py merge <task-dir> [--root DIR]   merge every <run>/evidence.jsonl, then check
    evidence.py check <task-dir> [--root DIR]   recompute stale marks
    evidence.py brief <task-dir>                print the instructions a run brief carries
Relative paths in source resolve against --root (default: the current directory).
"""
import argparse
import json
import sys
from pathlib import Path
from evidence_rows import KINDS as KINDS, QUOTED as QUOTED, parameters as parameters, load as load, problem as problem, source_path as source_path, sha as sha, interpreter as interpreter, squash as squash, stale as stale, same as same, check as check, observed_hash as observed_hash, duplicate as duplicate
MERGED = "evidence-merged.jsonl"
RENDERED = "EVIDENCE.md"
RUN_FILE = "evidence.jsonl"
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
        if r.get("runtime"):
            out.append(f"Runtime: {r['runtime']}")
            out.append("")
        out += ["```", str(body).rstrip("\n"), "```"]
    return "\n".join(out) + "\n"
def write(task, rows):
    # A row holds a lone surrogate for each source byte that is not UTF-8; backslashreplace writes
    # it as \udcXX, which inside a JSON string is the escape json.loads reads back to the same value.
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    (task / MERGED).write_text(text, errors="backslashreplace")
    (task / RENDERED).write_text(render(rows), errors="backslashreplace")
def merge(task, root):
    rows = load(task / MERGED, root)
    check(rows, root)
    kept = {(r["kind"], r["source"]): r for r in rows if r.get("status") not in {"conflict", "stale"}}
    added = dup = conflict = 0
    errors = []
    for run_file in sorted(task.glob(f"*/**/{RUN_FILE}")):
        run = str(run_file.parent.relative_to(task))
        for n, row in enumerate(load(run_file, root), 1):
            why = problem(row)
            if why:
                errors.append(f"{run_file}:{n}: {why}")
                continue
            row.setdefault("run", run)
            if row["kind"] == "program":
                row["program_sha"] = observed_hash(row, rows, root)
            key = (row["kind"], row["source"])
            row["status"] = "stale" if stale(row, root) else "fresh"
            old = kept.get(key)
            if duplicate(row, rows, old):
                dup += 1
                continue
            row["id"] = f"E{len(rows) + 1}"
            if row["status"] == "stale":
                added += 1
            elif old is not None:
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
  {{"kind": "program", "claim": "...", "source": "program path", "runtime": "version command first line", "version_command": ["runtime", "--version"], "program_sha": "SHA-256 of program bytes at execution", "value": "complete stdout"}}
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
        rows = load(task / MERGED, args.root.resolve())
        check(rows, args.root.resolve())
        write(task, rows)
        print(f"rows {len(rows)} stale {sum(r['status'] == 'stale' for r in rows)}")
        return 0
    return brief(task)
if __name__ == "__main__":
    sys.exit(main())
