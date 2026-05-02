# Global Agent Rules

Reusable Claude Code rules, organized by domain. Language-independent.

## Structure

```
.claude/
├── CLAUDE.md               # This file — global overview
├── skills/
│   ├── commit/SKILL.md     # /commit — full commit workflow
│   ├── review-code/SKILL.md # /review-code — code quality review workflow
│   ├── perf/SKILL.md       # /perf — performance optimization pipeline
│   ├── debug/SKILL.md      # /debug — reproduce-first bug fix protocol
│   ├── review-docs/SKILL.md # /review-docs — docs audit against type rules
│   └── update-tests/SKILL.md # /update-tests — design-driven test coverage audit
└── rules/
    ├── rulewriting.md      # How to write rule files (always active)
    │
    ├── code/               # Writing code
    │   ├── quality.md      # Code quality standards (scoped to code files)
    │   ├── testing.md      # Testing standards (scoped to test files)
    │   └── debugging.md    # Debugging guardrails (scoped to code + test files)
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
        ├── committing.md   # Git commit guardrails (always active, minimal)
        ├── change-policy.md # API change and verification rules (always active)
        ├── git-safety.md   # Multi-agent git safety rules (always active)
        ├── performance.md  # Performance optimization guardrails (scoped to perf files)
        └── skilling.md     # Skill authoring standards (scoped to SKILL.md, skills/)
```

`rulewriting.md`, `workflow/committing.md`, `workflow/change-policy.md`, and `workflow/git-safety.md` have no `paths:` — always active. Other rules use `paths:` frontmatter to activate only when working with matching files.

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/commit` | User asks to commit | Full staging, classification, multi-commit workflow |
| `/review-code` | User asks to review or verify code | detekt + tests + build + code smell scan |
| `/perf` | User asks to optimize or benchmark | 8-step measurement-driven optimization pipeline |
| `/debug` | User reports a bug or test failure | Reproduce-first investigation and fix protocol |
| `/review-docs` | User asks to review documentation | Audit docs/ against idea/model/design/spec/impl/todo/index rules |
| `/update-tests` | User asks to add, audit, or update tests | Design-driven coverage audit, add missing, remove stale |

Skills are active procedures. Rules are passive guardrails. Both layers enforce the same standards.
