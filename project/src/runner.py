"""Layer A: detached, resumable job-queue runner (no LLM needed).

Queue file: state/queue.json  {"jobs":[{id,kind,params,status,attempts,cycle,priority,...}]}
status in: pending | running | done | failed | failed_permanent | skipped_budget
"""
import json, os, sys, time, threading, traceback, random, importlib, csv
from pathlib import Path
from .state import (ROOT, STATE, read_json, write_json, now_iso, FileLock,
                    touch_heartbeat, atomic_write_text)

MAX_ATTEMPTS = 3          # 1 try + 2 retries
RESULTS = ROOT / "results"
CKPT = ROOT / "checkpoints"

def _queue_path(mode):
    return STATE / ("queue.json" if mode == "full" else "queue_quick.json")

def load_queue(mode):
    return read_json(_queue_path(mode), {"jobs": []})

def qlock(mode):
    return FileLock(STATE / f"queue_{mode}.qlock", blocking=True)

def save_queue(mode, q):
    write_json(_queue_path(mode), q)

class Budget:
    """Counts actual compute seconds; persisted every 60 s; summed across restarts."""
    def __init__(self, cycle, enabled=True):
        self.cycle = str(cycle); self.enabled = enabled
        self.lock = threading.Lock(); self.pending = 0.0; self.last = None
    def _b(self):
        return read_json(STATE / "budget.json", {"global_seconds": 0, "per_cycle_seconds": {},
                                                 "cycle_budget_s": 54000, "global_budget_s": 432000})
    def start(self):
        with self.lock: self.last = time.time()
    def stop(self):
        with self.lock:
            if self.last is not None:
                self.pending += time.time() - self.last; self.last = None
        self.flush()
    def flush(self):
        if not self.enabled: return
        with self.lock:
            if self.last is not None:
                t = time.time(); self.pending += t - self.last; self.last = t
            add, self.pending = self.pending, 0.0
        if add <= 0: return
        b = self._b()
        b["global_seconds"] = b.get("global_seconds", 0) + add
        pc = b.setdefault("per_cycle_seconds", {})
        pc[self.cycle] = pc.get(self.cycle, 0) + add
        b["updated"] = now_iso()
        write_json(STATE / "budget.json", b)
    def exhausted(self):
        b = self._b()
        cyc = b.get("per_cycle_seconds", {}).get(self.cycle, 0) + self.pending
        return (cyc >= b.get("cycle_budget_s", 54000) or
                b.get("global_seconds", 0) + self.pending >= b.get("global_budget_s", 432000))

class Ctx:
    """Handed to every job function."""
    def __init__(self, job, mode):
        self.job = job; self.mode = mode; self.quick = (mode == "quick")
        self.ckpt_dir = CKPT / job["id"]; self.ckpt_dir.mkdir(parents=True, exist_ok=True)
        self.res_dir = RESULTS / ("quick" if self.quick else "")
        self.res_dir.mkdir(parents=True, exist_ok=True)
        self._last_ckpt = time.time()
    def heartbeat(self, msg=""):
        touch_heartbeat(f"{self.job['id']} {msg}")
    def should_checkpoint(self, every_s=600):
        return time.time() - self._last_ckpt >= every_s
    def save_ckpt(self, obj, tag):
        import torch
        tmp = self.ckpt_dir / f".tmp_{tag}.pt"; dst = self.ckpt_dir / f"ckpt_{tag}.pt"
        torch.save(obj, tmp); os.replace(tmp, dst); self._last_ckpt = time.time()
        cks = sorted(self.ckpt_dir.glob("ckpt_*.pt"), key=lambda p: p.stat().st_mtime)
        for p in cks[:-2]: p.unlink(missing_ok=True)       # keep last 2
    def load_ckpt(self):
        import torch
        cks = sorted(self.ckpt_dir.glob("ckpt_*.pt"), key=lambda p: p.stat().st_mtime)
        for p in reversed(cks):
            try: return torch.load(p, weights_only=False)
            except Exception: continue
        return None
    def write_result(self, rows):
        """rows: list of flat dicts. Appended to raw_results.csv + <job_id>.json immediately."""
        if isinstance(rows, dict): rows = [rows]
        for r in rows:
            r.setdefault("job_id", self.job["id"]); r.setdefault("written", now_iso())
            r.setdefault("cycle", self.job.get("cycle"))
        jp = self.res_dir / f"{self.job['id']}.json"
        prev = read_json(jp, [])
        write_json(jp, prev + rows)
        csvp = self.res_dir / "raw_results.csv"
        lines = [json.dumps(r, default=str) for r in rows]
        with open(self.res_dir / "raw_results.jsonl", "a") as f:
            f.write("\n".join(lines) + "\n")
        # csv with union of keys is awkward to append; jsonl is the canonical raw store,
        # raw_results.csv is regenerated from jsonl by scripts/final_report.py.

