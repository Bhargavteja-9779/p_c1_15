# JKSU-CIS benchmark: paper anatomy, metrics and the MSTDP comparison

Target journal: Journal of King Saud University – Computer and Information Sciences (JKSU-CIS), Springer Nature, ISSN 1319-1578 (OpenAlex source S2764955546, ISSNs 1319-1578 / 2213-1248).
Compiled 2026-11-24. **Rule: every number here comes from a file I read in `literature/fulltext/`, from `literature/journal_papers_matrix.csv` (an earlier subagent built it from the same HTML), from the OpenAlex API, or from our own `data/jit/*.arff`. Anything I could not check is marked UNVERIFIED.**

Sources and method
- Full text: 23 Springer HTML pages in `literature/fulltext/` (12 already on disk, plus 11 fetched in this pass with `curl -sL https://link.springer.com/article/<doi>`; a browser User-Agent got a "Client Challenge" page, so I fetched without one). Plus ProRE (Elsevier era, abstract only; ScienceDirect/linkinghub returned a 2.7 KB redirect stub, so not opened).
- How the counts were made (my own parsing with BeautifulSoup):
  - **#figs / #tables**: the number of distinct "Fig. N" / "Table N" captions inside `<figure>` in the article body.
  - **#refs**: the count of `li.c-article-references__item`.
  - **Sections**: taken from `<h2>`/`<h3>`.
  - **Statistical tests and metrics**: found by regex over the body text, then checked by hand. Hits that only appeared in reference titles were removed: "Holm" in RISE and "ANOVA" in KAN-AdamW were false positives.
- OpenAlex searches (filter `primary_location.source.issn:1319-1578[|2213-1248]`, `from_publication_date:2023-01-01`), all run in this pass:
  - `title_and_abstract.search` with each of: software defect prediction, defect prediction, just-in-time, concept drift, label noise, data stream, software fault, bug prediction, verification latency, online learning, code review, software engineering.
  - `title.search` with each of: defect, fault, bug, vulnerability, software, drift, noisy labels, imbalanced, incremental learning, commit, software testing, streaming, data streams, concept-drifting, label, online, cross-project, code smell.
  - **Result: MSTDP is the only software-defect-prediction paper in JKSU-CIS since 2023 that OpenAlex returns.**
    - title.search "defect" gave 16 hits; all except MSTDP are industrial or visual defect detection.
    - "cross-project", "code smell", "fault prediction" and "bug" gave 0 title hits.
  - I therefore added the closest papers by kind: software-engineering ML papers, online/open-world stream learning, and imbalance learning.

---

## (a) All papers covered

Type: M = method paper, E = mainly empirical, S = survey. Code: "public" means a repository link appears in the article; otherwise the article's own wording is given. Stats = formal statistical tests found in the text (Wilcoxon = Wilcoxon signed-rank).

