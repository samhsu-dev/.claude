---
paths:
  - "**/pyproject.toml"
  - "uv.lock"
  - ".github/workflows/*.yml"
---

# Python Release Rules

Release standards by distribution type. Project-specific release facts — distribution names, artifact inventories, tag names, credential mechanism, identity policy — live in the project's `docs/releasing.md`, never here.

---

## Distribution Types

| Type | Contents | Artifacts |
|------|----------|-----------|
| Pure-Python | Python code only | sdist + `py3-none-any` wheel |
| Binary-carrying | Platform-specific executables or shared objects | Platform-tagged wheels only |
| Multi-distribution workspace | Several distributions from one uv workspace | Union of each member's artifacts |

## All Distributions

- A version uploaded to PyPI or TestPyPI is burned. Never rebuild and re-upload under the same version; bump instead.
- Quality gate green before the version-bump commit: formatter, linter, type checker, tests.
- Version bump, lock-file update, and dependent-pin updates land in one commit.
- Publish path: TestPyPI → install-and-import verification from TestPyPI → PyPI. The artifacts uploaded to PyPI are the identical files verified on TestPyPI.
- `twine check` passes on every artifact before upload.

## Pure-Python Distributions

- Artifacts: sdist + one `py3-none-any` wheel, built by `uv build`.
- Version stream follows the code: bump on every released change.

## Binary-Carrying Distributions

- No sdist and no any-wheel: an any-wheel of a binary package mis-ships every platform's content.
- One wheel per target platform. Wheel tags carry the `py3-none` prefix when the package holds no Python-version-specific code.
- A statically linked Linux binary uses the compressed tag set `manylinux_<x>_<y>_<arch>.musllinux_<x>_<y>_<arch>`: one wheel per architecture serves glibc and musl; the WHEEL file carries one `Tag:` line per tag.
- The distribution version mirrors the carried binary's version. A repack without binary change appends one extra version segment.
- Wheels are reproducible: fixed timestamps and permissions. Two builds of the same tree are byte-identical; a non-identical rebuild indicates an unintended content change.
- Every wheel ships the carried binary's third-party licenses in `.dist-info/licenses/` with one `License-File:` header per file. A duplicate file name across license sources fails the build.

## Multi-Distribution Workspaces

- A new distribution is created only when content is (a) optional for the main distribution, (b) platform-binary content requiring wheel tags separate from pure code, or (c) an independent product. Pure-Python growth goes into the existing distribution's import package.
- One user-facing install name per product. An internal companion's description states it is not for direct installation; the companion has no README, no docs directory, and no public Python API.
- The main↔companion contract is an entry-point group plus an exactly pinned extra: `main[extra]` resolves to `companion==X.Y.Z`. The companion depends on nothing; nothing except the extra depends on the companion.
- Version streams are decoupled: each member bumps only on its own changes.
- The exact pin changes in the same commit as the companion's version. `uv lock` fails when the workspace member's version disagrees with the pin.

## Release Procedure

1. Quality gate green.
2. Bump versions per the type rules; update dependent pins; run `uv lock`; commit.
3. Tag the release commit `<distribution>-v<version>`; one tag per distribution being released.
4. Push the commit and tag. CI builds, checks, publishes to TestPyPI, verifies the install, and publishes to PyPI after approval.

Manual fallback (CI unavailable): build all artifacts; rebuild and compare hashes to verify reproducibility; `twine check` every artifact; upload to TestPyPI and verify install-and-import; upload the identical artifacts to PyPI.

## Tag-Driven CI

- One tag `<distribution>-v<version>` releases one distribution.
- The workflow parses the tag, fails when the tag version differs from that distribution's pyproject version, and runs `uv lock --check`.
- Publish path in CI: TestPyPI environment → install-and-smoke-test from TestPyPI → PyPI environment with required reviewers; the final publish waits for manual approval.
- Publish credentials are CI environment secrets. The credential mechanism (API token or trusted publishing) is a project decision recorded in the project's `docs/releasing.md`.
- First upload of a name unregistered on the index requires an account-scoped token; after registration, the token is scoped to the released projects.
