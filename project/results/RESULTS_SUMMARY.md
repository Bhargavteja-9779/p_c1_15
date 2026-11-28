# RESULTS SUMMARY (auto-generated 2026-11-28T17:06:41+00:00 by scripts/final_report.py)

Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.

Frozen config: `{"frozen": "2026-11-25T07:54:45+00:00", "plan": "plan_v3", "proposed": {"variant": "law_lagakos_model_gmax_lat", "method": "law", "delay_est": "lagakos", "prior": "model", "thr_policy": "gmax_lat"}, "baselines": [{"variant": "nowait", "method": "nowait"}, {"variant": "wait_W90", "method": "wait", "W": 90}, {"variant": "orb_W90", "method": "orb", "W": 90}, {"variant": "odasc_W30", "method": "odasc", "W": 30, "odasc_delta": 0.9}, {"variant": "wait_W30_gmax_lat", "method": "wait", "W": 30, "thr_policy": "gmax_lat"}, {"variant": "odasc_W15_gmax_lat", "method": "odasc", "W": 15, "odasc_delta": 0.9, "thr_policy": "gmax_lat"}], "oracle": {"variant": "oracle", "method": "oracle"}, "primary_comparator": "odasc_W30", "n_dev_variants": 44, "n_dev_runs": 528, "dev_means": {"oracle": 0.7938, "law_lagakos_model_gmax_lat": 0.7632, "law_naive_model_gmax_lat": 0.7611, "odasc_W30": 0.7497, "odasc_W15_gmax_lat": 0.7491, "odasc_W30_gmax_lat": 0.7489, "law_naive_base_gmax_lat": 0.7475, "law_lagakos_base_gmax_lat": 0.7474, "odasc_W15": 0.7466, "wait_W30_gmax_lat": 0.7437, "odasc_W60_gmax_lat": 0.7424, "wait_W60_gmax_lat": 0.7392, "wait_W15_gmax_lat": 0.7389, "odasc_W60": 0.7367, "wait_W90_gmax_lat": 0.7367, "odasc_W90_gmax_lat": 0.7339, "wait_W180_gmax_lat": 0.7317, "orb_W180_gmax_lat": 0.7288, "orb_W90": 0.7239, "odasc_W180_gmax_lat": 0.7229, "orb_W90_gmax_lat": 0.7178, "odasc_W90": 0.7167, "orb_W60": 0.7116, "orb_W60_gmax_lat": 0.7097, "wait_W90": 0.7095, "orb_W180": 0.6901, "nowait_gmax_lat": 0.6881, "wait_W60": 0.686, "orb_W30_gmax_lat": 0.6832, "wait_W180": 0.6831, "law_lagakos_base_ratematch": 0.6784, "law_naive_base_ratematch": 0.6764, "law_lagakos_base": 0.6643, "law_naive_base": 0.6637, "orb_W30": 0.6636, "odasc_W180": 0.6564, "orb_W15_gmax_lat": 0.6463, "nowait_ratematch": 0.6327, "wait_W30": 0.6206, "law_lagakos_model": 0.6128, "orb_W15": 0.6065, "law_naive_model": 0.58, "wait_W15": 0.5457, "nowait": 0.3855}}`

Jobs: {'done': 1681, 'pending': 877, 'running': 4}

## G-mean by project (mean over seeds)

### D1

| variant           |   fabric |   neutron |   sentry |   MEAN |
|:------------------|---------:|----------:|---------:|-------:|
| oracle_young_H180 |    0.755 |     0.872 |    0.72  |  0.782 |
| oracle_young_H30  |    0.719 |     0.796 |    0.707 |  0.741 |
| oracle_old_H30    |    0.559 |     0.574 |    0.57  |  0.568 |
| oracle_old_H180   |    0.453 |     0.254 |    0.535 |  0.414 |

### E0

