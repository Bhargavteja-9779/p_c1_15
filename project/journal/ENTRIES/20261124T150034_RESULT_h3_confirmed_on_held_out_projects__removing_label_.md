# RESULT: H3 confirmed on held-out projects: removing label noise alone beats the oracle-gap and the best waiting rule on 10/10 projects

*Written 2026-11-24T15:00:34+00:00*

E3b (pre-registered in plan_v3 before any test run), 10 test projects x SEEDS_CONFIRM: wait_W30 0.620 -> decomp_L1_W30 (same training examples, true labels) 0.722; oracle 0.715. Share of the oracle - wait_W30 gap recovered: 1.08 (per project 0.85-1.36). decomp_L1_W30 vs wait_W90: +0.068 (95% CI 0.049..0.092), 10 wins / 0 losses, Holm p 0.0039; vs wait_W30: +0.102 (CI 0.069..0.141), 10/0, Holm p 0.0039. At W=90 denoising recovers 50% of its (smaller) gap. Adding young unfound bugs without their clean neighbours hurts (L2 < L1 at both W).
Meaning: on these 14 projects the verification-latency penalty of a short waiting time is essentially all label noise from old, still-undiscovered bugs; excluding young negatives costs nothing (slightly helps: L1_W30 >= oracle). This contradicts the common framing of W as a noise-versus-staleness trade-off in which short W mainly costs 'missing' information.
