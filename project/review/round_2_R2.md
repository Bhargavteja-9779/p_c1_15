# Review round 2 — Reviewer R2 (novelty/related work), verbatim (simulated reviewer: AI agent with fresh context)

**Referee report: novelty, positioning and related work (round 2)**
Manuscript: "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects"

**Overall score: 5/10. Recommendation: major revision.**

The revision is substantial. It adds the Shapley factorial split, the age strata, AUC as the primary metric, an honest account of test-set reuse and a narrowed RQ5. The empirical core is now more defensible. However, the round-1 positioning concern about Song et al. (2022) was not resolved, and the response to it is factually wrong. Two attributions also misstate their sources, and one of them reverses a finding that bears directly on this paper. Claims C1 and C2 are worded more strongly than Tables 4 and 5 support. The case for this journal is still not made.

### Concerns

**1. [MAJOR] The closest prior experiment, ODaSC-opt and ODaSC-flt in Song et al. 2022, is still ignored, and the round-1 response about it is untrue.**
- Round-1 R2#5 asked the authors to reconcile with ODaSC-opt. `review/round_1.md` replies that ODaSC-opt "could not be located as a separate verifiable publication."
- It is not a separate publication. It is a benchmark inside the cited IJCNN paper (`literature/pdfs/Song_IJCNN2022.txt`, about lines 735–763 and 969–982):
  - ODaSC-opt uses true-label confidence (α = 1 if the observed label is correct, 0 otherwise).
  - ODaSC-flt removes the false-clean examples.
  - Both are compared with OOB trained on observed labels, online, with a 15-day wait, on 14 projects that include 6 Cabral projects.
- The authors' own journal shows they knew this. `journal/ENTRIES/20261124T040516_TURN_...md` cites "ODaSC (Song et al. IJCNN 2022, Table II) … ODaSC-opt" by name.
- This is a noisy-versus-clean contrast in the same online waiting setting. It is the closest prior work for C1, closer than Falessi or Fan, which the claim table names instead.
- The two sets of results also disagree in size. From Table II of Song et al.: OOB mean G-mean 0.582, ODaSC-flt 0.616, ODaSC-opt 0.621, so clean labels gain about +0.035–0.04. Here, L1 gains +0.102 at W = 30. In Song et al., estimated confidence was statistically indistinguishable from optimal confidence (p = 0.73). Here, the kNN adaptation ties waiting on ApacheJIT.
- **Resolution:**
  - Add ODaSC-opt/flt to Section 2.2, to the C1 row and to the Discussion.
  - Explain the difference in effect size. Candidate reasons: relabel versus filter versus reweight; W = 15 versus 30/90; Hoeffding-tree OOB versus LightGBM; first 10k commits versus full histories.
  - Restate the novelty as the freshness/noise factorial plus age localisation, not the noisy-versus-clean contrast in the online setting.
  - Correct the response letter.

**2. [MAJOR] Song et al. 2023a is misattributed, and the conflict with it is not addressed.**
- Section 2.1 says it "showed that retrospective evaluation can misjudge methods if waiting time is not modelled."
- The EMSE abstract says the opposite: "the choice of waiting time did not have a significant impact on the validity and that even small waiting times resulted in high validity."
- That finding bears directly on this paper. Song et al. find that waiting-time noise is negligible for evaluation; this paper finds it dominates the training penalty.
- **Resolution:** correct the sentence and add a paragraph explaining why noise can matter for training but not for evaluation.

**3. [MAJOR] Falessi et al. 2022 is mischaracterised, which weakens the contrast drawn in C2 and Section 6.2.**
- The manuscript says Falessi et al. "showed that discarding the most recent releases helps" (Section 2.2). Section 6.2 adds that "at release level, dropping the latest release removes most of the snoring."
- What Falessi et al. actually removed is only the classes *labelled non-defective* in the last release(s), keeping the positives (TOSEM full text, RQ2, lines 592–635). That is the release-level counterpart of Wait-W.
- They also report that the gain is "particularly small in terms of AUC" and that removing more than one release hurts. Nothing supports "removes most of the snoring" (the 50%-of-releases removal is used for their clean reference set, not as a countermeasure).
- **Resolution:** describe the countermeasure correctly and present Wait-W as its online analogue. Then reframe the "localisation differs" argument, because the actual difference is the granularity of the cut-off, not the mechanism.

