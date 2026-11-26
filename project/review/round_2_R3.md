# Review round 2 — Reviewer R3 (clarity/reproducibility/ethics), verbatim (simulated reviewer: AI agent with fresh context)

## Referee report: clarity, reproducibility, ethics and journal compliance (round 2)

**Manuscript:** "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects" (v2)

**Overall score: 7/10. Recommendation: minor revision.** The two items tagged [MAJOR] below are must-fix problems with the accuracy of the disclosures, but they can be fixed in the text without new experiments.

### Summary
The revision is a real improvement. The README fast path regenerates every table and figure byte for byte. The strict audit finds no unmatched numbers. Both leakage suites pass. The test-set reuse, the two analysis lineages and the deviations from plan (Table 12) are now disclosed openly, and the story was honestly rewritten from "old noise" to "commits 30–180 days old". Most round-1 concerns are resolved. What remains:
- the disclosure of test-set use is incomplete, although it is presented as complete;
- the AI-simulated round-1 review is not disclosed and is described as if it were real peer review;
- a few claims are worded more strongly than their own tables support;
- labels and names are inconsistent between files, tables and the text;
- Fig. 1 needs another pass.

### Round-1 concerns: status
- **Resolved:**
  - R1: #1–3, #6–8, #10–14.
  - R2: #1–4, #6–12.
  - R3: #1–6, #9–15.
- **Rebuttal accepted as a stated limitation:** R1#5 (no unified, retuned ODaSC) and R1#9 (CIs not adjusted).
- **Partly resolved:**
  - R1#4 / R3#5: Table S3 is incomplete (concern 1). R1#4 also asked for the outcomes per branch, which S3 still does not give.
  - R3#8: Fig. 1 still has a title inside the image (concern 6).
  - R3#7: the declaration placeholders remain. This is legitimate, because only the authors can fill them.

### Concerns

1. **[MAJOR] Table S3 misses the revision's own Cabral test runs, but the paper calls it complete.**
   - **Evidence:** Section 4.6, Contribution 6 and the Threats section say S3 lists "every configuration ever run on the reused test set" (27 full runs plus 3 smoke runs). `results/review1/raw.jsonl` also contains 9 configurations run on the 10 Cabral test projects:
     - A3: `strata_30_180`, `strata_180_365`, `strata_365_730`, `strata_730_inf`, 50 runs each;
     - A4: `decomp_L1_W30_gap730`, `nowait_gap730`, `oracle_gap730`, `wait_W30_gap730`, `wait_W90_gap730`, 20 runs each.
   - **Cause:** `scripts/test_set_usage.py` only matches per-run `results/*.json` file names, so jsonl results are never seen.
   - These runs are diagnostics with true labels, so the effect on inference is small. The problem is that a disclosure described as complete is not.
   - Also, A4 used only seeds 100–101. That is stated in `plan_v8_review1.yaml` but not in the paper.
   - **Fix:** extend the scanner to read the jsonl files, regenerate S3, and update the counts in Section 4.6 and the Threats section. State the 2-seed design of A4 in the paper.

2. **[MAJOR] The internal, AI-simulated review round is presented as real peer review.**
   - `review/round_1_R3.md` is headed "(Simulated reviewer, fresh context)".
   - The manuscript says the decomposition was "revised and extended in response to reviewers" (Section 1). It also refers to "the first version of this study" (Section 3.3), "first manuscript version" (Table 12, plan_v3 row) and "the first version of this paper's explanation" (Section 6.3).
   - Editors at JKSU-CIS will read this as an earlier external review or an earlier submission. Neither is declared in the cover letter.
   - **Fix:** either remove the version history from the main text, or disclose in Section 4.6 and in the AI statement that an AI agent ran an internal review round. Give the model and version in the AI statement as well.

3. **[MINOR] The plural "denoisers" overstates what was run on the Cabral test set.**
   - Abstract: "Feature-based denoisers beat it on the reused Cabral test set". Conclusion: "Feature-based denoisers beat waiting on one dataset".
   - According to S3, only the second lineage's ODaSC-style rule (`odasc_W30`) was ever run on Cabral test, as a single comparison that was not pre-registered. LAW-M, Dual and the main lineage's ODaSC were never run there.
   - **Fix:** write "one ODaSC-style adaptation", as Contribution 4 already does.

4. **[MINOR] The age-band claims are stronger than Table 5 / T9 support.**
   - Highlight 3 says "older commits add nothing". On Cabral, the 180–365-day band adds an AUC share of 0.173 (10/10 projects, p = 0.002). The highlight would be accurate as "commits over a year old add nothing".
   - Contribution 2 says relabelling commits older than one year "adds nothing". On Cabral, the 365–730-day band gives AUC +0.004 (9/10 projects, p = 0.006).
   - Section 5.2 says the oldest bands "slightly lower" both metrics on ApacheJIT. In G-mean, the 365–730 band has share −0.132 and the ≥730 band has share −0.12 (1/9 projects improved, p = 0.027). Those G-mean rows are in the T9 file and Fig. 3 but not in the printed Table 5.
   - **Fix:** reword these claims, and add the missing G-mean rows to Table 5.

