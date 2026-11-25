#!/usr/bin/env python3
"""Download the Cabral et al. ICSE'19 artifact from Zenodo and extract the 14 ARFF datasets to data/jit/. Idempotent."""
import os, sys, zipfile, urllib.request, hashlib, io
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dst = os.path.join(ROOT, "data", "jit"); os.makedirs(dst, exist_ok=True)
if len([f for f in os.listdir(dst) if f.endswith(".arff")]) >= 14:
    print("data present"); sys.exit(0)
url = "https://zenodo.org/api/records/2591761/files/geocabral/spdisc-icse19-V1.02.zip/content"
raw = urllib.request.urlopen(url, timeout=300).read()
print("sha256", hashlib.sha256(raw).hexdigest())
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    for n in z.namelist():
        if "/datasets/" in n and n.endswith(".arff"):
            open(os.path.join(dst, os.path.basename(n)), "wb").write(z.read(n))
        if n.endswith("License.txt"):
            open(os.path.join(dst, "License.txt"), "wb").write(z.read(n))
print("extracted to", dst)
