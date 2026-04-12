# Project Rules

Python project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add Python-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md           # This file
└── rules/
    ├── codequality.md  # Python code quality and toolchain (*.py)
    ├── committing.md   # Project commit, push, and PR rules
    ├── designing.md    # Python design standards (design.md)
    ├── implementing.md # Implementation doc standards (*implementation.md)
    ├── tasking.md      # Task management standards (todo.md)
    ├── testing.md      # Testing standards (test files)
    └── debugging.md    # Debugging standards (test files)
```

Rules use `paths:` frontmatter to load only when working with matching files.
