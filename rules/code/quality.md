---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript Code Quality

TypeScript-specific rules and toolchain. Extends global `code/quality.md`. Google TypeScript Style Guide / TypeScript handbook / typescript-eslint `strictTypeChecked`.

---

## Naming

- `UpperCamelCase` classes, interfaces, type aliases, type parameters and closed-set objects (`rules/docs/design.md` Type Selection). `lowerCamelCase` functions, methods, variables, parameters and properties. `CONSTANT_CASE` module-level constants and closed-set members.
- Acronyms as words: `loadHttpUrl`, not `loadHTTPURL`.
- No `_` prefix or suffix, no `I` prefix on interfaces, no Hungarian notation.

## Formatting

- Layout is the `prettier --write` output with default options: 80-character lines, double quotes, 2-space indentation, semicolons, trailing commas. No `.prettierrc` overrides.

## Imports and Exports

- Named exports only. `no-restricted-exports` with every `restrictDefaultExports` option checks it. Exception: a tool config file whose tool reads the default export (`eslint.config.js`, `vitest.config.ts`).
- Relative imports for internal modules, with the `.js` extension of the emitted file: `./parser.js`. A directory import names its index file: `./parser/index.js`.
- `import type` for type-only imports. `verbatimModuleSyntax` checks it.
- Groups: `node:` builtins, third-party, local -- blank line between each. Builtins always carry the `node:` prefix.
- ES module syntax only. No `require`, no `import x = require()`, no `namespace`.
- No circular imports. dependency-cruiser `no-circular` checks it. A cycle is fixed at module structure level, never with a dynamic `import()`.

## Error Handling

- Throw `Error` subclasses only. `@typescript-eslint/only-throw-error` checks it.
- `new DomainError(msg, { cause: err })` to chain. Never drop the caught error.
- `catch (err: unknown)`; narrow with `instanceof` before use.
- `try` blocks cover minimum code.

## TypeScript Idioms

- `===` / `!==`. Exception: `== null` matches `null` and `undefined` together.
- `??` for defaulting, `?.` for optional access. Not `||` or nested guards.
- `interface` for object shapes. `type` for unions, tuples, mapped and conditional types.
- `foo?: T` for an optional property. A type alias never bakes in `| undefined`.
- `T[]` for simple element types. `readonly T[]` for parameters the function does not mutate.
- `for...of` for iteration. No `for...in` on arrays.
- `function` declarations for named functions. Arrow functions for callbacks.
- A `switch` over a closed set handles every member. `@typescript-eslint/switch-exhaustiveness-check` checks it.

## Async

- `async`/`await`. Not `.then` chains.
- Every promise is awaited, returned, or discarded with `void`. `@typescript-eslint/no-floating-promises` checks it.
- Independent promises run together through `Promise.all` / `Promise.allSettled`.
- A caller-cancellable operation takes an `AbortSignal` and passes it to every I/O call.

## Performance Idioms

- `Set` / `Map` for membership and keyed lookup. Not `Array.includes` in a loop, not a plain object as a dictionary.
- `array.join("")` for strings built in a loop.
- `Object.freeze` / `as const` for fixed data.

## Resource Management

- `using` / `await using` with `Symbol.dispose` / `Symbol.asyncDispose` for resource lifecycle. `try`/`finally` for an API without a dispose method.
- Memoization of a pure function in a `Map` keyed by its argument, owned by the module that owns the function.

## Types

- `@tsconfig/strictest` plus the runtime base (`rules/workflow/releasing.md` All Distributions) in `tsconfig.json` `extends`.
- `erasableSyntaxOnly: true`: no `enum`, no runtime `namespace`, no parameter properties, no `import =`.
- `verbatimModuleSyntax: true`. `types` lists every ambient package (`["node"]`).
- Node code: `module` `nodenext`. Bundled browser code: `module` `preserve`, `moduleResolution` `bundler`. A published library never uses bundler resolution.
- `readonly` on every property and parameter array the code does not mutate.

## No Weak Types

- No `any`, no non-null `!`. `strictTypeChecked` checks both. `unknown` for values held but not inspected.
- No `as` assertion without a comment stating the invariant that makes it safe. Exception: `as const`.
- External data (HTTP bodies, files, env, queue messages) is parsed at the boundary through a zod schema: `import * as z from "zod"`. The type derives from the schema: `type User = z.infer<typeof User>`.
- `satisfies` for a typed constant that keeps its literal type.

## Classes

- `private` / `protected` / `readonly` modifiers. No `#private` fields, no explicit `public`.
- Constructor assigns fields explicitly. No parameter properties (`erasableSyntaxOnly`).
- Getters are pure and O(1). An accessor without logic becomes a plain property.
- Module-local functions over private static methods.
- No decorator definitions. Framework-supplied decorators only.

## Docs (TSDoc)

- `/** ... */` on every exported symbol: summary sentence, `@param name - description`, `@returns`, `@throws {ErrorType}`.
- No types in tags. TypeScript carries them.
- No tag restating a keyword: no `@private`, `@override`, `@enum`.
- `@deprecated` names the replacement.

## Disallowed

- `var`, `with`, `eval`, `new Function(...)`, `const enum`.
- Mutating builtins or prototypes.
- `debugger` and `console.*` in committed code. ESLint `no-debugger` and `no-console` check them. Exception: a CLI's user-facing output module.

---

## Quality Workflow

### Before editing
- `npx eslint <target>` -- check existing violations.

### After editing
- `npx prettier --write <target>`.
- `npx eslint <target>` -- zero violations.
- `npx tsc --noEmit`.
- `npx depcruise src` -- zero violations.
- `npx vitest run` -- all pass.

---

## Toolchain

Run tools through the repository package manager: `npx` under npm, `pnpm exec` under pnpm.

| Tool | Command | Purpose |
|------|---------|---------|
| prettier | `prettier --write` | Formatter |
| eslint + typescript-eslint | `eslint .` | Linter: `eslint.config.js` through `defineConfig` from `eslint/config`, `strictTypeChecked` + `stylisticTypeChecked`, `parserOptions.projectService: true` |
| typescript | `tsc --noEmit` | Type checker. The `typescript` version satisfies the typescript-eslint `peerDependencies` range |
| dependency-cruiser | `depcruise src` | Import graph: `no-circular` and the project's layer rules in `.dependency-cruiser.js` |
| vitest + @vitest/coverage-v8 | `vitest run --coverage` | Test runner and branch coverage report |
| zod | -- | Boundary validation |