| variant                    |   fabric |   neutron |   nova |   sentry |   MEAN |
|:---------------------------|---------:|----------:|-------:|---------:|-------:|
| oracle                     |    0.75  |     0.866 |  0.838 |    0.722 |  0.794 |
| law_lagakos_model_gmax_lat |    0.713 |     0.828 |  0.8   |    0.713 |  0.763 |
| law_naive_model_gmax_lat   |    0.713 |     0.826 |  0.798 |    0.708 |  0.761 |
| odasc_W30                  |    0.7   |     0.798 |  0.817 |    0.684 |  0.75  |
| odasc_W15_gmax_lat         |    0.718 |     0.773 |  0.798 |    0.708 |  0.749 |
| odasc_W30_gmax_lat         |    0.711 |     0.8   |  0.784 |    0.702 |  0.749 |
| law_naive_base_gmax_lat    |    0.689 |     0.817 |  0.792 |    0.692 |  0.748 |
| law_lagakos_base_gmax_lat  |    0.683 |     0.814 |  0.796 |    0.697 |  0.747 |
| odasc_W15                  |    0.71  |     0.76  |  0.813 |    0.703 |  0.747 |
| wait_W30_gmax_lat          |    0.699 |     0.821 |  0.774 |    0.68  |  0.744 |
| odasc_W60_gmax_lat         |    0.686 |     0.815 |  0.78  |    0.688 |  0.742 |
| wait_W60_gmax_lat          |    0.67  |     0.828 |  0.788 |    0.671 |  0.739 |
| wait_W15_gmax_lat          |    0.707 |     0.808 |  0.754 |    0.685 |  0.739 |
| odasc_W60                  |    0.669 |     0.824 |  0.813 |    0.641 |  0.737 |
| wait_W90_gmax_lat          |    0.662 |     0.831 |  0.787 |    0.665 |  0.737 |
| odasc_W90_gmax_lat         |    0.673 |     0.812 |  0.777 |    0.674 |  0.734 |
| wait_W180_gmax_lat         |    0.64  |     0.832 |  0.793 |    0.661 |  0.732 |
| orb_W180_gmax_lat          |    0.659 |     0.833 |  0.772 |    0.651 |  0.729 |
| orb_W90                    |    0.653 |     0.817 |  0.788 |    0.637 |  0.724 |
| odasc_W180_gmax_lat        |    0.644 |     0.81  |  0.78  |    0.658 |  0.723 |
| orb_W90_gmax_lat           |    0.684 |     0.832 |  0.695 |    0.66  |  0.718 |
| odasc_W90                  |    0.629 |     0.828 |  0.806 |    0.604 |  0.717 |
| orb_W60                    |    0.679 |     0.769 |  0.75  |    0.649 |  0.712 |
| orb_W60_gmax_lat           |    0.674 |     0.821 |  0.68  |    0.663 |  0.71  |
| wait_W90                   |    0.638 |     0.784 |  0.771 |    0.645 |  0.709 |
| orb_W180                   |    0.501 |     0.837 |  0.807 |    0.616 |  0.69  |
| nowait_gmax_lat            |    0.7   |     0.77  |  0.607 |    0.675 |  0.688 |
| wait_W60                   |    0.667 |     0.671 |  0.742 |    0.664 |  0.686 |
| orb_W30_gmax_lat           |    0.694 |     0.738 |  0.633 |    0.667 |  0.683 |
| wait_W180                  |    0.474 |     0.838 |  0.805 |    0.614 |  0.683 |
| law_lagakos_base_ratematch |    0.681 |     0.69  |  0.709 |    0.634 |  0.678 |
| law_naive_base_ratematch   |    0.681 |     0.691 |  0.709 |    0.625 |  0.676 |
| law_lagakos_base           |    0.673 |     0.682 |  0.619 |    0.683 |  0.664 |
| law_naive_base             |    0.669 |     0.677 |  0.625 |    0.683 |  0.664 |
| orb_W30                    |    0.683 |     0.649 |  0.656 |    0.666 |  0.664 |
| odasc_W180                 |    0.482 |     0.808 |  0.787 |    0.548 |  0.656 |
| orb_W15_gmax_lat           |    0.693 |     0.618 |  0.605 |    0.669 |  0.646 |
| nowait_ratematch           |    0.66  |     0.673 |  0.552 |    0.646 |  0.633 |
| wait_W30                   |    0.66  |     0.48  |  0.658 |    0.684 |  0.621 |
| law_lagakos_model          |    0.668 |     0.496 |  0.614 |    0.673 |  0.613 |
| orb_W15                    |    0.668 |     0.546 |  0.558 |    0.654 |  0.607 |
| law_naive_model            |    0.646 |     0.456 |  0.554 |    0.664 |  0.58  |
| wait_W15                   |    0.597 |     0.369 |  0.554 |    0.663 |  0.546 |
| nowait                     |    0.471 |     0.245 |  0.295 |    0.531 |  0.385 |

