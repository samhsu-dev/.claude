---
paths:
  - "**/*Test.kt"
  - "**/*test*.kt"
  - "**/src/test/**"
---

# Kotlin Testing

Kotlin/JUnit 5 conventions.

---

## Test Design (Kotlin)

JUnit 5 implementations of black-box test design:

### Equivalence partitioning + boundary analysis via parameterized tests
```kotlin
@ParameterizedTest
@CsvSource("0, false", "1, true", "6, true", "12, true", "13, false")
fun `validate month boundary`(month: Int, valid: Boolean) {
    if (valid) {
        assertEquals(month, validateMonth(month))
    } else {
        assertThrows<IllegalArgumentException> { validateMonth(month) }
    }
}
```

---

## Layout

- Test root: `src/test/kotlin/`. Global `code/testing.md` owns source-tree mirroring.
- Files: `{ClassName}Test.kt`.

## Discovery

- Classes annotated or containing `@Test` / `@ParameterizedTest` methods.
- Test classes marked `internal`.
- No inheritance-based test suites. Plain classes with annotated methods.

## Setup and Fixtures

- `lateinit var` for test fixtures initialized in `@BeforeEach`. Avoids nullable types.
- `@BeforeAll` / `@AfterAll` in `companion object` with `@JvmStatic`.
- Use `@TempDir` for the temporary-resource contract in global `code/testing.md`.
- Use fresh fixture objects per test to meet global `code/testing.md` Maintenance.

```kotlin
internal class ParserTest {
    private lateinit var parser: Parser

    @BeforeEach
    fun setUp() {
        parser = Parser()
    }
}
```

## Assertions

- `assertEquals(expected, actual)` -- expected first.
- `assertThrows<ExceptionType> { block }` for error cases.
- `assertAll` for grouped assertions verifying one behavior.
- `kotlin.test.assertFailsWith<T>` as Kotlin-idiomatic alternative.
- Assertion specificity: global `code/testing.md` Assertions.

## Parameterized Tests

- `@ParameterizedTest` with `@CsvSource`, `@ValueSource`, `@MethodSource`, or `@EnumSource`.
- `@MethodSource`: companion function returning `Stream<Arguments>`.
- `@DisplayName` or backtick syntax for readable names.

## Naming

- Backtick syntax: `` `should return empty when no items`() ``.
- Or: `test_<component>_<condition>_<expected>`.
- `@DisplayName` for parameterized test descriptions.

## Execution

- Replaces global `code/testing.md` Execution unit-only default and Types separate execution: `./gradlew test` -- all tests.
- `./gradlew test --tests "*.ParserTest"` -- single class.
- `./gradlew test --tests "*.ParserTest.should*"` -- pattern match.
- Verbose diagnostics: `code/debugging.md` Tools.

## Configuration

```kotlin
// build.gradle.kts
tasks.test {
    useJUnitPlatform()
}
```

## Mocking

- MockK for Kotlin-idiomatic mocking when needed: `mockk<T>()`, `every { }`, `verify { }`.
- `spyk` for partial mocks. `relaxed = true` for stubs.
