# Competency-Model Validity Audit — README

Cycle: adversarial technical-validity audit of competency definitions **C034 (RCU grace periods), C047 (callback teardown), C053 (pin initialization)** — independent of measurement-engine correctness.

**Central question:** are these three constructs technically defensible representations of real Rust-for-Linux engineering competencies, and do their L0–L5 boundaries distinguish meaningful capability increases?

**Maintained identity:** HONEST MEASUREMENT ENGINE + INCORRECT/INCOMPLETE COMPETENCY MODEL = HONESTLY MEASURING THE WRONG THING. This audit evaluates the model; it does **not** modify it (audit-first mandate; any model change requires a new instrument freeze under calibration rules).

## Method

Per competency: DEFINITION → EXISTENCE → CONSTRUCTION → STABILITY → INTERPRETATION (§4 framework). Every behavioral claim gets independent TECHNICAL_CLAIM_VALIDITY and CONSTRUCT_MEASUREMENT_VALIDITY judgments (§15). Boundaries audited explicitly (§7), including CAPABILITY COMPLEXITY ≠ TASK COMPLEXITY. External grounding from primary kernel.org / Rust-project documentation (source-manifest.yaml); secondary material used only to locate primary evidence. Construct-validity probes (§13) are paper probes attacking adjacent boundaries — they are **not** calibration data and produce no assessor-agreement claims.

## Package

| File | Content |
|---|---|
| instrument-manifest.yaml | Hashed audited inputs (22 files, digest `c09377b5ddcbcd1b…`) at audit baseline |
| source-manifest.yaml | External source records (evidence classes, access dates) |
| findings.yaml | Machine-readable findings ledger (CM-001…CM-020) |
| C034-analysis.md / C047-analysis.md / C053-analysis.md | Per-competency audits |
| cross-competency-analysis.md | Overlap matrix and composition/duplication verdicts |
| level-boundary-analysis.md | All 15 L-boundaries + construct-validity probes |
| adversarial-profiles.md | Profiles A–H against the matrices |
| missing-competencies.md | Omission attack with classifications |
| final-assessment.md | Required conclusions A–J, dispositions, release implications |

## Epistemic discipline (mandatory)

- No assessor-reliability, criterion-validity, or measurement-validity claims are made or implied. This phase supplies evidence to the first two stages only: TECHNICAL COMPETENCY AUDIT → CONSTRUCT VALIDITY HYPOTHESES.
- Frozen calibration/criterion/kernel states are untouched: calibration BLOCKED; criterion_validity NOT_ESTABLISHED; measurement_validity NOT_ESTABLISHED; release BLOCKED (unchanged by this audit).
- Evidence hierarchy respected: upstream implementation evidence is never evidence of candidate competence; expert judgment is never PROOF; synthetic probes are never empirical calibration.
