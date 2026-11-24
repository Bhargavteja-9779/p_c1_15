# RESULTS SUMMARY (auto-generated 2026-11-24T21:33:34+00:00 by scripts/final_report.py)

Journal: JKSU-CIS (see journal_selection/selected_journal.md). Topic: topic/selected_topic.md. Plan: experiments/plan_v*.yaml.

Frozen config (plan_v1, superseded): `{}`

Frozen config (plan_v3/v4): `{}`

Jobs: {'done': 153, 'skipped_plan': 192, 'running': 3, 'pending': 468}

## G-mean by project (mean over seeds)

### E0

| variant           |   fabric |   neutron |    nova |   sentry |   MEAN |
|:------------------|---------:|----------:|--------:|---------:|-------:|
| oracle            |    0.75  |     0.866 | nan     |    0.722 |  0.779 |
| orb_W90           |    0.653 |     0.817 | nan     |    0.637 |  0.703 |
| orb_W60           |    0.679 |     0.769 | nan     |    0.649 |  0.699 |
| wait_W90          |    0.638 |     0.784 | nan     |    0.645 |  0.689 |
| wait_W60          |    0.667 |     0.671 | nan     |    0.664 |  0.667 |
| orb_W30           |    0.683 |     0.649 | nan     |    0.666 |  0.666 |
| law_lagakos_base  |    0.673 |     0.682 |   0.619 |    0.683 |  0.664 |
| law_naive_base    |    0.669 |     0.677 |   0.625 |    0.683 |  0.664 |
| orb_W180          |    0.501 |     0.837 | nan     |    0.616 |  0.651 |
| wait_W180         |    0.474 |     0.838 | nan     |    0.614 |  0.642 |
| orb_W15           |    0.668 |     0.546 | nan     |    0.654 |  0.623 |
| law_lagakos_model |    0.668 |     0.496 |   0.614 |    0.673 |  0.613 |
| wait_W30          |    0.66  |     0.48  | nan     |    0.684 |  0.608 |
| law_naive_model   |    0.646 |     0.456 | nan     |    0.664 |  0.589 |
| wait_W15          |    0.597 |     0.369 | nan     |    0.663 |  0.543 |
| nowait            |    0.471 |     0.245 | nan     |    0.531 |  0.416 |

## Statistics

```json
{
 "generated": "2026-11-24T21:33:34+00:00",
 "n_variants_logged": 10
}
```

Compute used: 2.17 CPU-h (summed worker seconds). Variants logged: 10.
