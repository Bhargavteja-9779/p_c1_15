# Graphical abstract (description for the designer)

Left panel: a commit timeline; recent commits drawn as grey "provisionally clean" dots, some of which turn red (defect discovered) months or years later. A shaded "wait W days" band covers only the youngest commits; red dots 1–6 months to the left of the band are labelled "harmful: defects not yet found (30–180 days old)"; much older red dots are labelled "long-dormant: harmless for the online model".

Right panel: a bar chart with three bars per dataset family (Cabral test, ApacheJIT): Wait-30, Wait-30 with true labels, Oracle (values from Table 3: 0.620 / 0.722 / 0.715 and 0.687 / 0.762 / 0.770). Caption: "True labels on the same training data close the gap: the latency penalty is label noise on commits one to six months old."
