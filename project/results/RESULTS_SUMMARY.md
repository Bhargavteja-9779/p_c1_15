# RESULTS SUMMARY (auto-generated 2026-11-24T15:00:06+00:00 by scripts/final_report.py)

Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.

Frozen config: `{"frozen": "2026-11-24T13:19:55+00:00", "plan": "plan_v2", "candidate": "awt_e0.4", "candidate_dev_mean": 0.6968, "best_baseline_dev_mean": 0.7239, "candidate_beats_baseline_on_dev": false, "n_candidates_tried_on_dev": 8, "wait_W": 90, "orb_W": 90, "best_baseline_on_dev": "orb_W90", "dev_means": {"oracle": 0.7938, "orb_W90": 0.7239, "orb_W60": 0.7116, "wait_W90": 0.7095, "awt_e0.4": 0.6968, "awt_e0.3": 0.6937, "orb_W180": 0.6901, "wait_W60": 0.686, "wait_W180": 0.6831, "awt_e0.2": 0.6662, "law_lagakos_base": 0.6643, "awt_e0.5": 0.6643, "law_naive_base": 0.6637, "orb_W30": 0.6636, "wait_W30": 0.6206, "law_lagakos_model": 0.6128, "orb_W15": 0.6065, "law_naive_model": 0.58, "wait_W15": 0.5457, "nowait": 0.3855}, "proposed_plan_v1": "law_lagakos_model (pre-specified in plan_v1; kept in E1 as pre-registered)", "n_e0_runs": 240}`

Jobs: {'done': 900, 'pending': 335, 'running': 3}

## G-mean by project (mean over seeds)

### E0

| variant           |   fabric |   neutron |   nova |   sentry |   MEAN |
|:------------------|---------:|----------:|-------:|---------:|-------:|
| oracle            |    0.75  |     0.866 |  0.838 |    0.722 |  0.794 |
| orb_W90           |    0.653 |     0.817 |  0.788 |    0.637 |  0.724 |
| orb_W60           |    0.679 |     0.769 |  0.75  |    0.649 |  0.712 |
| wait_W90          |    0.638 |     0.784 |  0.771 |    0.645 |  0.709 |
| orb_W180          |    0.501 |     0.837 |  0.807 |    0.616 |  0.69  |
| wait_W60          |    0.667 |     0.671 |  0.742 |    0.664 |  0.686 |
| wait_W180         |    0.474 |     0.838 |  0.805 |    0.614 |  0.683 |
| law_lagakos_base  |    0.673 |     0.682 |  0.619 |    0.683 |  0.664 |
| law_naive_base    |    0.669 |     0.677 |  0.625 |    0.683 |  0.664 |
| orb_W30           |    0.683 |     0.649 |  0.656 |    0.666 |  0.664 |
| wait_W30          |    0.66  |     0.48  |  0.658 |    0.684 |  0.621 |
| law_lagakos_model |    0.668 |     0.496 |  0.614 |    0.673 |  0.613 |
| orb_W15           |    0.668 |     0.546 |  0.558 |    0.654 |  0.607 |
| law_naive_model   |    0.646 |     0.456 |  0.554 |    0.664 |  0.58  |
| wait_W15          |    0.597 |     0.369 |  0.554 |    0.663 |  0.546 |
| nowait            |    0.471 |     0.245 |  0.295 |    0.531 |  0.385 |

### E0b

| variant       |   fabric |   neutron |   nova |   sentry |   MEAN |
|:--------------|---------:|----------:|-------:|---------:|-------:|
| decomp_L1_W30 |    0.731 |     0.865 |  0.84  |    0.705 |  0.785 |
| decomp_L2_W30 |    0.714 |     0.869 |  0.832 |    0.66  |  0.769 |
| decomp_L1_W90 |    0.641 |     0.863 |  0.832 |    0.65  |  0.746 |
| decomp_L2_W90 |    0.547 |     0.847 |  0.81  |    0.618 |  0.706 |
| awt_e0.4      |    0.594 |     0.762 |  0.771 |    0.66  |  0.697 |
| awt_e0.3      |    0.539 |     0.811 |  0.796 |    0.629 |  0.694 |
| awt_e0.2      |    0.435 |     0.826 |  0.803 |    0.602 |  0.666 |
| awt_e0.5      |    0.62  |     0.642 |  0.714 |    0.682 |  0.664 |

### E1

