---
paths:
  - "**/evaluation.tex"
  - "**/evaluations.tex"
  - "**/experiment.tex"
  - "**/experiments.tex"
---

# Evaluation Structure

## Section Order

| # | Block | Content |
|---|-------|---------|
| 1 | RQ list | One framing sentence, then the enumerated research questions |
| 2 | Experimental Setup | Environment, datasets, baselines, metrics, unit and pool |
| 3 | RQ1..N | One subsection per research question, in list order |

## RQ Design

- Each RQ tests one claim and has one main table or figure.
- A configuration that adds one row to an existing comparison is a row of that comparison, not a new RQ. Example: replacing the LLM backend is a row of the ablation table.
- An RQ whose count aggregates the outputs of every system and configuration (real-world impact, zero-days) comes after every RQ that introduces those systems and configurations.
- An RQ is named by the claim it tests (Effectiveness, Exploitation, Ablation Study, Real-World Impact, Cost), never by a component of the tool.
- The section states whether the tool is implemented and deployed before RQ1.
- The tool's false positives and failures are reported in the same table as its true positives.

## RQ List Block

- The framing sentence states the number of research questions and that the section answers them.
- Each RQ is one `\item` of an `icompact` list, labeled `\textbf{RQ$n$ (Name):}` and followed by one question.
- The list holds no method, result, or metric definition.
- RQ count, numbers, names, and order are identical in the list and in the subsection titles.

## Experimental Setup Block

One `\para{}` per concern:

| Concern | Content |
|---------|---------|
| Environment | Hardware (CPU, cores, memory) and software (OS, language, tool versions) as exact figures |
| Datasets | Per dataset: source, measured size, inclusion criteria (an enumerated list when more than two), the RQs it serves, citation |
| Baselines | A table with `\caption` and `\label` listing each tool, version, and configuration; a statement that each tool runs in its authors' recommended configuration |
| Metrics | Each metric defined once by its formula at its first use: $FDR = FP/(FP+TP)$ |
| Unit and pool | The counting unit of one finding; the pool, the union of the findings confirmed for any system or configuration, each counted once |

- Every RQ counts in the setup's unit over the setup's pool.
- No RQ subsection restates the environment.

## RQ Subsections

- Title: `RQ$n$: Name`, with a `\label` of prefix `subsec:`.
- The first sentence states what the RQ measures and on which dataset.
- The method precedes the numbers: the metric, the ground-truth criterion, the unit.
- Results cite their table or figure with `\autoref`.
- Order of numbers: the tool, then each baseline, then the difference.
- The same metric is reported for the tool and every baseline.
- A sentence attributes a difference to a cause only when a controlled comparison in the evaluation isolates that cause. Otherwise it states the difference ("is lower", "differs").
- Show the overlap of the systems' findings over the pool in a set-intersection plot (UpSet or Venn). Never derive a system's unique findings by subtracting counts of different units.
- A zero-day is a finding that was not publicly known before the authors' disclosure. Never define it as a finding the other evaluated tools did not report.

## Tables and Figures

- Every result table has `\caption` and `\label` and is loaded by `\input{}` from its own file.
- The caption defines each column name and status term that the text does not define.
- A figure has width `\linewidth` and carries `\caption`, `\label`, and `\Description`.
- A regression or trend claim states the fit statistic ($R^2$) for the tool and each baseline.

## Quantification

- Write the number instead of an adjective: "an FNR of 11.34%", not "a low FNR".
- Each rate is followed by its raw counts: "an FDR of 13.9% (62 true positives, 10 false positives)".
- A performance claim states the measured value and the direction of the difference to each baseline.
