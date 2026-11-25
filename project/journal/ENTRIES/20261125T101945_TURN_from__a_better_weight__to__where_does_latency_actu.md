# TURN: From "a better weight" to "where does latency actually cost us"

*Written 2026-11-25T10:19:45+00:00*

Instead of tuning another weighting scheme on the same 10 (now used) test projects, cycle 2 will (1) decompose the cost of verification latency into an operating-point part and a ranking part, using the oracle as reference, and (2) attack the ranking part, which is where the headroom is (about 0.05 AUC). Any new method will be developed on dev projects only and confirmed on a FRESH set of projects that no session has touched, with every variant counted in variants_tried.csv. The 10 Cabral test projects are now considered used for model selection purposes.
