# RESULT: Harm per label is concentrated in recent commits, but older ones matter jointly

*Written 2026-11-28T09:00:00+00:00*

plan_v9 (committed before the runs): B1 is the W=90 age strata, B2 the false-clean counts per band, B3 leave-one-band-out at W=30 and W=90. Inputs: results/review1/raw.jsonl and flip_counts.json. Output: paper/tables/T12_age_bands_W90_and_leave_one_out.md.

**False-clean labels are spread over all ages.** Each band holds about 0.2–0.34 of them. The A3 localisation was therefore not an artefact of where the false-clean labels sit.

**The youngest waited-out band does 2–3× its share of the harm.** Leave-out AUC shares, with the band's share of false-clean labels in brackets:

| | Cabral | ApacheJIT |
|:--|:--|:--|
| W=30 | 0.775 (0.309) | 0.729 (0.341) |
| W=90 | 0.540 (0.196) | 0.497 (0.216) |

**Older bands: R1 (round 2) was right that "adds nothing" was too strong.**
- On Cabral at W=30 they matter little even jointly (0.091 / 0.038 / 0.019).
- On ApacheJIT they matter jointly but not alone: band-in shares are slightly negative, while leave-out costs 0.12–0.18 each.
- At W=90 they matter more on both families.

**Manuscript change.** "Harm is in commits 30–180 d old; older add nothing" becomes "per false-clean label the most recent waited-out commits do the most harm; older labels matter less, mainly jointly".
