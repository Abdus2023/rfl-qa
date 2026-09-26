# RFL-QA — Rust-for-Linux Engineering Qualification & Measurement

> Deterministic measurement and qualification system for Rust-for-Linux engineering capability.

RFL-QA is an executable, evidence-first system for measuring Rust-for-Linux engineering capability. It separates demonstrated capability, evidence strength, invariant classification, epistemic status, qualification scope, and long-term calibration. The system uses machine-readable schemas, behavioral rubrics, explicit test oracles, deterministic derivation, dual-assessor calibration, and downstream outcome records to prevent unsupported capability claims and self-validating certification.

## Why

Capability claims about kernel engineering are easy to make and hard to check. RFL-QA is designed against two specific failure modes:

- **Unsupported capability claims** — a level or label is asserted without evidence that would let anyone else reproduce the judgment.
- **Self-validating certification** — the process that produces a claim is also the only thing that checks it, so it can never be found wrong on its own terms.

Every qualification statement produced by RFL-QA is meant to be traceable to recorded evidence, derived by a fixed procedure, checked by more than one assessor, and tested afterwards against real outcomes.

## What the system keeps separate

RFL-QA deliberately does not collapse the following into a single score or title:

| Dimension | Question it answers |
| --- | --- |
| **Demonstrated capability** | What has actually been done, under known conditions? |
| **Evidence strength** | How direct, complete, and reproducible is the evidence behind each observation? |
| **Invariant classification** | Which kernel and Rust invariants (safety, soundness, ordering, lifetime, locking) does the evidence exercise? |
| **Epistemic status** | Is a claim observed, inferred, self-reported, or unknown? |
| **Qualification scope** | For which subsystems, task types, and risk levels is a qualification valid — and where is it silent? |
| **Long-term calibration** | Do qualifications predict downstream outcomes over time, and how are they corrected when they don't? |

## Mechanisms

| Mechanism | Role |
| --- | --- |
| **Machine-readable schemas** | Every artifact — evidence item, assessment, qualification, outcome record — has a fixed, validatable shape. |
| **Behavioral rubrics** | Criteria are stated as observable behaviors rather than adjectives, so independent assessors read the same thing. |
| **Explicit test oracles** | Each exercise defines up front what counts as pass, fail, or inconclusive. |
| **Deterministic derivation** | Qualification is computed from recorded evidence by a fixed procedure: same inputs, same output, no hidden judgment. |
| **Dual-assessor calibration** | Independent assessments are compared; disagreement is measured and fed back into rubrics and oracles. |
| **Downstream outcome records** | What happens after qualification — review results, regressions, incidents — is recorded and used to check the system against reality. |

## Focus areas

The areas of Rust-for-Linux work where the cost of being wrong is highest:

- Safety boundaries and `unsafe` justification
- FFI and C bindings
- Concurrency, locking, and memory ordering
- RCU

## Status

Early stage. This repository currently establishes the project's purpose and scope; schemas, rubrics, oracles, derivation tooling, and calibration records will be added incrementally.

## Topics

`rust-for-linux` · `rust` · `linux-kernel` · `kernel-development` · `engineering-assessment` · `qualification` · `verification` · `calibration` · `safety` · `ffi` · `concurrency` · `rcu`
