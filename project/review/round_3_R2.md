# Review round 3 — Reviewer R2 (novelty/related work), verbatim (simulated reviewer: AI agent with fresh context)

**Referee report, round 3: novelty, positioning and related work**
Manuscript: "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects" (`/home/user/p_c1_15/project/paper/manuscript.md`)

**Overall score: 7/10. Recommendation: minor revision.** All remaining issues can be fixed by rewording. None needs new experiments.

v3 deals with the substance of every round-2 R2 concern:
- ODaSC-opt/flt are now described and credited.
- The Song 2023a reading is corrected, and there is a new paragraph on training versus evaluation.
- The Falessi countermeasure is described correctly.
- Tan 2015 is credited.
- Liu 2025 and the Song & Minku finding are added.
- The interaction is now the headline, and the abstract gives both the path share and the Shapley share.
- The flip counts per band and the W = 90 strata were run.
- A journal-fit paragraph was added (Section 2.5).
- The contributions were cut to four.
- The triage document admits that the round-1 ODaSC-opt response was wrong.

I found no prior work that pre-empts the noise/freshness factorial or the age localisation. I searched the web and checked the repo's OpenAlex hits; the nearest hits were CodeFlowLM (arXiv 2512.00231), Tian 2026 and HumLa/Liu 2025. The novelty claim in Contribution 1 ("the separation of noise from freshness is new") holds.

What remains: one headline claim that holds under only one of the two designs, one misleading comparison with the closest prior work, and a few inconsistencies in the claim table.

### Concerns

**1. [MAJOR, text only] "Two to three times their share" holds only for the leave-one-band-out design.**
- The abstract, Contribution 2, Section 6.1, the Conclusion and the cover letter all state this ratio for "both families and both waits".
- From Table 7, the ratio of the recent band's share of the gain to its share of false-clean labels is:

| Setting | Leave-out ratio | Band-in ratio |
|:--|--:|--:|
| Cabral, W = 30 | 2.5 | 2.7 |
| Cabral, W = 90 | 2.8 | 3.1 |
| ApacheJIT, W = 30 | 2.1 | 1.4 |
| ApacheJIT, W = 90 | 2.3 | 0.94 |

- On ApacheJIT at W = 90, relabelling only the recent band recovers 0.203 of the gain with 0.216 of the labels. That is exactly its share.
- On ApacheJIT the recent band is therefore harmful mainly *in combination with* the other bands, the same caveat the paper already applies to the older bands. This is the remaining part of round-2 R2 #5.
- **Resolution:**
  - Say "when the other bands are corrected (leave-one-band-out)" wherever the ratio is quoted.
  - State that on ApacheJIT the band-in ratio is 1.4× at W = 30 and about 1× at W = 90.
  - Soften the highlight and the Answer to RQ2 for ApacheJIT.

**2. [MINOR, substantive] The effect-size comparison with ODaSC-opt/flt (Section 6.2) sets unlike contrasts side by side.**
- Section 6.2 sets Song et al.'s "true confidences brought no significant gain *over estimated confidences*" against "our L1 gains +0.102 *over Wait-30*".
- The like-for-like contrast is clean-label benchmark versus the observed-label learner (OOB). From Song et al. Table II (`literature/pdfs/Song_IJCNN2022.txt`, about lines 800–900):
  - Means over 14 projects: OOB 0.582, ODaSC-flt 0.616, ODaSC-opt 0.621, i.e. +0.034 and +0.039.
  - On the 5 projects shared with the Cabral test set (brackets, broadleaf, camel, jgroups, tomcat), ODaSC-opt − OOB is +0.053 on average.
- So the gap is about 2×, not "no gain versus +0.10".
- The more telling contrast is a different one, and it is not discussed:
  - Song et al. found estimated confidence ≈ optimal confidence.
  - Here, the ODaSC-style adaptations (0.718 on ApacheJIT) sit far below the true-label condition (0.762).
- The paper's first bullet already gives a plausible reason: ODaSC-opt with α = 0 still trains on the noisy example, only at a reduced oversampling rate, and adds no positive.
- **Resolution:** report the OOB-based numbers, and discuss the "estimated ≈ optimal there, far from optimal here" discrepancy as the real point of difference.

**3. [MINOR] The claim table (Table 2) is out of step with the body.**
- **C4** still says "depends on dataset *and implementation*". The triage removed "depends on implementation", and Section 5.4 says the two implementations agree on ApacheJIT. Change it to "dataset (or selection on the reused set)".
- **C5** ("helps only policies with a distorted prior") is stated as a claim, but Section 5.5 calls the distorted-prior reading post hoc. The supported claim is narrower: "on fresh data, the threshold significantly helped only No-wait".
- **C1:** add "(path share 0.44–0.78 at W = 90)" so that the "for short waits" qualifier is visibly tied to the evidence.

