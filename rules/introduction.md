---
paths:
  - "**/introduction.tex"
  - "**/intro.tex"
---

# Introduction Structure

Six-module funnel. Widest at domain background, narrowest at contributions. Each module's closing sentence pulls the next module open. No logical gaps between modules.

---

## Modules

| # | Module | Function | Internal order |
|---|--------|----------|----------------|
| 1 | Importance | Prove the domain is widespread and high-risk | Domain scale (data) → risk exists → risk quantified (data) → narrow to one core term |
| 2 | Prior work | Survey existing approaches and their inherent flaws | Approach A + flaw → approach B + flaw → "we identify N unsolved challenges" |
| 3 | Challenges | Itemize the N unsolved challenges | One bullet per challenge; each names one SOTA tool's specific failure |
| 4 | Method | Name, position, mechanism, innovations | Name + one-line position → mechanism overview → N innovations mapping 1:1 to module 3 |
| 5 | Results | Establish credibility with evidence | Datasets → strongest numeric result → baselines beaten |
| 6 | Contributions | Closing bullet list echoing the whole | N bullets grouped as design / implementation / evaluation |

## Method Module (4)

Three blocks, narrowing from name to innovations.

| # | Block | Function | Length |
|---|-------|----------|--------|
| 1 | Name + position | State the tool name, its method class, and the problem it solves | One sentence |
| 2 | Mechanism overview | Introduce one core artifact (data structure or intermediate representation) and trace the pipeline as "build → use" | One to two sentences |
| 3 | Transition | Declare that the following N innovations each solve one prior challenge | One sentence |

Each innovation bullet carries four elements in order:

- Name — the innovation's term, italicized. Self-coined terms give name and intuition only; defer formal definition to the body.
- Intuition — one sentence stating what it does.
- Location — which pipeline stage it occurs in, placed on the mechanism-overview map.
- Challenge — which module-3 challenge it resolves, named by the same vocabulary that challenge used.

Rules:
- Stand up one core artifact. Unify the method narrative as "build the artifact, then use it." No loose list of unrelated mechanisms.
- Every innovation states its pipeline stage. The reader locates it on the mechanism overview.
- Reuse module-3 challenge vocabulary in each bullet so the challenge↔innovation mapping is visible at a glance.

## Contributions Module (6)

Three bullets in fixed order: design → implementation → evaluation. Abstract to concrete to evidence.

| # | Category | Opening verb | Content |
|---|----------|--------------|---------|
| 1 | Design | We design | Method position + the N innovation capabilities, echoing the module-3/4 lists 1:1 |
| 2 | Implementation | We implement | Open-source prototype + quantified scale (lines of code, language, coverage or version) |
| 3 | Evaluation | We perform | Experiments + the strongest numeric result and dataset scale, echoing module 5 |

Rules:
- Each bullet opens with "We" + a category verb. The verb names the category: design, implement, perform.
- Bullet 1 closes by listing the N innovation capabilities, mapping 1:1 to the challenges.
- Bullet 2 states quantified scale. No prototype claim without a number.
- Bullet 3 states the strongest numeric result and the dataset scale.
- Close with numbers, mirroring the numbers that opened module 1.

## Module Transitions

| Transition | Closing function |
|-----------|------------------|
| 1 → 2 | Group domain phenomena under the core term used by all later modules |
| 2 → 3 | "After analyzing prior work, we identify N unsolved challenges" |
| 3 → 4 | "We propose [tool], a [position] approach" |
| 4 → 5 | "We implement a prototype and evaluate on K datasets" |
| 5 → 6 | "In summary, we make the following contributions:" |

## Invariants

- Challenge count = innovation count = contribution count. The three lists map 1:1.
- Criticize prior work by tool name and specific failure point. Never by generic claim.
- Open with numbers proving the work is worth doing. Close with numbers proving it was done.

## Concept Definition

- Definitions are inline, not a separate module.
- Define a term at the first module where the argument depends on it.
- Define to the depth the current module's argument needs. No more.
- Core term (module 1): close its definition before module 1 ends. All later modules build on it.
- Methodology terms (module 2): define by contrast — A versus B.
- Challenge terms (module 3): define inside the bullet, only deep enough to show why it is hard.
- Self-coined terms (module 4): give name and intuition only. Defer formal definition to the body.
- Terms the introduction's argument does not depend on: defer to the body section that uses them.
