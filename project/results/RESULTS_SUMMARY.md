# RESULTS SUMMARY (auto-generated 2026-11-25T07:56:29+00:00 by scripts/final_report.py)

Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.

Frozen config: `{"frozen": "2026-11-25T07:54:45+00:00", "plan": "plan_v3", "proposed": {"variant": "law_lagakos_model_gmax_lat", "method": "law", "delay_est": "lagakos", "prior": "model", "thr_policy": "gmax_lat"}, "baselines": [{"variant": "nowait", "method": "nowait"}, {"variant": "wait_W90", "method": "wait", "W": 90}, {"variant": "orb_W90", "method": "orb", "W": 90}, {"variant": "odasc_W30", "method": "odasc", "W": 30, "odasc_delta": 0.9}, {"variant": "wait_W30_gmax_lat", "method": "wait", "W": 30, "thr_policy": "gmax_lat"}, {"variant": "odasc_W15_gmax_lat", "method": "odasc", "W": 15, "odasc_delta": 0.9, "thr_policy": "gmax_lat"}], "oracle": {"variant": "oracle", "method": "oracle"}, "primary_comparator": "odasc_W30", "n_dev_variants": 44, "n_dev_runs": 528, "dev_means": {"oracle": 0.7938, "law_lagakos_model_gmax_lat": 0.7632, "law_naive_model_gmax_lat": 0.7611, "odasc_W30": 0.7497, "odasc_W15_gmax_lat": 0.7491, "odasc_W30_gmax_lat": 0.7489, "law_naive_base_gmax_lat": 0.7475, "law_lagakos_base_gmax_lat": 0.7474, "odasc_W15": 0.7466, "wait_W30_gmax_lat": 0.7437, "odasc_W60_gmax_lat": 0.7424, "wait_W60_gmax_lat": 0.7392, "wait_W15_gmax_lat": 0.7389, "odasc_W60": 0.7367, "wait_W90_gmax_lat": 0.7367, "odasc_W90_gmax_lat": 0.7339, "wait_W180_gmax_lat": 0.7317, "orb_W180_gmax_lat": 0.7288, "orb_W90": 0.7239, "odasc_W180_gmax_lat": 0.7229, "orb_W90_gmax_lat": 0.7178, "odasc_W90": 0.7167, "orb_W60": 0.7116, "orb_W60_gmax_lat": 0.7097, "wait_W90": 0.7095, "orb_W180": 0.6901, "nowait_gmax_lat": 0.6881, "wait_W60": 0.686, "orb_W30_gmax_lat": 0.6832, "wait_W180": 0.6831, "law_lagakos_base_ratematch": 0.6784, "law_naive_base_ratematch": 0.6764, "law_lagakos_base": 0.6643, "law_naive_base": 0.6637, "orb_W30": 0.6636, "odasc_W180": 0.6564, "orb_W15_gmax_lat": 0.6463, "nowait_ratematch": 0.6327, "wait_W30": 0.6206, "law_lagakos_model": 0.6128, "orb_W15": 0.6065, "law_naive_model": 0.58, "wait_W15": 0.5457, "nowait": 0.3855}}`

Jobs: {'done': 528, 'running': 3, 'pending': 797}

## G-mean by project (mean over seeds)

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

## Statistics

```json
{
 "generated": "2026-11-25T07:56:28+00:00",
 "n_variants_logged": 51
}
```

Compute used: 10.09 CPU-h (summed worker seconds). Variants logged: 51.
