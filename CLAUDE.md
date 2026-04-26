# Global Agent Rules

Reusable Claude Code rules, organized by domain. Language-independent.

## Structure

```
.claude/
├── CLAUDE.md               # This file — global overview
└── rules/
    ├── rulewriting.md      # How to write rule files (always active)
    │
    ├── code/               # Writing code
    │   ├── quality.md      # Code quality standards (scoped to code files)
    │   ├── testing.md      # Testing standards (scoped to test files)
    │   └── debugging.md    # Debugging standards (scoped to code + test files)
    │
    ├── docs/               # Writing documentation
    │   ├── concept.md      # Concept doc format (scoped to idea.md)
    │   ├── model.md        # Domain model doc format (scoped to *model.md)
    │   ├── design.md       # Design doc format (scoped to *design.md)
    │   ├── spec.md         # Algorithm spec format (scoped to spec.md)
    │   ├── impl.md         # Implementation doc format (scoped to *impl.md)
    │   ├── index.md        # Index/navigation doc format (scoped to index.md)
    │   ├── todo.md         # Task doc format (scoped to todo.md)
    │   ├── readme.md       # README format (scoped to README.md)
    │   └── llms.md         # LLM-consumable doc format (scoped to llms.txt, llms/*.md)
    │
    └── workflow/           # Operational processes
        ├── committing.md   # Git commit + PR standards (always active)
        ├── change-policy.md # API change and verification rules (always active)
        ├── performance.md  # Performance optimization pipeline (scoped to perf files)
        └── skilling.md     # Skill authoring standards (scoped to SKILL.md, skills/)
```

`rulewriting.md`, `workflow/committing.md`, and `workflow/change-policy.md` have no `paths:` — always active. Other rules use `paths:` frontmatter to activate only when working with matching files.
