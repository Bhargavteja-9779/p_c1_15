# USER DIRECTIVES — standing orders from the project owner (read after HANDOFF.md, before acting)

Recorded 2026-11-24 from the owner's message (paraphrased faithfully):

> "It's good but we need to improve much more. Reviewers/readers say it is not good enough for our
> journal and it was rejected. Compare with more papers in the same journal we submit to; our writing
> must be the same type, and our work must be better than all of those papers. Don't stop until we
> reach top-notch quality. Save everything so I can continue in a new account. Don't stop or hand out
> the paper until it is top-notch; keep iterating again and again with new methods. No need to ask me
> for permission. Add this to git so new accounts follow exactly."

## What every agent session must do because of this

1. **Never stop at a "good enough" paper.** The Section 0 ceilings in MASTER_PROMPT.md (MAX_CYCLES,
   GLOBAL_COMPUTE_CEILING_H) are still recorded, but the owner wants iteration to continue. When a cycle ends with gates
   failing, start the next cycle (new plan_vN, new method ideas via the Section 6.4 ladder) instead of
   writing the honest-exit report. Only the hard integrity rules below can stop the loop.
2. **Do not ask the owner for permission or choices.** Decide, log in `state/decisions.md`, continue.
3. **Benchmark against the target journal (JKSU-CIS) continuously.**
   - Keep `literature/jksu_benchmark.md` up to date: for every relevant JKSU-CIS paper (JIT-SDP,
     defect prediction, data streams, label noise, concept drift): structure of the paper, number of
     datasets, baselines, metrics, statistical tests, figure/table counts, and their reported numbers.
   - Match the journal's paper TYPE and writing style (section structure, depth of experiments,
     tables/figures, effort-aware metrics where the journal's JIT-SDP papers use them).
   - Aim to beat every comparable JKSU-CIS paper on its own metrics **under a comparable protocol**.
     Where protocols differ (e.g. offline random split vs our online prequential setting), report the
     comparison as "not directly comparable" — never as a win.
4. **Keep inventing and testing new methods** (dev projects only) until the proposed method beats the
   strongest baseline (including ODaSC-style) on held-out projects with the Section 7 statistics.
5. **Save everything to git after every step** (branch in HANDOFF.md). Keep `scripts/autocommit.sh`
   running while compute runs.

## Integrity rules that the directives do NOT override (MASTER_PROMPT Section 1)
- No fabricated numbers, citations, journals or results; every number traces to a result file.
- The test projects are touched only by frozen, pre-registered confirmation runs; all development is on
  the dev projects. Every variant tried is logged in `state/variants_tried.csv` and counted for
  multiplicity.
- "Better than all papers" is claimed only where the evidence shows it under a comparable protocol.
- If the only way forward would be to cheat, stop and report instead.