**4. [MAJOR] C1 ("mainly label noise") is worded more strongly than the W = 90 evidence supports.**
- At the tuned W = 90 on Cabral, the noise-first path share is 0.44 [0.33, 0.54], and the interaction (0.054) is close to the label effect (0.066).
- The Shapley share of 0.74 depends on splitting the interaction equally between the two factors. With an interaction this large, attribution is a convention rather than a measurement.
- The abstract's "adding the recent commits contributes nothing on average" (W = 30) hides a positive Oracle − L1 contrast inside the averaged freshness term.
- **Resolution:**
  - Make the interaction the headline: "the noise and the freshness are the same commits." The paper already says this in Section 5.2, and it is the more original result.
  - Report both path shares in the abstract.
  - Tone down "mainly" for W = 90.

**5. [MAJOR] C2 (the 30–180-day localisation) is partly an artefact of the design and is reported only at W = 30.**
- The lower bound of 30 days is set by W = 30, so the claim "neither the youngest commits" holds by construction.
- The bands have unequal widths (150, 185, 365 days, and open-ended) and unequal numbers of false-clean commits. Table 2 shows false-clean rates fall with age, so the band shares may simply track where the false-cleans are.
- On ApacheJIT the band explains only 0.49 of the AUC gain, and the bands do not add up. Contribution 2's "almost entirely" therefore holds only for Cabral.
- No strata are reported at the tuned W = 90.
- **Resolution:** report the gain per relabelled false-clean commit and the number of flips per band. Run the strata at W = 90 (on ApacheJIT at least). Qualify the wording for ApacheJIT.

**6. [MINOR] The ODaSC description and the adaptation diverge from the source.**
- In ODaSC, "counted as both classes" applies only to the micro-cluster counters (Eq. 12). Training uses the observed label with a confidence-modulated Poisson oversampling rate, Λ = λ·e^(α−δ) (Eq. 11).
- The ODaSC-style rule here counts low-confidence commits as both classes *in training*, which is a different mechanism.
- Song et al. also tuned at W = 15, while here W ∈ {30, 90}.
- **Resolution:** state these differences in Sections 3.2 and 7. C4 ("depends on implementation") should be framed as a claim about the adaptations, not about ODaSC.

**7. [MINOR] Waiting-rule credit.** Tan et al. (2015) already introduced the labelling gap or wait for online defect prediction. Cabral et al. (2019) cite it and use a variant in which positives are visible early. Credit both in Section 1 and in the Terminology table.

**8. [MINOR] Missing related work.**
- Liu et al. 2025, SCICO, "Human-in-the-loop online JIT-SDP: what have we achieved…" (10.1016/j.scico.2025.103296). It is already in `paper/crossref_cache.json` and was requested in round 1. It revisits HumLa (Song et al. 2023b) and the timing of human labels, so it belongs alongside Song et al. 2023b.
- Song & Minku 2023 (TSE) also showed that waiting-time label noise affects the validity of *continuous* evaluation. That finding should be stated, since the current text mentions only the procedure.
- I found no work that pre-empts the factorial decomposition or the age localisation. Searches on verification latency or waiting time combined with label noise in JIT-SDP returned only the Song/Minku/Cabral line of work.

**9. [MAJOR] Fit and value for this journal are not argued.**
- Section 2.5 explains only why MSTDP is not comparable. It does not say why a negative, diagnostic study belongs in a journal that publishes mostly method papers.
- The proposed method (LAW) failed, and none of the deployable methods significantly beats Wait-90 on fresh data.
- **Resolution:** argue the value explicitly: a benchmark protocol plus the true-label bound (0.735 versus 0.762) as a target for method papers, with released tooling. Alternatively, consider an empirical software engineering venue.

**10. [MINOR] Honesty and coherence.**
- The narrative of refuted hypotheses is commendably transparent.
- Two points undercut it:
  - the false statement about ODaSC-opt in the response letter (Concern 1);
  - the C1 framing that credits Falessi and Fan while omitting the in-domain precedent.
- The Contributions list (six items) mixes findings with protocol hygiene. Item 6 is not a scientific contribution.

### Citation attributions checked