| # | Title (short) | DOI | Year (OpenAlex) | Type | #datasets | #baselines | Metrics | Stats tests | #figs | #tables | #refs | Code |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **MSTDP**: multi-scale temporal DL for JIT-SDP | 10.1007/s44443-025-00401-y | 2026 | M | 9 projects | 7 | Acc, P, R, F1, AUC | Wilcoxon (3 pairwise) | 8 | 5 | 47 | public (anonymous.4open.science) |
| 2 | DMAE: dual-memory active ensemble, imbalanced drifting streams | 10.1007/s44443-026-01127-1 | 2026 | M | 20 (15 synthetic + 5 real) | 10 | G-mean, Kappa, recall, meta-rank | Friedman/Iman-Davenport + Nemenyi | 12 | 11 | 41 | on request |
| 3 | ADAWU-IDS: drift-aware intrusion detection | 10.1007/s44443-026-00964-4 | 2026 | M | 2 | 4 (+ablations) | weighted F1, attack F1, recall | paired t-test + Wilcoxon (Table 4); 95% CI | 1 | 8 | 42 | public (anonymous.4open.science) |
| 4 | Gamma–Weibull CUSUM drift detection, IoT malware | 10.1007/s44443-026-01091-w | 2026 | M | 2 (simulated + IoT-23) | 4 detectors + static LSTM/CNN | Acc, macro-F1, detection delay, false alarms | one-sided Wilcoxon | 24 | 20 | 36 | not stated |
| 5 | FedRnd: federated learning with label noise | 10.1007/s44443-026-00488-x | 2026 | M | 3 | 6 | Accuracy | none found (3 runs, mean ± std) | 5 | 6 | 39 | public (GitHub) |
| 6 | PCa-Stack: heterogeneous stacking + adaptive Borderline-SMOTE | 10.1007/s44443-026-01082-x | 2026 | M/E | 3 cohorts | 6 clinical scores + ML ensemble baselines | AUC, AUPRC, Brier, F1 | DeLong + Holm-Bonferroni, BCa bootstrap CI, Friedman | 8 | 5 | 43 | on request |
| 7 | MARS++: stability-aware meta framework for imbalance | 10.1007/s44443-026-01279-0 | 2026 | M | 12 (8 tabular + 4 image) | 14 | PR-AUC, ROC-AUC, F1 | Friedman + Nemenyi, Wilcoxon + Holm (all adjusted p > 0.05) | 8 | 13 | 41 | not stated |
| 8 | VRIF-VPSVM: fuzzy variance-penalised SVM | 10.1007/s44443-026-01401-2 | 2026 | M | 22 benchmark + artificial | 10 | G-mean, AUPRC, IBA | Friedman + Nemenyi | 13 | 10 | 41 | not stated |
| 9 | FIFT: fairness testing of ML software | 10.1007/s44443-026-01130-6 | 2026 | M | 5 | 5 | #IDIs, throughput | Wilcoxon | 9 | 14 | 63 | public (GitHub) |
| 10 | DSDP: data drift + differential privacy in FL | 10.1007/s44443-025-00239-4 | 2025 | M | 4 | 5 | Accuracy | none found | 9 | 4 | 47 | "on request" |
| 11 | Online label aggregation with incomplete crowd responses | 10.1007/s44443-025-00381-z | 2026 | M | 3 | 5 | Accuracy (final and instantaneous) | none found (3 seeds) | 4 | 9 | 48 | public (anonymous.4open.science) |
| 12 | Neutrosophic Transformer for imbalanced data | 10.1007/s44443-026-00664-z | 2026 | M | 3 | 10 | Acc, P, R, F1 | paired t-tests (10 repetitions) | 4 | 24 | 53 | public (GitHub) |
| 13 | ProRE: ACO programmer recommendation for bugs | 10.1016/j.jksuci.2022.12.017 | 2022/23 | M | 5 (abstract) | 3 (abstract) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| 14 | **ISOMFL**: multi-fault localisation by iterative self-organising clustering *(new)* | 10.1007/s44443-026-00845-w | 2026 | M | 6 programs | 5 | ANSE, T-EXAM, Top-N | Wilcoxon + Friedman + Cliff's delta (Table 12); 30 runs (Table 17) | 6 | 20 | 46 | public (GitHub) |
| 15 | **MDFVD**: vulnerability detection with multi-dimensional code features *(new)* | 10.1007/s44443-026-00569-x | 2026 | M | 4 | 5 | Acc, P, R, F1; plus TPR, FPR, AUC, G-mean, MCC (Table 5) | none found (results averaged over 5 runs) | 15 | 9 | 57 | data "from the corresponding author" |
| 16 | **RISE**: adversarial evasion of vulnerability detectors *(new)* | 10.1007/s44443-026-01312-2 | 2026 | M | 2 (× 3 victim models) | 3 | attack success rate (ASR), avg. queries, cosine similarity | none found | 6 | 5 | 58 | public (GitHub) |
| 17 | **OHCE**: online hash-centre evolution, encrypted traffic *(new)* | 10.1007/s44443-026-00949-3 | 2026 | M | 2 | 6 | Acc, F1 (known classes), PR-AUC (unknown-flow detection), overhead | none found (mean ± sd over 5 partitions) | 7 | 5 | 42 | not stated |
| 18 | **Class overlap in imbalanced learning** (review) *(new)* | 10.1007/s44443-026-00547-3 | 2026 | S | – | – | reviews metrics (Tables 5–6) | – | 11 | 12 | 194 | n/a |
| 19 | **TSP-SMOTE** oversampling *(new)* | 10.1007/s44443-026-00494-z | 2026 | M | 26 (KEEL) | 11 | F1, G-mean, AUC | Friedman (Table 14) + Wilcoxon (Table 15) | 15 | 15 | 56 | "on reasonable request" |
| 20 | **CodeDiffuSe**: masked diffusion for code completion/repair *(new)* | 10.1007/s44443-025-00237-6 | 2025 | M | 4 | 5 | EM, BLEU, CodeBLEU, AST acc., compilation rate | none found (3 seeds) | 10 | 9 | 38 | "Not applicable" |
| 21 | **RL-LLMfuzzer**: RL-guided LLM compiler fuzzing *(new)* | 10.1007/s44443-026-01115-5 | 2026 | M | 2 compilers | 4 | coverage, validity, diversity, confirmed bugs | Mann-Whitney U + Vargha-Delaney A12 (10 × 24 h) | 5 | 7 | 63 | no link found |
| 22 | **KAN-AdamW** agile cost estimation *(new)* | 10.1007/s44443-025-00058-7 | 2025 | M | 1 (75 projects + 1,000 SMOTE-NC synthetic) | ANN, function-point models | MAE, MRE, accuracy, R² | none found | 16 | 4 | 45 | "provided on request" |
| 23 | **Dual-encoder detector** for AI-generated Go code *(new)* | 10.1007/s44443-026-00626-5 | 2026 | M | 4 | 3 | F1 + 4 other indicators | paired t-tests (Tables 12–15) | 7 | 25 | 39 | no code link (GitHub links are data sources) |
| 24 | **Topo-MFP**: microservice fault detection and root-cause analysis *(new)* | 10.1007/s44443-026-01193-5 | 2026 | M | 2 | 3 fault-detection baselines (incl. UAC-AD) + RCA baselines (Random, Local-Score, Topology-RWR, Table 11) | F1, Hit@k | Wilcoxon (Table 13); 5 seeds | 4 | 26 | 36 | no link found |

