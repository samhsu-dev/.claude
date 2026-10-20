#!/usr/bin/env python3
"""Agent rules for a Codex run. Codex loads only AGENTS.md files, never the rules Claude Code loads.

pack <run-dir> [project-root]
    Writes <run-dir>/AGENTS.md: the always-active rule files the run reads in full before any work,
    the path-scoped rule files it reads before it reviews a matching file, and the skills.
    Writes <run-dir>/rules.json, the rule set of the launch, so a later rule change does not alter
    what the run is checked against.
gate <run-dir> [project-root]
    Checks the run's codex.log against the rules.json of <run-dir> or its nearest parent: every
    always-active rule file was read. Writes rules-missing.txt and exits 1 when one was not.

The run directory is the Codex working directory, so Codex loads its AGENTS.md after the global one.
The pointer list stays far below Codex's default project_doc_max_bytes, so no rule text is cut off.
"""
import json
import re
import sys
from pathlib import Path

GLOBAL = Path.home() / ".claude"


def frontmatter_paths(path):
    """The `paths` globs of a rule file, or [] when the rule is always active."""
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    globs = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        item = re.match(r"\s+-\s+\"?([^\"]+)\"?\s*$", line)
        if item:
            globs.append(item.group(1))
    return globs


def rule_files(root):
    """(file, globs) for every rule of a configuration root, CLAUDE.md first."""
    found = [(root / "CLAUDE.md", [])] if (root / "CLAUDE.md").exists() else []
    return found + [(f, frontmatter_paths(f)) for f in sorted((root / "rules").rglob("*.md"))]


def configuration(project):
    roots = [GLOBAL] + ([project / ".claude"] if project else [])
    return [(f, globs) for root in roots for f, globs in rule_files(root)]


def skills():
    for skill in sorted((GLOBAL / "skills").glob("*/SKILL.md")):
        text = skill.read_text()
        described = re.search(r"^description:\s*\"?(.+?)\"?\s*$", text, re.M)
        yield skill, described.group(1) if described else ""


def pack(run_dir, project):
    rules = configuration(project)
    always = [f for f, globs in rules if not globs]
    scoped = [(f, globs) for f, globs in rules if globs]
    lines = [
        "# Agent Rules of This Run",
        "",
        "The global instructions loaded before this file are the Codex profile of these rules, checked out at "
        "`~/.codex` and possibly older. Where they differ, the files below govern, and the profile's step that reads "
        "a project `.codex/AGENTS.md` does not apply to this run.",
        "",
        "## Before Any Work",
        "",
        "Read each file in full with a shell command (`cat <path>`), in this order. Global rules come first; "
        "a project rule extends or overrides the global rule it names. They bind every file you write, "
        "your final answer and every message you draft.",
        "",
        *[f"- `{f}`" for f in always],
        "",
        "You take part in the discussion that `rules/workflow/multi-agent.md` describes: your brief fixes your role, "
        "inputs, output directory and return format. You return findings, analysis or design as text. You never launch "
        "other runs and never edit a file, write the target repository, or run a Git command.",
        "",
        "## Before Reviewing a File",
        "",
        "Before you review or analyze a file whose path matches a glob, read every rule file listed for it "
        "with a shell command, the global one before the project one.",
        "",
        "| Rule file | Globs |",
        "|-----------|-------|",
        *[f"| `{f}` | {', '.join(f'`{g}`' for g in globs)} |" for f, globs in scoped],
        "",
        "## Skills",
        "",
        "A brief that names one of these procedures is carried out by reading its file first and following it.",
        "",
        *[f"- `{s}`: {d}" for s, d in skills()],
        "",
        "## Checks the Main Agent Will Run",
        "",
        "Claude Code hooks do not run here, and you write no files. The main agent runs the documentation check "
        "on every file it writes from your findings and lints every commit message, so any file you propose must "
        "meet both.",
        "",
    ]
    (run_dir / "AGENTS.md").write_text("\n".join(lines))
    (run_dir / "rules.json").write_text(json.dumps([[str(f), globs] for f, globs in rules], indent=1))


def launch_rules(run_dir, project):
    """The rule set packed for the run: rules.json of the run directory or its nearest parent."""
    for directory in [run_dir, *run_dir.parents]:
        if (directory / "rules.json").exists():
            return [(Path(f), globs) for f, globs in json.loads((directory / "rules.json").read_text())]
    return configuration(project)


def read_in_log(rule, log):
    spellings = {str(rule), str(rule).replace(str(Path.home()), "~")}
    return any(s in log for s in spellings)


def gate(run_dir, project):
    log = "".join(p.read_text(errors="replace") for p in run_dir.rglob("codex.log"))
    missing = [str(rule) for rule, globs in launch_rules(run_dir, project)
               if not globs and not read_in_log(rule, log)]
    report = run_dir / "rules-missing.txt"
    if missing:
        report.write_text("\n".join(missing) + "\n")
        return 1
    report.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in ("pack", "gate"):
        sys.exit(__doc__)
    run, proj = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve() if len(sys.argv) == 4 else None
    sys.exit(pack(run, proj) or 0 if sys.argv[1] == "pack" else gate(run, proj))
