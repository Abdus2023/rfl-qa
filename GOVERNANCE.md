# Alpha governance and unresolved execution boundaries

No assessor certification, independent calibration panel or release authority is claimed to exist. Repository maintainers must appoint conflict-free domain assessors and a reviewer independent of the implementation author before a release. No L5/E5 bootstrapping assertion is required or fabricated.

## Review and release

1. Preserve immutable raw artifacts and their provenance, rubric/schema versions and scope before assessment.
2. Assign two distinct independent assessors; blind them to each other's findings and the training answer key. Record conflicts and training evidence outside the synthetic fixture pair.
3. Record raw observations; run validation, derivation and divergence reporting.
4. Resolve disputes by documented third review. Never replace raw records; create a revised assessment with rationale and links to the originals.
5. Inspect actual CI logs and local execution ledger; verify every mandatory gate, including human calibration. No automatic tag is implemented.
6. Publish scope and limitations with the release. Unit-test success is not measurement reliability or criterion validity.

## Contradiction ledger (smallest affected boundary)

| ID | Classification | Frozen statements in tension | Treatment / status |
|---|---|---|---|
| F-001 | specification contradiction | Execution prompt §1 lists VERIFIED; §2 also says PROVED. Earlier v1.1.1 and the alpha implementation contract specify VERIFIED. | Canonical schema keeps VERIFIED; rejects PROVED. Conflict recorded, not a new epistemic axis. |
| F-002 | implementation defect in supplied sample | Earlier sample derive.py promotes every hard-gate PASS to VERIFIED_WITHIN_SCOPE and trusts supplied capability. | Replaced with the expressly required behavioral derivation and weakest-required ceiling. Regression tests execute both constraints. |
| F-003 | specification contradiction | Earlier draft calibration examples accept ±1 level; latest execution prompt §20/23 and final handoff halt disagreements and prohibit averaging. | Exact automatic agreement implemented per latest execution prompt. Disputes halt; no silent adjudication. |
| F-004 | specification contradiction | Earlier prose defines VALIDATED_WITHIN_SCOPE as an outside-scope bug; no-scope/no-extrapolation and no-self-certification disallow claiming validation from that alone. | Outcome attribution remains an explicit reviewed input. No automatic defect→validation or defect→false-positive classifier implemented. Synthetic first case is INCONCLUSIVE. Final causal attribution policy remains OPEN for governance; unaffected schema/derivation tests continue. |
| F-005 | fixture limitation | Synthetic dual-assessor fixtures versus mandatory actual independent calibration. | Synthetic engine exercise can pass; human calibration and alpha release remain BLOCKED. No fabricated assessors or observations. |
| F-006 | specification normalization | Earlier texts use FAIL/BLOCKED and BLOCKED/REJECTED for different fields. | Hard gates PASS/BLOCKED; decisions PROVISIONAL/VERIFIED_WITHIN_SCOPE/REJECTED, as explicitly required by the implementation contract. |

No conceptual expansion is intended. The engine operates on bounded supplied records; real evidence adequacy, human independence and causal outcome classification cannot be established by internal consistency.
