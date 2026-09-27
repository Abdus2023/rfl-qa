# LAB-002 — RCU grace periods

This is an executable **measurement fixture**, not an executed kernel lab or a real candidate submission.

Read `task.yaml`, evaluate the supplied baseline schedule, then submit the required outputs. `oracle.yaml` defines each input, expected condition and failure condition. `expected-observations.yaml` is the assessor training key, not execution evidence. Real assessments must be completed independently before viewing the key.

The fixture uses a fictional artifact URI (`fixture://`), never a claimed upstream commit or real sanitizer log. Replace with verifiable artifacts for a live assessment. No C allocator, Pin, RCU, or refcount primitive alone establishes a complete soundness proof. Dynamic context restrictions not encoded by a specific API require runtime/contract evidence.

Run from repository root:

```bash
python tools/derive.py dossiers/examples/002-rcu.json
pytest -q
```

The callback oracle covers all five frozen interleavings, with explicit drain predicates. A compiler lifetime result is limited to its sound-API assumptions. Layout is not generically a compiler safety proof: representation and C ABI compatibility require their own contracts.

No human reliability or criterion-validity claim follows from these fixture runs.
