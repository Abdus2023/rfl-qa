# Scoped qualification Q-2026-0001

> This report is not universal certification or evidence of system validity.

## Scope

```json
{
  "competencies": [
    "C053"
  ],
  "domains": [
    "initialization"
  ],
  "environments": [
    "x86_64",
    "CONFIG_RUST=y",
    "PREEMPT_RT=y"
  ],
  "exclusions": [
    "arm64",
    "dma",
    "nmi_context"
  ],
  "task_classes": [
    "in_place_initialization",
    "partial_init_teardown"
  ]
}
```

## Capability

```json
{
  "demonstrated_behaviors": [
    "CB-053-01",
    "CB-053-02",
    "CB-053-03"
  ],
  "evidence_refs": [
    "ARTIFACT"
  ],
  "failed_behaviors": [],
  "level": "L3",
  "level_boundary": {
    "L0_satisfied": true,
    "L1_satisfied": true,
    "L2_satisfied": true,
    "L3_satisfied": true,
    "L4_satisfied": false,
    "L5_satisfied": false
  }
}
```

## Evidence tier

```json
"E4"
```

## Evidence records

```json
[
  {
    "artifact_ref": "fixture://001-pin-init/ARTIFACT",
    "assumptions": [],
    "coverage": {
      "executed": 1,
      "population": "Synthetic lab schedules, not a kernel run"
    },
    "detected_defects": [],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "epistemic_status": "VERIFIED",
    "establishes": "BOUNDED_OBSERVATION",
    "id": "ARTIFACT",
    "limitations": [
      "Synthetic evidence; no actual kernel test executed."
    ],
    "method": "manual_review",
    "record_type": "evidence",
    "required": true,
    "statement": "No defect observed in the executed synthetic trace population.",
    "strength": "OBSERVATION",
    "tier": "E4"
  },
  {
    "artifact_ref": "fixture://001-pin-init/TYPE",
    "assumptions": [
      "Sound compiler and safe API; unsafe implementation meets its contract."
    ],
    "coverage": {
      "executed": 1,
      "population": "Synthetic lab schedules, not a kernel run"
    },
    "detected_defects": [],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "epistemic_status": "VERIFIED",
    "establishes": "ASSUMPTION_BOUND_PROOF",
    "id": "TYPE",
    "limitations": [
      "Synthetic evidence; no actual kernel test executed."
    ],
    "method": "rustc",
    "record_type": "evidence",
    "required": true,
    "statement": "Borrow cannot escape the safe guard under the stated model assumptions.",
    "strength": "PROOF",
    "tier": "E4"
  },
  {
    "artifact_ref": "fixture://001-pin-init/TEST",
    "assumptions": [],
    "coverage": {
      "executed": 1,
      "population": "Synthetic lab schedules, not a kernel run"
    },
    "detected_defects": [],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "epistemic_status": "PARTIALLY_VERIFIED",
    "establishes": "BOUNDED_OBSERVATION",
    "id": "TEST",
    "limitations": [
      "Synthetic evidence; no actual kernel test executed."
    ],
    "method": "kcsan",
    "record_type": "evidence",
    "required": true,
    "statement": "No defect observed in the executed synthetic trace population.",
    "strength": "OBSERVATION",
    "tier": "E4"
  },
  {
    "artifact_ref": "fixture://001-pin-init/COVERAGE",
    "assumptions": [],
    "coverage": {
      "executed": 1000000,
      "population": "Synthetic lab schedules, not a kernel run"
    },
    "detected_defects": [],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "epistemic_status": "PARTIALLY_VERIFIED",
    "establishes": "MEASURED_COVERAGE",
    "id": "COVERAGE",
    "limitations": [
      "Synthetic evidence; no actual kernel test executed."
    ],
    "method": "scheduler",
    "record_type": "evidence",
    "required": true,
    "statement": "1000000 generated interleavings represented; total state space unknown.",
    "strength": "COVERAGE",
    "tier": "E4"
  },
  {
    "artifact_ref": "fixture://001-pin-init/NMI",
    "assumptions": [],
    "coverage": {
      "executed": 0,
      "population": "Synthetic lab schedules, not a kernel run"
    },
    "detected_defects": [],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "epistemic_status": "OPEN",
    "establishes": "NOT_TESTED",
    "id": "NMI",
    "limitations": [
      "Synthetic evidence; no actual kernel test executed."
    ],
    "method": "not_tested",
    "record_type": "evidence",
    "required": false,
    "statement": "NMI context was not exercised.",
    "strength": "ABSENCE_OF_EVIDENCE",
    "tier": "E4"
  },
  {
    "artifact_ref": "fixture://001-pin-init/EXT-001",
    "assumptions": [],
    "coverage": {
      "executed": 1,
      "population": "Synthetic lab schedules, not a kernel run"
    },
    "detected_defects": [],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "epistemic_status": "VERIFIED",
    "establishes": "BOUNDED_OBSERVATION",
    "id": "EXT-001",
    "limitations": [
      "Synthetic evidence; no actual kernel test executed."
    ],
    "method": "source_audit",
    "record_type": "evidence",
    "required": true,
    "statement": "No defect observed in the executed synthetic trace population.",
    "strength": "OBSERVATION",
    "tier": "E4"
  }
]
```

