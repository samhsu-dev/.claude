---
paths:
  - "**/impl.md"
  - "**/impl-*.md"
---

# Python Implementation Documents

Python-specific `impl.md` conventions.

---

## API Entry Format

**[library]** `from library import Thing` -- when/gotcha.

Example:
**[requests]** `requests.get(url, timeout=10)` -- no default timeout; omitting it hangs forever.
**[jinja2]** `Environment(loader=FileSystemLoader(path))` -- loader required; omitting disables file templates.

## Library Entry Format

- library_name >= version -- purpose. `uv add library_name`.