5. **[MINOR] Names and labels are inconsistent.**
   - **Policy names:**
     - "ORB-W" (Section 3.2), "ORB-style-90" (tables) and "ORB-90" (text).
     - "AWT" vs "Adaptive waiting (ε = 0.4)".
     - Internal identifiers in Table 6 ("LAW (lagakos, …)").
   - **ODaSC-style rows:** Table 9's "ODaSC-style W30" is the second lineage's k50/δ0.9 version, while Table 7's row is the main lineage's θ0.8 version. Tag every ODaSC-style row with its lineage.
   - **Hypotheses:** H1, H2a, H3, H6, H9a and H9b are used but never listed together. Add a short list of hypotheses.
   - **File names vs table numbers:**
     - Table 4 = `T3b`, Table 5 = `T9`, Table 7 = `T5`, Table 8 = `T6`, Table 9 = `T7`, Table 10 = `T11`, Table 11 = `T11b`.
     - Supplementary S4 = `T10_…`, which is easily confused with main-text Table 10.
     - `T3c` (Cabral W = 90 path share) is never referenced.
     - The README script for Table 9 is still called `reproduce_table7.py`.
   - **Fix:** rename the files to match the table numbers (or add a mapping table to the README), and label the supplementary items S1–S5 consistently.

6. **[MINOR] Figures.**
   - **Fig. 1:**
     - Still has a title inside the image (R3#8).
     - No legend: the colours are explained only in that title, and the 30/90-day lines are not labelled.
     - The x-axis stops at 1,500 days, while P90 delays reach 2,811 days.
     - Blue/red is the only cue; vary line style as well for readers with colour-vision deficiencies.
   - **Fig. 2:**
     - Where the true-label gain exceeds the oracle gap in G-mean (npm, wagtail, broadleaf, camel, jgroups), the filled bar hides the outline.
     - The two "oracle − Wait-30" legend entries look identical.
     - The legend shows only the red (ApacheJIT) colour.
     - There are no panel letters.
   - **Fig. 3:** acceptable.

7. **[MINOR] Parts of the method are described only in the Results.**
   - The latency-corrected G-mean threshold rule ("+thr") and the "second-lineage simulator" (Table 10) are introduced only in Section 5.5.
   - **Fix:** describe both in Section 3, and say how the second lineage's simulator differs from the main one, or that it does not.

8. **[MINOR] Table structure.**
   - Three tables are unnumbered: the Terminology table, the claims table in Section 2.4 and the inline spread table in Section 5.5. The last one duplicates Table 8.
   - Table 12 and Table 5 are cited (in Section 1) before Tables 2–4. Springer expects tables to be numbered in order of first citation.

9. **[MINOR] Format and length for this journal.**
   - The abstract has 381 words and uses nested bullets. Springer journals usually ask for a single paragraph of about 150–250 words; check the JKSU-CIS author guide.
   - The body is about 9,500 words with 12 tables. That is acceptable, but heavy use of bullets in the Results and Discussion reads like notes. Convert key passages to prose.
   - The graphical abstract plots G-mean, in which L1 (0.722) sits above the oracle (0.715). This contradicts the paper's decision to make AUC the primary metric. Use AUC instead.

10. **[MINOR] README.**
    - The "Data" section mentions only the Cabral data, although `get_data.py` also downloads ApacheJIT.
    - The legacy "Reproduce" block (E1–E3, `final_report.py`, `audit_numbers.py`) duplicates and contradicts the fast path. It calls `run_all.py --mode quick` "<1 min" in one place and "a few minutes" in another.
    - Table 8 needs a manual `data/` symlink in the archive folder.
    - `results/diag_law_neutron.json` and `diag_survival_dev.txt`, cited in Section 5.3, have no README command (`scripts/diag_law.py` exists).
    - The seeded dev/test draw (rng(0), stated in `plan_v1.yaml`) has no code; the split is hard-coded.
    - The pinned `requirements.txt` includes torch and xgboost, which appear to be unused.

11. **[MINOR] Declarations.**
    - **Placeholders that legitimately need the human authors:**
      - authors, affiliations and corresponding author;
      - the authors' role and verification in the AI statement;
      - funding, competing interests and author contributions;
      - repository URL and archival DOI;
      - ethics confirmation;
      - cover letter date, signature, and originality/preprint confirmation.
    - **Missing:** Acknowledgements, and "Consent to participate/publish: not applicable". In the AI statement, name the model and version and the scope of AI use, including the internal review (concern 2).

### Checks run
- `python scripts/audit_paper_strict.py`: **Unmatched: 0**.
- `python scripts/build_references.py`: 44 references, none uncited, none unresolved. The working tree stayed clean afterwards.
- `tests/test_no_future.py`: **passed**. `tests/test_no_future_threshold_rules.py`: **passed**.
- `review1_shapley.py` and `paper_numbers.py`, run in a scratch copy: all `paper/tables/*.md` and all three PNG figures are **identical** to the committed files. In the copy, `test_set_usage.py` found 0 commits because it reads the parent git repository; this does not affect the manuscript.
- `results/review1/raw.jsonl` inspected: revision runs on the Cabral test set (A3, A4) are not in S3 (concern 1). A4 has 2 seeds and 10 Cabral + 9 ApacheJIT projects.
- README commands: every referenced script exists, including the archive script, and `enqueue.py` defines E0–E0e, E1, E3b and E8. Installed Python 3.13 and package versions match `requirements.txt`.
- Arithmetic spot checks are consistent:
  - 265,003 + 66,934 = 331,937 commits; 29.5 + 15.0 + 5.0 = 49.5 CPU-hours.
  - Exact Wilcoxon/Holm values (0.0039, 0.0078, 7 × 0.0039 = 0.027).
  - Detectable difference ≈ 0.020 at SD 0.0192 and n = 9.
- Highlights: 5 bullets of 75, 78, 73, 79 and 81 characters, so the format is compliant. The content issue in Highlight 3 is covered in concern 4.
- Figures viewed: see concern 6.
- `git status`: clean. No tracked file was modified.
