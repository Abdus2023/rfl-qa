# AUD-007/AUD-008 — Workflow Correction & Current-Source CI Verification Receipt

Cycle: post-push workflow correction and current-source CI verification.
Sealed predecessor package: `evidence/aud-007-008/` (unmodified; `seal.py --verify` PASS at this commit).

## 1. What happened this cycle

1. **Discovered the workflow patch was already applied and published by the repository owner.**
   The separated patch file (`/home/user/alpha-gates-manual-update.patch`) did not survive a sandbox
   rehydration. It was **regenerated from durable artifacts** — the surviving working-tree
   `alpha-gates.yml` diffed against the committed blob at `d3abe21` — and verified byte-identical to
   the previously recorded two-hunk patch. Inspection of the remote then showed the owner had already
   committed and pushed exactly that change as **`6b426364`** ("Update release gates script and
   artifact paths", parent `d3abe21`, 1 file, +3/−3). The committed `d3abe21..6b426364` diff was
   verified byte-identical to the recorded patch (blobs `bf1d929..181501d`). No alternative workflow
   change was reconstructed; no new workflow commit was needed; nothing was force-pushed.
2. **Workflow semantic audit** (`workflow-audit.yaml`): the change alters **evidence destination
   only** — same tests, same commands, same gate ordering, same exit behavior, same release-blocking
   logic, `permissions: contents: read` unchanged, `if: always()` upload retained.
3. **Sealed evidence preserved**: `seal.py --verify` PASS at `6b426364` (80 evidence + 98 source
   files; 183 prior evidence files byte-preserved). No sealed file edited; historical SHAs
   (`06053bf`, `c11657d`) inside sealed files were left as recorded.
4. **Local validation at `6b426364`**: `pytest -q` → **653 passed** (564 retained + 89 provenance);
   `tools/validate.py --all` → PASS; provenance suite → **89 passed**; all three canonical
   derive/report pipelines **byte-identical** to sealed outputs (workflow-only change; zero
   qualification-output drift).
5. **Current-source CI observed** (§ below). Software gates PASS; procedural release gate exit 1 —
   the designed BLOCKED outcome; evidence upload succeeded under the **new** artifact name, proving
   the new evidence path executed.
6. **Dispositions reassessed only from actual evidence** (below). Release remains BLOCKED. No tag.

## 2. Publication record

| Item | Value |
|---|---|
| Parent commit | `d3abe21f4c28b70932aba9f3054e1000537fd993` |
| Workflow commit (current source) | `6b426364c594c1040f98f47ba7e8c49d2b2b2a91` |
| Remote SHA | `6b426364c594c1040f98f47ba7e8c49d2b2b2a91` |
| Force push | **false** (fast-forward lineage throughout) |
| Workflow change applied by | repository owner (manual push), as planned |
| Receipt commit | created this cycle on `arena/01a0dfcc-rfl-qa` (SHA recorded in the post-commit publication note) |

## 3. Current-source CI (run at the pushed workflow commit)

**Primary: run `36304213414`** (push event, workflow "Alpha release gates", SHA `6b426364`,
2026-09-27T07:48:00Z → 07:49:56Z, conclusion **failure** — deliberate, see §5).

| Step | Result |
|---|---|
| Install pinned dependencies | PASS |
| Schema and reference gate | PASS |
| Automated gates (`pytest -q`) | PASS |
| CLI derivation and reporting | PASS |
| Full evidence and procedural release gate | **BLOCKED / exit 1 by design** |
| Retain actual execution evidence (upload, `if: always()`) | PASS |

Corroboration: PR run `36304216174`, same SHA, same shape (only the procedural gate failed).
Prior run `36304104832` (at `d3abe21`) recorded as historical predecessor — **not substituted**.
No older run, other branch, or local execution was used as current-source CI evidence.

## 4. Evidence path verification

Artifact API metadata (OBSERVED): **`aud-007-008-execution-evidence`**, id `10925809245`,
107,829 bytes, created 2026-09-27T07:49:54Z, `expired: false`. This artifact name exists only in the
new workflow version, so the upload from **`evidence/aud-007-008/ci-execution/`** executed in CI.
Archive byte-download: **EOF** (Azure blob closed the connection; 0 bytes) →
`content_available: false`, `detailed_contents: UNCONFIRMED`. No content hash claimed; contents
viewable manually in the Actions UI.

## 5. Log availability

`gh run view 36304213414 --log` → **EOF** (same infrastructure behavior as all historical runs).
`logs: available: false, retrieval_error: EOF, detailed_log_claims: UNCONFIRMED`. CI API metadata
(step conclusions) and log content are kept as separate evidence classes; nothing was inferred from
absent logs. What remains established without logs: step-success semantics (pytest exits nonzero on
any failure ⇒ suite green at this SHA). What stays UNCONFIRMED: CI-printed counts, per-case log
lines, in-CI procedural blocking text.

## 6. Finding dispositions (reassessed from actual evidence only)

- **AUD-007 = FIXED_AND_RETESTED** (`verified_fix_claim: true`).
  Basis: local implementation (rules 1.1-alpha.3); regressions 89/89 at this commit (653/653 full);
  adversarial C1–C15 15/15 with both original counterexamples REJECTED and paired controls passing
  (sealed `replay-results.json`; counterexamples reproduced pre-fix in sealed `before.json`);
  determinism (sealed 16+16 processes; fresh canonical outputs byte-identical this cycle); and
  current-source CI support (run `36304213414` at `6b426364`: Automated gates/Schema/CLI steps
  success).
- **AUD-008 = FIXED_AND_RETESTED** (`verified_fix_claim: true`).
  Basis: same structure plus P1–P10 prose-authority cases — unbound prose has no qualification
  authority; bound prose is authoritative only within declared binding/extraction scope.
- Naming crosswalk (current mission naming vs frozen earlier audit naming) is documented in
  `provenance-results.yaml` and the sealed `findings.yaml`; historical artifacts are not relabeled.
- **These dispositions do not close qualification.** They establish that the audited bypasses no
  longer succeed at the current published source under local execution and current-source CI
  software gates.

## 7. Final verification matrix

| Gate | Status | Evidence |
|---|---|---|
| Schema | PASS | CI step success (run 36304213414); local `validate.py --all` exit 0 at `6b426364` |
| Derivation | PASS | CI CLI step success; local 3 pipelines byte-identical to sealed |
| Invariant | PASS | CI Automated gates success (invariant suite within 653); sealed `procedural/invariant.log` |
| Oracle | PASS | CI Automated gates success; sealed `procedural/oracle.log`; asserted-PASS regressions |
| Hard-gate | PASS | CI Automated gates success; sealed `procedural/hard_gate.log`, C13 |
| AUD-007 | FIXED_AND_RETESTED | sealed replay 15/15 + controls; 89 regressions at current SHA; CI run 36304213414 |
| AUD-008 | FIXED_AND_RETESTED | sealed P1–P10 receipts; 89 regressions at current SHA; CI run 36304213414 |
| Calibration | BLOCKED (human NOT_RUN) | no independent dual human calibration executed |
| Reproducibility | PASS | sealed 16+16 processes; fresh canonical byte-identical at `6b426364` |
| CI | PASS (executed; software gates green; procedural exit 1 by design) | run `36304213414` at `6b426364` |
| Kernel execution | NOT_RUN | no kernel/compiler/sanitizer execution |
| Criterion validity | NOT_ESTABLISHED | no longitudinal external outcome evidence |
| Release | BLOCKED | prerequisites absent: human calibration, kernel execution, criterion validity, upstream verification |

## 8. Mandatory distinctions (not conflated)

- CURRENT-SOURCE EXECUTION ≠ MEASUREMENT VALIDITY.
- CI SOFTWARE PASS ≠ RELEASE ELIGIBILITY.
- FIXED_AND_RETESTED (AUD-007/AUD-008) does not establish internal coherence as reliability, nor
  criterion validity, nor authorize release.
- Evidence tiers used here: **EXECUTED** (local commands this cycle), **OBSERVED** (CI/artifact API
  metadata), **DERIVED** (step-success ⇒ suite-green implication), **UNCONFIRMED** (CI log text,
  artifact internal contents), **NOT_RUN** (human calibration, kernel), **NOT_ESTABLISHED**
  (criterion validity). No state was upgraded because another state passed.

## 9. State

- Remote tip / current source: `6b426364c594c1040f98f47ba7e8c49d2b2b2a91`
- Test count: **653 passed** (564 retained + 89 new); new-regression count this cycle: 0 (no test changes permitted or made)
- Determinism: canonical outputs unchanged (byte-identical); sealed 16+16 process experiment retained
- Working tree: clean; sealed evidence untouched
- Tag: **none**; Release: **BLOCKED**; Human calibration: NOT_RUN; Kernel: NOT_RUN; Criterion validity: NOT_ESTABLISHED

## 10. Limitations

- CI logs and artifact bytes were not retrievable from this environment (EOF ×2 each, consistent
  across all historical runs); their contents remain UNCONFIRMED and unclaimed.
- Case-level adversarial receipts bind source `aa71917`; the tree at `6b426364` is byte-identical to
  it except the workflow file (verified by the sealed 98-file source manifest), so they bind the
  current tree by identity — this is a preservation argument, not a re-execution.
- This receipt records software/provenance verification only. It is not a security certification,
  not human calibration, and not measurement validity.
