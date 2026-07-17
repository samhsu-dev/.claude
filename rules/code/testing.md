---
paths:
  - "**/*test*"
  - "**/*.spec.ts"
---

# TypeScript Testing

TypeScript/Vitest conventions.

---

## Test Design (TypeScript)

Vitest implementations of black-box test design:

### Equivalence partitioning + boundary analysis via test.each
test.each([
  [0, false],   // below minimum
  [1, true],    // minimum boundary
  [6, true],    // nominal (one per valid partition)
  [12, true],   // maximum boundary
  [13, false],  // above maximum
])('validateMonth(%i) valid=%s', (month: number, valid: boolean) => {
  if (valid) {
    expect(validateMonth(month)).toBe(month);
  } else {
    expect(() => validateMonth(month)).toThrowError(RangeError);
  }
});

---

## Layout

- tests/ at repo root, mirroring src/: src/a/b/foo.ts -> tests/a/b/foo.test.ts.
- Shared setup in tests/helpers/. Loaded explicitly by import, or globally via test.setupFiles for cross-cutting hooks.

## Discovery

- Files: <component>.test.ts. Integration tests: <component>.integration.test.ts, excluded from the default run.
- test() at top level. it() only inside describe() blocks.
- describe() groups one component's behavior families. No nesting deeper than two levels.
- No test classes. No shared mutable state at module scope of a test file.

## Fixtures

- test.extend({ fixture: async ({}, use) => { ...setup; await use(value); ...teardown; } }) for reusable setup with teardown.
- beforeEach/afterEach for per-test hooks. beforeAll only for read-only resources.
- Fixtures return fresh objects per test. No shared mutable state.
- Temporary files via fs.mkdtemp(os.tmpdir()). Removed in teardown.

## Mocking

- vi.fn() for standalone mock functions. vi.spyOn(obj, 'method') for observed methods.
- vi.mock('./module') for module replacement. Hoisted above imports; shared variables via vi.hoisted().
- Partial mock: vi.mock(import('./mod'), async (orig) => ({ ...await orig(), fn: vi.fn() })).
- restoreMocks: true in config. No manual mock cleanup in tests.
- vi.useFakeTimers() paired with vi.useRealTimers() in afterEach. vi.setSystemTime() never leaks across tests.
- Mock at system boundaries only. Real behavior for internal collaborators.

## Assertions

- toBe for primitives and reference identity. toEqual for structural equality. toStrictEqual when undefined-vs-missing matters.
- expect(() => fn()).toThrowError(ErrorType) with message or field check.
- await expect(promise).rejects.toThrowError(ErrorType) for async failures.
- expect.assertions(n) in tests where assertions run inside callbacks.
- toBeCloseTo for floats.

## Execution

- vitest run -- all unit tests, single pass.
- vitest run --bail=1 -- stop on first failure.
- vitest run tests/<subdir>/ -- one directory.
- vitest run -t "keyword" -- name match.
- vitest run --coverage -- V8 coverage via @vitest/coverage-v8.

## Configuration

// vitest.config.ts
export default defineConfig({
  test: {
    include: ['tests/**/*.test.ts'],
    exclude: ['tests/**/*.integration.test.ts'],
    restoreMocks: true,
  },
});
