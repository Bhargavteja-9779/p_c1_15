# Round 1 — Reviewer 2 (novelty & related work) — score 5/10, MAJOR REVISION
No pre-empting work found for the commit-level online decomposition. Concerns:
1 MAJOR C1 overstated vs Falessi 2021/22 & Fan 2021 (same noisy-vs-clean design); novelty = online/waiting setting + "recency cut-off fails because noise is old"
2 MAJOR decomposition order-dependent; share>1 => interaction; report both orders / Shapley + CIs; explain L1>oracle
3 MAJOR RQ2 only in G-mean@0.5; redo in AUC / Popt / best or deployable threshold
4 MAJOR "old" not tested: relabel by age stratum [W,180),[180,365),[365,730),>=730
5 MAJOR reconcile with Song EMSE 2023, Song & Minku TSE 2023 (10.1109/TSE.2022.3158831), ODaSC-opt
6 MAJOR C4 row inaccurate: ORB, Cabral&Minku 2023, Pessoa 2021, arXiv 2611.21914
7 MAJOR significance for a methods journal; abstract uses dev numbers
8 MINOR wording: false-clean share vs labels; "contradicts"->"refines"; L2 only Cabral; SZZ-final alignment; keep test-reuse caveat by p-values
9 MINOR missing related work (Tan 2015, Kim 2011, Tantithamthavorn 2015, Liu 2022, Herbold 2022, Vandehei 2021, McIntosh&Kamei 2018, Falessi 2020, Zliobaite 2010, Souza 2015, Plasse&Adams 2016, Gomes 2022, Liu SCICO 2025)
10 MINOR reference name fixes (Di Penta, De Gruttola, Komei order)
11 MINOR C3 is about the kNN adaptation of ODaSC
12 MINOR evaluation-label dormancy: sensitivity with 730-day exclusion