Headline numbers for the 11 new papers (each with its source):
- **ISOMFL**:
  - grep, average case, 4-fault: ANSE 838.96 vs MSeer 1020.04, FSMFL 911.15, FLITSR 945.69 (Table 5, quoted in text).
  - Friedman χ² = 52.25, p = 2.65×10⁻¹¹.
  - ISOMFL vs FSMFL is *not* significant (Sect. 4, Table 12).
- **MDFVD**:
  - F1 gains over the best baseline of 15.15 / 21.25 / 9.37 / 14.67 %, and accuracy gains of 7.63 / 8.20 / 8.60 / 9.70 % (Table 4).
  - On Reveal, recall falls 0.6178 → 0.5985.
- **RISE**:
  - mean ASR 88.60 / 66.03 / 59.46 % on CodeBERT / UniXcoder / CodeLlama (Table 3).
  - Against the strongest baseline SLODA on DiverseVul/CodeLlama: 28.99 → 56.35 %.
- **OHCE**: PR-AUC +0.74 % and +0.95 % over FOSS on the two datasets (Table 2, mean over 5 class partitions).
- **TSP-SMOTE**:
  - ranked 1st on average; highest value in 118 of 234 metrics (abstract).
  - ranked first 39, 40 and 39 times out of 78 (Sect. 4).
- **CodeDiffuSe**: CodeXGLUE-Python 54.2 % EM and 67.8 BLEU, +7.9 EM over CodeGen (Table 3).
- **RL-LLMfuzzer**:
  - +32.1 % backend line coverage vs Fuzz4All, p < 0.001 (abstract).
  - 28 officially confirmed bugs in GCC/LLVM.
- **KAN-AdamW**: MAE 11,504.08, MRE 0.12 (abstract).
- **Dual-encoder**: about 7.6 % average F1 gain over the strongest baseline per dataset (abstract).
- **Topo-MFP** (abstract; Tables 14–15, 18–19):
  - F1 0.949 / 0.951 on AIOps2022 / TT.
  - Hit@1 0.872 / 0.901.

Headline numbers for papers 1–13 are in `literature/reported_results.md` and the matrix CSV. MSTDP is covered in full in (d) below.