## Invariants

```json
[
  {
    "class": "A",
    "critical": false,
    "description": "Compiler-enforced borrow lifetime within a sound safe interface.",
    "epistemic_status": "VERIFIED",
    "evidence_refs": [
      "TYPE"
    ],
    "external_evidence": [],
    "id": "A01",
    "record_type": "invariant",
    "required": true
  },
  {
    "class": "B",
    "critical": false,
    "description": "Safe API prevents repeated initialization and reference escape; sound implementation remains a premise.",
    "epistemic_status": "VERIFIED",
    "evidence_refs": [
      "ARTIFACT"
    ],
    "external_evidence": [],
    "id": "B01",
    "record_type": "invariant",
    "required": true
  },
  {
    "class": "C",
    "critical": false,
    "description": "Runtime drain/synchronization completes before final release; bounded tests observe this protocol.",
    "epistemic_status": "PARTIALLY_VERIFIED",
    "evidence_refs": [
      "TEST"
    ],
    "external_evidence": [],
    "id": "C01",
    "record_type": "invariant",
    "required": true
  },
  {
    "class": "D",
    "critical": true,
    "description": "External C registration/allocator contract keeps the target alive until quiescence.",
    "epistemic_status": "VERIFIED",
    "evidence_refs": [
      "EXT-001"
    ],
    "external_evidence": [
      {
        "assessor": "assessor-a",
        "description": "Synthetic source audit of unregister/drain contract.",
        "ref": "EXT-001",
        "type": "source_audit"
      }
    ],
    "id": "D01",
    "record_type": "invariant",
    "required": true
  }
]
```

## Epistemic ceiling

```json
"PARTIALLY_VERIFIED"
```

## Hard gates

```json
{
  "findings": [],
  "status": "PASS"
}
```

## Assessors (raw records)

```json
[
  {
    "assessor_id": "assessor-a",
    "claimed_level": "L3",
    "dossier_digest": "b679a966d91e2dc069bf3e85aa00de1f0af2f49f90ec8a782d7a53aedf23b238",
    "dossier_ref": "Q-2026-0001",
    "evidence_refs": [
      "ARTIFACT"
    ],
    "evidence_tier": "E4",
    "hard_gates": {
      "findings": [],
      "status": "PASS"
    },
    "independent": true,
    "invariant_findings": [
      {
        "class": "A",
        "epistemic_status": "VERIFIED",
        "invariant_ref": "A01"
      },
      {
        "class": "B",
        "epistemic_status": "VERIFIED",
        "invariant_ref": "B01"
      },
      {
        "class": "C",
        "epistemic_status": "PARTIALLY_VERIFIED",
        "invariant_ref": "C01"
      },
      {
        "class": "D",
        "epistemic_status": "VERIFIED",
        "invariant_ref": "D01"
      }
    ],
    "limitations": [
      "Simulated independent record, not an independent human assessment."
    ],
    "observations": [
      {
        "behavior_id": "CB-053-01",
        "evidence_refs": [
          "ARTIFACT"
        ],
        "status": "DEMONSTRATED"
      },
      {
        "behavior_id": "CB-053-02",
        "evidence_refs": [
          "ARTIFACT"
        ],
        "status": "DEMONSTRATED"
      },
      {
        "behavior_id": "CB-053-03",
        "evidence_refs": [
          "ARTIFACT"
        ],
        "status": "DEMONSTRATED"
      }
    ],
    "record_type": "assessment"
  },
  {
    "assessor_id": "assessor-b",
    "claimed_level": "L3",
    "dossier_digest": "b679a966d91e2dc069bf3e85aa00de1f0af2f49f90ec8a782d7a53aedf23b238",
    "dossier_ref": "Q-2026-0001",
    "evidence_refs": [
      "ARTIFACT"
    ],
    "evidence_tier": "E4",
    "hard_gates": {
      "findings": [],
      "status": "PASS"
    },
    "independent": true,
    "invariant_findings": [
      {
        "class": "A",
        "epistemic_status": "VERIFIED",
        "invariant_ref": "A01"
      },
      {
        "class": "B",
        "epistemic_status": "VERIFIED",
        "invariant_ref": "B01"
      },
      {
        "class": "C",
        "epistemic_status": "PARTIALLY_VERIFIED",
        "invariant_ref": "C01"
      },
      {
        "class": "D",
        "epistemic_status": "VERIFIED",
        "invariant_ref": "D01"
      }
    ],
    "limitations": [
      "Simulated independent record, not an independent human assessment."
    ],
    "observations": [
      {
        "behavior_id": "CB-053-01",
        "evidence_refs": [
          "ARTIFACT"
        ],
        "status": "DEMONSTRATED"
      },
      {
        "behavior_id": "CB-053-02",
        "evidence_refs": [
          "ARTIFACT"
        ],
        "status": "DEMONSTRATED"
      },
      {
        "behavior_id": "CB-053-03",
        "evidence_refs": [
          "ARTIFACT"
        ],
        "status": "DEMONSTRATED"
      }
    ],
    "record_type": "assessment"
  }
]
```

