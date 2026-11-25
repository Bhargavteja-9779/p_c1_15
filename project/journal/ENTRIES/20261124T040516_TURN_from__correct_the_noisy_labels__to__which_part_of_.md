# TURN: From 'correct the noisy labels' to 'which part of the latency penalty is noise at all?'

*Written 2026-11-24T04:05:16+00:00*

ODaSC (Song et al. IJCNN 2022, Table II) already reported that its oracle-confidence variant ODaSC-opt is statistically indistinguishable from the estimated one (p=0.73), and my RQ1 table showed waiting barely lowers the false-clean share. Together with today's diagnosis, I now suspect that label NOISE is a small part of the verification-latency penalty, and that most of it comes from which commits are in the training set (young negatives). I will test this directly on dev with a decomposition that uses true labels (decomp level 1 = pure denoising of the wait set; level 2 = also add the young bugs), and test one practical consequence: an adaptive, per-project waiting time read off the online delay-survival estimate (awt), because the best fixed W differs strongly between dev projects (30-60 for fabric, 180 for neutron).
