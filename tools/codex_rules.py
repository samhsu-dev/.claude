#!/usr/bin/env python3
"""Agent rules for a Codex run. Codex loads only AGENTS.md files, never the rules Claude Code loads.

pack <run-dir> [project-root] [--lean]
    Writes <run-dir>/AGENTS.md: the always-active rule files the run reads in full before any work,
    the path-scoped rule files it reads before it reviews a matching file, and the skills.
    --lean packs a chain session: it leaves out the coordination rules only the main agent
    applies, and lets the run commit on its own branch.
    Writes <run-dir>/rules.json, the rule set of the launch, so a later rule change does not alter
    what the run is checked against.
gate <run-dir> [project-root]
    Checks the run's codex.log against the rules.json of <run-dir> or its nearest parent: every
    always-active rule file was read. Writes rules-missing.txt and exits 1 when one was not.

The run directory is the Codex working directory, so Codex loads its AGENTS.md after the global one.
It lies outside every Git work tree, so no agent instruction file lands in a project; a run that writes
a worktree reaches it with `codex exec --add-dir <worktree>`.
The pointer list stays far below Codex's default project_doc_max_bytes, so no rule text is cut off.
"""
import json
import re
import sys
from pathlib import Path

GLOBAL = Path.home() / ".claude"
COORDINATION = {GLOBAL / "rules/workflow/multi-agent.md", GLOBAL / "rules/workflow/development.md"}
DISCUSSION_ROLE = ("You are a read-only run of the work that `rules/workflow/multi-agent.md` describes: your brief fixes your role, "
                   "inputs, output directory and return format. You return findings, analysis or design as text, and write files "
                   "only where your brief names them. You never launch other runs and never run a Git command.")
IMPLEMENTATION_ROLE = ("You are the chain session of one task chain: your brief fixes the worktree, inputs, progress file and "
                       "return format. You append each finished step to the progress file, decide the chain's agent-decidable "
                       "design questions under `rules/workflow/decisions.md` Decision Runs, and stop an item whose question is "
                       "user-decidable. You write only that worktree and your run directory, commit on the worktree's branch, "
                       "and never push, merge, rebase or launch other runs.")


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
    rules = [(f, globs) for root in roots for f, globs in rule_files(root)
             if not (root / "rules/project").resolve() in f.resolve().parents]
    directory = project / ".codex/rules/project" if project else None
    project_rules = sorted(directory.rglob("*.md")) if directory and directory.is_dir() else []
    return rules + [(path, []) for path in project_rules]


def skills():
    for skill in sorted((GLOBAL / "skills").glob("*/SKILL.md")):
        text = skill.read_text()
        described = re.search(r"^description:\s*\"?(.+?)\"?\s*$", text, re.M)
        yield skill, described.group(1) if described else ""


def work_tree(path):
    """The Git work tree holding path, or None; a worktree marks its root with a .git file."""
    return next((d for d in [path, *path.parents] if (d / ".git").exists()), None)


def pack(run_dir, project, lean=False):
    tree = work_tree(run_dir)
    if tree:
        sys.exit(f"pack: run directory {run_dir} lies inside the work tree {tree}; use a run directory outside it")
    rules = [(f, globs) for f, globs in configuration(project) if not (lean and f in COORDINATION)]
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
        IMPLEMENTATION_ROLE if lean else DISCUSSION_ROLE,
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
        "Claude Code hooks do not run here. The main agent or the module lead runs the documentation check and the "
        "quality gate on every file written from your work and lints every commit message, so any file you write "
        "or propose must meet them.",
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
    lean = "--lean" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--lean"]
    if len(args) not in (2, 3) or args[0] not in ("pack", "gate") or (lean and args[0] != "pack"):
        sys.exit(__doc__)
    run, proj = Path(args[1]).resolve(), Path(args[2]).resolve() if len(args) == 3 else None
    sys.exit(pack(run, proj, lean) or 0 if args[0] == "pack" else gate(run, proj))
