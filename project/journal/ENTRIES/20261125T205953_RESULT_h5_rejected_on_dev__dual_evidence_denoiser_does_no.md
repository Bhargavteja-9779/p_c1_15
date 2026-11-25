# RESULT: H5 rejected on dev: dual-evidence denoiser does not beat lawm or odasc

*Written 2026-11-25T20:59:53+00:00*

E0e (plan_v6, dev projects fabric/neutron/nova/sentry x seeds 0-2, 48 runs; tables/E0e_dev_tuning.csv).
Mean dev G-mean: dual_W30_k50 0.6812 (best dual), dual_W90_k50 0.6368, dual_W30_k20 0.6218, dual_W90_k20 0.5828;
lawm_soft_W30 0.7551; odasc_W30_t0.8 0.7598.
The dual denoiser is competitive on fabric (0.7151 vs odasc 0.7145) and best on neutron (0.8477 vs lawm 0.8370, odasc 0.7790),
but collapses on nova (0.4745 vs 0.80-0.83 for lawm/odasc). Mean over projects is therefore far below both.
H5 (dual beats lawm and odasc on dev) = false. freeze_v6 primary candidate (best dev mean) = odasc_W30_t0.8, i.e. the
re-implemented ODaSC-style baseline, not one of our own methods.
Consequence: plan_v7 E8 (fresh ApacheJIT confirmation) runs exactly as pre-registered (all 3 frozen candidates + baselines);
H6 then tests whether the best dev configuration beats the waiting baselines on fresh data. Our own methods (lawm, dual) are
reported as secondary candidates. The nova collapse of dual is a dev diagnostic target for the next method round (likely
an operating-point / noisy-OR saturation issue; NOT yet verified).
