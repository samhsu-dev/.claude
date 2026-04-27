# Project Rules

Python project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add Python-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md               # This file
└── rules/
    ├── code/               # Writing code
    │   ├── quality.md      # Python code quality and toolchain (*.py)
    │   ├── testing.md      # Pytest conventions (test files)
    │   └── debugging.md    # Python debugging tools (*.py, test files)
    │
    ├── docs/               # Writing documentation
    │   ├── design.md       # Python design standards (*design.md)
    │   ├── impl.md         # Python impl.md conventions (*impl.md)
    │   └── todo.md         # Python task conventions (todo.md)
    │
    └── workflow/           # Operational processes
        └── committing.md   # Project commit and push rules
```

Rules use `paths:` frontmatter to load only when working with matching files.

## Workflow

- No summary/README generation after task completion. Update existing files only.
