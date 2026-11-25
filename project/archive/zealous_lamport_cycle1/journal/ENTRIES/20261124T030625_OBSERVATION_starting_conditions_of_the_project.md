# OBSERVATION: Starting conditions of the project

*Written 2026-11-24T03:06:25+00:00*

I am starting from an empty repository. The machine has 4 CPU cores, 15 GB RAM and no GPU (no nvidia-smi; torch reports no CUDA). The container is ephemeral, so git is my only durable memory. This means every experiment I design must be feasible on CPU within the 15 h per-cycle budget, which rules out most deep-learning-at-scale topics before I even look at journals.
