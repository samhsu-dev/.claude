#!/usr/bin/env python3
"""PreToolUse hook for Bash: blocks the git operations of rules/workflow/git-safety.md, a bypass
of the Git hooks in tools/git-hooks, a `git add` or `git commit` of a path that
rules/workflow/committing.md Staging never commits, and AI attribution in `gh pr create` and
`gh pr edit` bodies. The commit-msg hook of tools/git-hooks checks the commit message itself.

A never-committed path is one the global Git ignore file excludes, asked of `git check-ignore`.

`git branch -D` passes only for branches that are archived: `branch.<name>.archive` names a bundle
that `git bundle verify` accepts and whose heads hold the branch's current tip, so the deletion loses
no commit.
A repository whose own ignore rules re-include the path (an agent configuration repository's
`!` whitelist) commits it: Git reports the re-including pattern, so the hook reads the same list
Git applies and keeps no copy of it.

Exit 2 blocks the call; stderr is the reason Claude reads.
"""
import json
import os
import re
import shlex
import subprocess
import sys

GIT = r"\bgit(?:\s+(?:-C\s+\S+|-c\s+\S+|--[\w-]+(?:=\S+)?))*\s+"

# (pattern on the command with quoted text masked, reason with the safe alternative)
PROHIBITED = [
    (GIT + r"reset\b", "git reset moves HEAD. Create a revert commit instead."),
    (GIT + r"checkout\s+(?:.*\s)?(?:--(?:\s|$)|-f\b|\.(?:\s|$))",
     "git checkout --/./-f discards changes. Inspect with git diff, then edit by hand."),
    (GIT + r"restore\b", "git restore discards changes. Inspect with git diff, then edit by hand."),
    (GIT + r"clean\b", "git clean deletes untracked files. Remove known files by name with rm."),
    (GIT + r"stash\b", "git stash hides changes from other agents. Commit the work in progress on the current branch under a `wip:` subject."),
    (GIT + r"push\s+(?:.*\s)?(?:--force(?:-with-lease)?\b|-f\b)", "Force push rewrites history. Use git push and investigate a rejection."),
    (GIT + r"rebase\s+(?:.*\s)?(?:-i\b|--interactive\b)", "Interactive rebase can drop commits."),
    (GIT + r"commit\s+(?:.*\s)?--amend\b", "git commit --amend rewrites a commit. Create a fixup commit."),
    (GIT + r"add\s+(?:.*\s)?(?:-A\b|--all\b|\.(?:\s|$))", "Stage specific files by name, never git add -A or git add ."),
    (GIT + r"(?:.*\s)?--no-verify\b", "--no-verify skips the Git hooks. Fix what the hook reports."),
    (GIT + r"commit\s+(?:.*\s)?-[a-zA-Z]*n[a-zA-Z]*\b", "git commit -n skips the Git hooks. Fix what the hook reports."),
    (r"\bgit\s+(?:.*\s)?-c\s+core\.hooksPath\b|\bLEFTHOOK(?:_CONFIG)?=", "Overriding the Git hooks skips their checks. Fix what the hook reports."),
]

TRAILER = re.compile(r"^\s*(Co-Authored-By|Signed-off-by|Claude-Session)\s*:", re.I | re.M)
AI_MARK = re.compile(r"Generated with \[Claude Code\]|noreply@anthropic\.com|claude\.ai/code/session", re.I)
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\s*\1\b", re.S)
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
GH_PR = r"\bgh\s+pr\s+(?:create|edit)\b"
FILE_ARG = r"(?:^|\s)(?:{})(?:\s+|=)('[^']*'|\"[^\"]*\"|[^\s;&|]+)"


def mask(command):
    """Replace heredoc bodies and quoted strings with a token so message text never matches."""
    command = HEREDOC.sub(" Q ", command)
    return QUOTED.sub(" Q ", command)


def invocations(command, verb):
    """(invocation, arguments, words) of each `git <verb>` outside quoted text. Its arguments end at the
    next one; its words are the shell words up to the end of its own command (`;`, `&`, `|` or a newline)."""
    blanked = HEREDOC.sub(lambda m: "Q" * len(m.group(0)), command)
    blanked = QUOTED.sub(lambda m: "Q" * len(m.group(0)), blanked)
    found = list(re.finditer(GIT + verb + r"\b", blanked))
    for index, match in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(command)
        stop = re.search(r"[;&|\n]", blanked[match.end():end])
        own = command[match.end():match.end() + stop.start()] if stop else command[match.end():end]
        try:
            words = shlex.split(own)
        except ValueError:
            words = own.split()
        yield command[match.start():match.end()], command[match.end():end], words


def git(directory, *arguments, stdin=None):
    """Output lines of a git command run in `directory`; none when it fails."""
    result = subprocess.run(["git", "-C", directory, *arguments], input=stdin, capture_output=True, text=True)
    return result.stdout.splitlines() if result.returncode == 0 else []


