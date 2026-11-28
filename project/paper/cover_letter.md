[Date]

To the Editor-in-Chief,
Journal of King Saud University – Computer and Information Sciences

Dear Editor,

We submit the manuscript "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects" for consideration as a research article.

Online just-in-time defect prediction is retrained while the labels of recent commits are still unknown: a defect is discovered only when a later fix points back to it. The standard remedy, waiting a fixed number of days before trusting a "clean" label, is usually described as a trade-off between label noise and stale data.

We study this on 14 projects of Cabral et al. and a fresh confirmation set of 9 ApacheJIT projects, using a prequential design and a factorial decomposition. The main findings are:
- Wrong labels and lost freshness interact: the recent commits a wait excludes have the highest false-clean rate and help only when correctly labelled. For a 30-day wait, true labels on the same training commits close 0.81 and 0.92 of the AUC gap to an oracle.
- For the tuned 90-day wait they close 0.44 and 0.78; how the remainder is attributed depends on how the interaction is split.
- False-clean labels are spread over all ages, but when the other age bands are corrected, the commits just past the wait do two to three times their share of the harm.
- Age-only corrections did not beat a 90-day wait at the operating point on Cabral, though the latency-aware weighting ranks better. Neither feature-based denoisers nor a latency-aware decision threshold significantly beat a 90-day wait on fresh data.

The study reports negative and mixed results alongside the positive ones, including a result that did not replicate on fresh data. It discloses every configuration ever run on the reused test set, the use of an AI research agent (including internal review rounds), and releases code, committed plans and a full log of every configuration tried. We believe it is of interest to the journal's readers working on software analytics, data-stream learning and label noise.

The manuscript is original, has not been published, and is not under consideration elsewhere. [Authors: confirm; declare any preprint.] The research was conducted with substantial assistance from an AI research agent, as disclosed in the Declarations. [Authors: complete per the journal's AI policy.]

Sincerely,
[Corresponding author name, affiliation, e-mail — to be completed by the authors]
