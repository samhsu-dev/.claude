---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
  - "**/*test*"
---

# Debugging Guardrails

Full procedure: `/debug` skill.

---

- Write a failing reproduction test before changing implementation code.
- Read the full traceback before changing code.
- Root-cause repair: `workflow/change-policy.md`.
- Debugging evidence for the verification rule in `rules/workflow/change-policy.md` is an assertion, log, or test.
- No silent fallbacks. Internal `map[key] ?: default` masks bugs — throw on missing key.
- Keep reproduction tests permanently. Never delete after fix.
