# Regression Plan (§14) — specified BEFORE any implementation

Mandatory classes mapped to the existing suite (all currently PASS at 653; none may be weakened) + new competency-specific tests with explicit oracles. Implementation order in Stage B: tests first or alongside the delta (never after).

## Existing protected classes (retain; must keep passing)

| Class | Existing protection |
|---|---|
| E→L separation | tests asserting evidence tier never raises capability (existing suite) |
| Epistemic ceiling | weakest-required-ceiling derivation tests |
| Hard-gate veto | veto-wins-regardless-of-level tests (incl. CS-008-style fixtures in suite) |
| Type-D handling | external-assumption tests (critical_external_assumption cannot be neutralized) |
| Provenance closure | 89 provenance tests (C1–C15, M1–M7, P1–P10) |
| Oracle provenance | asserted-PASS-cannot-derive tests |
| Canonical hashing | semantic-vs-presentation hash identity tests |
| Deterministic derivation | byte-equality multi-process tests |
| Historical evidence immutability | seal verify + phase manifests |
| Schema validation | tools/validate.py --all + schema tests |

## New competency-specific tests (Stage B; each with explicit oracle)

| Test ID | Protects | Test | Oracle (exact pass condition) |
|---|---|---|---|
| RG-CM001-1 | CM-001 context semantics | fixture dossier declaring PREEMPT_RT-sleepable context with a blocking spinlock acquisition inside an RCU read-side section | derivation does NOT trigger prohibited_sleep BLOCK for the declared context; deadlock/critical gates still evaluated; E→L unaffected |
| RG-CM001-2 | CM-001 | same artifact declared under CLASSIC_RCU_READ_SIDE context | prohibited_sleep BLOCKS (classic rule intact) — proves context-dependence is real, not a blanket weakening |
| RG-CM014-1 | CM-014 publication behavior | artifact asserting publication with no synchronization/ownership-transfer statement | OR-PIN-publication fails → CB-053-06 UNSUPPORTED → L4 not supported; no tier/capability inflation |
| RG-CM014-2 | CM-014 positive | artifact with explicit release-publish + acquire-consume + registration ordering | check PASSES; ceiling unchanged otherwise |
| RG-C034B-1 | C034 L1→L2 guidance | calibration-case harness: vocabulary-only CB-034-02 answer | harness scores UNSUPPORTED under alpha.4 guidance (documented in case guidance, engine-external check documented here) |
| RG-C047O-1 | C047 oracle scope | schema/static check | scope_metadata present on all three oracles with not-universal flag; assessed check fields byte-unchanged vs alpha.3 (semantic freeze) |
| RG-L5OBS-1 | L5 observability | dossier with all L4 satisfied + policy artifact | derivation supports ≤L4; L5 marked UNSATISFIED-BY-INFRASTRUCTURE; ceiling epistemics unchanged; no silent L5 grant |
| RG-DUP-1 | double-counting | dossier reusing one ordering artifact for CB-034-03 AND CB-047-03 | derivation flags reuse annotation; second competency does not earn DEMONSTRATED from the same artifact alone |
| RG-GATE-1/2 | veto strength | existing veto fixtures rerun post-delta | every existing hard-gate veto still fires identically (no weakening) |
| RG-HIST-1 | immutability | seal verify + audit-package hash check | all historical evidence byte-identical after implementation |

## Anti-weakening rule (§14)

If any new test cannot pass without changing engine behavior beyond the declared delta, the delta is wrong — STOP and redesign (§24). No existing test may be edited to accommodate the revision.
