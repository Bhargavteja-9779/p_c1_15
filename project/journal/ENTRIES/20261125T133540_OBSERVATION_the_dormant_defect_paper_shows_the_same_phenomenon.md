# OBSERVATION: The dormant-defect paper shows the same phenomenon at release level

*Written 2026-11-25T13:35:40+00:00*

I read the full text of Falessi, Ahluwalia & Di Penta (TOSEM 2021, arXiv 2105.12372). In release-level defect prediction on 19 Apache projects, classes labelled clean while their defects are still dormant ('snoring') lower recall with a large effect, and dropping the classes labelled clean in the last release raises Recall, F1, Kappa and MCC by about 30%. That is the release-level version of our waiting-time finding, so H3 cannot be presented as a new phenomenon; what is new must be the commit-level, online part (which old dormant bugs carry the cost under a waiting-time rule) and the denoiser that keeps recent data.