| variant           |   brackets |   broadleaf |   camel |   jgroups |   matplotlib |   npm |   spring-integration |   tomcat |   wagtail |   zulip |   MEAN |
|:------------------|-----------:|------------:|--------:|----------:|-------------:|------:|---------------------:|---------:|----------:|--------:|-------:|
| oracle            |      0.786 |       0.727 |   0.705 |     0.64  |        0.742 | 0.689 |                0.766 |    0.71  |     0.697 |   0.686 |  0.715 |
| orb_W90           |      0.731 |       0.683 |   0.667 |     0.586 |        0.7   | 0.638 |                0.622 |    0.627 |     0.709 |   0.621 |  0.658 |
| wait_W90          |      0.731 |       0.691 |   0.665 |     0.576 |        0.682 | 0.63  |                0.595 |    0.628 |     0.694 |   0.653 |  0.654 |
| awt_e0.4          |      0.721 |       0.665 |   0.649 |     0.479 |        0.706 | 0.628 |                0.631 |    0.455 |     0.643 |   0.616 |  0.619 |
| law_lagakos_model |      0.721 |       0.643 |   0.652 |     0.56  |        0.691 | 0.449 |                0.633 |    0.664 |     0.543 |   0.607 |  0.616 |
| nowait            |      0.536 |       0.511 |   0.469 |     0.34  |        0.603 | 0.23  |                0.343 |    0.368 |     0.4   |   0.49  |  0.429 |

### E2

| variant          |   brackets |   MEAN |
|:-----------------|-----------:|-------:|
| law_lagakos_base |      0.727 |  0.727 |
| law_naive_base   |      0.725 |  0.725 |
| law_naive_model  |      0.711 |  0.711 |

### E3b

| variant       |   brackets |   broadleaf |   camel |   jgroups |   matplotlib |   npm |   spring-integration |   tomcat |   wagtail |   zulip |   MEAN |
|:--------------|-----------:|------------:|--------:|----------:|-------------:|------:|---------------------:|---------:|----------:|--------:|-------:|
| decomp_L1_W30 |      0.783 |       0.736 |   0.72  |     0.666 |        0.739 | 0.702 |                0.752 |    0.712 |     0.726 |   0.685 |  0.722 |
| decomp_L2_W30 |      0.772 |       0.745 |   0.71  |     0.618 |        0.75  | 0.666 |                0.706 |    0.663 |     0.727 |   0.669 |  0.702 |
| decomp_L1_W90 |      0.732 |       0.708 |   0.67  |     0.587 |        0.742 | 0.655 |                0.713 |    0.653 |     0.717 |   0.668 |  0.684 |
| wait_W90      |      0.731 |       0.691 |   0.665 |     0.576 |        0.682 | 0.63  |                0.595 |    0.628 |     0.694 |   0.653 |  0.654 |
| decomp_L2_W90 |      0.716 |       0.671 |   0.598 |     0.454 |        0.753 | 0.568 |                0.605 |    0.577 |     0.694 |   0.616 |  0.625 |
| wait_W30      |      0.768 |       0.662 |   0.649 |     0.57  |        0.644 | 0.552 |                0.506 |    0.621 |     0.611 |   0.622 |  0.62  |

## Statistics

