# Graphical abstract (description for the designer)

Left panel: a commit timeline; recent commits drawn as grey "provisionally clean" dots, some of which turn red (defect discovered) months or years later. A shaded "wait W days" band covers only the youngest commits; red dots 1–6 months to the left of the band are labelled "most harmful per label: defects just past the wait, not yet found"; much older red dots are labelled "long-dormant: little effect on their own".

Right panel: a bar chart in AUC (the paper's primary metric for the decomposition) with three bars per dataset family: Wait-30, Wait-30 with true labels, Oracle. Values from `results/review1/shapley.json` (cells_mean): Cabral test 0.745 / 0.802 / 0.815; ApacheJIT 0.783 / 0.856 / 0.862. Caption: "True labels on the same training commits close most of the gap; per label, the most recent waited-out commits do the most harm."
