# Project Rules

Rust project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add Rust-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md               # This file
└── rules/
    ├── code/               # Writing code
    │   ├── quality.md      # Rust code quality, lints, and toolchain (*.rs)
    │   ├── constants.md    # Value placement: constant vs config struct vs data file (*.rs)
    │   ├── organization.md # Crate and module naming, package layout, workspaces, entry points (*.rs, Cargo.toml)
    │   ├── testing.md      # cargo test and rstest conventions (test files)
    │   └── debugging.md    # Rust debugging tools (*.rs, test files)
    │
    ├── docs/               # Writing documentation
    │   ├── design.md       # Rust design standards (design.md, design-*.md)
    │   ├── impl.md         # Rust impl.md conventions (impl.md, impl-*.md)
    │   ├── readme.md       # Rust README badge set (README.md)
    │   └── todo.md         # Rust task conventions (todo.md)
    │
    └── workflow/           # Operational processes
        ├── committing.md   # Project commit and push rules
        └── releasing.md    # Release standards by crate type (Cargo.toml, Cargo.lock, workflows)
```

Rules use `paths:` frontmatter to load only when working with matching files.

## Workflow

- No summary/README generation after task completion. Update existing files only.
