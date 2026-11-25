# RESULTS SUMMARY (auto-generated 2026-11-25T21:37:23+00:00 by scripts/final_report.py)

Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.

Frozen config: `{"frozen": "2026-11-24T13:19:55+00:00", "plan": "plan_v2", "candidate": "awt_e0.4", "candidate_dev_mean": 0.6968, "best_baseline_dev_mean": 0.7239, "candidate_beats_baseline_on_dev": false, "n_candidates_tried_on_dev": 8, "wait_W": 90, "orb_W": 90, "best_baseline_on_dev": "orb_W90", "dev_means": {"oracle": 0.7938, "orb_W90": 0.7239, "orb_W60": 0.7116, "wait_W90": 0.7095, "awt_e0.4": 0.6968, "awt_e0.3": 0.6937, "orb_W180": 0.6901, "wait_W60": 0.686, "wait_W180": 0.6831, "awt_e0.2": 0.6662, "law_lagakos_base": 0.6643, "awt_e0.5": 0.6643, "law_naive_base": 0.6637, "orb_W30": 0.6636, "wait_W30": 0.6206, "law_lagakos_model": 0.6128, "orb_W15": 0.6065, "law_naive_model": 0.58, "wait_W15": 0.5457, "nowait": 0.3855}, "proposed_plan_v1": "law_lagakos_model (pre-specified in plan_v1; kept in E1 as pre-registered)", "n_e0_runs": 240}`

Jobs: {'done': 1526, 'skipped_budget': 144, 'skipped_plan': 117}

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

### E0c

| variant        |   fabric |   neutron |   nova |   sentry |   MEAN |
|:---------------|---------:|----------:|-------:|---------:|-------:|
| lawm_soft_W30  |    0.688 |     0.837 |  0.802 |    0.693 |  0.755 |
| lawm_soft_W90  |    0.622 |     0.853 |  0.813 |    0.643 |  0.733 |
| lawm_count_W90 |    0.637 |     0.798 |  0.777 |    0.648 |  0.715 |
| lawm_count_W30 |    0.665 |     0.549 |  0.719 |    0.687 |  0.655 |

### E0d

| variant        |   fabric |   neutron |   nova |   sentry |   MEAN |
|:---------------|---------:|----------:|-------:|---------:|-------:|
| odasc_W30_t0.8 |    0.715 |     0.779 |  0.831 |    0.714 |  0.76  |
| odasc_W90_t0.8 |    0.676 |     0.847 |  0.817 |    0.664 |  0.751 |
| odasc_W30_t0.9 |    0.722 |     0.75  |  0.817 |    0.705 |  0.749 |
| odasc_W90_t0.9 |    0.666 |     0.838 |  0.803 |    0.635 |  0.735 |

### E0e

| variant      |   fabric |   neutron |   nova |   sentry |   MEAN |
|:-------------|---------:|----------:|-------:|---------:|-------:|
| dual_W30_k50 |    0.715 |     0.848 |  0.475 |    0.687 |  0.681 |
| dual_W90_k50 |    0.611 |     0.854 |  0.464 |    0.618 |  0.637 |
| dual_W30_k20 |    0.713 |     0.61  |  0.473 |    0.691 |  0.622 |
| dual_W90_k20 |    0.617 |     0.628 |  0.465 |    0.622 |  0.583 |

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

| variant          |   brackets |   broadleaf |   camel |   MEAN |
|:-----------------|-----------:|------------:|--------:|-------:|
| law_naive_base   |      0.725 |       0.654 | nan     |  0.69  |
| law_lagakos_base |      0.727 |       0.659 |   0.668 |  0.685 |
| law_naive_model  |      0.712 |       0.627 | nan     |  0.669 |

### E3

| variant               |   brackets |   broadleaf |   camel |   MEAN |
|:----------------------|-----------:|------------:|--------:|-------:|
| wait_W90_ds2          |      0.731 |       0.688 |   0.671 |  0.697 |
| orb_W90_ds2           |      0.732 |       0.683 |   0.666 |  0.694 |
| law_lagakos_model_ds2 |      0.702 |       0.611 |   0.638 |  0.65  |
| nowait_ds2            |      0.452 |       0.455 |   0.445 |  0.451 |

