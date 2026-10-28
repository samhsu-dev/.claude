---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
  - "**/*test*"
---

# Debugging Guardrails

Full procedure: `/debug` skill.

---

- Reproduction before repair: `code/testing.md` Reproductions.
- Read the full traceback before changing code.
- Root-cause repair: `workflow/change-policy.md`.
- Debugging evidence for the verification rule in `rules/workflow/change-policy.md` is an assertion, log, or test.
- Failure handling and missing required values: `code/quality.md` Error Handling.
- Reproduction retention: `code/testing.md` Reproductions.
