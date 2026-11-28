# Review round 3 — Reviewer R3 (clarity/reproducibility/ethics), verbatim (simulated reviewer: AI agent with fresh context)

## Referee report, round 3: clarity, reproducibility, ethics and journal compliance (manuscript v3)

**Overall score: 8/10. Recommendation: minor revision.**

I found no major problems. Every table and figure regenerates byte for byte, and the strict audit finds no unmatched numbers. The leakage tests pass. S3 is now complete, and the internal AI review is disclosed openly. What remains:
- one claim row that is out of date;
- the README's re-simulation table still uses the old table numbers;
- some numbering and citation gaps;
- a few small inconsistencies.

### Round-2 concerns from R3: status
- **#1, test-set disclosure: resolved.**
  - The scanner now reads the jsonl results, and S3 lists A3, A4, B1 and B3.
  - I checked the counts against S3: 16 complete, 11 partial and 3 smoke-only. They match Section 4.6.
  - The two seeds of A4 are now stated in Threats.
  - A small labelling error remains (concern 6).
- **#2, internal AI review: resolved.** It is disclosed in Section 4.6, the AI statement, Threats and the cover letter, and the model is named. A leftover wording in Table 14 is covered in concern 5.
- **#3, plural "denoisers": resolved.** The abstract and conclusion are now correct, but the claims table was not updated (concern 1).
- **#4, age-band claims: resolved.** "Adds nothing" is gone. The claims now rest on band-in, leave-out and per-label shares. Table 7 points to the G-mean versions instead of printing them, which is acceptable.
- **#5, names and labels: mostly resolved.**
  - The policy names are now consistent (ORB-style, AWT), every ODaSC-style row is tagged with its lineage, and Section 3.4 lists the hypotheses.
  - The README has a correct table-to-file mapping.
  - Open: S4 still lives in a file called `T10_…`, `T3c` is generated but never cited, and the README's re-simulation table is still on the old numbering (concern 2).
- **#6, figures: resolved.** One caption mismatch remains (concern 7).
- **#7, method described only in the Results: resolved.** Section 3.2 now describes the threshold rule and the second simulator.
- **#8, table structure: partly resolved.** The tables are now numbered 1–14 in order of first mention, but Tables 9 and 14 are never cited in the text (concern 3).
- **#9, format and length: partly resolved.**
  - Abstract: one paragraph, 233 words.
  - Graphical abstract: now in AUC.
  - Still about 116 bullet items in the body (concern 8).
- **#10, README: mostly resolved.** The manual `data/` symlink step for Table 10 remains (concern 2).
- **#11, declarations: resolved** apart from the placeholders, which legitimately need the human authors.

### Round-2 concerns from R1 and R2
- R1#6 asked to remove "and implementation". It was removed everywhere except the Table 2 C4 row (concern 1).
- R1#7 also asked for predicted-positive versus true rates per policy on ApacheJIT. That was not done. The text now calls the interpretation post hoc, which is acceptable, but Table 2 C5 still states it as a finding (concern 1).
- R1#11 (leakage tests now cover decomp and kafka) and R1#12 (1,188 commits) are resolved.
- R2#1–3 (ODaSC-opt/flt, Song 2023a, Falessi) are corrected in Sections 2.2 and 6.2.

### Concerns

1. **[MINOR] Table 2 contradicts the revised text.**
   - The C4 row reads "the gain from kNN adaptations of ODaSC depends on dataset and implementation". But Section 5.4 says "the two implementations agree", and the round-2 response says this wording was removed.
   - The C5 row reads "helps only policies with a distorted prior". Section 5.5 calls this "our post-hoc interpretation", and only No-wait passes.
   - **Fix:** change C4 to "one adaptation beat Wait-90 on the reused Cabral set; both tie on fresh data". Change C5 to "significantly helped only No-wait on fresh data (post-hoc interpretation: distorted prior)".

2. **[MINOR] The README's re-simulation table uses the v2 table numbers.**
   - The mapping table at the bottom of the README is correct, but the "Full re-simulation" table and the fast-path comments are not.

   | README says | Should be |
   |:--|:--|
   | `review1_shapley.py` "(Table 4)" | Table 6 |
   | "Table 6 (RQ3)" | Table 8 |
   | "Tables 3-4, Cabral (RQ2)" | Tables 5–6 |
   | "Table 7 (RQ4)" | Table 9 |
   | "Table 5 / Fig. 3 (A3)" | Table 7 / Fig. 3 |
   | "Tables 10-11 (A5)" | Tables 12–13 |
   | "Table 8 (RQ5 diagnostic)" | Table 10 |
   | "Table 9 (RQ5 confirmation)" | Table 11 |

   - Other README problems:
     - A blank line in the middle of the table breaks the Markdown, so the last three rows render as a separate table.
     - The script is still called `reproduce_table7.py` although it reproduces Table 11.
     - Table 10 still needs a manual `data/` symlink.
   - The README says the dev/test split came from `default_rng(0)`, but gives no code. I checked it: `np.random.default_rng(0).choice(sorted(projects), 4, replace=False)` returns exactly fabric, neutron, nova, sentry.
   - **Fix:** renumber, close the table, rename the script or note it, and add the one-line split command.