Seen in OpenAlex but **not opened**: Elsevier-era JKSU-CIS software-engineering papers, all behind ScienceDirect, which I could not reach. All titles below are as returned by OpenAlex:
- 10.1016/j.jksuci.2023.101676 (multi-fault localisation, Chameleon)
- 10.1016/j.jksuci.2023.02.023 (multi-fault localisation, PSO)
- 10.1016/j.jksuci.2023.101668 (multi-fault localisation, ACO)
- 10.1016/j.jksuci.2024.102189 (software effort estimation, ensemble rule)
- 10.1016/j.jksuci.2024.102118 (empirical study, requirement-to-code traceability)
- 10.1016/j.jksuci.2024.101958 (MTLink, issue–commit traceability)
- 10.1016/j.jksuci.2024.102132 (systematic review, software reliability prediction)
- 10.1016/j.jksuci.2024.101978 (SDE software reliability models)

Their contents are UNVERIFIED.

---

## (b) Typical JKSU-CIS paper anatomy

All values are over the 23 full-text papers (rows 1–12 and 14–24).

| Quantity | Median | Min–max |
|---|---|---|
| Figures | **8** | 1–24 |
| Tables | **9** | 4–26 |
| References | **45** | 36–194 (the survey has 194; the method papers stay within 36–63) |
| Body words (incl. equations and captions, rough) | **~12,800** | 8,400–24,200 |
| Numbered top-level sections | **6** | 4–11 |

MSTDP, the only JIT-SDP paper, is long: 21,900 words, 8 figures, 5 tables, 47 references.

Common section order. Recurring pattern, by `<h2>` headings:
1. Abstract.
2. **1 Introduction.** 16/23 papers state an explicit contributions list ("main/key contributions").
3. **2 Related work.** Sometimes preceded by "Preliminaries/Background".
4. **3 Methodology / Proposed method.** Often with algorithm boxes and a complexity note.
5. **4 Experimental setup.** Datasets table, baselines list, metric definitions, hardware/software and hyperparameter table.
6. **5 Results.** These include:
   - main comparison table (mean ± sd where repeated);
   - **ablation** (18/23);
   - **sensitivity/parameter analysis** as its own heading (8/23);
   - statistical tests;
   - cost/runtime table.
   Research questions written as RQ1… appear in 6/23 (MSTDP, MDFVD, RL-LLMfuzzer, FIFT, RISE, CodeDiffuSe).
7. **Discussion** as its own top-level section (9/23).
8. **Threats to validity** (7/23: MSTDP, MDFVD, ISOMFL, RL-LLMfuzzer, FIFT, Topo-MFP, RISE). Every software-engineering paper with an SE venue style has one.
9. **Limitations** heading (9/23).
10. **Conclusion** (with future work).
11. Back matter required by Springer:
    - **Data availability** (23/23);
    - **Code availability** as a separate heading (2/23);
    - Ethics declarations / competing interests;
    - Author contributions / Funding.

