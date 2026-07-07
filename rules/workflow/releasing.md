---
paths:
  - "**/pyproject.toml"
  - "tools/make_wheels.py"
  - "uv.lock"
---

# Release Rules — Multi-Distribution uv Workspace

Release process for a uv workspace publishing a pure-Python façade, a binary companion, and an independent binary tool to PyPI.

---

## Distribution Layout

- Three PyPI distributions from one uv workspace: `static-php-py` (façade, pure code), `static-php-py-binary` (internal companion carrying the PHP binary), `static-php-build` (independent CLI tool carrying spc).
- `static-php-py` is the only user-facing install name. The companion's description states it is not for direct installation; the companion has no README, no docs directory, and no public Python API.
- A new PyPI distribution is created only when content is (a) optional for the façade, (b) platform-binary content requiring platform wheel tags separate from pure code, or (c) an independent product. Pure-Python growth goes into `static_php_py` import packages inside the existing distribution.
- The façade↔companion contract is an entry-point group plus an exactly pinned extra. The companion depends on nothing; nothing except the façade's extra depends on the companion.

## Versioning

- Version streams are decoupled: `static-php-py` bumps freely; `static-php-py-binary` bumps only when the bundled PHP binary changes; `static-php-build` bumps on its own changes.
- The façade pins the companion exactly: `bundled = ["static-php-py-binary==X.Y.Z"]`. The pin changes in the same commit that changes the companion version. The workspace member's version equals the pin, or `uv lock` fails.
- At the next binary change, the companion version switches to mirroring the bundled PHP version (e.g. `8.4.5`); a repack without binary change appends a fourth segment.
- A version uploaded to PyPI or TestPyPI is burned. Never rebuild and re-upload under the same version; bump instead.

## Artifacts

Per full release, 12 artifacts:

| Distribution | Artifacts | Built by |
|--------------|-----------|----------|
| static-php-py | sdist + `py3-none-any` wheel | `uv build` |
| static-php-py-binary | 5 platform wheels | `uv run python tools/make_wheels.py` |
| static-php-build | 5 platform wheels | `uv run python tools/make_wheels.py` |

- Platform tags: `manylinux_2_17_x86_64`, `manylinux_2_17_aarch64`, `macosx_11_0_x86_64`, `macosx_11_0_arm64`, `win_amd64`, all with `py3-none` prefix.
- Binary-carrying distributions publish no sdist and no any-wheel: a `uv build` any-wheel of a binary package mis-ships every platform's archives.
- `tools/make_wheels.py` auto-discovers binary-carrying packages by `packages/*/src/*/_resources/*.tar.gz`; it pre-extracts the binary, tags the wheel, and excludes macOS AppleDouble (`._*`) archive members.
- Wheels are reproducible: fixed 1980 timestamps and fixed permissions. Two builds of the same tree are byte-identical; a non-identical rebuild indicates an unintended content change.

## Release Procedure

1. Quality gate green: `ruff format`, `ruff check`, `mypy --strict`, `pytest`.
2. Bump versions per the versioning rules; update the façade pin when the companion bumps; run `uv lock`.
3. Build all artifacts; verify reproducibility by rebuilding and comparing hashes.
4. `twine check` on every artifact.
5. Upload to TestPyPI; verify `pip install` from TestPyPI resolves and imports on the host.
6. Upload the identical artifacts to PyPI.

## Identity

- Package metadata, wheel `METADATA`, and project URLs carry only the pseudonymous identity ("static-php-py contributors", samhsu-dev). No real names or emails in any released artifact.
- Local git history contains the real identity. Never push this history to a public remote; releases ship artifacts, not history.