## Capabilities by assessor

```json
[
  {
    "assessor_id": "assessor-a",
    "capability": {
      "demonstrated_behaviors": [
        "CB-053-01",
        "CB-053-02",
        "CB-053-03"
      ],
      "evidence_refs": [
        "ARTIFACT"
      ],
      "failed_behaviors": [],
      "level": "L3",
      "level_boundary": {
        "L0_satisfied": true,
        "L1_satisfied": true,
        "L2_satisfied": true,
        "L3_satisfied": true,
        "L4_satisfied": false,
        "L5_satisfied": false
      }
    }
  },
  {
    "assessor_id": "assessor-b",
    "capability": {
      "demonstrated_behaviors": [
        "CB-053-01",
        "CB-053-02",
        "CB-053-03"
      ],
      "evidence_refs": [
        "ARTIFACT"
      ],
      "failed_behaviors": [],
      "level": "L3",
      "level_boundary": {
        "L0_satisfied": true,
        "L1_satisfied": true,
        "L2_satisfied": true,
        "L3_satisfied": true,
        "L4_satisfied": false,
        "L5_satisfied": false
      }
    }
  }
]
```

## Inter-rater result

```json
{
  "agreement": true,
  "automatic_qualification_halted": false,
  "events": []
}
```

## Decision

```json
{
  "epistemic_ceiling": "PARTIALLY_VERIFIED",
  "scope": {
    "competencies": [
      "C053"
    ],
    "domains": [
      "initialization"
    ],
    "environments": [
      "x86_64",
      "CONFIG_RUST=y",
      "PREEMPT_RT=y"
    ],
    "exclusions": [
      "arm64",
      "dma",
      "nmi_context"
    ],
    "task_classes": [
      "in_place_initialization",
      "partial_init_teardown"
    ]
  },
  "status": "PROVISIONAL"
}
```

## Signature

```json
"L3-E4-C053-PARTIALLY_VERIFIED"
```

## Limitations

```json
[
  "Synthetic training fixture only; all E4 labels simulate artifacts, not actual upstream evidence.",
  "Synthetic fixture: not a real candidate qualification or human calibration."
]
```

## Provenance

```json
{
  "input_sha256": "2eff35238201556ba6174c4c416cff32c7dcde9e384cbb39ce241ef1daf61a98",
  "invariant_catalog_sha256": "6578e8f4f8e31b7d8aea25ef85497e271542a2ab5783dd1b9bfe534e7fa61e7d",
  "oracles_sha256": "4e4c19b138200a90673009662438bb6f43ab5773c723a6b263c759f73d9bd689",
  "rubric_sha256": "183732b29a232c0fe972c33911524d8dc9d4429c9b4ada4a3a3427e2de443f33",
  "rules_version": "1.1-alpha.1"
}
```

## Hash

```json
"d33165a89c2ac65f570ff14bfd825aec53830cfd893ee8ecf8124a6c29365f6e"
```