**4. [MINOR] The abstract and Section 6.1 imply that age-only corrections were tested on fresh data.**
- Adaptive waiting never ran on ApacheJIT.
- LAW ran there only inside the H9 threshold family. At 0.5 it was descriptively *ahead* of Wait-90 (+0.015, unadjusted p = 0.039; Section 5.3).
- **Resolution:** reword the abstract sentence to "Age-only corrections lost to a 90-day wait at the operating point on Cabral; feature-based denoisers and a latency-aware threshold did not significantly beat it on fresh data."

**5. [MINOR] Liu et al. 2025 is summarised only partly, and the omitted part bears on this design.**
- The abstract (PDF read) says HumLa's performance under practical conditions "significantly deviate[s]" from what was reported.
- It also advocates evaluating online classifiers with *observed* labels, not ground-truth labels.
- The manuscript evaluates against final labels.
- **Resolution:**
  - State Liu et al.'s evaluation recommendation, and justify final-label evaluation as a retrospective research protocol (consistent with Song 2023a).
  - Note that Liu et al.'s finding that HITL helps "even when SQA feedback delay equals BFC delay" (by improving label quality) independently supports the label-noise thesis.

**6. [MINOR] Cabral et al. 2023 (BORB) is under-used.**
- It is cited only as "online JIT-SDP with prequential evaluation".
- Its contribution is that *offline (batch) base learners* in an online, waiting-time JIT-SDP setting outperform online Hoeffding-tree ensembles (EMSE abstract in `crossref_cache.json`).
- That is the direct precedent for the paper's batch-retrained LightGBM, and it softens the "one learner, not Hoeffding trees" threat.
- **Resolution:** cite it in Section 3.1 and in the external-validity threats.
- Optional: the 2021 BORB thesis ("Batch algorithms and fixed prediction rates for online JIT-SDP", in `literature/prior_art_hits.json`) studies fixed defect-prediction rates. This is a precedent for the rate-matching threshold in RQ5.

**7. [MINOR] Falessi et al. (2022) residual wording.**
- Section 6.2 says the countermeasure "brought small gains".
- The TOSEM abstract says removing the last release's non-defective classes "significantly improves the accuracy"; the gain is small specifically in AUC.
- Section 2.2 says "removing more than one release reduced precision", but the RQ2 summary (lines 1388–1392) adds that removing two releases improved all other metrics.
- **Resolution:** write "significant but small, particularly in AUC" and "removing two releases improved recall but reduced precision".
- The explanation "harmful examples are not confined to the most recent window" also sits uneasily with C2 ("concentrated in recent commits"). Clarify that the harmful commits lie *just beyond* the cut-off.

**8. [MINOR] Missing context, optional.**
- Marrs et al. 2010 and Krempl et al. 2014 coined and framed "verification latency" in stream mining. One sentence in Section 2.1 would suffice.
- CodeFlowLM (Monteiro, Cabral & Oliveira, arXiv 2512.00231) claims to handle verification latency through continual fine-tuning. It could be mentioned as recent online JIT-SDP work.

**9. [MINOR] The journal-fit argument (Section 2.5) is adequate and could be sharper.**
- It now argues a benchmark/bound role. The repo's own survey (`literature/jksu_benchmark.md`) shows JKSU-CIS publishes drift/stream and label-noise method papers (e.g., DMAE 10.1007/s44443-026-01127-1; FedRnd).
- Citing one or two of these would show that the readership exists beyond MSTDP.
- The observation that MSTDP-style offline final-label evaluation corresponds to the oracle condition is the most journal-relevant point. It is already made; keep it prominent.

**10. [MINOR] Honesty and coherence: good.**
- The refuted hypotheses, the test-set reuse, the AI provenance and the plan deviations are disclosed unusually fully.
- The story (method failed → diagnosis → decomposition → localisation → corrections do not transfer) is coherent.
- The only remaining tension is Concern 1, where the headline ratio is design-selected.

### Status of round-2 R2 concerns

| # | Concern | Status |
|:--|:--|:--|
| 1 | ODaSC-opt/flt ignored; response untrue | Resolved in 2.2, Table 2 and the triage. The effect-size discussion uses the wrong contrast (Concern 2) |
| 2 | Song 2023a reversed | Resolved (text matches abstract: 13 projects, no significant impact); training-vs-evaluation paragraph added |
| 3 | Falessi mischaracterised | Resolved; small residual wording (Concern 7) |
| 4 | C1 overstated at W = 90 | Resolved: abstract gives the path share (0.44/0.78) and the Shapley share; interaction is the headline |
| 5 | C2 localisation artefact | Mostly resolved: flip counts, per-label normalisation, W = 90 strata, ApacheJIT qualifiers. Headline ratio holds only for leave-out (Concern 1) |
| 6 | ODaSC mechanism difference | Resolved in 3.2 and 7; Table 2 C4 not updated (Concern 3) |
| 7 | Tan 2015 credit | Resolved (Section 1, Table 1) |
| 8 | Liu 2025; Song & Minku finding | Resolved; Liu summary incomplete (Concern 5) |
| 9 | Journal fit | Resolved adequately (Concern 9 optional) |
| 10 | Honesty/contributions | Resolved (four contributions; response corrected) |