### E1

| variant                    |   brackets |   broadleaf |   camel |   jgroups |   matplotlib |   npm |   spring-integration |   tomcat |   wagtail |   zulip |   MEAN |
|:---------------------------|-----------:|------------:|--------:|----------:|-------------:|------:|---------------------:|---------:|----------:|--------:|-------:|
| oracle                     |      0.786 |       0.727 |   0.705 |     0.64  |        0.742 | 0.689 |                0.766 |    0.71  |     0.697 |   0.686 |  0.715 |
| law_lagakos_model_gmax_lat |      0.774 |       0.731 |   0.697 |     0.646 |        0.727 | 0.657 |                0.68  |    0.694 |     0.689 |   0.665 |  0.696 |
| odasc_W15_gmax_lat         |      0.77  |       0.731 |   0.694 |     0.644 |        0.733 | 0.636 |                0.683 |    0.692 |     0.708 |   0.662 |  0.695 |
| odasc_W30                  |      0.737 |       0.733 |   0.716 |     0.652 |        0.723 | 0.654 |                0.678 |    0.681 |     0.714 |   0.662 |  0.695 |
| wait_W30_gmax_lat          |      0.76  |       0.721 |   0.683 |     0.613 |        0.723 | 0.613 |                0.652 |    0.671 |     0.692 |   0.63  |  0.676 |
| orb_W90                    |      0.731 |       0.683 |   0.667 |     0.586 |        0.7   | 0.638 |                0.622 |    0.627 |     0.709 |   0.621 |  0.658 |
| wait_W90                   |      0.731 |       0.691 |   0.665 |     0.576 |        0.682 | 0.63  |                0.595 |    0.628 |     0.694 |   0.653 |  0.654 |
| nowait                     |      0.536 |       0.511 |   0.469 |     0.34  |        0.603 | 0.23  |                0.343 |    0.368 |     0.4   |   0.49  |  0.429 |

### E2

| variant                   |   brackets |   broadleaf |   camel |   jgroups |   matplotlib |   MEAN |
|:--------------------------|-----------:|------------:|--------:|----------:|-------------:|-------:|
| law_naive_model_gmax_lat  |      0.775 |       0.731 |   0.696 |     0.632 |      nan     |  0.709 |
| law_lagakos_base_gmax_lat |      0.767 |       0.71  |   0.689 |     0.619 |        0.711 |  0.699 |
| nowait_gmax_lat           |      0.752 |       0.722 |   0.68  |     0.619 |      nan     |  0.693 |
| law_lagakos_model         |      0.721 |       0.643 |   0.652 |     0.56  |        0.691 |  0.653 |

### E7

| variant           |   aj_activemq |   aj_cassandra |   aj_flink |   aj_groovy |   aj_hbase |   aj_hive |   aj_ignite |   aj_kafka |   brackets |   broadleaf |   camel |   jgroups |   matplotlib |   MEAN |
|:------------------|--------------:|---------------:|-----------:|------------:|-----------:|----------:|------------:|-----------:|-----------:|------------:|--------:|----------:|-------------:|-------:|
| oracle            |         0.714 |          0.784 |      0.782 |       0.676 |      0.779 |     0.809 |       0.773 |      0.781 |      0.789 |       0.724 |   0.707 |     0.639 |        0.741 |  0.746 |
| oracle_young_H180 |         0.653 |          0.78  |      0.768 |       0.6   |      0.774 |     0.798 |       0.763 |      0.796 |      0.787 |       0.724 |   0.708 |     0.647 |      nan     |  0.733 |
| oracle_young_H30  |         0.572 |          0.735 |      0.742 |       0.543 |      0.736 |     0.769 |       0.725 |      0.782 |      0.769 |       0.679 |   0.663 |     0.6   |      nan     |  0.693 |
| oracle_old_H30    |         0.682 |          0.687 |      0.765 |       0.636 |      0.745 |     0.782 |       0.729 |      0.783 |      0.579 |       0.615 |   0.538 |     0.429 |        0.701 |  0.667 |
| oracle_old_H180   |         0.603 |          0.592 |      0.729 |       0.564 |      0.687 |     0.748 |       0.697 |      0.755 |      0.527 |       0.511 |   0.47  |     0.36  |        0.655 |  0.607 |
| nowait            |         0.587 |          0.563 |      0.716 |       0.546 |      0.669 |     0.711 |       0.684 |      0.761 |      0.535 |       0.517 |   0.469 |     0.335 |        0.6   |  0.592 |

