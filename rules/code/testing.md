---
paths:
  - "**/tests/**/*.ts"
  - "**/*.test.ts"
  - "**/vitest.config.ts"
---

# TypeScript Testing

TypeScript/Vitest conventions. Extends global `code/testing.md`.

---

## Test Design (TypeScript)

Vitest implementations of black-box test design:

### Equivalence partitioning + boundary analysis via test.for
```typescript
test.for([
  [0, false], // below minimum
  [1, true], // minimum boundary
  [6, true], // nominal (one per valid partition)
  [12, true], // maximum boundary
  [13, false], // above maximum
] as const)("month %i valid=%s", ([month, valid]) => {
  if (valid) {
    expect(validateMonth(month)).toBe(month);
  } else {
    expect(() => validateMonth(month)).toThrow(RangeError);
  }
});
```

---

## Layout

- Test root: `tests/` at repo root, outside `src/`. `src/<sub>/<module>.ts` is tested in `tests/<sub>/<module>.test.ts`. Global `code/testing.md` Layout owns the mirroring.
- Integration tests: `tests/<sub>/<module>.integration.test.ts`.
- Shared fixtures in `tests/fixtures.ts`, exported as an extended `test`. Test data files in `tests/data/`.

## Discovery

- Files: `*.test.ts`. Functions and hooks imported from `vitest`. No `globals: true`.
- `test()` only. No `it()` alias.
- `describe()` names the component. No nesting deeper than two levels.
- No shared mutable state at module scope of a test file.

## Naming

- `describe("<component>")` holding `test("<condition> <expected>")`: `test("month 13 throws RangeError")`.

## Fixtures

### Scope
- Test (default): per test.
- `file`: per test file. For setup shared across one file.
- `worker`: per worker. For read-only resources.

### Patterns
- `test.extend("<name>", async (ctx, { onCleanup }) => value)` for setup with teardown. The builder form infers fixture types.
- `fs.mkdtemp(path.join(os.tmpdir(), "<prefix>-"))` for a unique directory per test, removed through `onCleanup`.
- `vi.stubEnv` for environment variables, reverted by `unstubEnvs: true`.
- Fixtures return fresh objects to meet global `code/testing.md` Maintenance.

## Mocking

- Module doubles via `vi.mock(import("../src/<sub>/<module>.js"))`. The promise form types the factory against the real module and follows file moves.
- Typed access to a mocked export through `vi.mocked(fn)`. No `as` cast to a mock type.
- `vi.spyOn(obj, "method")` for an observed method on a real object.
- `vi.mock` is hoisted above imports. Variables a factory reads come from `vi.hoisted()`.
- `vi.useFakeTimers()` paired with `vi.useRealTimers()` in `afterEach`.

## Assertions

- `toBe` for primitives and identity. `toStrictEqual` for structures.
- `expect(() => fn()).toThrow(ErrorType)` with a field check through `toThrow(expect.objectContaining({ ... }))`.
- `await expect(promise).rejects.toThrow(ErrorType)` for async failures.
- `expect.assertions(n)` when assertions run inside callbacks.
- `toBeCloseTo` for floats.

## Parametrize

- `test.for` for data-driven tests. Each case is one array element; the callback receives it whole.
- `describe.for` for a fixture variant across a group of tests.

## Execution

- `npx vitest run --project unit` -- unit tests, the default `test` script.
- `npx vitest run --project integration` -- integration tests.
- `npx vitest run --bail=1` -- stop on first failure.
- `npx vitest run tests/<sub>/` -- one directory.
- `npx vitest run -t "<keyword>"` -- name match.
- `npx vitest run --project unit --coverage` -- branch coverage with missing lines; fails below `thresholds.branches`.

## Configuration

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    mockReset: true,
    restoreMocks: true,
    unstubEnvs: true,
    projects: [
      { test: { name: "unit", include: ["tests/**/*.test.ts"], exclude: ["tests/**/*.integration.test.ts"] } },
      { test: { name: "integration", include: ["tests/**/*.integration.test.ts"] } },
    ],
    coverage: {
      provider: "v8",
      include: ["src/**/*.ts"],
      reporter: ["text", "json-summary"],
      thresholds: { branches: 90 },
    },
  },
});
```
