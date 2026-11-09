#!/usr/bin/env python3
"""PreToolUse hook for Bash: blocks a polling loop, an `until` or `while` loop whose body sleeps,
the rule of rules/workflow/multi-agent.md.

A loop that waits on a process by matching its command line can match its own shell and never
end; any polling loop holds a shell and spends turns on unchanged state. The awaited command runs
in the foreground, or as a tracked background run whose completion notifies the caller.

Quoted text and heredoc bodies are masked first, so a loop written inside a message or a file
body never matches. Exit 2 blocks the call; stderr is the reason the agent reads.
"""
import json
import re
import sys

HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n\s*\1\b", re.S)
QUOTED = re.compile(r"'[^']*'|\"(?:\\.|[^\"\\])*\"")
LOOP = re.compile(r"(?:^|[;&|(\s])(?:until|while)\s.*?(?:;|\n)\s*do\b.*?\bsleep\b", re.S)

REASON = (
    "Polling loop blocked (until/while with sleep). Run the awaited command itself in the "
    "foreground, or as a background run with completion notification (Bash run_in_background), "
    "and act on the notification. To wait on external state the host cannot notify about, use "
    "the host's monitor or scheduled wakeup."
)


def mask(command):
    """Replace heredoc bodies and quoted strings with a token so message text never matches."""
    return QUOTED.sub(" Q ", HEREDOC.sub(" Q ", command))


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    if LOOP.search(mask(command)):
        print(REASON, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