How common rigour elements are:
- A **public code link** is in 8/23: MSTDP, ADAWU-IDS, Online label aggregation, FedRnd, Neutrosophic, FIFT, ISOMFL, RISE.
- Formal statistical tests are in 14/23. Wilcoxon signed-rank is the most common (8), then Friedman (+Nemenyi or Iman-Davenport) (6) and paired t-tests (3).
- Effect sizes appear in only 2/23 (Cliff's delta in ISOMFL; Vargha-Delaney A12 in RL-LLMfuzzer).
- **Scott-Knott ESD: 0/23.**
- Repeated runs or seeds are typically 3–10 (FedRnd 3, Online label aggregation 3, ADAWU-IDS 3, Topo-MFP 5, MDFVD 5, GW-CUSUM 10, RL-LLMfuzzer 10 × 24 h, ISOMFL 30 for stability).
- MSTDP reports no seeds or repetitions.

Editorial signal:
- The published MSTDP text still contains a reviewer-response fragment, "(Reviewer 2, Point 3)", in Sect. 4.6.
- Its code link reads "…MSTDP-D77E4ArtificialIntelligencePeerRiview".
- The text says "NVIDIA H80 GPU".
- This suggests light copy-editing. The bar for experimental rigour in JKSU-CIS is set by the authors, not enforced by the journal.

---

## (c) Metrics reported (focus: JIT-SDP and imbalanced/streaming classification)

| Metric | Papers reporting it (of the 23 full texts) |
|---|---|
| Accuracy, Precision, Recall, F1 | almost all classification papers. **MSTDP: Acc, P, R, F1, AUC only** (Table 2) |
| ROC-AUC | MSTDP, PCa-Stack, MARS++, TSP-SMOTE, MDFVD (supplementary), OHCE |
| G-mean | DMAE (main metric for real streams, Table 5), VRIF-VPSVM, TSP-SMOTE, MDFVD (Table 5); also mentioned in PCa-Stack |
| MCC | **only MDFVD** (supplementary Table 5) |
| PR-AUC / AUPRC | MARS++, VRIF-VPSVM, PCa-Stack, OHCE |
| Kappa | DMAE (stream metric) |
| Brier / calibration | PCa-Stack only |
| Effort-aware (Popt, IFA, Recall@20%Effort, Effort@20%) | **0/23.** MSTDP lists effort-aware metrics only as a limitation ("Future research can incorporate … effort-aware or defect severity", Sect. 5.3) |
| Stream-specific (prequential curves, detection delay, false alarms) | DMAE (prequential G-mean/Kappa curves), GW-CUSUM (detection delay ± sd, false alarms, Table 7), ADAWU-IDS (chunk-wise predict-then-update with delayed labels) |
| Compute cost table | MSTDP Table 5 (training 5.1 h, inference 28.5 ms per commit, from text), OHCE Table 5, ISOMFL Table 19, TSP-SMOTE Table 13 |

What this means for us:
- To match MSTDP, report Acc, P, R, F1 and AUC.
- To exceed it, add the following:
  - G-mean and MCC (both used in this journal);
  - recall of each class (with |R0 − R1| if that is our main metric);
  - PR-AUC;
  - **effort-aware metrics** (Popt, Recall@20%Effort, IFA), which MSTDP explicitly admits it lacks.
- Reporting prequential curves over time follows DMAE's practice in this journal.
- The standard online JIT-SDP metrics of Cabral et al. (G-mean, recalls of each class) are not stated here from a source read in this pass: UNVERIFIED in this document; check against `literature/pdfs/` before citing.

---

## (d) MSTDP (10.1007/s44443-025-00401-y): protocol, per-project numbers, comparability

### Protocol (from the full text)
- **Task:** offline (batch) binary commit classification. Labels are "obtained through the SZZ algorithm" (Sect. 3.1) and treated as ground truth. The threat section concedes SZZ false positives and negatives (Sect. 5.1).
- **Split:**
  - "strictly split datasets in chronological order … training set accounts for 80% of total data, and the test set accounts for 20%" (Sect. 4.1.4; also Sect. 3.4.3);
  - early stopping on a validation set (patience 10);
  - **one split per project, no repetitions or seeds reported.**
- **Verification latency:**
  - **none.** The text never mentions waiting time, verification latency or label delay;
  - all training labels are the final dataset labels, including those of commits made just before the split point;
  - in a real deployment those commits would still look clean;
  - it cites Cabral et al. 2021 (ICSME, concept drift) but not the ICSE'19 verification-latency work, and cites PU learning for JIT-SDP (Liu et al. 2024a) without using it.
- **Online aspects:**
  - (i) "Natural drift" (Sect. 4.4.1): a sliding window of 15 days with a 7-day step, training on all history before each window. Only the standard deviations of metrics across windows are reported, in Fig. 5 (e.g. npm recall sd 0.2188; AUC sd for neutron/nova "around 0.02").
  - (ii) Synthetic sudden drift (Sect. 4.4.2): a +30 % random offset on selected features at the 50 % point.
  - (iii) Synthetic gradual drift (Sect. 4.4.3): a linear 0→30 % offset over the 30–70 % interval.
  - None of these are prequential, and none model label delay.
- **Model and setup** (Sects. 3.4.2, 4.1.4):
  - Adam, lr 0.001, batch 32, dropout 0.2, L2 1e-4, hidden 64;
  - windows of 24 h / 7 d / 4 weeks;
  - PyTorch 1.9.0;
  - "NVIDIA H80 GPU (96GB)" (sic), Xeon Gold 6248R, 128 GB RAM.
- **Statistics** (Sect. 4.2.3): Wilcoxon signed-rank over the 9 projects, p = 0.0312 vs JITBoost, 0.0156 vs FENSE and 0.0078 vs JIT-CF. **The metric tested is not stated.**
- **Baselines:** JITBoost, FENSE, JIT-CF, TLEL, MULTI, DWA_JIT, EALGB. The text says nothing on whether these were re-implemented, re-run or copied from earlier papers. They "are" "7 representative state-of-the-art methods" (Sect. 4.1.2).
- **Validation set:** used for early stopping; how it is carved out of the 80 % is not stated in the extracted text.
- **Decision threshold:** "made through thresholding" (Sect. 3.3.5). The value is not stated in the extracted text (UNVERIFIED).

### MSTDP Table 1 vs our `data/jit/*.arff` (Cabral et al. artifact, Zenodo 2591761, per README)
I counted complete data rows in our ARFF files:
- `contains_bug` = True is the defective count;
- `author_date_unix_timestamp` gives the date range;
- each ARFF except camel and tomcat ends with one truncated line, which I excluded.

| Project | MSTDP Table 1: commits / defective / rate / start–end | Our ARFF: commits / defective / rate / start–end (UTC) |
|---|---|---|
| brackets | 21,347 / 8,082 / 37.86 % / 2011-12-08 – 2017-08-30 | 21,347 / 8,082 / 37.86 % / 2011-12-07 – 2017-08-30 |
| camel | 36,753 / 12,488 / 33.98 % / 2007-03-19 – 2017-11-30 | 36,753 / 12,488 / 33.98 % / 2007-03-19 – 2017-11-29 |
| fabric | 15,591 / 5,177 / 33.21 % | 15,591 / 5,177 / 33.21 % |
| jgroups | 21,468 / 6,305 / 29.37 % | 21,468 / 6,305 / 29.37 % |
| neutron | 24,057 / 9,214 / 38.30 % | 24,057 / 9,214 / 38.30 % |
| nova | 61,364 / 24,857 / 40.51 % | 61,364 / 24,857 / 40.51 % |
| npm | 9,258 / 2,773 / 29.95 % | 9,258 / 2,773 / 29.95 % |
| spring-integration | 10,999 / **4,648** / 42.19 % | 10,999 / **4,640** / 42.19 % (4,648/10,999 would be 42.26 %, so MSTDP's 4,648 looks like a typo) |
| tomcat | 24,043 / 10,372 / 43.14 % | 24,043 / 10,372 / 43.14 % |

**MSTDP's dataset is the same 9 Cabral ARFF files we use.** Commit counts, defect counts and dates match to the day, apart from time-zone ±1 day and the spring-integration typo. MSTDP does not name Cabral's artifact as its source; it says only "9 large-scale open-source software projects from GitHub".

This **corrects** the note in `journal_papers_matrix.csv` / `reported_results.md` that MSTDP's "commit counts/defect rates differ from Cabral ICSE'19 data". They may differ from the summary numbers printed in the ICSE'19 paper (not re-checked here), but they are identical to the ARFF files in our `data/jit/`.

The MSTDP text says it uses "code semantic features" and five feature dimensions (Sect. 3.1). The ARFF files contain only the 14 Kamei-style metrics plus fix, timestamp and commit_type. **How MSTDP obtained semantic, code or developer-identity inputs from these files is not explained: UNVERIFIED.**

### MSTDP Table 2: per-project test-set results (chronological last 20 %), all 5 metrics, MSTDP vs best baseline

Values are copied from `literature/fulltext/10.1007_s44443-025-00401-y_table2.html`.

| Project | Acc | Prec | Rec | F1 | AUC | Best baseline on F1 (value) | Best baseline on AUC (value) |
|---|---|---|---|---|---|---|---|
| brackets | 0.7930 | 0.6775 | 0.7544 | 0.7139 | 0.8614 | JITBoost 0.7073 | JITBoost 0.8538 |
| camel | 0.6942 | 0.3105 | 0.7481 | 0.4374 | 0.7851 | JITBoost 0.4325 | JITBoost 0.7785 |
| fabric | 0.7416 | 0.8819 | 0.3579 | 0.5091 | 0.8241 | **FENSE 0.5254** | JITBoost 0.8162 |
| jgroups | 0.7336 | 0.4973 | 0.6549 | 0.5653 | 0.7743 | **JIT-CF 0.5816** | **JIT-CF 0.7864** |
| neutron | 0.7922 | 0.5632 | 0.9166 | 0.6977 | 0.8992 | **JITBoost 0.7042** | JITBoost 0.8910 |
| nova | 0.7926 | 0.5444 | 0.8606 | 0.6669 | 0.8960 | JITBoost 0.6610 | **JITBoost 0.9085** |
| npm | 0.8504 | 0.4901 | 0.3626 | 0.4168 | 0.7076 | **TLEL 0.4298** | **TLEL 0.7253** |
| spring-integration | 0.7700 | 0.7794 | 0.8577 | 0.8167 | 0.8363 | JITBoost 0.8090 | JITBoost 0.8285 |
| tomcat | 0.7528 | 0.7472 | 0.5907 | 0.6598 | 0.7848 | **FENSE 0.6775** | **FENSE 0.8012** |
| **Average** | **0.7689** | **0.6102** | **0.6782** | **0.6093** | **0.8188** | JITBoost 0.6047 | JITBoost 0.8136 |

Bold baseline = beats MSTDP.

Full baseline averages (Table 2):

| Baseline | Acc | P | R | F1 | AUC |
|---|---|---|---|---|---|
| JITBoost | 0.7633 | 0.6049 | 0.6718 | 0.6047 | 0.8136 |
| FENSE | 0.7575 | 0.6010 | 0.6708 | 0.6032 | 0.8066 |
| JIT-CF | 0.7342 | 0.5817 | 0.6457 | 0.5809 | 0.7809 |
| TLEL | 0.7145 | 0.5676 | 0.6273 | 0.5651 | 0.7609 |
| MULTI | 0.7021 | 0.5531 | 0.6159 | 0.5531 | 0.7453 |
| DWA_JIT | 0.6830 | 0.5421 | 0.6011 | 0.5414 | 0.7311 |
| EALGB | 0.6721 | 0.5318 | 0.5922 | 0.5353 | 0.7102 |

My own checks on Table 2 (computed in this pass, not claims of the paper):
- MSTDP's Average row equals the mean of its 9 project rows for all 5 metrics. The JITBoost F1 mean computes to 0.6049 vs 0.6047 printed (rounding).
- MSTDP is best in only **24 of 45** project × metric cells. Text Sect. 4.2.1 nonetheless says "MSTDP method achieves optimal performance across all evaluation metrics". The 21 losses are:
  - tomcat, all 5 metrics (FENSE);
  - npm, all 5 metrics (TLEL);
  - jgroups, all 5 metrics (JIT-CF);
  - fabric recall and F1 (FENSE);
  - neutron precision and F1 (JITBoost);
  - nova AUC (JITBoost);
  - camel accuracy (JITBoost).
- I ran an exact two-sided Wilcoxon signed-rank test (scipy) on the 9 per-project values:
  - MSTDP vs JITBoost: F1 p = 0.066, AUC p = 0.121;
  - vs FENSE: F1 p = 0.570, AUC p = 0.055;
  - vs JIT-CF: F1 p = 0.0078, AUC p = 0.0078.
  - **So the paper's p = 0.0312 (JITBoost) and 0.0156 (FENSE) cannot be reproduced from Table 2 for F1 or AUC.** Only the JIT-CF value matches. The paper does not say which metric was tested, so this is a discrepancy, not proof of error.
- The text says brackets F1 rose "from the best baseline's 0.7073 to 0.7139, achieving a significant improvement of 6.6%" (Sect. 4.2.2). Arithmetically that is +0.93 % relative.

Drift experiments (text only, Sect. 4.4.2–4.4.3; the figures were not digitised):
- Sudden drift, F1 before → after:
  - npm 0.3697 → 0.5091;
  - spring-integration 0.4881 → 0.5249;
  - camel 0.6658 → 0.5244;
  - fabric 0.5891 → 0.5247;
  - neutron and nova fell 6.1 % and 4.8 %.
- Gradual drift: spring-integration 0.4881 → 0.5672 → 0.7249; neutron peaks at 0.7823 from 0.6858 mid-drift.
- **These "pre-drift" F1 values do not match the Table 2 F1 of the same projects** (e.g. camel 0.6658 vs 0.4374; spring-integration 0.4881 vs 0.8167). The drift experiments evidently use another, unstated train/test configuration.

Ablation (Sect. 4.3.2, Tables 3–4, values quoted in text):
- removing the temporal module costs F1 −4.31 % and precision −4.82 % on average;
- code-only costs F1 −9.18 %;
- the developer module costs 1.3–1.6 %;
- the lifecycle module costs 0.75–0.89 %.

Cost (Sect. 4.6 / Table 5): training 5.1 h, inference 28.5 ms per commit.

### Comparability with our online prequential evaluation against final labels
- **Not directly comparable.**
  - MSTDP trains once on the first 80 % of commits with *final* SZZ labels: no waiting time, an oracle-label batch setting.
  - It tests once on the last 20 %.
  - It has no per-time-step evaluation, no seeds and no variance.
  - Our setting updates online with labels revealed only after verification latency, and scores every prediction prequentially.
  - MSTDP's training labels for the late part of the training period include defects that were found only later, so its numbers are best read as an **upper reference with no latency**.
- **What *is* comparable:**
  - the data are identical (same ARFF files, same 9 projects);
  - its test labels are also the final labels.
- A fair side-by-side is therefore possible if we report, in addition to our full-stream prequential metrics, **the same 5 metrics (Acc, P, R, F1, AUC) restricted to the chronologically last 20 % of each project**, scored against final labels, with the threshold stated.
- Even then, the caveat must be explicit:
  - different training regimes: online with delayed labels vs batch with oracle labels;
  - MSTDP's undocumented extra features;
  - no seed variance in MSTDP.
- MSTDP's average AUC 0.8188 and F1 0.6093 should be cited as "batch, no-latency, single split" numbers, not as a state of the art our online method must beat.

---

## (e) Gaps: what a paper must contain to look as strong as the strongest of these

The strongest examples, by rigour:
- ISOMFL (Wilcoxon + Friedman + Cliff's delta, 30-run stability, public code, threats section);
- DMAE (prequential protocol, 20 streams, Iman-Davenport + Nemenyi CD diagram, ablations);
- Topo-MFP (5 seeds, split/leakage protocol table, significance table, threats and reproducibility sections);
- PCa-Stack (bootstrap CIs, DeLong + Holm, external validation);
- RL-LLMfuzzer (10 repetitions, Mann-Whitney + A12).

1. **Statistics:**
   - report mean ± sd over ≥ 5 seeds (Topo-MFP uses 5; ISOMFL uses 30);
   - add a Friedman / Iman-Davenport test with a Nemenyi critical-difference diagram (DMAE, MARS++, VRIF);
   - add pairwise Wilcoxon with Holm correction, plus an effect size (Cliff's delta or A12; only 2/23 do this, so it is a differentiator);
   - adding Scott-Knott ESD would be a first in this journal (0/23).
   - MSTDP has none of these beyond 3 unadjusted Wilcoxon p-values.
2. **Metrics:**
   - add AUC, G-mean, MCC, recall of each class (or |R0 − R1|) and PR-AUC;
   - **add effort-aware metrics (Popt, Recall@20%Effort, IFA)**. No JKSU-CIS paper reports them, and MSTDP names their absence as a limitation;
   - add prequential curves over time (DMAE style).
3. **Baselines:**
   - MSTDP uses 7; the median here is about 5;
   - include latency-unaware online JIT-SDP (no waiting time), waiting-time ORB/OOB-style baselines and an oracle (no latency) upper bound;
   - also include ODaSC-type label-confidence methods (see the ledger), a PU-learning baseline, and say whether each baseline was re-run.
4. **Datasets:** use all 14 Cabral projects (MSTDP uses 9; DMAE uses 20 streams). Explicitly report the MSTDP-comparable last-20 % view on its 9 projects (see (d)).
5. **Protocol transparency:**
   - give a protocol/leakage table like Topo-MFP Table 9: label-availability rule, waiting time W, time-step granularity, threshold, warm-up;
   - MSTDP leaves its threshold, validation split and metric tested unstated.
6. **Ablation and sensitivity:** 18/23 papers have ablations and 8/23 have a sensitivity section. Run W sweeps and component ablations.
7. **Cost table:** training and update time per commit (as in MSTDP Table 5, OHCE Table 5, ISOMFL Table 19).
8. **Threats to validity** section (all SE-style papers here have one), split into internal, external, construct and conclusion validity as MSTDP does.
9. **Public code and data link** in a "Code availability" statement. Only 8/23 give one; an anonymous link is accepted (MSTDP, ADAWU-IDS). Also a Data availability statement (23/23).
10. **Size and format:**
    - aim for about 6 numbered sections, 8–10 figures, 8–12 tables, about 45–60 references and 11–15 k words;
    - state RQs explicitly (6/23, including MSTDP-style SE papers);
    - give an explicit contributions list (16/23).