### E3b

| variant       |   brackets |   broadleaf |   camel |   jgroups |   matplotlib |   npm |   spring-integration |   tomcat |   wagtail |   zulip |   MEAN |
|:--------------|-----------:|------------:|--------:|----------:|-------------:|------:|---------------------:|---------:|----------:|--------:|-------:|
| decomp_L1_W30 |      0.783 |       0.736 |   0.72  |     0.666 |        0.739 | 0.702 |                0.752 |    0.712 |     0.726 |   0.685 |  0.722 |
| decomp_L2_W30 |      0.772 |       0.745 |   0.71  |     0.618 |        0.75  | 0.666 |                0.706 |    0.663 |     0.727 |   0.669 |  0.702 |
| decomp_L1_W90 |      0.732 |       0.708 |   0.67  |     0.587 |        0.742 | 0.655 |                0.713 |    0.653 |     0.717 |   0.668 |  0.684 |
| wait_W90      |      0.731 |       0.691 |   0.665 |     0.576 |        0.682 | 0.63  |                0.595 |    0.628 |     0.694 |   0.653 |  0.654 |
| decomp_L2_W90 |      0.716 |       0.671 |   0.598 |     0.454 |        0.753 | 0.568 |                0.605 |    0.577 |     0.694 |   0.616 |  0.625 |
| wait_W30      |      0.768 |       0.662 |   0.649 |     0.57  |        0.644 | 0.552 |                0.506 |    0.621 |     0.611 |   0.622 |  0.62  |

### E8

| variant        |   aj_activemq |   aj_cassandra |   aj_flink |   aj_groovy |   aj_hadoop-hdfs |   aj_hbase |   aj_hive |   aj_ignite |   aj_kafka |   MEAN |
|:---------------|--------------:|---------------:|-----------:|------------:|-----------------:|-----------:|----------:|------------:|-----------:|-------:|
| oracle         |         0.714 |          0.784 |      0.781 |       0.678 |            0.83  |      0.778 |     0.808 |       0.773 |      0.783 |  0.77  |
| decomp_L1_W30  |         0.707 |          0.782 |      0.776 |       0.671 |            0.794 |      0.772 |     0.807 |       0.763 |      0.784 |  0.762 |
| dual_W30_k50   |         0.681 |          0.755 |      0.754 |       0.682 |            0.762 |      0.741 |     0.754 |       0.743 |      0.744 |  0.735 |
| lawm_soft_W30  |         0.639 |          0.752 |      0.739 |       0.626 |            0.749 |      0.758 |     0.776 |       0.731 |      0.779 |  0.728 |
| odasc_W30_t0.8 |         0.641 |          0.741 |      0.742 |       0.624 |            0.724 |      0.733 |     0.776 |       0.737 |      0.74  |  0.718 |
| wait_W90       |         0.624 |          0.728 |      0.748 |       0.617 |            0.707 |      0.748 |     0.772 |       0.722 |      0.781 |  0.716 |
| orb_W90        |         0.645 |          0.711 |      0.732 |       0.64  |            0.662 |      0.708 |     0.752 |       0.723 |      0.784 |  0.706 |
| wait_W30       |         0.607 |          0.666 |      0.734 |       0.59  |            0.621 |      0.718 |     0.748 |       0.714 |      0.784 |  0.687 |
| nowait         |         0.587 |          0.561 |      0.715 |       0.544 |            0.596 |      0.671 |     0.713 |       0.683 |      0.758 |  0.648 |

## Statistics

