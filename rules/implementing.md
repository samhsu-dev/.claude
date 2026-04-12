---
paths:
  - "**/*impl.md"
---

# Python Implementation Documents

Python-specific `impl.md` conventions.

---

## API Entry Format

**[library]** `from library import Thing` -- when/gotcha.

Example:
**[pydantic-ai]** `Agent(model, result_type=T)` -- result_type must be BaseModel subclass.
**[jinja2]** `Environment(loader=FileSystemLoader(path))` -- loader required; omitting disables file templates.

## Library Entry Format

- library_name >= version -- purpose. `uv add library_name`.

## Verification

- Check `impl.md` for existing findings before writing integration code.
- Record all findings immediately. Not in conversation only.
- Verify via DeepWiki, Context7, or minimal test. No guessing.
