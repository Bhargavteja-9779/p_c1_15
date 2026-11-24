# RESULTS SUMMARY (auto-generated 2026-11-24T13:21:27+00:00 by scripts/final_report.py)

Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.

Frozen config: `{"frozen": "2026-11-24T13:19:55+00:00", "plan": "plan_v2", "candidate": "awt_e0.4", "candidate_dev_mean": 0.6968, "best_baseline_dev_mean": 0.7239, "candidate_beats_baseline_on_dev": false, "n_candidates_tried_on_dev": 8, "wait_W": 90, "orb_W": 90, "best_baseline_on_dev": "orb_W90", "dev_means": {"oracle": 0.7938, "orb_W90": 0.7239, "orb_W60": 0.7116, "wait_W90": 0.7095, "awt_e0.4": 0.6968, "awt_e0.3": 0.6937, "orb_W180": 0.6901, "wait_W60": 0.686, "wait_W180": 0.6831, "awt_e0.2": 0.6662, "law_lagakos_base": 0.6643, "awt_e0.5": 0.6643, "law_naive_base": 0.6637, "orb_W30": 0.6636, "wait_W30": 0.6206, "law_lagakos_model": 0.6128, "orb_W15": 0.6065, "law_naive_model": 0.58, "wait_W15": 0.5457, "nowait": 0.3855}, "proposed_plan_v1": "law_lagakos_model (pre-specified in plan_v1; kept in E1 as pre-registered)", "n_e0_runs": 240}`

Jobs: {'done': 293, 'pending': 942, 'running': 3}

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

| variant   |   brackets |   MEAN |
|:----------|-----------:|-------:|
| awt_e0.4  |      0.721 |  0.721 |

## Statistics

```json
{
 "generated": "2026-11-24T13:21:26+00:00",
 "E1_H1_family_law_and_candidate_vs_baselines": [],
 "n_variants_logged": 28
}
```

Compute used: 5.41 CPU-h (summed worker seconds). Variants logged: 28.
