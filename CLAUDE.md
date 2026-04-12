# Global Agent Rules

Reusable Claude Code rules, organized by topic and file type. Language-independent.

## Structure

```
.claude/
├── CLAUDE.md           # This file — global overview
└── rules/
    ├── rulewriting.md  # How to write rule files (always active)
    ├── codequality.md  # Source code quality (scoped to code files)
    ├── committing.md   # Git commit standards (always active)
    ├── designing.md    # Design doc standards (scoped to design.md)
    ├── implementing.md # Implementation doc standards (scoped to *implementation.md)
    ├── tasking.md      # Task management standards (scoped to todo.md)
    ├── idea.md         # Idea/concept doc standards (scoped to idea.md)
    ├── readme.md       # README standards (scoped to README.md)
    ├── testing.md      # Testing standards (scoped to test files)
    ├── debugging.md    # Debugging standards (scoped to test files)
    ├── performance.md  # Performance optimization pipeline (scoped to perf files)
    ├── llm-guiding.md  # Agent-consumable documentation (scoped to llms.txt, llms/*.md)
    └── skilling.md     # Skill authoring standards (scoped to SKILL.md, .claude/skills/)
```

`rulewriting.md` and `committing.md` have no `paths:` — always active. Other rules use `paths:` frontmatter to activate only when working with matching files.

## Python Toolchain

- Always use `uv run` to execute Python commands (e.g., `uv run python`, `uv run pytest`, `uv run mypy`).
- Always use `uv` to manage Python project dependencies (e.g., `uv add`, `uv remove`, `uv sync`). Never use `pip install` or `pip` directly.