def global_ignore_file(directory):
    """The global Git ignore file: `core.excludesFile`, else `$XDG_CONFIG_HOME/git/ignore`."""
    configured = git(directory, "config", "--path", "core.excludesFile")
    if configured:
        return os.path.realpath(os.path.expanduser(configured[0]))
    return os.path.realpath(os.path.join(os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config"), "git", "ignore"))


def never_committed(directory, paths):
    """The paths, relative to `directory`, that the global Git ignore file excludes and no rule of the repository re-includes."""
    if not paths:
        return []
    excludes = global_ignore_file(directory)
    blocked = []
    for line in git(directory, "check-ignore", "--no-index", "-v", "--stdin", stdin="\n".join(paths)):
        found = re.match(r"(.*):\d+:(.*)\t(.*)$", line)
        if found and not found.group(2).startswith("!") and os.path.realpath(os.path.join(directory, found.group(1))) == excludes:
            blocked.append(found.group(3))
    return blocked


def named_paths(words):
    """Path arguments: every word after `--`, and before it every word that is not an option."""
    if "--" in words:
        cut = words.index("--")
        return [w for w in words[:cut] if not w.startswith("-")] + words[cut + 1:]
    return [w for w in words if not w.startswith("-")]


def staging_errors(command, cwd):
    """Never-committed paths that a `git add` names or forces, or that a `git commit` would record."""
    paths = []
    for invocation, _, words in invocations(command, "add"):
        directory = git_cwd(invocation, cwd)
        named = named_paths(words)
        if any(w in ("-u", "--update") for w in words):
            named += git(directory, "diff", "--name-only", "--relative")
        if any(w in ("-f", "--force") for w in words) and named:
            named += git(directory, "ls-files", "--others", "--ignored", "--exclude-standard", "--", *named)
        paths += never_committed(directory, named)
    for invocation, _, words in invocations(command, "commit"):
        directory = git_cwd(invocation, cwd)
        top = git(directory, "rev-parse", "--show-toplevel")
        if not top:
            continue
        recorded = git(top[0], "diff", "--cached", "--name-only")
        if any(w == "--all" or re.fullmatch(r"-[a-zA-Z]*a[a-zA-Z]*", w) for w in words):
            recorded += git(top[0], "diff", "--name-only")
        paths += never_committed(top[0], recorded)
        if "--" in words:
            paths += never_committed(directory, words[words.index("--") + 1:])
    if not paths:
        return []
    return [f"Agent configuration, local records and run artifacts are never committed: {', '.join(sorted(set(paths)))}. "
            "Leave them out of the index; `git rm --cached <path>` unstages a staged one (rules/workflow/committing.md Staging)."]


def file_text(rest, flags, cwd):
    """Text of the message file named by the first of `flags` in `rest`, or None for none or stdin."""
    found = re.search(FILE_ARG.format(flags), rest)
    if not found or found.group(1).strip("'\"") == "-":
        return None
    path = os.path.join(cwd, os.path.expanduser(found.group(1).strip("'\"")))
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return None


def git_cwd(invocation, cwd):
    """Directory git runs in: `cwd` after each `-C <dir>` option of the matched git invocation, in order."""
    for directory in re.findall(r"(?:^|\s)-C\s+(\S+)", invocation):
        cwd = os.path.join(cwd, os.path.expanduser(directory.strip("'\"")))
    return cwd


def archived(directory, branch):
    """True when `branch.<branch>.archive` names a verified bundle whose heads hold the branch's tip."""
    tip = git(directory, "rev-parse", "--verify", "-q", f"refs/heads/{branch}")
    bundle = git(directory, "config", "--path", f"branch.{branch}.archive")
    if not tip:
        return True  # no such branch: git refuses it and no commit is lost
    if not bundle or not os.path.isfile(bundle[0]):
        return False
    if subprocess.run(["git", "-C", directory, "bundle", "verify", "-q", bundle[0]], capture_output=True).returncode != 0:
        return False
    return any(line.split()[0] == tip[0] for line in git(directory, "bundle", "list-heads", bundle[0]) if line.strip())


def force_delete_errors(command, cwd):
    """A `git branch -D` (or `--delete --force`) of a branch that is not archived."""
    errors = []
    for invocation, _, words in invocations(command, "branch"):
        options = [w for w in words if w.startswith("-")]
        force = "-D" in options or ("--force" in options or "-f" in options) and ("--delete" in options or "-d" in options)
        if not force:
            continue
        directory = git_cwd(invocation, cwd)
        names = [w for w in words if not w.startswith("-")]
        missing = [n for n in names if not archived(directory, n)] or ([] if names else ["<none>"])
        if missing or set(options) - {"-D", "-d", "--delete", "-f", "--force"}:
            errors.append(f"git branch -D deletes unmerged commits: {', '.join(missing) or 'extra options'}. Archive the "
                          "branch first (a verified bundle named by branch.<name>.archive), or use git branch -d.")
    return errors


def check(command, cwd="."):
    """Return the list of violation messages for one Bash command run in `cwd`."""
    masked = mask(command)
    errors = [reason for pattern, reason in PROHIBITED if re.search(pattern, masked)]
    if re.search(GH_PR, masked):
        rest = re.split(GH_PR, command, maxsplit=1)[1]
        body = command + "\n" + (file_text(rest, r"--body-file|-F", cwd) or "")
        if TRAILER.search(body) or AI_MARK.search(body):
            errors.append("Pull request body carries an attribution trailer or AI marker. Remove it (rules/workflow/committing.md).")
    return errors + force_delete_errors(command, cwd) + staging_errors(command, cwd)


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    errors = check(command, payload.get("cwd") or os.getcwd())
    if errors:
        print("Blocked by ~/.claude/hooks/git_guard.py:\n- " + "\n- ".join(errors), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
