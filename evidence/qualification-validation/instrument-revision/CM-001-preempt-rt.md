# CM-001 Change Analysis — PREEMPT_RT / Execution-Context Semantics

## The defect, precisely

Every oracle's `prohibited_sleep` check states: `expected_condition: no sleep in prohibited context`. No instrument file defines which contexts are "prohibited." The frozen scope selects **PREEMPT_RT=y** — a configuration in which primary sources show the classic mapping inverts: sleeplockified spinlocks **may** be acquired (and block) inside RCU read-side critical sections, and RCU read-side critical sections are preemptible (S2/S3). A context-free gate applied to a context-sensitive configuration produces an ambiguous or wrong competency signal: either a false veto (assessor flags legal-under-RT behavior) or a false pass (candidate's classic-kernel assumption survives review).

## The abstraction question (§6)

"Sleep prohibited" is NOT universally equivalent to "blocking prohibited." The correct primitive is **execution context**, classified per configuration: what blocks differs between classic, PREEMPT=y, and PREEMPT_RT kernels (spinlock type, RCU flavor, BH/workqueue context all shift). The competency should encode **context-sensitive behavior requirements**, not a context-free prohibition.

## Alternatives analysis (mandatory schema)

| Option | Technical basis | Advantages | Failure modes | Schema impact | Rubric impact | Oracle impact | Calibration impact | Version sensitivity | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| A. Status quo (context-free gate) | classic-kernel convention | zero churn | false veto/pass under RT (demonstrated by S2/S3); ambiguity already found by audit | none | assessor must improvise | predicate ill-defined for frozen scope | assessors would disagree → calibration risk | HIGH — wrong for PREEMPT_RT scope | REJECTED |
| B. Context-tagged execution environments | kernel docs classify contexts (atomic/IRQ, RCU flavors, sleepable) | explicit; machine-checkable declarations; matches frozen scope | taxonomy maintenance as kernels evolve | behavior/oracle tasks gain `execution_contexts` field; _schema extended | assessor scores gate per declared context | predicate becomes per-context table | required (material change) | MEDIUM — context set evolves with kernel | **SELECTED (core of CH-1)** |
| C. Configuration-sensitive behavior requirements | same as B + config dimension | most faithful (same context differs across configs) | combinatorial explosion of config × context matrix; alpha scope only needs PREEMPT_RT vs classic distinction | larger: `config_sensitivity` field per behavior | heavier assessor load | per-config predicate variants | higher | MEDIUM | PARTIALLY ADOPTED — config axis recorded as scope metadata in B, not per-behavior matrix |
| D. Explicit PREEMPT_RT semantics separation (special-case override) | minimal delta from status quo | small diff | special-casing hides the general defect; other contexts still undefined | minimal | one override note | one override | lower | LOW | REJECTED — treats symptom |
| E. Split generic vs configuration-specific claims into separate behaviors | cleanest conceptually | strongest construct separation | doubles behavior count; violates smallest-justified-delta; overlaps C034 LKMM depth | large | large | large | high | LOW | REJECTED for this cycle (deferred candidate) |

## Evidence for selection

- S2/S3: PREEMPT_RT permits blocking spinlocks and preemptible RCU read-side critical sections; SRCU permits sleeping locks; classic RCU forbids blocking. sleeping is a **context × configuration** predicate.
- The oracle wording itself ("no sleep **in prohibited context**") already presupposes a context classification — option B completes the instrument's own intent.
- Invariant C01 ("runtime drain/synchronization completes before final release") remains configuration-independent and unaffected — the change refines the sleep gate, not the drain invariant.

## What does NOT change (§4)

Hard-gate veto strength (atomic-context sleep remains forbidden universally); the deadlock/critical-external-assumption gates; C01 drain invariant; E→L separation; all epistemic vocabulary. Sleeping **legally** under RT does not earn capability; it merely removes a false veto.