### E8

| variant                    |   aj_activemq |   aj_cassandra |   aj_flink |   aj_groovy |   aj_hbase |   aj_hive |   aj_ignite |   aj_kafka |   MEAN |
|:---------------------------|--------------:|---------------:|-----------:|------------:|-----------:|----------:|------------:|-----------:|-------:|
| oracle                     |         0.714 |          0.784 |      0.781 |       0.678 |      0.778 |     0.809 |       0.774 |      0.783 |  0.763 |
| law_lagakos_model_gmax_lat |         0.616 |          0.755 |      0.723 |       0.674 |      0.769 |     0.787 |       0.684 |      0.799 |  0.726 |
| odasc_W15_gmax_lat         |         0.642 |          0.752 |      0.729 |       0.674 |      0.747 |     0.771 |       0.706 |      0.784 |  0.726 |
| wait_W30_gmax_lat          |         0.632 |          0.736 |      0.731 |       0.678 |      0.744 |     0.769 |       0.701 |      0.784 |  0.722 |
| odasc_W30                  |         0.657 |          0.745 |      0.725 |       0.648 |      0.725 |     0.78  |       0.742 |      0.743 |  0.721 |
| wait_W90                   |         0.624 |          0.728 |      0.747 |       0.617 |      0.747 |     0.77  |       0.723 |      0.781 |  0.717 |
| orb_W90                    |         0.645 |          0.709 |      0.734 |       0.64  |      0.706 |     0.753 |       0.721 |      0.784 |  0.711 |
| nowait                     |         0.587 |          0.565 |      0.716 |       0.547 |      0.671 |     0.712 |       0.685 |      0.758 |  0.655 |

### E9

| variant                                 |   fabric |   neutron |   sentry |   MEAN |
|:----------------------------------------|---------:|----------:|---------:|-------:|
| law_lagakos_model_gmax_lat__insp_rand_5 |    0.72  |     0.834 |    0.713 |  0.756 |
| law_lagakos_model_gmax_lat__insp_top_5  |    0.721 |     0.831 |    0.713 |  0.755 |
| law_lagakos_model_gmax_lat__insp_unc_5  |    0.717 |     0.836 |    0.709 |  0.754 |
| law_lagakos_model_gmax_lat__insp_rand_2 |    0.717 |     0.833 |    0.711 |  0.754 |
| law_lagakos_model_gmax_lat__insp_top_2  |    0.714 |     0.833 |    0.712 |  0.753 |
| law_lagakos_model_gmax_lat__insp_unc_2  |    0.713 |     0.833 |    0.711 |  0.752 |
| odasc_W30__insp_unc_5                   |    0.7   |     0.827 |    0.687 |  0.738 |
| odasc_W30__insp_top_5                   |    0.703 |     0.82  |    0.687 |  0.736 |
| odasc_W30__insp_rand_5                  |    0.704 |     0.811 |    0.688 |  0.734 |
| nowait_gmax_lat__insp_top_5             |    0.713 |     0.797 |    0.686 |  0.732 |
| nowait_gmax_lat__insp_unc_5             |    0.706 |     0.811 |    0.678 |  0.732 |
| odasc_W30__insp_unc_2                   |    0.699 |     0.809 |    0.686 |  0.731 |
| odasc_W30__insp_top_2                   |    0.701 |     0.807 |    0.685 |  0.731 |
| odasc_W30__insp_rand_2                  |    0.7   |     0.805 |    0.685 |  0.73  |
| nowait_gmax_lat__insp_rand_5            |    0.71  |     0.797 |    0.682 |  0.73  |
| nowait_gmax_lat__insp_unc_2             |    0.709 |     0.796 |    0.678 |  0.728 |
| nowait_gmax_lat__insp_top_2             |    0.704 |     0.779 |    0.681 |  0.721 |
| nowait_gmax_lat__insp_rand_2            |    0.702 |     0.78  |    0.681 |  0.721 |

