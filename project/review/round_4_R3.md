# Review round 4 — Reviewer R3 (clarity/reproducibility/ethics), verbatim (simulated reviewer: AI agent with fresh context)

## Referee report, round 4 (R3: clarity, reproducibility, ethics, journal compliance). Manuscript v4, commit a292cb6

**Overall score: 8.5/10. Recommendation: minor revision (close to accept).**

There is nothing that would block acceptance.
- Every table and figure regenerates byte for byte.
- S3 regenerates byte for byte against the real git history.
- The audit finds 0 unmatched numbers, and the leakage tests pass.
- All ten round-3 R3 concerns are resolved or properly handed to the authors.

What remains is small and textual.

**Note:** the repository changed while I was reviewing. Commits 93dd08e and ebe6101 ("v5 in progress") arrived, and `highlights.md` changed. I reviewed v4. For each concern I say whether it still applies to the current working tree. One v5 change creates a new problem: the abstract is now 264 words (concern 1).

### Round-3 R3 concerns: status
1. **Table 2, rows C4/C5: resolved.** C4 now reads "beat Wait-90 on the reused set, tie on fresh data". C5 now reads "significantly helped only No-wait".
2. **README: mostly resolved.** The renumbering is done, the table renders, the split one-liner is present and correct, and the script name is explained. One leftover label is wrong (concern 3).
3. **Citations: resolved.**
   - Tables 1–14, Figs. 1–3 and S1–S6 are all first cited in order.
   - Tables 9 and 14 are now cited.
   - T3c is listed in S4.
4. **Accuracy points: resolved.**
   - The W15 configuration is noted.
   - All six H1 tests are reported, including AWT vs Wait-90 (−0.035, 2/8).
   - Table 5 now explains "— = not run".
   - The leave-out design is stated in the abstract, Sections 5.2 and 6.1, and the conclusion.
   - The RQ1/H2a wording is now "first reading of the RQ1 numbers, hypothesis H2a". That is acceptable.
5. **Table 14 wording: resolved.** It now says "internal (AI) review request".
6. **S3 true-label flag: resolved.** The flag is now set from the variant name, so E1 oracle shows True. The regenerated file is identical, and its counts (16 complete, 11 partial, 3 smoke-only) match Section 4.6.
7. **Figures: resolved.** The Fig. 1 caption now covers line styles and the symlog scale. Fig. 3's y-axis now reads "share". All three PNGs match their captions.
8. **Bullets: partly resolved.** The RQ2 and RQ5 answers are now prose. The body still has about 114 bullet items and about 12,650 words.
9. **Highlight wording and graphical-abstract image: resolved.** The highlight now says "median relative". The need for a designer-made image is in SUBMISSION_READINESS.
10. **Declarations: resolved** apart from the placeholders, which legitimately need the human authors.

### Concerns
1. **[MINOR] Abstract length (v5 working tree only).**
   - v4 is 249 words, which passes but has almost no margin under different word counters.
   - The v5 abstract in the working tree is **264 words**, over the 250 limit.
   - **Fix:** trim to ≤ 245 before submission.
2. **[MINOR] The AI statement contradicts the repository (v4).**
   - The Declarations say "two internal review rounds". The repository holds round_1 to round_3, and SUBMISSION_READINESS says three.
   - The working tree now says "four", which is correct only if this round is counted.
   - **Fix:** make the Declarations, Section 4.6 and SUBMISSION_READINESS agree on one number.
3. **[MINOR] README leftover (still present in the working tree).**
   - The fast-path comment for `scripts/test_set_usage.py` still says "Supplementary Table S3". It should say S1.
   - `test_set_usage.py` assumes the project sits one level inside the git repository (`REPO = parent`, paths `project/results`). If the code is archived with the project at the repository root, the script will find no commits.
   - Table 10 still needs a manually linked `data/` folder.
   - **Fix:** correct the label. Note the expected layout, or make `REPO` configurable.
4. **[MINOR] Typography artefacts (still present).**
   - "RecallS20% effort" appears in Section 4.2 and the Table 9 header. "G-mean S0.5" and "Sbest thr." appear in the Table 10 and Table 12 headers. These are presumably a garbled "@".
   - Section 5.5, H9b, has a missing full stop: "Holm p = 0.027) Wait-30 gains".
   - p-value precision is inconsistent: 0.002 in Table 7, 0.0020 in Section 5.2.
5. **[MINOR] Wording that slightly overclaims or confuses (v4; the first two are fixed in the working tree).**
   - The abstract said age-only corrections "lost to" Wait-90, but Holm p ≥ 0.148. The conclusion correctly says "did not beat".
   - The introduction calls the reused Cabral test set "the ten held-out projects", which conflicts with Section 4.6. Section 5.5 also says "held-out G-mean spread".
   - The Table 2 C1 row says "for short waits the penalty is label noise", then quotes W = 90 path shares (0.44–0.78). Separate the W = 30 claim from the W = 90 range.
6. **[MINOR] Supplementary file names do not match their labels.**
   - S1 is the file `S3_…`, S6 is `S1_…`, and S5 is `T10_…`. S3 is a JSON file, not a table.
   - The README flags this ("file names predate the final numbering"). Renaming the files before archiving would avoid reviewer confusion.
7. **[MINOR] Length.** About 12,650 words before the references, with 14 main tables. As suggested in round 3, Tables 10 and 13 could move to the supplement, and the Section 5.2 bullet lists could become prose. Optional.

### Disclosures and declarations: adequate
- The AI agent and its model are named.
- The internal reviews are described as not peer review.
- The two lineages and five branches are explained.
- Test-set reuse is stated in bold, and S1 is complete and regenerable.
- Exploratory and confirmatory analyses are labelled per family, including the plan_v8/v9 analyses on ApacheJIT.
- The deviations are tabulated in Table 14.

These placeholders legitimately need the human authors:
- authors, affiliations and corresponding author;
- Acknowledgements, Funding, Competing interests and Author contributions;
- the repository URL and DOI;
- the authors' role in the AI statement;
- the ethics confirmation;
- in the cover letter: date, signature, originality/preprint confirmation and AI-policy text;
- the graphical-abstract image.

Nothing else is missing. Compute adds up: 29.5 + 15.0 + 11.6 = 56.1 CPU-hours.

### Checks run
- `python scripts/audit_paper_strict.py`: **Unmatched: 0** on v4, and again on the current working tree.
- `python scripts/build_references.py`: 45 references, none uncited, no unresolved "et al." citations. `git status` stayed clean.
- `pytest tests/`: **4 passed** in 158 s.
- **Scratch copy** (`/tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/copy4`):
  - `review1_shapley.py` and `paper_numbers.py`: all 20 `paper/tables/*.md`, all 3 PNGs, `paper_numbers.json` and `shapley.json` are **byte-identical** to the committed files.
  - `test_set_usage.py`, pointed at the real repository: S3 is byte-identical, with 197 commits scanned and counts 16/11/3 plus 21 review configurations.
- **Numbering:** first-citation order checked by script for Tables 1–14, Figs. 1–3 and S1–S6, all in order. The README's table-to-file mapping matches the manuscript; the only error is the one label in concern 3.
- **Abstract:** v4 has 249 words in one paragraph; v5 has 264.
- **Highlights:** 5 bullets. v4: 81, 83, 78, 65 and 85 characters. Current file: 81, 83, 78, 78 and 81. All ≤ 85.
- **Figures:** F1–F3 viewed; they agree with their captions and with Table 7.
- No tracked file was modified by me.
