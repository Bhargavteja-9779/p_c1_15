"""Job registry: every queue job's `kind` is a function name in this module.
Signature: fn(params: dict, ctx: runner.Ctx) -> None (results via ctx.write_result)."""

def smoke(params, ctx):
    """Infrastructure self-test job."""
    import time
    for i in range(3):
        ctx.heartbeat(f"smoke {i}"); time.sleep(0.2)
    ctx.write_result({"kind": "smoke", "ok": True, "seed": params.get("seed", 0)})