## Statistics

```json
{
 "generated": "2026-11-28T17:06:39+00:00",
 "E1_main_proposed_vs_baselines": [
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "nowait",
   "n_projects": 10,
   "mean_diff": 0.267,
   "ci95": [
    0.2165,
    0.3199
   ],
   "wins": 10,
   "losses": 0,
   "wilcoxon_p": 0.001953125,
   "paired_t_p": 5.019410082692971e-06,
   "rank_biserial": 1.0,
   "holm_p": 0.01171875,
   "G5_pass": true
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "wait_W90",
   "n_projects": 10,
   "mean_diff": 0.0417,
   "ci95": [
    0.0258,
    0.0575
   ],
   "wins": 9,
   "losses": 1,
   "wilcoxon_p": 0.00390625,
   "paired_t_p": 0.000941668170484443,
   "rank_biserial": 0.964,
   "holm_p": 0.01953125,
   "G5_pass": true
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "orb_W90",
   "n_projects": 10,
   "mean_diff": 0.0377,
   "ci95": [
    0.0216,
    0.0511
   ],
   "wins": 9,
   "losses": 1,
   "wilcoxon_p": 0.005859375,
   "paired_t_p": 0.0011187150714508604,
   "rank_biserial": 0.927,
   "holm_p": 0.01953125,
   "G5_pass": true
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "odasc_W30",
   "n_projects": 10,
   "mean_diff": 0.0009,
   "ci95": [
    -0.0086,
    0.0114
   ],
   "wins": 6,
   "losses": 4,
   "wilcoxon_p": 0.76953125,
   "paired_t_p": 0.8634546291541089,
   "rank_biserial": 0.127,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "wait_W30_gmax_lat",
   "n_projects": 10,
   "mean_diff": 0.0202,
   "ci95": [
    0.0115,
    0.0289
   ],
   "wins": 9,
   "losses": 1,
   "wilcoxon_p": 0.00390625,
   "paired_t_p": 0.0019154862775619945,
   "rank_biserial": 0.964,
   "holm_p": 0.01953125,
   "G5_pass": true
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "odasc_W15_gmax_lat",
   "n_projects": 10,
   "mean_diff": 0.0008,
   "ci95": [
    -0.005,
    0.0067
   ],
   "wins": 7,
   "losses": 3,
   "wilcoxon_p": 0.625,
   "paired_t_p": 0.8058545015479147,
   "rank_biserial": 0.2,
   "holm_p": 1.0,
   "G5_pass": false
  }
 ],
 "E1_primary_comparator": "odasc_W30",
 "E2_ablation_full_vs_component_removed": [
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "law_lagakos_model",
   "n_projects": 5,
   "mean_diff": 0.0618,
   "ci95": [
    0.0432,
    0.0803
   ],
   "wins": 5,
   "losses": 0,
   "wilcoxon_p": 0.0625,
   "paired_t_p": 0.004465520114453937,
   "rank_biserial": 1.0,
   "holm_p": 0.25,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "law_naive_model_gmax_lat",
   "n_projects": 4,
   "mean_diff": 0.0036,
   "ci95": [
    -0.0008,
    0.0107
   ],
   "wins": 3,
   "losses": 1,
   "wilcoxon_p": null,
   "paired_t_p": 0.3823201006659317,
   "rank_biserial": 0.4,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "law_lagakos_base_gmax_lat",
   "n_projects": 5,
   "mean_diff": 0.016,
   "ci95": [
    0.0093,
    0.0226
   ],
   "wins": 5,
   "losses": 0,
   "wilcoxon_p": 0.0625,
   "paired_t_p": 0.01413029710945977,
   "rank_biserial": 1.0,
   "holm_p": 0.25,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "nowait_gmax_lat",
   "n_projects": 4,
   "mean_diff": 0.019,
   "ci95": [
    0.0125,
    0.0246
   ],
   "wins": 4,
   "losses": 0,
   "wilcoxon_p": null,
   "paired_t_p": 0.014625946368356254,
   "rank_biserial": 1.0,
   "holm_p": 1.0,
   "G5_pass": false
  }
 ],
 "E8_H6_replication_apachejit": [
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "nowait",
   "n_projects": 8,
   "mean_diff": 0.0708,
   "ci95": [
    0.0315,
    0.1144
   ],
   "wins": 7,
   "losses": 1,
   "wilcoxon_p": 0.015625,
   "paired_t_p": 0.018017865084826865,
   "rank_biserial": 0.944,
   "holm_p": 0.09375,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "wait_W90",
   "n_projects": 8,
   "mean_diff": 0.0087,
   "ci95": [
    -0.0109,
    0.028
   ],
   "wins": 5,
   "losses": 3,
   "wilcoxon_p": 0.546875,
   "paired_t_p": 0.44572810292815396,
   "rank_biserial": 0.278,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "orb_W90",
   "n_projects": 8,
   "mean_diff": 0.0145,
   "ci95": [
    -0.0097,
    0.0374
   ],
   "wins": 5,
   "losses": 3,
   "wilcoxon_p": 0.3125,
   "paired_t_p": 0.29936505059591756,
   "rank_biserial": 0.444,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "odasc_W30",
   "n_projects": 8,
   "mean_diff": 0.0052,
   "ci95": [
    -0.0208,
    0.0295
   ],
   "wins": 5,
   "losses": 3,
   "wilcoxon_p": 0.640625,
   "paired_t_p": 0.717935008005708,
   "rank_biserial": 0.222,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "wait_W30_gmax_lat",
   "n_projects": 8,
   "mean_diff": 0.004,
   "ci95": [
    -0.0071,
    0.0149
   ],
   "wins": 4,
   "losses": 4,
   "wilcoxon_p": 0.4609375,
   "paired_t_p": 0.5302899439175804,
   "rank_biserial": 0.333,
   "holm_p": 1.0,
   "G5_pass": false
  },
  {
   "proposed": "law_lagakos_model_gmax_lat",
   "baseline": "odasc_W15_gmax_lat",
   "n_projects": 8,
   "mean_diff": 0.0002,
   "ci95": [
    -0.0115,
    0.0112
   ],
   "wins": 4,
   "losses": 4,
   "wilcoxon_p": 1.0,
   "paired_t_p": 0.9706461906551831,
   "rank_biserial": 0.0,
   "holm_p": 1.0,
   "G5_pass": false
  }
 ],
 "E7_H5_decomposition": {
  "cabral_test": {
   "n_projects": 5,
   "median_gap_auc": 0.063,
   "median_recovery": {
    "oracle_old_H180": 0.0661,
    "oracle_old_H30": 0.3121,
    "oracle_young_H180": 0.9412,
    "oracle_young_H30": 0.7753
   },
   "mean_recovery": {
    "oracle_old_H180": 0.0769,
    "oracle_old_H30": 0.3117,
    "oracle_young_H180": 0.9519,
    "oracle_young_H30": 0.801
   },
   "H5_young30_ge_0.5": true,
   "H5_old180_le_0.2": true,
   "projects_young30_ge_0.5": 4,
   "projects_old180_le_0.2": 4,
   "young30_minus_old180_auc": {
    "mean": 0.0596,
    "ci95": [
     0.0441,
     0.0772
    ],
    "wins": 4,
    "n": 4,
    "wilcoxon_p": null
   },
   "H5_supported": true
  },
  "apachejit": {
   "n_projects": 8,
   "median_gap_auc": 0.0835,
   "median_recovery": {
    "oracle_old_H180": 0.1015,
    "oracle_old_H30": 0.5973,
    "oracle_young_H180": 0.7752,
    "oracle_young_H30": 0.3338
   },
   "mean_recovery": {
    "oracle_old_H180": 0.183,
    "oracle_old_H30": 0.6382,
    "oracle_young_H180": 0.6866,
    "oracle_young_H30": 0.2897
   },
   "H5_young30_ge_0.5": false,
   "H5_old180_le_0.2": true,
   "projects_young30_ge_0.5": 1,
   "projects_old180_le_0.2": 5,
   "young30_minus_old180_auc": {
    "mean": 0.0046,
    "ci95": [
     -0.0234,
     0.0294
    ],
    "wins": 5,
    "n": 8,
    "wilcoxon_p": 0.7421875
   },
   "H5_supported": false
  }
 },
 "n_variants_logged": 76
}
```

Compute used: 18.77 CPU-h (summed worker seconds). Variants logged: 76.
