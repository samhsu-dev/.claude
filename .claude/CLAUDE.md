# Agent Rules

A collection of reusable Claude Code rules, organized by topic and file type.

## Structure

```
.claude/
├── CLAUDE.md           # This file — project overview
└── rules/
    ├── codequality.md  # Source code quality (scoped to code files)
    ├── designing.md    # Design doc standards (scoped to design.md)
    ├── implementing.md # Implementation doc standards (scoped to *implementation.md)
    ├── tasking.md      # Task management standards (scoped to todo.md)
    ├── idea.md         # Idea/concept doc standards (scoped to idea.md)
    ├── testing.md      # Testing standards (scoped to test files)
    └── debugging.md    # Debugging standards (scoped to test files)
```

All rules in `rules/` use `paths:` frontmatter to activate only when working with matching files.
