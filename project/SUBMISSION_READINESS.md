# Submission readiness: JKSU-CIS, Route A (empirical paper)

Updated 2026-11-28, branch `claude/zealous-lamport-bjc4um`. Every number in the manuscript traces to a result file: `python scripts/audit_paper_strict.py` reports 0 unmatched.

## 1. Status

- **Manuscript.** `paper/manuscript.md` (v4) is an empirical study: *Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects*. It does not claim a new method that beats the baselines, because that claim failed on held-out and fresh data.
- **Supporting files.** Highlights, cover letter, a graphical-abstract brief, 45 DOI-checked references, figures 1–3, tables 1–14 and supplementary items S1–S6.
- **Internal review.** Three rounds of simulated review, run by AI agents with a fresh context. These are not peer review.

  | Round | Methods | Novelty | Clarity |
  |:--|:--|:--|:--|
  | 1 | 5 | 5 | 6 |
  | 2 | 6 | 5 | 7 |
  | 3 | 7 (minor) | 7 (minor) | 8 (minor) |

  Round 4 is in progress. Triage and responses are in `review/round_*.md`.
- **Acceptance is not guaranteed.** JKSU-CIS mostly publishes method papers. Section 2.5 argues the fit (a benchmark protocol and bounds for method papers), but an empirical-SE venue would fit more naturally.

## 2. What the paper shows (held-out and fresh data)

- **Noise and freshness interact.**
  - For a 30-day wait, true labels on the waited-out training set close 0.81 (Cabral test) and 0.92 (ApacheJIT) of the AUC gap to an oracle.
  - For the tuned 90-day wait they close 0.44 and 0.78. The attribution of the remainder depends on how the interaction is split.
- **The harm is concentrated in the most recent waited-out commits.** When the other age bands are corrected, leaving these commits noisy costs 2–3× their share of the gain. On ApacheJIT the bands act jointly.
- **No practical correction reliably beat a tuned 90-day wait.**
  - Age-only corrections did not beat it at the operating point (Cabral).
  - Feature-based denoisers and a latency-aware threshold tied it on fresh data.
  - The threshold significantly helped only No-wait.
- **A result that did not replicate.** The earlier Cabral finding that a latency-aware threshold turns LAW into a winner did not replicate on ApacheJIT.

## 3. Comparison with JKSU-CIS work

MSTDP (Liu et al. 2026, JKSU-CIS) evaluates offline on final labels. Under our protocol that is the oracle condition, so its numbers are not comparable with ours, and we make no claim of beating it.

Our protocol has:
- prequential evaluation with verification latency;
- a fresh confirmation dataset;
- committed plans and leakage tests;
- full disclosure of test-set reuse (Supplementary S1).

These are stricter than the JKSU-CIS papers surveyed in `literature/jksu_benchmark.md`.

## 4. What the human authors must do before submission

- [ ] Fill in authors, affiliations, corresponding author, acknowledgements, funding, competing interests, author contributions and ethics confirmation (Declarations).
- [ ] Complete the AI-use statement under the journal's policy, and describe the authors' own role and verification. AI tools cannot be authors.
- [ ] Deposit the code and results (e.g. Zenodo) and insert the repository URL and DOI.
- [ ] Have a designer produce the graphical-abstract image from `paper/graphical_abstract.md`, if the journal requires one.
- [ ] Convert the Markdown to the journal's template (Springer LaTeX or Word), and check the reference style and length limits in the current author guide.
- [ ] Read the whole manuscript and verify the claims. The internal reviews do not replace this.
