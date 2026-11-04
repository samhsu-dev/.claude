#!/usr/bin/env python3
"""PreToolUse hook for Bash: blocks the git operations of rules/workflow/git-safety.md,
commit messages that break rules/workflow/committing.md, and AI attribution in
`gh pr create` and `gh pr edit` bodies.

Exit 2 blocks the call; stderr is the reason Claude reads.
"""
import json
import os
import re
import sys

GIT = r"\bgit(?:\s+(?:-C\s+\S+|-c\s+\S+|--[\w-]+(?:=\S+)?))*\s+"

# (pattern on the command with quoted text masked, reason with the safe alternative)
PROHIBITED = [
    (GIT + r"reset\b", "git reset moves HEAD. Create a revert commit instead."),
    (GIT + r"checkout\s+(?:.*\s)?(?:--(?:\s|$)|-f\b|\.(?:\s|$))",
     "git checkout --/./-f discards changes. Inspect with git diff, then edit by hand."),
    (GIT + r"restore\b", "git restore discards changes. Inspect with git diff, then edit by hand."),
    (GIT + r"clean\b", "git clean deletes untracked files. Remove known files by name with rm."),
    (GIT + r"stash\b", "git stash hides changes from other agents. Commit WIP to a temporary branch."),
    (GIT + r"push\s+(?:.*\s)?(?:--force(?:-with-lease)?\b|-f\b)", "Force push rewrites history. Use git push and investigate a rejection."),
    (GIT + r"branch\s+(?:.*\s)?-D\b", "git branch -D deletes unmerged commits. Use git branch -d."),
    (GIT + r"rebase\s+(?:.*\s)?(?:-i\b|--interactive\b)", "Interactive rebase can drop commits."),
    (GIT + r"commit\s+(?:.*\s)?--amend\b", "git commit --amend rewrites a commit. Create a fixup commit."),
    (GIT + r"add\s+(?:.*\s)?(?:-A\b|--all\b|\.(?:\s|$))", "Stage specific files by name, never git add -A or git add ."),
]

TRAILER = re.compile(r"^\s*(Co-Authored-By|Signed-off-by|Claude-Session)\s*:", re.I | re.M)
AI_MARK = re.compile(r"Generated with \[Claude Code\]|noreply@anthropic\.com|claude\.ai/code/session", re.I)
SUBJECT = re.compile(r"^[a-z]+(\([^)]+\))?!?: \S")
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\s*\1\b", re.S)
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
GH_PR = r"\bgh\s+pr\s+(?:create|edit)\b"
FILE_ARG = r"(?:^|\s)(?:{})(?:\s+|=)('[^']*'|\"[^\"]*\"|[^\s;&|]+)"


def mask(command):
    """Replace heredoc bodies and quoted strings with a token so message text never matches."""
    command = HEREDOC.sub(" Q ", command)
    return QUOTED.sub(" Q ", command)


def commit_subject(command):
    """First line of the commit message given by a heredoc or the first -m argument, or None."""
    after = re.split(GIT + r"commit\b", command, maxsplit=1)
    if len(after) < 2:
        return None
    rest = after[1]
    doc = HEREDOC.search(rest)
    message = re.search(r"(?:-m|--message)(?:\s+|=)('([^']*)'|\"((?:\\.|[^\"\\])*)\")", rest)
    if doc and (not message or doc.start() < message.end()):
        text = doc.group(2)
    elif message:
        text = message.group(2) if message.group(2) is not None else message.group(3)
    else:
        return None
    lines = [line for line in text.splitlines() if line.strip()]
    return lines[0].strip() if lines else None


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


def check(command, cwd="."):
    """Return the list of violation messages for one Bash command run in `cwd`."""
    masked = mask(command)
    errors = [reason for pattern, reason in PROHIBITED if re.search(pattern, masked)]
    if re.search(GH_PR, masked):
        rest = re.split(GH_PR, command, maxsplit=1)[1]
        body = command + "\n" + (file_text(rest, r"--body-file|-F", cwd) or "")
        if TRAILER.search(body) or AI_MARK.search(body):
            errors.append("Pull request body carries an attribution trailer or AI marker. Remove it (rules/workflow/committing.md).")
    if re.search(GIT + r"commit\b", masked):
        invocation = re.search(GIT + r"commit\b", command)
        message_file = file_text(command[invocation.end():], r"--file|-F", git_cwd(invocation.group(0), cwd))
        message = command + "\n" + (message_file or "")
        if TRAILER.search(message) or AI_MARK.search(message):
            errors.append("Commit message carries an attribution trailer or AI marker. Remove it (rules/workflow/committing.md).")
        subject = commit_subject(command)
        if subject is None and message_file:
            lines = [line for line in message_file.splitlines() if line.strip() and not line.startswith("#")]
            subject = lines[0].strip() if lines else None
        if subject is not None:
            if len(subject) > 72:
                errors.append(f"Commit subject is {len(subject)} chars; the limit is 72.")
            if not SUBJECT.match(subject):
                errors.append(f"Commit subject is not Conventional Commits `type[(scope)]: description`: {subject!r}")
    return errors


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    errors = check(command, payload.get("cwd") or os.getcwd())
    if errors:
        print("Blocked by ~/.claude/hooks/git_guard.py:\n- " + "\n- ".join(errors), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
