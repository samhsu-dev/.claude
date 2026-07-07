---
paths:
  - "**/pyproject.toml"
  - "tools/make_wheels.py"
  - "uv.lock"
  - ".github/workflows/*.yml"
---

# Release Rules — PyPI Distributions

Release process for publishing pure-Python and binary-carrying distributions to PyPI from a uv project or workspace.

---

## Distribution Layout

- A new PyPI distribution is created only when content is (a) optional for an existing distribution, (b) platform-binary content requiring platform wheel tags separate from pure code, or (c) an independent product. Pure-Python growth goes into import packages inside the existing distribution.
- One user-facing install name per product. A binary companion's description states it is not for direct installation; a companion has no README, no docs directory, and no public Python API.
- A façade↔companion pair contracts through an entry-point group plus an exactly pinned extra. The companion depends on nothing; nothing except the façade's extra depends on the companion.

## Versioning

- Version streams are decoupled per distribution: pure-code distributions bump freely; a binary carrier bumps only when its bundled binary changes.
- A façade pins its companion exactly: `bundled = ["<companion>==X.Y.Z"]`. The pin changes in the same commit that changes the companion version. The workspace member's version equals the pin, or `uv lock` fails.
- A binary carrier's version mirrors the bundled binary version (e.g. `8.4.5`); a repack without binary change appends a fourth segment.
- A version uploaded to PyPI or TestPyPI is burned. Never rebuild and re-upload under the same version; bump instead.

## Artifacts

| Distribution kind | Artifacts | Built by |
|-------------------|-----------|----------|
| Pure Python | sdist + `py3-none-any` wheel | `uv build` |
| Binary-carrying | 5 platform wheels | `uv run python tools/make_wheels.py` |

- Platform tags: `manylinux_2_17_x86_64`, `manylinux_2_17_aarch64`, `macosx_11_0_x86_64`, `macosx_11_0_arm64`, `win_amd64`, all with `py3-none` prefix.
- Binary-carrying distributions publish no sdist and no any-wheel: a `uv build` any-wheel of a binary package mis-ships every platform's archives.
- `tools/make_wheels.py` discovers binary content by `_resources/*.tar.gz` under the target package's src tree; it pre-extracts the binary, tags the wheel, and excludes macOS AppleDouble (`._*`) archive members.
- Wheels are reproducible: fixed 1980 timestamps and fixed permissions. Two builds of the same tree are byte-identical; a non-identical rebuild indicates an unintended content change.

## Release Procedure

Releases run through CI (see Tag-Driven CI Release). The local steps end at the tag push.

1. Quality gate green: `ruff format`, `ruff check`, `mypy --strict`, `pytest`.
2. Bump versions per the versioning rules; update the façade pin when the companion bumps; run `uv lock`; commit.
3. Tag the release commit `<distribution>-v<version>`; one tag per distribution being released.
4. Push the commit and tag. CI builds, checks, publishes to TestPyPI, verifies the install, and waits for `pypi` environment approval before publishing to PyPI.

Manual fallback (CI unavailable): build all artifacts; rebuild and compare hashes to verify reproducibility; `twine check` every artifact; upload to TestPyPI and verify `pip install` resolves and imports; upload the identical artifacts to PyPI.

## Tag-Driven CI Release

- `.github/workflows/release.yml` triggers on tags `<distribution>-v*`. One tag releases one distribution.
- The workflow parses `<distribution>-v<version>` from the tag, fails when the tag version differs from the distribution's pyproject version, and runs `uv lock --check` (catches a façade pin that disagrees with the companion's version).
- Build routing: pure distributions via `uv build`, with `--package <distribution>` in a workspace; binary carriers via `uv run python tools/make_wheels.py <package-dir>`. All binary archives are git-tracked, so a plain checkout builds every platform wheel on one Linux runner.
- Publish path: TestPyPI (`testpypi` environment) → install-and-smoke-test from TestPyPI → PyPI (`pypi` environment). The `pypi` environment carries required reviewers; the final publish waits for manual approval.
- Auth is token-based via org-level secrets `TEST_PYPI_API_TOKEN` and `PYPI_API_TOKEN`. Never switch to trusted publishing and never enable attestations: both attach repository provenance to the PyPI release, breaking the pseudonymous identity.
- First upload of a name unregistered on PyPI requires an account-scoped token; after registration, scope the secret's token to the released projects.

## Identity

- Package metadata, wheel `METADATA`, and project URLs carry only the project's pseudonymous identity and the samhsu-dev account. No real names or emails in any released artifact.
- Local git history contains the real identity. Never push this history to a public remote; releases ship artifacts, not history.
