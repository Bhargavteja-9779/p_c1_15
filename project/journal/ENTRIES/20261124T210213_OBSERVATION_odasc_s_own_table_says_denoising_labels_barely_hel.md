# OBSERVATION: ODaSC's own table says denoising labels barely helps

*Written 2026-11-24T21:02:13+00:00*

Reading the rest of ODaSC (Song et al. IJCNN 2022, Table II): with W=15 days, ODaSC with ORACLE label confidence (ODaSC-opt) and with oracle filtering of noisy examples (ODaSC-flt) have average Friedman ranks 2.00 and 2.07 against 2.43 for ODaSC itself, with no significant difference (p=0.73 and 0.69). Their gain over OOB (rank 4.00) therefore cannot come from correct label confidence; it comes from the resampling change itself. This fits my SURPRISE entry: false-clean labels are not the main thing hurting these learners. It is a warning for LAW, whose whole premise is better label confidence.
