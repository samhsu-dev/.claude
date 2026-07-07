# Global Agent Rules

Reusable Claude Code rules, organized by domain. Language-independent.

## Structure

```
.claude/
├── CLAUDE.md               # This file — global overview
├── skills/
│   ├── commit/SKILL.md     # /commit — full commit workflow
│   ├── update-codes/SKILL.md # /update-codes — audit, plan, and fix code quality
│   ├── perf/SKILL.md       # /perf — performance optimization pipeline
│   ├── debug/SKILL.md      # /debug — reproduce-first bug fix protocol
│   ├── update-docs/SKILL.md # /update-docs — audit, plan, and fix documentation
│   └── update-tests/SKILL.md # /update-tests — design-driven test coverage audit
└── rules/
    ├── meta/               # Authoring .claude assets
    │   ├── rulewriting.md  # How to write rule files (always active)
    │   └── skilling.md     # Skill authoring standards (scoped to SKILL.md, skills/)
    │
    ├── code/               # Writing code
    │   ├── quality.md      # Code quality standards (scoped to code files)
    │   ├── resource-bounds.md # Timeout, liveness, and bound-the-input rules (always active)
    │   ├── logging.md      # Logging standards (scoped to code files)
    │   ├── organization.md # File naming and organization (scoped to code files)
    │   ├── testing.md      # Testing standards (scoped to test files)
    │   ├── debugging.md    # Debugging guardrails (scoped to code + test files)
    │   └── resource-bounds.md # Timeout, liveness, and bound-the-input rules (always active)
    │
    ├── docs/               # Writing documentation
    │   ├── concept.md      # Concept doc format (scoped to concept.md, concept-*.md)
    │   ├── model.md        # Domain model doc format (scoped to model.md, model-*.md)
    │   ├── design.md       # Design doc format (scoped to design.md, design-*.md)
    │   ├── spec.md         # Algorithm spec format (scoped to spec.md, spec-*.md)
    │   ├── impl.md         # Implementation doc format (scoped to impl.md, impl-*.md)
    │   ├── index.md        # Index/navigation doc format (scoped to index.md)
    │   ├── todo.md         # Task doc format (scoped to todo.md)
    │   ├── readme.md       # README format (scoped to README.md)
    │   └── llms.md         # LLM-consumable doc format (scoped to llms.txt, llms/*.md)
    │
    ├── prompt/             # Writing LLM-agent prompts
    │   └── prompting.md    # Prompt construction standards (scoped to *.prompty, prompts/)
    │
    └── workflow/           # Operational processes
        ├── committing.md   # Git commit guardrails (always active, minimal)
        ├── change-policy.md # API change and verification rules (always active)
        ├── development.md  # Development phase pipeline (always active)
        ├── git-safety.md   # Multi-agent git safety rules (always active)
        └── performance.md  # Performance optimization guardrails (scoped to perf files)
```

`meta/rulewriting.md`, `code/resource-bounds.md`, `workflow/committing.md`, `workflow/change-policy.md`, `workflow/development.md`, and `workflow/git-safety.md` have no `paths:` — always active. Other rules use `paths:` frontmatter to activate only when working with matching files.

## Documentation Naming

Documents split by responsibility use prefix naming:

| Type | Single file | Split by concern |
|------|-------------|------------------|
| Concept | `concept.md` | `concept-{concern}.md` |
| Domain Model | `model.md` | `model-{concern}.md` |
| Design | `design.md` | `design-{concern}.md` |
| Spec | `spec.md` | `spec-{concern}.md` |
| Implementation | `impl.md` | `impl-{concern}.md` |

Each split file follows the same rules as its single-file counterpart. One concern per file.

Single doc file: 200 lines max. Exceeds limit → split by concern using prefix naming above. When a single concern still exceeds the limit, append numeric index: `concept-{concern}-{index}.md` (e.g., `design-auth-1.md`, `design-auth-2.md`).

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/commit` | User asks to commit | Full staging, classification, multi-commit workflow |
| `/update-codes` | User asks to update or fix code quality | Audit, plan fixes, apply after approval |
| `/update-docs` | User asks to update or fix documentation | Audit against type rules, plan fixes, apply after approval |
| `/update-tests` | User asks to add, audit, or update tests | Design-driven coverage audit, add missing, remove stale |
| `/perf` | User asks to optimize or benchmark | 8-step measurement-driven optimization pipeline |
| `/debug` | User reports a bug or test failure | Reproduce-first investigation and fix protocol |

Skills are active procedures. Rules are passive guardrails. Both layers enforce the same standards.
