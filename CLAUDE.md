# Project Rules

TypeScript project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add TypeScript-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md               # This file
└── rules/
    ├── code/               # Writing code
    │   ├── quality.md      # TypeScript code quality and toolchain (*.ts, *.tsx)
    │   ├── constants.md    # Value placement: constant vs config vs data file (*.ts)
    │   ├── organization.md # File naming, package layout, workspaces, entry points (*.ts, *.tsx)
    │   ├── testing.md      # Vitest conventions (test files)
    │   └── debugging.md    # TypeScript debugging tools (*.ts, test files)
    │
    ├── docs/               # Writing documentation
    │   ├── design.md       # TypeScript design standards (design.md, design-*.md)
    │   ├── impl.md         # TypeScript impl.md conventions (impl.md, impl-*.md)
    │   ├── readme.md       # npm badge set and placement (README.md)
    │   └── todo.md         # TypeScript task conventions (todo.md)
    │
    └── workflow/           # Operational processes
        ├── committing.md   # Project commit and push rules
        └── releasing.md    # Release standards by distribution type (package.json, lockfiles, workflows)
```

Rules use `paths:` frontmatter to load only when working with matching files.

## Workflow

- No summary/README generation after task completion. Update existing files only.
