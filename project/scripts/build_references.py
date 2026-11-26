#!/usr/bin/env python3
"""Build the manuscript reference list from Crossref metadata (paper/crossref_cache.json; fetched on a miss).
Writes paper/references.md (Springer basic style) and paper/references_checked.json, and checks that every
in-text citation key in paper/manuscript.md has exactly one reference and vice versa. Exit 1 on any mismatch."""
import json, os, re, sys, time, urllib.request
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CACHE = os.path.join(ROOT, "paper", "crossref_cache.json")
DOIS = [
    "10.1109/MSR.2019.00019", "10.1007/s10994-020-05877-5", "10.1007/s11219-026-09796-x", "10.1109/ICSE.2019.00076",
    "10.1109/TSE.2022.3175789", "10.1007/s10664-023-10335-6", "10.1145/2623330.2623634", "10.1145/2597073.2597108",
    "10.1145/3485447.3511965", "10.1145/1401890.1401920", "10.1145/3467895", "10.1109/TSE.2019.2929761",
    "10.1007/s10618-019-00654-y", "10.1145/3637226", "10.1080/02664763.2024.2319222", "10.1080/01621459.1989.10478780",
    "10.1109/TSE.2012.70", "10.1145/3524842.3527996", "10.1093/biomet/75.3.515", "10.1007/s44443-025-00401-y",
    "10.1613/jair.1.12125", "10.1109/ICSE43902.2021.00049", "10.1007/s10664-024-10514-z", "10.1109/IJCNN55064.2022.9891911",
    "10.1007/s10664-023-10341-8", "10.1145/3611643.3616307", "10.1109/TSE.2022.3150153", "10.1145/3779653",
    "10.1609/aaai.v35i5.16587", "10.1145/3366423.3380032", "10.1145/3534678.3539372",
    # added in revision 1 (reviewer R2 suggestions, each opened and DOI-checked)
    "10.1109/TSE.2022.3158831", "10.1109/ICSE.2015.139", "10.1145/1985793.1985859", "10.1109/ICSE.2015.93",
    "10.1109/TSE.2022.3156787", "10.1007/s10664-021-10092-4", "10.1145/3433928", "10.1109/TSE.2017.2693980",
    "10.1007/s10664-020-09868-x", "10.1109/ICDMW.2010.49", "10.1109/ICMLA.2015.174", "10.1109/BigData.2016.7840877",
    "10.1145/3523055",
]
# Crossref name-field errors corrected by hand (checked against the publisher pages)
NAME_FIX = {("10.1145/3467895", 2): ("Di Penta", "M"), ("10.1093/biomet/75.3.515", 2): ("De Gruttola", "V"),
            ("10.1145/3366423.3380032", 2): ("Fujita", "K")}
# year suffixes for same-first-author-same-year pairs
SUFFIX = {"10.1007/s10664-023-10341-8": "a", "10.1145/3611643.3616307": "b"}

def fetch(doi, cache):
    if doi in cache: return cache[doi]
    for k in range(5):
        try:
            req = urllib.request.Request("https://api.crossref.org/works/" + doi, headers={"User-Agent": "reference-check/1.0"})
            cache[doi] = json.load(urllib.request.urlopen(req, timeout=30))["message"]; return cache[doi]
        except Exception: time.sleep(2 ** k)
    raise SystemExit("crossref failed: " + doi)

def initials(given):
    return "".join(p[0] for p in re.split(r"[\s\-\.]+", given or "") if p and p[0].isalpha()).upper()

cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
refs, checked = [], []
for doi in DOIS:
    m = fetch(doi, cache); m = m.get("message", m)
    au = []
    for i, a in enumerate(m.get("author", [])):
        fam, ini = NAME_FIX.get((doi, i), (a.get("family", ""), initials(a.get("given", ""))))
        au.append((fam.title() if fam.isupper() else fam, ini))
    year = (m.get("published-print") or m.get("issued") or m.get("published-online"))["date-parts"][0][0]
    if doi == "10.1109/TSE.2022.3158831": year = 2023
    names = ", ".join(f"{f} {i}" for f, i in au[:6]) + (", et al." if len(au) > 6 else "")
    title = re.sub(r"\s+", " ", m["title"][0]).strip()
    venue = (m.get("container-title") or [""])[0]
    vol, iss, pg = m.get("volume"), m.get("issue"), m.get("page") or m.get("article-number")
    if m.get("type") == "journal-article":
        loc = (f" {vol}" if vol else "") + (f"({iss})" if iss else "") + (f":{pg}" if pg else "")
    else:
        loc = f", pp {pg}" if pg else ""
    sfx = SUFFIX.get(doi, "")
    key = (au[0][0] + (" & " + au[1][0] if len(au) == 2 else " et al." if len(au) > 2 else ""), f"{year}{sfx}")
    refs.append((au[0][0].lower(), year, sfx, f"{names} ({year}{sfx}) {title}{'' if title[-1] in '?!' else '.'} {venue}{loc}. https://doi.org/{doi}", key))
    checked.append(dict(doi=doi, ok=True, authors=key[0], year=year, title=title, venue=venue, vol=vol, issue=iss, pages=pg))
json.dump(cache, open(CACHE, "w"))
refs.sort(key=lambda r: (r[0], r[1], r[2]))
open(os.path.join(ROOT, "paper", "references.md"), "w").write("\n\n".join(r[3] for r in refs) + "\n")
json.dump(checked, open(os.path.join(ROOT, "paper", "references_checked.json"), "w"), indent=1)

# citation cross-check
ms = os.path.join(ROOT, "paper", "manuscript.md")
if os.path.exists(ms):
    body = open(ms).read().split("## References")[0]
    keys = {f"{k[0]} {k[1]}" for *_, k in refs}
    cited = set()
    for k in keys:
        a, y = k.rsplit(" ", 1)
        pats = [re.escape(a) + r"\s*\(?" + re.escape(y), re.escape(a.replace(" & ", " and ")) + r"\s*\(?" + re.escape(y)]
        if any(re.search(p, body) for p in pats): cited.add(k)
    uncited = sorted(keys - cited)
    found = set(re.findall(r"((?:Di |De )?[A-Z][\w\-']+(?: et al\.| & (?:Di |De )?[A-Z][\w\-']+)?),? \(?(\d{4}[ab]?)\b", body))
    surnames = {k.split(" ")[0] for k in keys}
    unknown = sorted({f"{a} {y}" for a, y in found if a.split(" ")[0] in surnames and f"{a} {y}" not in keys})
    print(f"{len(refs)} references; uncited: {uncited}; unresolved 'et al.' citations: {unknown}")
    sys.exit(1 if uncited or unknown else 0)
