---
paths:
  - "**/llms.txt"
  - "**/llms/*.md"
  - "**/llms/full.txt"
---

# LLM-Consumable Documentation Standards

Agent-facing documentation following the llms.txt specification (llmstxt.org).

---

## Audience

All llms.txt content is read by agents, not humans. Optimize for parsing under token constraints.

## File Layout

```
docs/
├── llms.txt          # L0 index — always loaded first
├── llms/             # L1 module docs — loaded on demand
│   ├── <module>.md   # One file per module/component
│   └── full.txt      # L2 all L1 content inlined — single-load option
```

- `llms.txt` is the entry point. Agents read this first.
- `llms/<module>.md` files are referenced from `llms.txt` via Markdown links.
- `llms/full.txt` concatenates `llms.txt` + all `llms/*.md` content. Regenerate on any change.

## llms.txt Structure (L0 Index)

Sections in order (llmstxt.org spec):

| Element | Required | Content |
|---------|----------|---------|
| `# Title` (H1) | Yes | Project name. One H1 only. |
| `> Blockquote` | Yes | One-sentence project purpose. |
| Body paragraphs | No | Key context an agent needs before reading links. No headings. |
| `## Instructions for Agents` | Yes | Behavioral directives: use X, never Y, call Z before W. |
| `## <Topic>` sections | Yes | Categorized link lists to L1 module docs. |
| `## Optional` | No | Links an agent can skip when context budget is limited. |

### Link format

```
- [Display Name](llms/<module>.md): One-line purpose.
```

- Relative paths from `llms.txt` location.
- Every link targets a file in `llms/` or another `docs/` file.
- No external URLs in link lists. External references go in L1 files.

### Instructions for Agents section

- Imperative mood. One directive per bullet.
- State the action, not the reason. "Use `model_lean.yaml` for simple apps." Not "Because simple apps have fewer variables, you should consider using the lean model."
- Include function/class names with backticks.
- Group by: what to call, what to configure, what to never do.

## Module Docs Structure (L1)

Each `llms/<module>.md` file:

| Section | Content |
|---------|---------|
| `# <Module Name>` (H1) | Module identifier. |
| `> Blockquote` | One-line responsibility. |
| `## Quick Start` | Minimal code to use this module (3-10 lines). |
| `## API` | One entry per public function/class. |
| `## Configuration` | Parameters, env vars, file paths. |
| `## Gotchas` | Non-obvious behavior, common mistakes, version constraints. |

### API entry format

```
**`function_name(param: Type) -> ReturnType`** — One-line purpose. Raises `ErrorType` when condition.
```

- Signature includes types. No docstring duplication.
- One line per function. No multi-line explanations.
- Group by: constructors, methods, helpers.

### Code examples

- One example per concept. 3-10 lines. No boilerplate.
- Working code only. Every example is copy-paste runnable.
- No comments explaining what the next line does. Code is self-evident or the example is wrong.

## full.txt Structure (L2)

- Starts with `llms.txt` content verbatim.
- Separator: `\n\n---\n\n# Referenced Documents\n\n`
- Each inlined file: `## Source: llms/<module>.md\n\n<content>\n\n---\n\n`
- Truncate files over 200 lines with `... (truncated, N total lines)`.
- Regenerate with a script. Never hand-edit.

## Language Rules

- No modifiers: no "properly", "easily", "simply", "just".
- No softeners: no "you might want to", "consider using", "it's recommended".
- No hedging: no "usually", "typically", "in most cases".
- Imperative for instructions: "Call X." Not "You should call X."
- Declarative for facts: "X returns Y." Not "X will return Y."
- Backticks for all code identifiers: functions, classes, parameters, file paths.

## Content Rules

- No prose paragraphs in L0 or L1. Lists and tables only. Exception: L0 body text (max 3 sentences).
- No redundancy between L0 and L1. L0 says what exists; L1 says how to use it.
- Update `full.txt` after every change to `llms.txt` or any `llms/*.md`.

### Include (Usage-Facing)
- What to call: function signatures, class constructors, CLI commands.
- What to pass: parameter names, types, valid ranges, defaults.
- What comes back: return types, response shapes, error codes.
- What to configure: env vars, config files, required setup steps.
- What order: workflows, call sequences, prerequisite dependencies.
- What to avoid: known pitfalls, invalid inputs, deprecated paths.

### Exclude (Internal Details)
- No algorithm descriptions — "Sorts results by relevance." not "Uses TF-IDF with BM25 ranking."
- No data structure internals — "Accepts a config object." not "Config is stored as a nested dict with keys X, Y, Z."
- No infrastructure — no container names, host paths, port mappings, process managers, orchestration details.
- No storage schemas — no database tables, column names, index strategies, migration history.
- No internal control flow — no "first it checks X, then loops over Y, then calls Z."
- No concurrency/threading model — "Thread-safe." not "Uses a read-write lock with writer preference."
- No performance characteristics — no Big-O, benchmark numbers, cache strategies, batch sizes.
- No internal error handling — "Raises `ConfigError` on invalid input." not "Catches `KeyError` internally and wraps it."
- No dependency justifications — no "uses library X because Y." State the public dependency, not why.
- No source file paths or line numbers. The agent calls the API, not the source.
- No version history or changelogs.
- No links to external documentation unless the external API is required for usage.

### Litmus Test
For every sentence: "Does the caller need this to use the API correctly?" No → remove.

## Verification

- Every link in `llms.txt` resolves to an existing file.
- Every `llms/*.md` file is referenced from `llms.txt`.
- `full.txt` matches the concatenation of `llms.txt` + all referenced files.
- No file exceeds 200 lines.
