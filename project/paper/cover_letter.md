[Date]

To the Editor-in-Chief,
Journal of King Saud University – Computer and Information Sciences

Dear Editor,

We submit the manuscript "Where does verification latency hurt online just-in-time defect prediction? A label-noise decomposition on 23 projects" for consideration as a research article.

Online just-in-time defect prediction is retrained while the labels of recent commits are still unknown; a defect is discovered only when a later fix points back to it. The standard remedy, waiting a fixed number of days before trusting a "clean" label, is usually described as a trade-off between label noise and stale data. Using a pre-registered prequential design on 14 projects of Cabral et al. and a fresh confirmation set of 9 ApacheJIT projects, we show that the penalty is mainly label noise from old, still-undiscovered defects: giving the same waited-out training data its true labels recovers essentially the whole gap to an oracle (10/10 and 9/9 projects, Holm-adjusted p = 0.0039 and 0.0078). We further show why corrections based on commit age cannot recover it, report feature-based denoisers that recover part of it but did not pass our confirmatory test, and show that comparisons of label policies are confounded by the decision threshold.

The study reports negative and mixed results alongside the positive one, fixes all configurations before held-out evaluation, and releases code, frozen plans and a full log of every configuration tried. We believe it is of interest to the journal's readers working on software analytics, data-stream learning and label noise.

The manuscript is original, has not been published, and is not under consideration elsewhere. [Authors: confirm; declare any preprint.] The research was conducted with substantial assistance from an AI research agent, as disclosed in the Declarations. [Authors: complete per the journal's AI policy.]

Sincerely,
[Corresponding author name, affiliation, e-mail — to be completed by the authors]
