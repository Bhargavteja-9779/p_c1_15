# HYPOTHESIS: H9, and completing H5 on all confirmation seeds

*Written 2026-11-28T16:54:49+00:00*

Written before looking at E7. The method is a tie on both benchmarks, so what is left is what I learned about latency itself. Two candidate findings: (a) the ranking cost of latency sits in the newest labels (H5, D1 on dev), and (b) the decision threshold matters more than the label policy (seen on dev and on Cabral-test). For (b) I pre-register H9 on ApacheJIT with five variants never run there: the latency-corrected threshold raises G-mean for nowait, wait-W90, ORB-W90 and ODaSC-W30 (Holm over 4), and the spread between thresholded label policies is smaller than the threshold gain. I have already seen ApacheJIT means for three thresholded policies (LAW, ODaSC-W15, Wait-W30), so H9b is not fully blind; I say so here.
