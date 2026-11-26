| comparison                              |   n |   mean_diff | ci95              |   wins |   losses |   wilcoxon_p |    holm_p | pass_margin   |
|:----------------------------------------|----:|------------:|:------------------|-------:|---------:|-------------:|----------:|:--------------|
| H9a: LAW+thr vs Wait-90                 |   9 |      0.0117 | [-0.007, 0.0301]  |      6 |        3 |   0.359375   | 1         | False         |
| H9a: LAW+thr vs ODaSC-style (lineage 2) |   9 |      0.0102 | [-0.015, 0.0335]  |      6 |        3 |   0.425781   | 1         | False         |
| H9b: nowait +thr vs fixed               |   9 |      0.0695 | [0.0319, 0.1105]  |      9 |        0 |   0.00390625 | 0.0273438 | True          |
| H9b: wait_W30 +thr vs fixed             |   9 |      0.0358 | [0.0124, 0.0618]  |      7 |        2 |   0.0390625  | 0.234375  | False         |
| H9b: wait_W90 +thr vs fixed             |   9 |      0.0036 | [-0.01, 0.0211]   |      4 |        5 |   0.820312   | 1         | False         |
| H9b: law_lagakos_model +thr vs fixed    |   9 |     -0.0034 | [-0.0202, 0.0119] |      5 |        4 |   0.734375   | 1         | False         |
| H9b: odasc_W30_d09_k50 +thr vs fixed    |   9 |      0.0017 | [-0.0131, 0.0176] |      4 |        5 |   1          | 1         | False         |