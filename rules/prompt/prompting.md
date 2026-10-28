---
paths:
  - "**/*.prompty"
  - "**/prompts/**"
---

# Project Agent Prompt Workflow

- Forced-action loop: every agent turn carries exactly one tool call (Strix, PentAGI).
- Explore-then-validate: a separate verifier or PoC gate confirms a finding before it surfaces. The strongest false-positive defense is architectural, not prompt wording (XBOW, Big Sleep).
- Report-gated output: findings exist only via a structured report tool requiring evidence fields.