def _worker_alive(mode, w):
    """True if worker w currently holds its runner lock (i.e. is alive)."""
    if w is None: return False
    try:
        with FileLock(STATE / f"run_{mode}_w{w}.lock"):
            return False
    except BlockingIOError:
        return True

def _heartbeat_thread(stop_evt, budget, ctx_holder):
    n = 0
    while not stop_evt.wait(30):
        j = ctx_holder.get("job")
        touch_heartbeat(f"runner {j or 'idle'}")
        n += 1
        if n % 2 == 0: budget.flush()

def run(mode="full", resume=True, only_kind=None, max_jobs=None, worker=0):
    from . import jobs as job_registry
    lock = FileLock(STATE / f"run_{mode}_w{worker}.lock")
    try:
        lock.__enter__()
    except BlockingIOError:
        print(f"[runner] another {mode} runner holds the lock; exiting (no-op)."); return 0
    try:
        st = read_json(STATE / "agent_state.json", {})
        cycle = st.get("cycle", 1)
        budget = Budget(cycle, enabled=(mode == "full"))
        holder = {}; stop_evt = threading.Event()
        th = threading.Thread(target=_heartbeat_thread, args=(stop_evt, budget, holder), daemon=True); th.start()
        with qlock(mode):
            q = load_queue(mode)
            # resume: jobs left "running" by a dead worker -- or by a previous incarnation of THIS worker id -- go back to pending
            for j in q["jobs"]:
                if j["status"] == "running" and (j.get("worker") == worker or not _worker_alive(mode, j.get("worker"))):
                    j["status"] = "pending"; j.setdefault("log", []).append(f"{now_iso()} reset running->pending on restart")
            save_queue(mode, q)
        done_count = 0
        while True:
            job = None
            with qlock(mode):
                q = load_queue(mode)
                for j in q["jobs"]:
                    if j["status"] == "failed" and j.get("attempts", 0) >= MAX_ATTEMPTS:
                        j["status"] = "failed_permanent"
                cands = [j for j in q["jobs"] if j["status"] in ("pending", "failed")
                         and j.get("attempts", 0) < MAX_ATTEMPTS and (only_kind is None or j["kind"] == only_kind)]
                if not cands:
                    save_queue(mode, q); print("[runner] queue empty.")
                elif mode == "full" and budget.exhausted():
                    for j in cands: j["status"] = "skipped_budget"
                    save_queue(mode, q); print("[runner] budget exhausted; remaining jobs skipped_budget.")
                else:
                    cands.sort(key=lambda j: (j.get("priority", 50), j["id"]))
                    job = cands[0]
                    job["status"] = "running"; job["attempts"] = job.get("attempts", 0) + 1
                    job["started"] = now_iso(); job["worker"] = worker
                    save_queue(mode, q)
            if job is None:
                break
            holder["job"] = job["id"]; ctx = Ctx(job, mode)
            print(f"[runner] {now_iso()} w{worker} start {job['id']} (attempt {job['attempts']})", flush=True)
            budget.start(); t0 = time.time(); status, err = "done", None
            try:
                fn = getattr(job_registry, job["kind"])
                fn(dict(job["params"], quick=(mode == "quick")), ctx)
            except Exception as e:
                status = "failed"; err = "".join(traceback.format_exception(e))[-3000:]
                print(err, flush=True)
            budget.stop(); holder["job"] = None
            with qlock(mode):
                q = load_queue(mode)
                for j in q["jobs"]:
                    if j["id"] == job["id"]:
                        j["status"] = status; j["finished"] = now_iso(); j["seconds"] = round(time.time() - t0, 1)
                        if err: j.setdefault("errors", []).append(err[-800:])
                        if status == "failed" and j["attempts"] >= MAX_ATTEMPTS: j["status"] = "failed_permanent"
                save_queue(mode, q)
            print(f"[runner] {now_iso()} w{worker} {status} {job['id']} in {time.time()-t0:.1f}s", flush=True)
            done_count += 1
            if max_jobs and done_count >= max_jobs: break
        stop_evt.set(); budget.flush()
        return 0
    finally:
        lock.__exit__()
