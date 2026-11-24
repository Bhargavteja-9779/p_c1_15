# OBSERVATION: The PU-learning paper I feared does not seem to exist

*Written 2026-11-24T23:02:09+00:00*

I spent the first part of this session looking for Liu et al. 2024a, "Positive and unlabeled learning for just-in-time defect prediction", which MSTDP (JKSU-CIS 2026) cites as Empir Softw Eng 29(5):98. Eight searches in Crossref and OpenAlex, including a listing of 159 EMSE articles from March-December 2024, found nothing. Article 98 in EMSE volume 29 is an unrelated paper about machine-learning asset management. I mark the reference UNVERIFIED and will not cite or rely on it. ODaSC remains the closest real prior work, so I added an ODaSC-style baseline (its label-confidence rule on our shared LightGBM learner) with the same five-configuration budget as Wait and ORB. A quick check on the first 4000 fabric commits gave ODaSC-style G-mean 0.699 vs Wait-60 0.641, so it is a serious competitor, not a straw man.
