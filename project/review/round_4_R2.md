# Review round 4 — Reviewer R2 (novelty/related work), verbatim (simulated reviewer: AI agent with fresh context)

## Referee report, round 4 (R2: novelty, positioning, related work)

**Overall score: 8/10. Recommendation: minor revision.**

None of the issues below blocks acceptance. Every round-3 R2 concern has been dealt with in substance, and each remaining item can be fixed by rewording.

**Novelty and fit:**
- I found no prior work that pre-empts the noise/freshness factorial design or the age-band localisation. I ran a fresh web search and re-checked the closest work (Song 2022 ODaSC-opt/flt, Falessi 2022, Liu 2025, Tian 2026, Song 2023a).
- The positioning against ODaSC is now fair and well argued.
- Fit with the journal is adequate: Section 2.5 frames the study as a source of bounds and an evaluation guide for the journal's method papers.
- Honesty is unusually high: refuted hypotheses, test-set reuse, plan deviations and AI provenance are all disclosed.

### Status of the round-3 R2 concerns

| # | Concern | Status in v4 |
|:--|:--|:--|
| 1 | "2–3×" holds only for leave-one-band-out | Resolved in the abstract, Contribution 2, §5.2, §6.1, the Conclusion and the cover letter. **Highlight 4 is still unqualified** (Concern 5) |
| 2 | ODaSC-opt contrast | Resolved: OOB-based numbers are used, and "estimated ≈ optimal there, far from optimal here" is now the point. Residual comparability issues remain (Concern 3) |
| 3 | Table 2 out of step | C2, C4 and C5 resolved. The parenthetical in C1 is misplaced (Concern 4) |
| 4 | Age-only corrections implied on fresh data | Resolved in the abstract and the RQ3 answer. Contribution 3 still says "cannot" (Concern 1) |
| 5 | Liu 2025 summarised only partly | Resolved: all three points are accurately stated (checked against the PDF) |
| 6 | BORB under-used | Partly: it is cited in §3.1 but not in the external-validity threats (Concern 6) |
| 7 | Falessi wording | Resolved in §2.2. **§6.2 still understates the effect** (Concern 2) |
| 8, 9 | Optional context | Declined (Concern 7) |
| 10 | Honesty | Still good |

### Concerns

**1. [MINOR] The age-only claim is overstated, and the label is imprecise.**
- Contribution 3 says "age-only corrections **cannot** recover the penalty", and Table 2 C3 says they "do not recover it". The RQ3 answer says only "Not reliably".
- At the operating point the losses to Wait-90 on Cabral are not significant (Holm p ≥ 0.148). In AUC, LAW beats Wait-90 on Cabral (+0.024).
- On ApacheJIT, LAW at 0.5 has 0.732 G-mean. That is descriptively above Wait-90 and LAW-M, and close to the best denoiser, Dual (0.735).
- LAW with the model prior is also not "age-only". Its prior p is the previous model's feature-based score, but RQ3 is defined as "corrections that use only commit age".
- The abstract's "lost to a 90-day wait" suggests a significant loss.
- **Resolution:**
  - Write "did not reliably recover" in Contribution 3 and C3.
  - Write "had lower means than (not significant)" in the abstract.
  - Call the family "age-based (delay-posterior) corrections", or state that the model-prior variant also uses features.

**2. [MINOR] §6.2 still misrepresents Falessi et al. (2022).**
- §6.2 says the countermeasure "improved accuracy significantly but modestly, particularly little in AUC", and concludes that "such cut-offs help little in both settings".
- Falessi et al. report that removing the last release's non-defective classes raises "Recall, F1, Kappa, and Matthews … by about 30%" (Falessi_TOSEM2021.txt, l. 89–92). Only the AUC gain is "particularly small" (l. 1015).
- In this paper's own data, waiting also helps a lot in G-mean: Wait-90 scores 0.654, Wait-30 0.620 and No-wait 0.429.
- Falessi et al. also anticipate two of this paper's points:
  - the trade-off between the amount and the quality of the data (l. 1386);
  - the recommendation to "identify which specific class in the last releases is erroneously labeled" (l. 1393), which is essentially this paper's closing recommendation.
- **Resolution:**
  - Write "large gains in recall/F1/MCC, small in AUC".
  - Restrict "help little" to AUC.
  - Credit Falessi et al. as the release-level precedent for the recommendation to target recent mislabelled items.

**3. [MINOR] The ODaSC effect-size comparison in §6.2 is still not like for like.**
- Song et al. compute G-mean prequentially with a fading factor of 0.99, over commits 2,000–10,000 (Song_IJCNN2022.txt l. 910–929). This paper's G-mean is computed differently, so "two to three times as much" compares different metrics.
- On the five projects shared with the Cabral test set, ODaSC-opt − OOB is +0.053 (from `song2022_table2_means.json`). That makes the ratio about 1.9×.
- The wait-length explanation points the wrong way: a 15-day wait leaves *more* noise to remove, not less.
- **Resolution:**
  - Add the metric caveat and the ratio on the shared projects.
  - Rephrase the wait-length bullet.

