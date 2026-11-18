---
paths:
  - "**/main.tex"
  - "**/abstract.tex"
  - "**/introduction.tex"
  - "**/conclusion.tex"
  - "**/conclusions.tex"
---

# Paper Structure

Abstract, introduction, contributions, and conclusions. Prose rules: `writing.md`.

---

## Opening

- The subject of the first substantive sentence is the paper's central artifact or domain, matching the title's primary noun (Gopen & Swan).
- No technology, language, or implementation detail appears as the grammatical subject of the opening unless the paper's title names it.
- Do not open by explaining to experts why their field is important. Open with the paper's specific purpose (Shewchuk).

## Paper Structure

- Abstract: four sentences — (1) the problem, (2) why it is hard, (3) the approach, (4) the result (Peyton Jones).
- Introduction: problem description and contribution list only. No background, no related work, no methodology. One page.
- Related work follows the core idea, not precedes it. Readers cannot evaluate related work before understanding the contribution (Peyton Jones).
- State the contribution at four levels of detail: title (~10 words), abstract (~100 words), introduction (~1000 words), body (~10,000 words). Each level is independently coherent and consistent with the others (Levin & Redell).

## Contributions

- Every paper must answer three questions: (1) What is the contribution? (2) What is the new result and how does it differ from prior work? (3) Why should the reader believe the result? (Shaw).
- Write the contribution list before drafting the body. The body provides evidence for the contributions, not the other way around (Peyton Jones).
- Each contribution is a single refutable sentence. "We describe X" is not a contribution. "We prove X satisfies property Y (Section N)" is (Peyton Jones).
- Forward-reference the evidence for each contribution at the point of the claim in the introduction.
- Signal explicitly whether the work is novel (new scientific observation) or incremental (improvement over prior work). Do not leave the reader to infer which (McDaniel).

## Conclusions

- Conclusions must add new information: implications, conjectures, open problems, perspective gained after reading the full paper (Shewchuk).
- Do not summarize the paper in the conclusions. The reader has just read it. A conclusion the reader could understand before reading the paper adds nothing.