```json
{
 "generated": "2026-11-24T15:00:05+00:00",
 "E1_main_law_vs_baselines": [
  {
   "proposed": "law_lagakos_model",
   "baseline": "nowait",
   "n_projects": 10,
   "mean_diff": 0.1872,
   "ci95": [
    0.1472,
    0.2288
   ],
   "wins": 10,
   "losses": 0,
   "wilcoxon_p": 0.001953125,
   "paired_t_p": 1.4333414264286952e-05,
   "rank_biserial": 1.0,
   "holm_p": 0.005859375,
   "G5_pass": true
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "wait_W90",
   "n_projects": 10,
   "mean_diff": -0.0381,
   "ci95": [
    -0.0848,
    0.0014
   ],
   "wins": 3,
   "losses": 7,
   "wilcoxon_p": 0.130859375,
   "paired_t_p": 0.13612852823803398,
   "rank_biserial": -0.564,
   "holm_p": 0.16796875,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "orb_W90",
   "n_projects": 10,
   "mean_diff": -0.0421,
   "ci95": [
    -0.0908,
    -0.0034
   ],
   "wins": 2,
   "losses": 8,
   "wilcoxon_p": 0.083984375,
   "paired_t_p": 0.10799677299662776,
   "rank_biserial": -0.636,
   "holm_p": 0.16796875,
   "G5_pass": false
  }
 ],
 "E2_ablation_full_vs_variants": [
  {
   "proposed": "law_lagakos_model",
   "baseline": "law_naive_model",
   "n_projects": 1,
   "mean_diff": 0.0101,
   "ci95": [
    0.0101,
    0.0101
   ],
   "wins": 1,
   "losses": 0,
   "wilcoxon_p": null,
   "paired_t_p": NaN,
   "rank_biserial": 1.0,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "law_lagakos_base",
   "n_projects": 1,
   "mean_diff": -0.0064,
   "ci95": [
    -0.0064,
    -0.0064
   ],
   "wins": 0,
   "losses": 1,
   "wilcoxon_p": null,
   "paired_t_p": NaN,
   "rank_biserial": -1.0,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "law_naive_base",
   "n_projects": 1,
   "mean_diff": -0.0046,
   "ci95": [
    -0.0046,
    -0.0046
   ],
   "wins": 0,
   "losses": 1,
   "wilcoxon_p": null,
   "paired_t_p": NaN,
   "rank_biserial": -1.0,
   "holm_p": 1.0,
   "G5_pass": false
  }
 ],
 "E1_H1_family_law_and_candidate_vs_baselines": [
  {
   "proposed": "law_lagakos_model",
   "baseline": "nowait",
   "n_projects": 10,
   "mean_diff": 0.1872,
   "ci95": [
    0.1472,
    0.2288
   ],
   "wins": 10,
   "losses": 0,
   "wilcoxon_p": 0.001953125,
   "paired_t_p": 1.4333414264286952e-05,
   "rank_biserial": 1.0,
   "holm_p": 0.005859375,
   "G5_pass": true,
   "holm_p_family6": 0.01171875
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "wait_W90",
   "n_projects": 10,
   "mean_diff": -0.0381,
   "ci95": [
    -0.0848,
    0.0014
   ],
   "wins": 3,
   "losses": 7,
   "wilcoxon_p": 0.130859375,
   "paired_t_p": 0.13612852823803398,
   "rank_biserial": -0.564,
   "holm_p": 0.16796875,
   "G5_pass": false,
   "holm_p_family6": 0.251953125
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "orb_W90",
   "n_projects": 10,
   "mean_diff": -0.0421,
   "ci95": [
    -0.0908,
    -0.0034
   ],
   "wins": 2,
   "losses": 8,
   "wilcoxon_p": 0.083984375,
   "paired_t_p": 0.10799677299662776,
   "rank_biserial": -0.636,
   "holm_p": 0.16796875,
   "G5_pass": false,
   "holm_p_family6": 0.251953125
  },
  {
   "proposed": "awt_e0.4",
   "baseline": "nowait",
   "n_projects": 10,
   "mean_diff": 0.1904,
   "ci95": [
    0.1396,
    0.2522
   ],
   "wins": 10,
   "losses": 0,
   "wilcoxon_p": 0.001953125,
   "paired_t_p": 0.00013953931642784144,
   "rank_biserial": 1.0,
   "holm_p": 0.005859375,
   "G5_pass": true,
   "holm_p_family6": 0.01171875
  },
  {
   "proposed": "awt_e0.4",
   "baseline": "wait_W90",
   "n_projects": 10,
   "mean_diff": -0.035,
   "ci95": [
    -0.0739,
    -0.0027
   ],
   "wins": 2,
   "losses": 8,
   "wilcoxon_p": 0.083984375,
   "paired_t_p": 0.10407513299644962,
   "rank_biserial": -0.636,
   "holm_p": 0.083984375,
   "G5_pass": false,
   "holm_p_family6": 0.251953125
  },
  {
   "proposed": "awt_e0.4",
   "baseline": "orb_W90",
   "n_projects": 10,
   "mean_diff": -0.039,
   "ci95": [
    -0.0772,
    -0.009
   ],
   "wins": 2,
   "losses": 8,
   "wilcoxon_p": 0.037109375,
   "paired_t_p": 0.06611970878501287,
   "rank_biserial": -0.745,
   "holm_p": 0.07421875,
   "G5_pass": false,
   "holm_p_family6": 0.1484375
  }
 ],
 "E3b_H3_denoised_W30_vs_wait": [
  {
   "proposed": "decomp_L1_W30",
   "baseline": "wait_W90",
   "n_projects": 10,
   "mean_diff": 0.0677,
   "ci95": [
    0.0487,
    0.0918
   ],
   "wins": 10,
   "losses": 0,
   "wilcoxon_p": 0.001953125,
   "paired_t_p": 0.000270606332888728,
   "rank_biserial": 1.0,
   "holm_p": 0.00390625,
   "G5_pass": true
  },
  {
   "proposed": "decomp_L1_W30",
   "baseline": "wait_W30",
   "n_projects": 10,
   "mean_diff": 0.1017,
   "ci95": [
    0.0689,
    0.1412
   ],
   "wins": 10,
   "losses": 0,
   "wilcoxon_p": 0.001953125,
   "paired_t_p": 0.0005540504299986918,
   "rank_biserial": 1.0,
   "holm_p": 0.00390625,
   "G5_pass": true
  }
 ],
 "E3b_H3_decomposition": {
  "gap_recovered_share_of_means": 1.0773,
  "gap_recovered_share_per_project": {
   "brackets": 0.849,
   "broadleaf": 1.15,
   "camel": 1.26,
   "jgroups": 1.36,
   "matplotlib": 0.974,
   "npm": 1.092,
   "spring-integration": 0.947,
   "tomcat": 1.023,
   "wagtail": 1.342,
   "zulip": 0.972
  },
  "mean_gap_oracle_minus_wait30": 0.0944,
  "denoise_gain_W30_mean": 0.1017,
  "denoise_gap_share_W30": 1.0773,
  "denoise_gain_W90_mean": 0.03,
  "denoise_gap_share_W90": 0.4977,
  "H3_pass": true
 },
 "n_variants_logged": 28
}
```

Compute used: 10.05 CPU-h (summed worker seconds). Variants logged: 28.
