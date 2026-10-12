#!/usr/bin/env python3
"""PreToolUse hook for Bash: blocks the git operations of rules/workflow/git-safety.md
and commit messages that break rules/workflow/committing.md.

Exit 2 blocks the call; stderr is the reason Claude reads.
"""
import json
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
AI_MARK = re.compile(r"Generated with \[Claude Code\]|noreply@anthropic\.com", re.I)
SUBJECT = re.compile(r"^[a-z]+(\([^)]+\))?!?: \S")
HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\s*\1\b", re.S)
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")


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


def check(command):
    """Return the list of violation messages for one Bash command."""
    masked = mask(command)
    errors = [reason for pattern, reason in PROHIBITED if re.search(pattern, masked)]
    if re.search(GIT + r"commit\b", masked):
        if TRAILER.search(command) or AI_MARK.search(command):
            errors.append("Commit message carries an attribution trailer or AI marker. Remove it (rules/workflow/committing.md).")
        subject = commit_subject(command)
        if subject is not None:
            if len(subject) > 72:
                errors.append(f"Commit subject is {len(subject)} chars; the limit is 72.")
            if not SUBJECT.match(subject):
                errors.append(f"Commit subject is not Conventional Commits `type[(scope)]: description`: {subject!r}")
    return errors


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    errors = check(command)
    if errors:
        print("Blocked by ~/.claude/hooks/git_guard.py:\n- " + "\n- ".join(errors), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