**4. [MINOR] The C1 row in Table 2 and Contribution 1 are worded misleadingly.**
- C1 reads "for short waits the penalty is label noise (path share 0.44–0.78 at W = 90)". The W = 90 numbers do not support the short-wait clause they are attached to.
- **Resolution:** write "(path share 0.81–0.92 at W = 30; 0.44–0.78 at W = 90)".
- Contribution 1 says "almost entirely label noise" for a path share of 0.81. "Mostly" fits better.

**5. [MINOR] Highlight 4 is unqualified.**
- It says "Per wrong label, the commits just past the wait do the most harm".
- On ApacheJIT at W = 90 in the band-in design, that band recovers 0.203 of the gain with 0.216 of the false-clean labels, which is exactly its share.
- **Resolution:** add "when the other bands are corrected".

**6. [MINOR] BORB is missing from the threats.** The external-validity point "One learner (LightGBM) …" should note that Cabral et al. (2023) found offline learners competitive in online JIT-SDP. This was requested in round 3 but only half done.

**7. [MINOR, optional] Missing context, and the reason given for declining it is weak.**
- The triage declines R2 #8/#9 as "would need verification".
- Krempl et al. (2014, SIGKDD Explorations, "Open challenges for data stream mining research") and Marrs et al. (2010) are the standard sources for the term "verification latency" and are easy to verify.
- One JKSU-CIS drift or label-noise paper (e.g., DMAE, 10.1007/s44443-026-01127-1) would strengthen the journal-fit section.

**8. [MINOR] The Declarations are out of date.** "Use of AI" mentions "two internal review rounds", but three exist (`review/round_1`–`3`). Update the count, and check §4.6 for the same.

### Attribution check

| # | Attribution in the manuscript | Source checked | Verdict |
|:--|:--|:--|:--|
| 1 | ODaSC-opt and ODaSC-flt do not differ from ODaSC (p = 0.7278, 0.6932); ODaSC beats OOB | Song 2022 txt l. 977–980 | Accurate |
| 2 | Song 2022 used the first 10,000 commits of 14 projects and W = 15 | Song 2022 l. 649, 921–930 | Accurate (tuned on 0–2k, evaluated on 2k–10k; fading-factor G-mean not mentioned) |
| 3 | Table II means: opt 0.621, flt 0.616, OOB 0.582 (+0.039/+0.034) | `song2022_table2_means.json` | Accurate. The "2–3×" comparison is not like for like (Concern 3) |
| 4 | Cabral 2019: clean after ω days, defective as soon as found | Cabral ICSE txt l. 274–277 | Accurate |
| 5 | Tan 2015 introduced a labelling gap | Cabral ICSE l. 376–377 (positives also wait in Tan) | Accurate |
| 6 | Cabral & Minku 2023: drift plus latency impair stability; a more stable approach is proposed | TSE txt abstract | Accurate |
| 7 | Cabral et al. 2023: offline base learners can beat online Hoeffding-tree ensembles | EMSE abstract (crossref_cache) | Accurate |
| 8 | Song 2023a: 13 GitHub projects; waiting time had no significant impact on validity; short waits gave high validity | EMSE abstract | Accurate |
| 9 | Song & Minku 2023: waiting-time noise affects continuous evaluation | As stated in the Song 2023a abstract | Accurate |
| 10 | Liu 2025: practical-scenario degradation; observed-label evaluation; human feedback helps at equal delay through label quality | SCICO PDF abstract | Accurate |
| 11 | Falessi 2022 (§2.2): significant gain, little in AUC; two releases improve recall, reduce precision | TOSEM l. 14, 1011–1016 | Accurate |
| 12 | Falessi 2022 (§6.2): "significantly but modestly" | TOSEM l. 89–92 (about 30% in recall/F1/MCC) | **Inaccurate** (Concern 2) |
| 13 | Tian 2026: combines waiting time with test feedback | TOSEM abstract | Accurate |
| 14 | MSTDP: offline chronological 80/20 split, final labels | JKSU full-text HTML | Accurate |
| 15 | Chapelle 2014 posterior p·S/(1 − p + p·S) | Known model (exponential S in the original) | Accurate (generalised to a nonparametric S, which is stated as adaptation) |

No files were modified. Main evidence:
- `/home/user/p_c1_15/project/literature/pdfs/Falessi_TOSEM2021.txt`
- `/home/user/p_c1_15/project/literature/pdfs/Song_IJCNN2022.txt`
- `/home/user/p_c1_15/project/literature/pdfs/CabralICSE2019.txt`
- `/home/user/p_c1_15/project/results/review1/song2022_table2_means.json`
- `/home/user/p_c1_15/project/paper/crossref_cache.json`
- `/tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/liu/liu.txt`

Sources (web search; nothing published in 2026 that pre-empts this study turned up):
- [Song et al. 2023a, EMSE (PDF)](https://research.birmingham.ac.uk/files/206466882/s10664_023_10341_8.pdf)
- [Song et al. 2022, ODaSC](https://research.birmingham.ac.uk/en/publications/a-novel-data-stream-learning-approach-to-tackle-one-sided-label-n)
- [Cabral & Minku, "Towards reliable online JIT-SDP"](https://research.birmingham.ac.uk/en/publications/towards-reliable-online-just-in-time-software-defect-prediction/)
- [IRJIT, arXiv 2210.02435](https://arxiv.org/pdf/2210.02435)
