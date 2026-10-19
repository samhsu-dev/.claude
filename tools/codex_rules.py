#!/usr/bin/env python3
"""Agent rules for a Codex run. Codex loads only AGENTS.md files, never the rules Claude Code loads.

pack <run-dir> [project-root]
    Writes <run-dir>/AGENTS.md: the always-active rule files the run reads in full before any work,
    the path-scoped rule files it reads before it writes or reviews a matching file, and the skills.
    Writes <run-dir>/rules.json, the rule set of the launch, so a later rule change does not alter
    what the run is checked against.
gate <run-dir> [project-root]
    Checks the run's codex.log against the rules.json of <run-dir> or its nearest parent: every
    always-active rule file, and every path-scoped rule file whose globs match a file that a patch
    under <run-dir> writes, was read. Writes rules-missing.txt and exits 1 when one was not.
doccheck <repo> <file>...
    Runs the documentation check hook on each file as it now stands in <repo> and prints its findings,
    one per line with line numbers removed, so an applier can diff the findings before and after a patch.

The run directory is the Codex working directory, so Codex loads its AGENTS.md after the global one.
The pointer list stays far below Codex's default project_doc_max_bytes, so no rule text is cut off.
"""
import json
import re
import sys
from pathlib import Path

GLOBAL = Path.home() / ".claude"
SKIPPED_PATCH_DIRS = {"snapshots", "evidence", "replay", "baseline", "sources"}


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


def expand_braces(glob):
    match = re.search(r"\{([^{}]*)\}", glob)
    if not match:
        return [glob]
    return [g for option in match.group(1).split(",")
            for g in expand_braces(glob[:match.start()] + option + glob[match.end():])]


def glob_regex(glob):
    """Regex for a rule glob; `**/` matches any directory prefix, including none."""
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("**", i):
            out, i = out + ".*", i + 2
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif glob[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return re.compile(out + "$")


def matches(globs, path):
    return any(glob_regex(g).search(path) for glob in globs for g in expand_braces(glob))


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
        "The global instructions loaded before this file are an older import of these rules with `.claude` rewritten "
        "to `.Codex`. Where they differ, the files below govern, and every `.Codex` path means `.claude`.",
        "",
        "## Before Any Work",
        "",
        "Read each file in full with a shell command (`cat <path>`), in this order. Global rules come first; "
        "a project rule extends or overrides the global rule it names. They bind every file you write, "
        "your final answer and every message you draft.",
        "",
        *[f"- `{f}`" for f in always],
        "",
        "You are a worker of the hierarchy that `rules/workflow/multi-agent.md` describes: your brief fixes your role, "
        "inputs, write directory and return format. You never launch other runs and never write the target "
        "repository or its Git metadata.",
        "",
        "## Before Writing or Reviewing a File",
        "",
        "Before you write, patch or review a file whose path matches a glob, read every rule file listed for it "
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
        "## Checks the Hooks Would Run",
        "",
        "Claude Code hooks do not run here. The applier runs the documentation check on every file a patch "
        "writes and rejects new findings, and it lints every commit message. Meet both before you return.",
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


def patch_targets(run_dir):
    targets = set()
    for patch in run_dir.rglob("*.patch"):
        if SKIPPED_PATCH_DIRS & set(patch.relative_to(run_dir).parts):
            continue
        for line in patch.read_text(errors="replace").splitlines():
            header = re.match(r"^\+\+\+ b/(.+)$", line)
            if header:
                targets.add(header.group(1))
    return targets


def read_in_log(rule, log):
    spellings = {str(rule), str(rule).replace(str(Path.home()), "~")}
    return any(s in log for s in spellings)


def gate(run_dir, project):
    log = "".join(p.read_text(errors="replace") for p in run_dir.rglob("codex.log"))
    targets = patch_targets(run_dir)
    missing = []
    for rule, globs in launch_rules(run_dir, project):
        forms = {t for target in targets
                 for t in (target, f"{GLOBAL}/{target}", f"{project}/{target}" if project else target)}
        needed = not globs or any(matches(globs, form) for form in forms)
        if needed and not read_in_log(rule, log):
            missing.append(str(rule))
    report = run_dir / "rules-missing.txt"
    if missing:
        report.write_text("\n".join(missing) + "\n")
        return 1
    report.unlink(missing_ok=True)
    return 0


def doccheck(repo, files):
    import subprocess
    for name in files:
        path = repo / name
        if not path.is_file():
            continue
        payload = json.dumps({"tool_input": {"file_path": str(path), "content": path.read_text(errors="replace")}})
        result = subprocess.run([sys.executable, str(GLOBAL / "hooks" / "doc_check.py")], input=payload,
                                capture_output=True, text=True, cwd=repo)
        for line in result.stderr.splitlines()[1:]:
            print(f"{name}: " + re.sub(r":\d+\b|\b\d+ (lines|citation|glossary)", r"\1", line.strip()))
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "doccheck":
        sys.exit(doccheck(Path(sys.argv[2]).resolve(), sys.argv[3:]))
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in ("pack", "gate"):
        sys.exit(__doc__)
    run, proj = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve() if len(sys.argv) == 4 else None
    sys.exit(pack(run, proj) or 0 if sys.argv[1] == "pack" else gate(run, proj))
