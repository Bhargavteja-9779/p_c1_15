# Archived parallel lineage: claude/zealous-lamport-bjc4um (cycle 1, 2026-11-24/25)

An independent session continued from the same handoff commit (b18fc8e) as keen-edison/zen-cray/magical-bardeen.
Kept for reference and as an independent replication; its compute (15.0 CPU-h) is NOT counted in the main
lineage's state/budget.json.

What it did (all numbers from results/statistics.json and results/raw_results.jsonl in this folder):
- ODaSC-style baseline (kNN label confidence at labelling time), latency-corrected G-mean threshold (gmax_lat),
  528 dev runs / 44 variants; frozen plan_v3: LAW(lagakos, model prior) + gmax_lat.
- E1 on the 10 Cabral test projects x 5 confirm seeds: vs odasc_W30 +0.0009 (CI -0.0086..0.0114, Holm p=1.0, G5 fail);
  vs wait_W90 +0.0417 and orb_W90 +0.0377 (Holm p=0.0195, 9/10 wins).
- Independent agreement with the main lineage: no proposed method beats ODaSC-style; recovering the
  wait->oracle gap is the robust effect. Operating-point diagnosis: results/diag/operating_point_dev.csv.
- Liu et al. 2024a (EMSE 29(5):98, cited by MSTDP) not found anywhere -> treated as non-existent.
