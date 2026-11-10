#!/usr/bin/env python3
"""Report branch and worktree state that skill `multi-agent` Branch Lifecycle resolves.

Reads the project's `Integration` values (`integration.branch`, `integration.upstream`,
`integration.branch_lifetime`) from `.claude/rules/project/integration.md`; a project without
them gets no report. Reports, against the upstream ref:
- the integration branch holding unpushed commits or lagging the upstream;
- task branches whose every change is on the upstream (delete or archive them);
- task branches with unlanded changes past the branch lifetime;
- task branches with no `branch.<name>.description` (no owning row);
- worktrees whose branch has nothing beyond the upstream (remove them), and missing worktrees.

Usage: branch_check.py [repository] [--hook EVENT] [--no-fetch]. With --hook the report is
printed as hook additional context; without findings nothing is printed.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_rules import fields, repository_root, rule_directory  # noqa: E402

UNITS = {"hour": 3600, "day": 86400, "week": 604800}
PUSH = re.compile(r"\bgit\b(?:\s+-C\s+\S+)?\s+push\b")


def git(repository: Path, *args: str, timeout: float = 30) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        capture_output=True, text=True, timeout=timeout, check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def lifetime_seconds(value: str) -> int | None:
    match = re.fullmatch(r"\s*(\d+)\s*(hour|day|week)s?\s*", value or "")
    return int(match.group(1)) * UNITS[match.group(2)] if match else None


def unlanded(repository: Path, upstream: str, branch: str) -> int:
    return sum(line.startswith("+") for line in git(repository, "cherry", upstream, branch).splitlines())


def created_at(repository: Path, branch: str) -> int | None:
    stamps = git(repository, "reflog", "show", "--format=%ct", f"refs/heads/{branch}").split()
    return int(stamps[-1]) if stamps else None


def branch_findings(repository: Path, integration: str, upstream: str, lifetime: int | None) -> list[str]:
    findings = []
    counts = git(repository, "rev-list", "--left-right", "--count", f"{integration}...{upstream}").split()
    if len(counts) == 2 and counts != ["0", "0"]:
        ahead, behind = counts
        if ahead != "0":
            findings.append(f"{integration} has {ahead} commit(s) not on {upstream}: push them now")
        if behind != "0":
            findings.append(f"{integration} lags {upstream} by {behind}: git merge --ff-only {upstream}")
    names = git(repository, "for-each-ref", "--format=%(refname:short)", "refs/heads/").split()
    landed, past, unowned = [], [], []
    now = time.time()
    for name in names:
        if name == integration or git(repository, "config", f"branch.{name}.archive").strip():
            continue
        if unlanded(repository, upstream, name) == 0:
            landed.append(name)
            continue
        born = created_at(repository, name)
        if lifetime and born and now - born > lifetime:
            past.append(f"{name} ({int((now - born) // 86400)}d)")
        if not git(repository, "config", f"branch.{name}.description").strip():
            unowned.append(name)
    if landed:
        findings.append(f"{len(landed)} branch(es) with every change on {upstream}, delete (git branch -d) or archive: " + ", ".join(landed))
    if past:
        findings.append(f"{len(past)} unlanded branch(es) past the branch lifetime, consolidate or archive: " + ", ".join(past))
    if unowned:
        findings.append(f"{len(unowned)} unlanded branch(es) with no branch description (no owning row): " + ", ".join(unowned))
    return findings


def worktree_findings(repository: Path, upstream: str) -> list[str]:
    removable, missing = [], []
    blocks = git(repository, "worktree", "list", "--porcelain").split("\n\n")
    for block in blocks[1:]:
        entry = dict(line.split(" ", 1) if " " in line else (line, "") for line in block.splitlines())
        path = entry.get("worktree")
        if not path:
            continue
        if "prunable" in entry or not Path(path).exists():
            missing.append(path)
            continue
        if "locked" in entry:
            continue
        head = entry.get("HEAD", "")
        if git(Path(path), "status", "--porcelain", "--ignore-submodules=none", timeout=60).strip():
            continue
        if head and unlanded(repository, upstream, head) == 0:
            removable.append(path)
    findings = []
    if removable:
        findings.append(f"{len(removable)} clean worktree(s) with nothing beyond {upstream}, remove them: " + ", ".join(removable))
    if missing:
        findings.append(f"{len(missing)} missing worktree(s), git worktree prune: " + ", ".join(missing))
    return findings


def report(repository: Path, fetch: bool) -> list[str]:
    values = fields(rule_directory(repository, ".claude") / "integration.md", "Integration")
    integration, upstream = values.get("integration.branch"), values.get("integration.upstream")
    if not integration or not upstream:
        return []
    if fetch and "/" in upstream:
        git(repository, "fetch", "--quiet", upstream.split("/", 1)[0], timeout=20)
    lifetime = lifetime_seconds(values.get("integration.branch_lifetime", ""))
    return branch_findings(repository, integration, upstream, lifetime) + worktree_findings(repository, upstream)


def main(argv: list[str]) -> int:
    hook = argv[argv.index("--hook") + 1] if "--hook" in argv else None
    positional = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--hook")]
    if hook:
        try:
            payload = json.load(sys.stdin)
        except ValueError:
            payload = {}
        command = (payload.get("tool_input") or {}).get("command") or ""
        if hook == "PostToolUse" and not PUSH.search(command):
            return 0
        start = Path(payload.get("cwd") or ".")
    else:
        start = Path(positional[0]) if positional else Path(".")
    repository = repository_root(start.resolve())
    try:
        findings = report(repository, fetch="--no-fetch" not in argv)
    except subprocess.TimeoutExpired:
        findings = ["branch check timed out; run ~/.claude/tools/branch_check.py by hand"]
    if not findings:
        return 0
    text = "Branch Lifecycle check (skill multi-agent):\n" + "\n".join(f"- {line}" for line in findings)
    if hook:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": hook, "additionalContext": text}}))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
