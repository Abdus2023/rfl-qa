# Calibration protocol and limits

`tests/fixtures/calibration/lab003_assessor_a.yaml` and `lab003_assessor_b.yaml` are separately serialized **synthetic** records tied to the same raw dossier digest. They exercise data preservation and comparison only. They were not produced by independent humans.

Run `pytest -q tests/test_inter_rater.py`. Agreement, disagreement, invariant-class differences, epistemic differences, evidence-tier differences and mismatched dossier hashes are tested. A discrepancy creates an OPEN event in the derived output; the report preserves both records. Automatic derivation stops, rather than inventing a causal attribution or averaging L3 and L4.

Reviewed divergence categories: acceptable, assessor_training_issue, rubric_ambiguity, oracle_ambiguity, specification_defect, artifact_ambiguity. These are not evidence tiers or epistemic states. Until independently reviewed, a conflict remains unresolved artifact ambiguity; it is not automatically specification failure.

For an actual calibration run follow `assessors/review-protocol.md`. Save raw independent records, all evidence, conflicts, training, comparison results and adjudication history. Report disagreement before and after adjudication separately. Do not count synthetic concordance as empirical inter-rater reliability. One agreement pair alone does not establish general reliability.

## Downstream outcomes

The claim schema's outcome and calibration_case definitions preserve observation window, patch and defect counts, maintainer feedback and confounders. The seven frozen classification values are accepted as **explicit reviewed inputs**, not inferred from whether any later bug happened. Each requires scope analysis, candidate behavior, assessment record, oracle capability, specification coverage, confounders, evidence references and rationale.

Out-of-scope defects cannot automatically validate or invalidate an in-scope qualification. Attribution may be INCONCLUSIVE. Only reviewed ASSESSMENT_ERROR, ORACLE_FAILURE or SPECIFICATION_FAILURE can carry a revision-required flag; even these need a rationale. An assessment error may instead require assessor training. No automatic causal classifier or predictive-accuracy score is claimed.

CAL-001 and the outcome example are synthetic and explicitly labeled. No historical or future upstream event has been observed for this project. The human calibration gate remains BLOCKED until the actual procedure is independently completed.
