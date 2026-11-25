"""Persistent-state helpers. Every write is atomic (tmp file -> os.replace).
All paths are relative to the project root (the folder containing this src/)."""
import json, os, time, datetime, csv, tempfile, fcntl
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

def atomic_write_text(path, text):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp_" + path.name)
    with os.fdopen(fd, "w") as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)

def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)

def write_json(path, obj):
    atomic_write_text(path, json.dumps(obj, indent=2, sort_keys=False, default=str) + "\n")

class FileLock:
    """Advisory lock (fcntl). Use as context manager; raises BlockingIOError if held."""
    def __init__(self, path, blocking=False):
        self.path = Path(path); self.blocking = blocking; self.fh = None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(self.path, "a+")
        fcntl.flock(self.fh, fcntl.LOCK_EX | (0 if self.blocking else fcntl.LOCK_NB))
        self.fh.seek(0); self.fh.truncate(); self.fh.write(f"{os.getpid()} {now_iso()}\n"); self.fh.flush()
        return self
    def __exit__(self, *a):
        fcntl.flock(self.fh, fcntl.LOCK_UN); self.fh.close()

def touch_heartbeat(extra=""):
    atomic_write_text(STATE / "heartbeat", f"{now_iso()} {time.time():.0f} {extra}\n")

def heartbeat_age_s():
    p = STATE / "heartbeat"
    if not p.exists():
        return None
    try:
        return time.time() - float(p.read_text().split()[1])
    except Exception:
        return None

def log_decision(decision, reason):
    with open(STATE / "decisions.md", "a") as f:
        f.write(f"\n- **{now_iso()}** — {decision}\n  - Reason: {reason}\n")

def journal_entry(kind, title, body):
    """Append-only research diary entry (Section 8). Never overwrites."""
    d = ROOT / "journal" / "ENTRIES"; d.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S")
    slug = "".join(c if c.isalnum() else "_" for c in title.lower())[:50]
    p = d / f"{ts}_{kind.upper()}_{slug}.md"
    i = 1
    while p.exists():
        p = d / f"{ts}_{kind.upper()}_{slug}_{i}.md"; i += 1
    p.write_text(f"# {kind.upper()}: {title}\n\n*Written {now_iso()}*\n\n{body.strip()}\n")
    return p

VARIANT_FIELDS = ["timestamp", "cycle", "variant_id", "description", "data_split_used",
                  "metric", "value", "outcome", "notes"]

def log_variant(**kw):
    p = STATE / "variants_tried.csv"
    new = not p.exists()
    with open(p, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=VARIANT_FIELDS)
        if new:
            w.writeheader()
        row = {k: kw.get(k, "") for k in VARIANT_FIELDS}
        row["timestamp"] = row["timestamp"] or now_iso()
        w.writerow(row)

def get_agent_state():
    return read_json(STATE / "agent_state.json", {})

def update_agent_state(**kw):
    s = get_agent_state(); s.update(kw); s["updated"] = now_iso()
    write_json(STATE / "agent_state.json", s); return s
