#!/usr/bin/env python3
"""Download the Cabral et al. ICSE'19 artifact from Zenodo and extract the 14 ARFF datasets to data/jit/. Idempotent."""
import os, sys, zipfile, urllib.request, hashlib, io
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dst = os.path.join(ROOT, "data", "jit"); os.makedirs(dst, exist_ok=True)
def get_cabral():
  import json
  ref = json.load(open(os.path.join(ROOT, "scripts", "cabral_sha256.json")))
  if len([f for f in os.listdir(dst) if f.endswith(".arff")]) >= 14:
    for n, hx in ref["arff_sha256"].items():   # verify the extracted files, not just their presence
      assert hashlib.sha256(open(os.path.join(dst, n), "rb").read()).hexdigest() == hx, f"checksum mismatch: {n}"
    print("cabral data present, 14 ARFF checksums verified"); return
  url = "https://zenodo.org/api/records/2591761/files/geocabral/spdisc-icse19-V1.02.zip/content"
  raw = urllib.request.urlopen(url, timeout=300).read()
  hx = hashlib.sha256(raw).hexdigest(); print("sha256", hx)
  assert hx == ref["zip_sha256"], "Cabral archive checksum mismatch"
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
      for n in z.namelist():
          if "/datasets/" in n and n.endswith(".arff"):
              open(os.path.join(dst, os.path.basename(n)), "wb").write(z.read(n))
          if n.endswith("License.txt"):
              open(os.path.join(dst, "License.txt"), "wb").write(z.read(n))
  print("extracted to", dst)

# ---- ApacheJIT (fresh confirmation benchmark, plan_v7): Zenodo 5907847, CC-BY-4.0
def get_apachejit():
    import urllib.request, zipfile, hashlib, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "apachejit_raw"); os.makedirs(d, exist_ok=True)
    z = os.path.join(d, "apachejit.zip")
    if not os.path.exists(z):
        urllib.request.urlretrieve("https://zenodo.org/api/records/5907847/files/apachejit_dataset_replication.zip/content", z)
    h = hashlib.sha256(open(z, "rb").read()).hexdigest()
    assert h == "533e7c6fc4f7cb6f34b35539a972d00baa63a125e88ddb5743283dd277edcd5c", h
    with zipfile.ZipFile(z) as f:
        f.extractall(d, [m for m in f.namelist() if m.startswith(("apachejit/data/", "apachejit/dataset/"))])
    print("apachejit sha256", h, "extracted to", d)

if __name__ == "__main__":
    get_cabral(); get_apachejit()   # both idempotent