```json
{
 "generated": "2026-11-25T21:37:21+00:00",
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
   "n_projects": 2,
   "mean_diff": 0.0127,
   "ci95": [
    0.0093,
    0.0161
   ],
   "wins": 2,
   "losses": 0,
   "wilcoxon_p": null,
   "paired_t_p": 0.16715243846529462,
   "rank_biserial": 1.0,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "law_lagakos_base",
   "n_projects": 3,
   "mean_diff": -0.0126,
   "ci95": [
    -0.0158,
    -0.0064
   ],
   "wins": 0,
   "losses": 3,
   "wilcoxon_p": null,
   "paired_t_p": 0.05554002980531053,
   "rank_biserial": -1.0,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model",
   "baseline": "law_naive_base",
   "n_projects": 2,
   "mean_diff": -0.0077,
   "ci95": [
    -0.0108,
    -0.0046
   ],
   "wins": 0,
   "losses": 2,
   "wilcoxon_p": null,
   "paired_t_p": 0.24360322930246942,
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
 "E3_robust_delay_x2": [
  {
   "proposed": "law_lagakos_model_ds2",
   "baseline": "nowait_ds2",
   "n_projects": 3,
   "mean_diff": 0.1997,
   "ci95": [
    0.1557,
    0.2506
   ],
   "wins": 3,
   "losses": 0,
   "wilcoxon_p": null,
   "paired_t_p": 0.01854791781040511,
   "rank_biserial": 1.0,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_ds2",
   "baseline": "wait_W90_ds2",
   "n_projects": 3,
   "mean_diff": -0.0463,
   "ci95": [
    -0.0765,
    -0.0294
   ],
   "wins": 0,
   "losses": 3,
   "wilcoxon_p": null,
   "paired_t_p": 0.09259897165814186,
   "rank_biserial": -1.0,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_ds2",
   "baseline": "orb_W90_ds2",
   "n_projects": 3,
   "mean_diff": -0.0432,
   "ci95": [
    -0.0721,
    -0.028
   ],
   "wins": 0,
   "losses": 3,
   "wilcoxon_p": null,
   "paired_t_p": 0.09572833080478216,
   "rank_biserial": -1.0,
   "holm_p": 1.0,
   "G5_pass": false
  }
 ],
 "E8_planv7_H6_primary_vs_baselines": [
  {
   "proposed": "odasc_W30_t0.8",
   "baseline": "wait_W90",
   "n_projects": 9,
   "mean_diff": 0.0012,
   "ci95": [
    -0.0117,
    0.0117
   ],
   "wins": 6,
   "losses": 3,
   "wilcoxon_p": 0.5703125,
   "paired_t_p": 0.8618882859627292,
   "rank_biserial": 0.244,
   "holm_p": 0.6015625,
   "G5_pass": false,
   "H6_pass": false
  },
  {
   "proposed": "odasc_W30_t0.8",
   "baseline": "orb_W90",
   "n_projects": 9,
   "mean_diff": 0.0114,
   "ci95": [
    -0.0071,
    0.0297
   ],
   "wins": 6,
   "losses": 3,
   "wilcoxon_p": 0.30078125,
   "paired_t_p": 0.2900614865143757,
   "rank_biserial": 0.422,
   "holm_p": 0.6015625,
   "G5_pass": false,
   "H6_pass": false
  }
 ],
 "E8_H6_family_note": "primary=odasc_W30_t0.8; primary is the odasc baseline itself -> self-comparison dropped, Holm over 2 tests (decision 2026-11-25, before E8 analysis)",
 "E8_H6_all_pass": false,
 "E8_descriptive_dual_W30_k50": [
  {
   "proposed": "dual_W30_k50",
   "baseline": "wait_W90",
   "n_projects": 9,
   "mean_diff": 0.0186,
   "ci95": [
    -0.0033,
    0.0404
   ],
   "wins": 6,
   "losses": 3,
   "wilcoxon_p": 0.203125,
   "paired_t_p": 0.15757963053946636,
   "rank_biserial": 0.511,
   "holm_p": 0.203125,
   "G5_pass": false
  },
  {
   "proposed": "dual_W30_k50",
   "baseline": "orb_W90",
   "n_projects": 9,
   "mean_diff": 0.0288,
   "ci95": [
    0.0063,
    0.0521
   ],
   "wins": 8,
   "losses": 1,
   "wilcoxon_p": 0.0546875,
   "paired_t_p": 0.048525306715819075,
   "rank_biserial": 0.733,
   "holm_p": 0.1640625,
   "G5_pass": false
  },
  {
   "proposed": "dual_W30_k50",
   "baseline": "odasc_W30_t0.8",
   "n_projects": 9,
   "mean_diff": 0.0175,
   "ci95": [
    0.003,
    0.0323
   ],
   "wins": 8,
   "losses": 1,
   "wilcoxon_p": 0.0546875,
   "paired_t_p": 0.05957730615487514,
   "rank_biserial": 0.733,
   "holm_p": 0.1640625,
   "G5_pass": false
  }
 ],
 "E8_descriptive_lawm_soft_W30": [
  {
   "proposed": "lawm_soft_W30",
   "baseline": "wait_W90",
   "n_projects": 9,
   "mean_diff": 0.0113,
   "ci95": [
    0.0028,
    0.0209
   ],
   "wins": 7,
   "losses": 2,
   "wilcoxon_p": 0.0546875,
   "paired_t_p": 0.05189217546020266,
   "rank_biserial": 0.733,
   "holm_p": 0.1640625,
   "G5_pass": false
  },
  {
   "proposed": "lawm_soft_W30",
   "baseline": "orb_W90",
   "n_projects": 9,
   "mean_diff": 0.0215,
   "ci95": [
    0.0028,
    0.0433
   ],
   "wins": 6,
   "losses": 3,
   "wilcoxon_p": 0.09765625,
   "paired_t_p": 0.08509184734149532,
   "rank_biserial": 0.644,
   "holm_p": 0.1953125,
   "G5_pass": false
  },
  {
   "proposed": "lawm_soft_W30",
   "baseline": "odasc_W30_t0.8",
   "n_projects": 9,
   "mean_diff": 0.0102,
   "ci95": [
    0.0011,
    0.0202
   ],
   "wins": 6,
   "losses": 3,
   "wilcoxon_p": 0.203125,
   "paired_t_p": 0.09085919816656027,
   "rank_biserial": 0.511,
   "holm_p": 0.203125,
   "G5_pass": false
  }
 ],
 "E8_secondary_H3_replication": [
  {
   "proposed": "decomp_L1_W30",
   "baseline": "wait_W90",
   "n_projects": 9,
   "mean_diff": 0.0453,
   "ci95": [
    0.0291,
    0.0624
   ],
   "wins": 9,
   "losses": 0,
   "wilcoxon_p": 0.00390625,
   "paired_t_p": 0.001074120743562676,
   "rank_biserial": 1.0,
   "holm_p": 0.0078125,
   "G5_pass": true
  },
  {
   "proposed": "decomp_L1_W30",
   "baseline": "wait_W30",
   "n_projects": 9,
   "mean_diff": 0.0749,
   "ci95": [
    0.0461,
    0.107
   ],
   "wins": 8,
   "losses": 1,
   "wilcoxon_p": 0.0078125,
   "paired_t_p": 0.002036213625019109,
   "rank_biserial": 0.956,
   "holm_p": 0.0078125,
   "G5_pass": true
  }
 ],
 "E8_secondary_H3_decomposition": {
  "gap_recovered_share_of_means": 0.903,
  "gap_recovered_share_per_project": {
   "aj_activemq": 0.936,
   "aj_cassandra": 0.983,
   "aj_flink": 0.902,
   "aj_groovy": 0.926,
   "aj_hadoop-hdfs": 0.828,
   "aj_hbase": 0.9,
   "aj_hive": 0.978,
   "aj_ignite": 0.838,
   "aj_kafka": 0.75
  }
 },
 "n_variants_logged": 47
}
```

Compute used: 29.50 CPU-h (summed worker seconds). Variants logged: 47.
