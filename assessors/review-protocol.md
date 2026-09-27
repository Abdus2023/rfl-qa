# Independent review protocol

1. Freeze a candidate dossier, explicit scope/exclusions, all evidence and the rubric/oracle versions.
2. Obtain two independent assessors' conflict declarations and training records. Distinct IDs and `independent: true` are required but do not prove independence.
3. Each assessor receives the same raw dossier, not the other findings. `dossier_digest` hashes all fields except `assessments` and must match.
4. Each records claimed capability, observed/failed behaviors with evidence, tier, invariant classes/statuses, hard gates and limitations independently.
5. Validate references, derive per-assessor supported capability and compare raw findings. Exact agreement is required for automatic qualification in alpha. Any safety veto wins even during disagreement.
6. Differences produce an OPEN calibration event and halt automatic qualification. No averages, majority vote or hidden replacement. Missing/invalid evidence is a validation error, not a vote.
7. A third reviewer reviews a dispute and documents whether it reflects training, rubric, oracle, specification or artifact ambiguity. The engine's initial artifact_ambiguity marker is not a causal finding.
8. Corrections create new input and output hashes; retain old records. A release reviewer must separately verify real human independence and procedural completion.
