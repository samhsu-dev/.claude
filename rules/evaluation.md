---
paths:
  - "**/evaluation.tex"
  - "**/evaluations.tex"
  - "**/experiment.tex"
  - "**/experiments.tex"
---

# Evaluation Structure

The section opens by listing the research questions, then sets up the experiment once, then answers each question in its own subsection. Each research question maps to exactly one body subsection. Every quantitative claim cites a table or figure. The reader holds one set of questions, one experimental setup, and one answer per question.

---

## Section Order

| # | Block | Function |
|---|-------|----------|
| 1 | RQ list | One sentence framing, then an enumerated list of research questions |
| 2 | Experimental Setup | Environment, datasets, baselines/tools, metrics — the shared basis for every RQ |
| 3 | RQ1..N | One subsection per research question, in the order the RQ list names them |

## RQ List Block

- One framing sentence: the section evaluates the tool by answering the research questions below.
- Each RQ is one `\item` in an enumerated list (e.g., `icompact`), bolded as `\textbf{RQ$n$:}`.
- Each RQ is one question stating the capability or property measured, in one sentence.
- RQ count, numbering, and order are identical here and in the body subsections.
- No method, no result, no metric definition in the list. The list is a map.

## Experimental Setup Block

One subsection covering the shared basis every RQ reuses. Each concern is one `\paragraph{}` or bolded label.

| Concern | Content |
|---------|---------|
| Environment | Hardware (CPU, cores, memory) and software (OS, language, tool versions) as exact figures. |
| Datasets | One named paragraph per dataset: source, size, construction criteria, and which RQ it serves. Cite the dataset. |
| Baselines | The compared tools in a table with versions and configurations. State that recommended configurations were used. |
| Metrics | Define each metric by its formula at first use (e.g., $FDR = FP/(FP+TP)$). |

Rules:
- State every dataset's size as a measured count, and the RQ it answers.
- Dataset construction states the inclusion criteria as an enumerated list when more than two.
- Baseline tools, versions, and configurations go in a table with `\caption` and `\label`.
- Each metric is defined once, at the point of first dependence.

## RQ Subsections

One subsection per research question, in the order the RQ list names them. Each:

- Carries a `\label{subsec:rqN}` and a title naming the property measured.
- Opens on one sentence restating what the RQ measures and on which dataset.
- States the measurement method before the numbers: the metric, the ground-truth basis, the unit of analysis.
- Reports results referencing a table or figure (`\autoref{tab:...}`, `\autoref{fig:...}`).
- Reports the tool's number first, then each baseline's, then states the gap.
- Closes by interpreting the result: the one mechanism that explains the gap.

Rules:
- Every result number appears in a table or figure; prose references it, never replaces it.
- Comparison is symmetric: report the same metric for the tool and every baseline.
- Each gap is explained by a stated cause, not asserted as superiority.

## Tables and Figures

- Every result table has `\caption`, `\label`, and is filled by `\input{}` of a separate table file.
- The caption defines any non-obvious column or status term used in the table.
- A figure spans `\linewidth` and carries `\caption`, `\label`, and `\Description`.
- Regression or trend claims state the fit statistic (e.g., $R^2$) for the tool and each baseline.

## Quantification

- No bare adjective where a number exists. "FNR of 11.34%" not "low FNR".
- Every rate carries its raw count in parentheses: "0.3% (only 2 false positives)".
- Counts of true positives, false positives, false negatives are stated when a rate is derived from them.
- Performance claims state both the measured value and the comparison direction against each baseline.

## Invariants

- One RQ per body subsection. RQ numbering and order match the opening list.
- One experimental setup, defined before RQ1, reused by every RQ. No per-RQ environment restatement.
- Each metric is defined once, by formula, at first use.
- Every result number is anchored to a table or figure with a `\label`.
- Every comparative claim reports the same metric for the tool and all baselines, and names the cause of the gap.