3. **[MINOR] Citations of tables and supplementary items.**
   - Table 9 and Table 14 are never cited in the text; Table 14 appears only as "Section 7".
   - The supplementary items are first cited in the order S3, S2, S4, S1. S5 and S6 are never cited.
   - S5 lists `T8`, which is already the source of main-text Table 5.
   - `T3c_W90_share_cabral.md` is generated but never referenced.
   - **Fix:**
     - Cite Table 9 in Section 5.4 and Table 14 in Sections 1 and 4.6.
     - Renumber the S items in order of first citation, or cite them in order.
     - Cite S5 and S6 where they are used: Section 5.2, and the false-clean counts behind Table 7.
     - Drop `T3c` or reference it.

4. **[MINOR] Small accuracy points.**
   - Section 3.2 says "our waits (30 or 90 days) differ from the 15 days" of Song et al. Yet Table 11 has "ODaSC-style W15 +thr", which was run on Cabral test.
   - H1 is a family of six tests, but Section 5.3 reports only five. AWT vs Wait-90 (−0.035, 2/8, CI [−0.074, −0.003]; from `paper_numbers.json` `rq3_tests`) is missing. Report it.
   - Section 6.3 says "Our first reading of RQ1 was wrong (Section 5.2)". The refuted hypothesis, H2a, belongs to RQ2. Reword.
   - The claim "two to three times its share" holds for the leave-out shares, but not for band-in on ApacheJIT at W = 30 (0.489 / 0.341 = 1.4). Say "leave-out" explicitly in Section 5.2 and in the abstract or conclusion.
   - Table 5 shows "—" for ApacheJIT W = 30, L2 without explanation. Add a note that it was not run.

5. **[MINOR] Leftover wording about the internal review.**
   - Table 14, plan_v8 row, gives the reason as "reviewer request". Write "internal (AI) review request", in line with Section 4.6.

6. **[MINOR] S3 labels the true-label column wrongly for E1 rows.**
   - E1 `oracle` is marked `uses_true_labels = False`, but A4 `oracle_gap730` is marked True.
   - **Cause:** `scripts/test_set_usage.py`, line 32, sets the flag only for the experiments E3b, A3, A4, B1 and B3.
   - **Fix:** set the flag from the variant name alone, then regenerate S3.

7. **[MINOR] Figures.**
   - Fig. 1:
     - The caption says "dotted and dashed lines mark 30 and 90 days", but both vertical lines are dotted.
     - The caption explains only the colours, while the plot also uses solid lines for Cabral and dashed lines for ApacheJIT.
     - The caption does not mention that the x-axis is on a symmetric log scale.
   - Fig. 3: the y-axis label "share (AUC)" also covers the grey false-clean-label share, which is not an AUC quantity.
   - Fig. 2 is fine.

8. **[MINOR] Writing and length.**
   - The body is about 11,400 words including tables, with 14 tables and about 116 bullet items.
   - The Results (Sections 5.2–5.5) and Section 6.3 still read like notes. Convert the "Answer to RQx" bullets and the bulleted findings into short paragraphs.
   - Consider moving Table 10 (dev diagnostic) and Table 13 (test list) to the supplement.

9. **[MINOR] Highlights and graphical abstract.**
   - Highlight 1 is exactly 85 characters and compliant. "Lowers … by a median 15.3%" is a relative reduction and can be misread as percentage points; consider "by a relative 15.3% (median)" if the space allows.
   - `graphical_abstract.md` is a description for a designer. The journal needs an actual image if a graphical abstract is submitted. Producing it falls to the authors or production, but say so in the submission checklist.

10. **[MINOR] Declarations. These placeholders legitimately need the human authors:**
    - authors, affiliations and corresponding author;
    - Acknowledgements, Funding, Competing interests and Author contributions;
    - the repository URL and archival DOI;
    - the authors' role and verification in the AI statement;
    - the ethics confirmation;
    - in the cover letter: date, signature, originality/preprint confirmation and AI-policy completion.

    Nothing else is missing: the Consent statement and Compute are present, and the CPU-hours add up (29.5 + 15.0 + 11.6 = 56.1).

### Checks run
- `python scripts/audit_paper_strict.py`: **Unmatched: 0**.
- `python scripts/build_references.py`: 45 references, none uncited, no unresolved "et al." citations. `git status` stayed clean.
- `pytest tests/`: **4 passed** in 158 s. This covers both leakage suites, which test decomp levels, the strata and fabric + kafka.
- **Scratch-copy regeneration:**
  - `review1_shapley.py` and `paper_numbers.py`: all 20 `paper/tables/*.md` files and all 3 PNG figures are **byte-identical** to the committed ones.
  - `test_set_usage.py` in the copy found 0 commits, because it scans the git history and the copy's history is not usable. The committed S3 was checked by hand instead.
- **README:** every referenced script and result file exists, including the archive script, `diag_law.py`, `review2_flip_counts.py`, `flip_counts.json`, both `variants_tried.csv` files and plans v1–v9. The bottom mapping table matches the manuscript's numbering; the re-simulation table does not (concern 2).
- **Numbering:** Tables 1–14 and Figs. 1–3 first appear in order. Tables 9 and 14 are never cited in the text, and the S items are out of order (concern 3).
- **Abstract:** 233 words, one paragraph. **Highlights:** 5 bullets of 85, 83, 78, 75 and 74 characters.
- **Spot checks:**
  - leave-out share ÷ false-clean share: 2.5, 2.1, 2.8 and 2.3;
  - graphical-abstract AUC shares: (0.802 − 0.745) / (0.815 − 0.745) = 0.81;
  - the dev/test split reproduces with `default_rng(0)`.
- **Figures viewed:** see concern 7.
- No tracked file was modified (`git status` clean). The scratch copy is at `/tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/copy`.