### Attributions checked

| # | Attribution in manuscript | Source checked | Accurate? |
|:--|:--|:--|:--|
| 1 | ODaSC: micro-cluster confidence modulates the oversampling rate of OOB with Hoeffding trees | Song 2022 full text | Yes |
| 2 | ODaSC-opt (α = 1/0) and ODaSC-flt (filter); 14 projects, first 10k commits, W = 15; p = 0.7278 / 0.6932 vs ODaSC | Song 2022, lines 735–763, 915–982 | Yes |
| 3 | ODaSC beat OOB trained on observed labels | Song 2022 (p = 0.0131) | Yes |
| 4 | Section 6.2: Song found no gain from true labels, versus L1 +0.102 | Song 2022 Table II | Misleading: opt/flt beat OOB by +0.034–0.039 (Concern 2) |
| 5 | Song 2023a: 13 GitHub projects; waiting time had no significant impact on validity | EMSE abstract | Yes |
| 6 | Song & Minku 2023: waiting-time noise affects validity of continuous evaluation | Song 2023a abstract | Yes |
| 7 | Liu 2025: human feedback improves O-JIT-SDP via better label quality | SCICO PDF abstract | Yes, but omits the observed-label evaluation recommendation and the practical-scenario degradation of HumLa |
| 8 | Falessi 2022: remove non-defective classes of last release(s); gain small in AUC; more than one release reduces precision | TOSEM full text, RQ2 (lines 1005–1016, 1370–1392) | Yes; "small gains" in 6.2 understates "significant" |
| 9 | Cabral 2019: waiting rule with positives entering early; ORB | ICSE full text (lines 228–231, 275, 376–377) | Yes |
| 10 | Tan 2015 introduced a labelling gap | Cabral 2019's account of Tan (positives also wait) | Yes |
| 11 | Cabral & Minku 2023: drift plus latency impairs stability | TSE full text | Yes |
| 12 | Cabral et al. 2023: online JIT-SDP with prequential evaluation | EMSE abstract | Yes, but under-uses the BORB offline-learner finding (Concern 6) |
| 13 | Tian 2026 combine waiting time with test feedback | TOSEM abstract | Yes |
| 14 | Grzenda 2020: delayed labels as an evaluation problem | DMKD abstract | Yes |
| 15 | Guo 2024: SZZ labelling noise in JIT-SDP | TOSEM abstract | Yes |
| 16 | Falessi 2020: ignoring time order inflates estimates | EMSE abstract | Yes, broadly |
| 17 | MSTDP is the only JIT-SDP paper in JKSU-CIS since 2023; offline 80/20 split with final labels | `literature/jksu_benchmark.md` (OpenAlex searches) | Consistent |

No files were modified. The Liu 2025 PDF I downloaded and its extracted text are at `/tmp/claude-0/-home-user-p-c1-15/d2d09730-2a6d-533c-ae80-9e44077990c7/scratchpad/liu/liu.txt`.

Main evidence: `/home/user/p_c1_15/project/literature/pdfs/Song_IJCNN2022.txt`, `/home/user/p_c1_15/project/literature/pdfs/Falessi_TOSEM2021.txt`, `/home/user/p_c1_15/project/literature/pdfs/CabralICSE2019.txt`, `/home/user/p_c1_15/project/paper/crossref_cache.json`, `/home/user/p_c1_15/project/literature/prior_art_hits.json`, `/home/user/p_c1_15/project/review/round_2_R2.md`, `/home/user/p_c1_15/project/review/round_2.md`.

Sources (web):
- [Liu et al. 2025, SCICO (PDF)](https://liu906.github.io/papers/1-s2.0-S0167642325000358-main.pdf)
- [CodeFlowLM, arXiv 2512.00231](https://arxiv.org/abs/2512.00231)
- [Rethinking data labeling for JIT vulnerability prediction, arXiv 2611.05013](https://arxiv.org/abs/2611.05013) (checked; not relevant)
- [Liu et al. 2025 on ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0167642325000358)
- [Tian et al. 2026, TOSEM](https://dl.acm.org/doi/10.1145/3779653)
