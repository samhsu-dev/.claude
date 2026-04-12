---
paths:
  - "**/*test*"
  - "**/*Test*"
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

### Error case checklist per function
- Invalid type / wrong class.
- Empty input (`""`, `emptyList()`, `emptyMap()`).
- `null` when nullable parameter.
- Out-of-range values (boundary -1, boundary +1).
- Missing required fields.

---

## Layout

- Test root: `src/test/kotlin/`. Mirror source packages.
- Files: `{ClassName}Test.kt`.

## Discovery

- Classes annotated or containing `@Test` / `@ParameterizedTest` methods.
- Test classes marked `internal`.
- No inheritance-based test suites. Plain classes with annotated methods.

## Setup and Fixtures

- `lateinit var` for test fixtures initialized in `@BeforeEach`. Avoids nullable types.
- `@BeforeAll` / `@AfterAll` in `companion object` with `@JvmStatic`.
- `@TempDir` for temporary directories. Auto-cleaned.
- Fresh objects per test. No shared mutable state across tests.

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
- No boolean-only assertions when specific assertions exist.

## Parameterized Tests

- `@ParameterizedTest` with `@CsvSource`, `@ValueSource`, `@MethodSource`, or `@EnumSource`.
- `@MethodSource`: companion function returning `Stream<Arguments>`.
- `@DisplayName` or backtick syntax for readable names.

## Naming

- Backtick syntax: `` `should return empty when no items`() ``.
- Or: `test_<component>_<condition>_<expected>`.
- `@DisplayName` for parameterized test descriptions.

## Execution

- `./gradlew test` -- all tests.
- `./gradlew test --tests "*.ParserTest"` -- single class.
- `./gradlew test --tests "*.ParserTest.should*"` -- pattern match.
- `./gradlew test --info` -- verbose output.

## Configuration

```kotlin
// build.gradle.kts
tasks.test {
    useJUnitPlatform()
}
```

## Mocking

- Mock at system boundaries only. Real objects for internal collaborators.
- MockK for Kotlin-idiomatic mocking when needed: `mockk<T>()`, `every { }`, `verify { }`.
- `spyk` for partial mocks. `relaxed = true` for stubs.