| # | Claim in manuscript | Source checked | Accurate? |
|:--|:--|:--|:--|
| 1 | ODaSC estimates clean-label confidence from micro-cluster class composition and counts low-confidence examples as both classes | Song et al. 2022, full text (Sections IV–V) | Partly. "Both classes" applies to cluster counters only; training uses confidence-weighted oversampling |
| 2 | Song et al. 2022 is the closest prior work, and the noisy-vs-clean design is credited to Falessi and Fan | Song et al. 2022, full text (ODaSC-opt/flt, Table II) | No. Omits the in-paper true-label benchmark |
| 3 | Song et al. 2023a: retrospective evaluation can misjudge methods if waiting time is not modelled | EMSE abstract | **No, the finding is reversed** |
| 4 | Falessi et al. 2022 compared models trained on dormant-noisy and clean labels | TOSEM full text, RQ1 | Yes |
| 5 | Falessi et al. 2022: discarding the most recent releases helps; dropping the latest release removes most snoring | TOSEM full text, RQ2 | No. Only non-defective classes are removed; "most" is unsupported |
| 6 | Cabral et al. 2019 introduced the waiting-time rule with ORB for class-imbalance evolution | ICSE full text | Yes (Tan et al. 2015's earlier gap is not credited) |
| 7 | Cabral & Minku 2023: drift plus latency impairs stability; they propose a more stable approach | TSE full text, abstract | Yes |
| 8 | Falessi et al. 2020: ignoring time order inflates offline estimates | EMSE abstract | Yes, broadly (walk-forward is less biased; all techniques tend to overestimate) |
| 9 | Tian et al. 2026 combine waiting time with test feedback | TOSEM abstract | Yes |
| 10 | Grzenda et al. 2020 treat delayed labels as an evaluation problem | DMKD abstract | Yes |
| 11 | Gomes et al. 2023 survey delayed, partially labelled streams | CSUR abstract | Yes |
| 12 | Cabral et al. 2023 study online JIT-SDP with prequential evaluation | EMSE abstract (BORB) | Yes |
| 13 | MSTDP uses an offline chronological 80/20 split with final labels | JKSU full text (literature/fulltext) | Yes |
| 14 | Guo et al. 2024 address SZZ labelling errors in JIT-SDP | TOSEM abstract | Yes |

### Status of round-1 R2 concerns

| R2 concern | Status |
|:--|:--|
| #1 C1 overstated vs Falessi/Fan | Partly resolved. ODaSC-opt is still missing (Concern 1) |
| #2 Order dependence | Resolved (Shapley split) |
| #3 RQ2 used only G-mean@0.5 | Resolved (AUC primary) |
| #4 "Old" noise not tested | Resolved, and it changed the story. The new localisation is still incompletely controlled (Concern 5) |
| #5 Reconcile with Song 2023a, Song & Minku 2023 and ODaSC-opt | Not resolved. The response is incorrect and Song 2023a is misread |
| #6 C4/C5 claim-table row | Resolved |
| #7 Significance for a methods journal | Not resolved (Concern 9) |
| #8 Wording | Resolved |
| #9 Missing related work | Mostly resolved; SCICO 2025 still missing |
| #10 Reference names | Resolved |
| #11 C3 concerns the kNN adaptation | Resolved in wording; the mechanism difference is still unstated (Concern 6) |
| #12 Evaluation-label dormancy | Resolved (730-day sensitivity) |

No files were modified. The main evidence comes from:
- `/home/user/p_c1_15/project/literature/pdfs/Song_IJCNN2022.txt`
- `/home/user/p_c1_15/project/literature/pdfs/Falessi_TOSEM2021.txt`
- `/home/user/p_c1_15/project/paper/crossref_cache.json`
- `/home/user/p_c1_15/project/journal/ENTRIES/20261124T040516_TURN_from__correct_the_noisy_labels__to__which_part_of_.md`
- `/home/user/p_c1_15/project/review/round_1.md`

Sources (web): https://minkull.github.io/publications/SongEMSE2023.pdf ; https://research.birmingham.ac.uk/en/publications/a-novel-data-stream-learning-approach-to-tackle-one-sided-label-n ; https://liu906.github.io/papers/1-s2.0-S0167642325000358-main.pdf
