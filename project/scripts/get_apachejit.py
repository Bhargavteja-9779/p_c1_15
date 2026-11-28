#!/usr/bin/env python3
"""Download ApacheJIT (Keshavarz & Nagappan, MSR 2022; Zenodo 5907847) and extract to data/apachejit_raw/. Idempotent.
Verifies the sha256 recorded in literature/data_sha256.txt."""
import os, sys, zipfile, urllib.request, hashlib, io
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dst = os.path.join(ROOT, "data", "apachejit_raw")
if os.path.exists(os.path.join(dst, "apachejit", "dataset", "apachejit_total.csv")):
    print("data present"); sys.exit(0)
SHA = "533e7c6fc4f7cb6f34b35539a972d00baa63a125e88ddb5743283dd277edcd5c"
url = "https://zenodo.org/api/records/5907847/files/apachejit_dataset_replication.zip/content"
raw = urllib.request.urlopen(url, timeout=600).read()
h = hashlib.sha256(raw).hexdigest(); print("sha256", h)
if h != SHA: sys.exit("sha256 mismatch: the Zenodo file differs from the one used in the study")
os.makedirs(dst, exist_ok=True)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    for n in z.namelist():
        if n.startswith("apachejit/dataset/") or n.startswith("apachejit/data/commit_links_") or n == "apachejit/readme.md":
            z.extract(n, dst)
print("extracted to", dst)
