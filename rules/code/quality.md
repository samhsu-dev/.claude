---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript Code Quality

TypeScript-specific rules and toolchain. Google TypeScript Style Guide / TS handbook / typescript-eslint strict.

---

## Naming

- UpperCamelCase: classes, interfaces, type aliases, enums, type parameters.
- lowerCamelCase: variables, parameters, functions, methods, properties.
- CONSTANT_CASE: module-level constants and enum members.
- No underscore prefix or suffix. No Hungarian notation. No I-prefix on interfaces.
- Acronyms as words: loadHttpUrl, not loadHTTPURL.

## Imports and Exports

- Named exports only. No default exports.
- import type { X } for type-only imports. verbatimModuleSyntax enforces it.
- Relative imports for internal modules, with explicit .js extension under NodeNext resolution.
- Import groups: node: builtins, third-party, local -- blank line between each.
- ES module syntax only. No namespace, no require, no import x = require().

## Error Handling

- Throw Error subclasses only. Never strings or plain objects.
- new Error(msg, { cause: exc }) to chain.
- Domain errors with structured fields. Defined in errors.ts.
- catch binds unknown. Narrow before use.
- try blocks cover minimum code. An intentionally empty catch carries a comment stating why.

## TypeScript Idioms

- === / !==. Exception: == null to match null and undefined together.
- ?? for defaulting. Not ||.
- ?. over nested existence guards.
- interface for object types. type for unions, tuples, mapped and conditional types.
- foo?: T over foo: T | undefined. Type aliases never bake in | null / | undefined.
- as const array plus derived union for finite value sets. enum permitted; const enum never.
- T[] for simple element types. Array<T> for complex ones.
- for...of for arrays. Unfiltered for...in never.
- function declarations for named functions. Arrow functions for callbacks and expressions.
- Primitive types lowercase: string, number, boolean. Wrapper types String/Number/Boolean/Object never.

## Async

- async/await. Not .then chains.
- No floating promises: every promise is awaited, returned, or explicitly discarded with void.
- Arrays of promises go through Promise.all / allSettled / race.
- No async callback passed where a void return is expected.

## No Weak Types

- No any. unknown for values held but not inspected, narrowed before use.
- No non-null assertion (!). No as assertion without a comment stating the invariant that makes it safe.
- External data (HTTP bodies, files, env, queue messages) parsed at the boundary via schema (zod). Types derive from schemas: z.infer<typeof schema>.

## Classes

- private / protected modifiers. No #private fields. No explicit public.
- Parameter properties for constructor assignment. No empty constructors.
- readonly on every property never reassigned outside the constructor.
- Getters are pure and O(1). An accessor without added logic becomes a plain property.
- Module-local functions over private static methods.

## Docs (TSDoc)

- /** ... */ for every top-level export. // for implementation comments.
- No types in @param / @returns. TypeScript carries them.
- No tag restating a keyword: no @private, @override, @enum.
- @deprecated includes the replacement for call sites.

## Disallowed

- var, with, eval, Function(...) constructor.
- debugger statements in committed code.
- Mutating builtins or prototypes.
- Defining decorators. Framework-supplied decorators only.
- Relying on automatic semicolon insertion. Semicolons required.

---

## Compiler Options

- Base: @tsconfig/strictest -- strict, noUncheckedIndexedAccess, exactOptionalPropertyTypes, noImplicitOverride, noImplicitReturns, noFallthroughCasesInSwitch, noUnusedLocals, noUnusedParameters, isolatedModules.
- verbatimModuleSyntax: true.
- Node code: module and moduleResolution nodenext. Bundled code: module preserve, moduleResolution bundler. Published libraries never use bundler resolution.

## Quality Workflow

### Before editing
- eslint <target> -- check existing violations.

### After editing
- prettier --write <target>.
- eslint <target> -- zero violations.
- tsc --noEmit.
- vitest run -- all pass.

---

## Toolchain

Run tools through the repo package manager (npx / pnpm exec). Lockfile determines the manager: package-lock.json -> npm, pnpm-lock.yaml -> pnpm. Never mix lockfiles.

| Tool | Command | Purpose |
|------|---------|---------|
| prettier | prettier --write | Formatter |
| eslint + typescript-eslint | eslint . | Linter, flat config, strictTypeChecked + stylisticTypeChecked |
| tsc | tsc --noEmit | Type checker (@tsconfig/strictest base) |
| vitest | vitest run | Test runner |
| zod | -- | Boundary validation |
