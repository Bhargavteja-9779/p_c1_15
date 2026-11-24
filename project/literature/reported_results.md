# Reported results of the JKSU-CIS papers in the literature matrix
Companion to journal_papers_matrix.csv. Every number was copied from article HTML or Springer table pages (https://link.springer.com/article/<DOI>/tables/<n>) fetched 2026-11-24 (by a literature subagent; raw HTML in literature/fulltext/, DOI with / replaced by _; table pages end in _table<n>.html). A table is cited by the caption printed on its page; for 10.1007/s44443-026-01401-2 the /tables/<n> index is one higher than the caption number. Anything not in fetched text is UNVERIFIED. Full text opened for 12 of 13 papers; ProRE (Elsevier) abstract-only (ScienceDirect 403).

## 1. MSTDP, JIT-SDP (10.1007/s44443-025-00401-y) — closest JKSU-CIS paper
- Data (Table 1), 9 projects, SZZ labels: brackets 21,347 commits / 37.86% defective; camel 36,753 / 33.98%; fabric 15,591 / 33.21%; jgroups 21,468 / 29.37%; neutron 24,057 / 38.3%; nova 61,364 / 40.51%; npm 9,258 / 29.95%; spring-integration 10,999 / 42.19%; tomcat 24,043 / 43.14%.
- Protocol: chronological 80/20 split (Sect. 4.1.4).
- Table 2, average over 9 projects, MSTDP vs best baseline JITBoost: Accuracy 0.7689 vs 0.7633; Precision 0.6102 vs 0.6049; Recall 0.6782 vs 0.6718; F1 0.6093 vs 0.6047; AUC 0.8188 vs 0.8136.
- Table 2 per-project: brackets F1 0.7139 vs JITBoost 0.7073; neutron AUC 0.8992 vs 0.8910; nova AUC 0.8960 (< JITBoost 0.9085); spring-integration F1 0.8167; npm F1 0.4168 (< TLEL 0.4298).
- Statistics (Sect. 4.2.3): Wilcoxon p = 0.0312 vs JITBoost, 0.0156 vs FENSE, 0.0078 vs JIT-CF. Seeds not stated.
- Drift (Sect. 4.4): sudden drift camel F1 0.6658 -> 0.5244, npm F1 0.3697 -> 0.5091; gradual drift spring-integration F1 0.4881 -> 0.5672 -> 0.7249.
- No waiting time, no verification-latency simulation, no re-weighting of provisional clean labels. Cites Liu et al. 2024a (PU learning for JIT-SDP, Empir Softw Eng 29(5):98) without using it.

## 2. DMAE (10.1007/s44443-026-01127-1)
Prequential in MOA, 20% labelling budget. Table 7 meta-rank: DMAE 1.06; CALMID 3.71; AdaOB 4.13; OALM-MI 4.13; ROSE 4.42; SRP 5.49; CSARF 9.89. Table 5 G-Mean (%): penbased 92.20 vs 90.67 (AdaOB); banana 88.90 vs 85.86; letter 70.94 vs 61.73 (ROSE); ring 97.84 vs 97.54; diabetes 44.08 vs 45.3 (ROSE better). Iman-Davenport (Table 11) + Nemenyi CD 2.655.

## 3. ADAWU-IDS (10.1007/s44443-026-00964-4)
Table 3, CICIDS2017, 3 runs: ADAWU-IDS-Cal W-F1 0.9022±0.0106, Attack F1 0.7831±0.0203; Static LSTM W-F1 0.8865±0.0040; Leveraging Bagging W-F1 0.9859±0.0004, Attack F1 0.9663±0.0009; DWM 0.9854; Online Bagging 0.9855. Table 4 vs Static LSTM: W-F1 t-test p = 0.0562, Wilcoxon p = 0.2500 (not significant).

## 4. Gamma–Weibull CUSUM, IoT malware (10.1007/s44443-026-01091-w)
Table 4: LSTM accuracy 0.987 -> 0.991, macro F1 0.977 -> 0.981; CNN macro F1 0.457 -> 0.576. Table 7 (20 reps) detection delay: GW-CUSUM abrupt 43.0±24.0 (FA 1.2); Page-Hinkley 125.2±106.0 (FA 0.0); ADWIN 1.1±1.2 (FA 1270.2); DDM 425.9±401.2 (FA 625.5).

## 5. FedRnd (10.1007/s44443-026-00488-x)
Table 2 accuracy (%), non-IID: CIFAR-10 eps=0.2/0.4/0.6 FedRnd 72.94/70.14/68.21 vs FedLSR 71.33/61.62/57.91; CIFAR-100 eps=0.6 21.02±0.23 vs 18.04±0.21. 3 runs; no significance test.

## 6. PCa-Stack (10.1007/s44443-026-01082-x)
Table 3: AUC 0.892 (0.876–0.908), AUPRC 0.752, Brier 0.107; XGBoost AUC 0.864. External AUC 0.871 and 0.858.

## 7. MARS++ (10.1007/s44443-026-01279-0)
Table 10 mean PR-AUC: MARS++ 0.877; SMOTE 0.870; ADASYN 0.864; RUS 0.834; NearMiss 0.615. Holm-adjusted p all > 0.05.

## 8. VRIF-VPSVM (10.1007/s44443-026-01401-2)
Table 3 clean: G-Mean 88.22%, AUPRC 82.41%; Table 4 noisy: G-Mean 88.45%.

## 9. FIFT (10.1007/s44443-026-01130-6) — 20.8%–190.4% more IDIs than strongest baseline.
## 10. DSDP (10.1007/s44443-025-00239-4) — Table 2 MNIST 97.57 vs FedAvg 95.56; no seeds/tests.
## 11. OLA-Incomplete (10.1007/s44443-025-00381-z) — Table 4 PostSent 95.99; seeds {1,2,3}.
## 12. Neutrosophic Transformer (10.1007/s44443-026-00664-z) — KNKNN F1 92.37%; 10 reps, paired t-tests.
## 13. ProRE (10.1016/j.jksuci.2022.12.017) — abstract only; table numbers UNVERIFIED.

## Comparability with our study
None of these 13 papers uses the Cabral et al. 14-project artifact under a prequential verification-latency protocol. MSTDP's 9 projects overlap by name but its data differ (e.g. brackets 21,347 / 37.86% vs 17,311 / 23% in Cabral ICSE'19; tomcat 24,043 / 43.14% vs 18,877 / 28%) and it uses a one-shot 80/20 split → **NOT directly comparable**. All others: NOT directly comparable.

## Novelty check within JKSU-CIS
No paper here re-weights provisionally-clean examples by the probability of being undiscovered defects or uses a right-truncation-aware delay estimator. Outside JKSU-CIS the closest prior work is ODaSC (Song et al., IJCNN 2022) and possibly Liu et al. 2024a (PU learning for JIT-SDP, not yet opened) — see state/novelty_ledger.json.
