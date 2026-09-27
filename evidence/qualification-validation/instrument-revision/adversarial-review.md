# Adversarial Review of the Proposed Revision (§16) — proposal-level findings ledger

Each §16 question answered against change-proposal.yaml (CH-1..CH-5, NC-1..NC-3). Statuses use the frozen vocabulary; the proposal as a whole is deliberately NOT marked VERIFIED.

| # | Attack question | Finding | Status |
|---|---|---|---|
| R1 | Can CH-1 introduce a new E→L inference? | No: context classification changes which *gates* fire; evidence tier still never raises level. RG-CM001-2 guards against blanket weakening (classic context still blocks). | SUPPORTED |
| R2 | Can a candidate game CB-053-06 (CH-2)? | Gaming surface: boilerplate "release/acquire" incantation without understanding. Mitigation: oracle requires schedule-specific ownership-transfer + registration-ordering statements (same anti-template pattern as C034 D1–D3); confounder Send/Sync-fluency named in the behavior spec. | PARTIALLY_SUPPORTED — wording must require binding to the specific artifact at implementation |
| R3 | Can an assessor interpret CH-1 contexts differently? | Context set is machine-readable per behavior, but boundary cases (BH-off sections under RT; NMI excluded by scope) remain judgment calls. | PARTIALLY_SUPPORTED — assessor guidance must include a boundary-case table; residual ambiguity recorded |
| R4 | Does any change test API memorization instead of competence? | CH-2 wording reviewed against CM-020 churn: anchored to invariants (visibility, ownership transfer) not macro spellings. RG-CM014 checks reasoning artifacts. | SUPPORTED |
| R5 | Does CH-2 duplicate another competency? | Publication ordering touches C047 registration admission; CH-2 explicitly absorbs only the init-side window (CM-019) and cross-references C047 for post-registration teardown; double-count rule CH-5 applies. | SUPPORTED |
| R6 | Does any change encode organizational privilege? | NC-1 explicitly refuses L5 reformulation into authority/leadership; CH-5 rule is authority-neutral. | SUPPORTED |
| R7 | Does any change become version-specific? | CH-1 context taxonomy tracks kernel context classes (evolves slowly; re-anchor per freeze — CM-020 discipline); CH-2 invariant-anchored; CH-4 exceptions list is kernel-version-sensitive (SLAB_TYPESAFE_BY_RCU etc.) → must be re-verified each freeze. | PARTIALLY_SUPPORTED — version re-anchoring is a standing freeze requirement, recorded |
| R8 | Does any change weaken an existing hard gate? | CH-1 narrows one gate's firing domain under declared contexts only; RG-GATE-1/2 + RG-CM001-2 prove classic-context blocking and all other vetoes unchanged. Veto strength (any fired gate blocks) untouched. | SUPPORTED |
| R9 | Does a Type-D assumption disappear? | No: D01 external contracts unchanged; CH-2 adds a runtime-invariant statement (publication requires kernel-level synchronization) that is itself class-C/D reasoning. | SUPPORTED |
| R10 | Does any change turn an oracle into a claimed theorem? | Opposite: CH-4's entire purpose is anti-theorem metadata + rubric rule; RG-C047O-1 freezes check semantics. | SUPPORTED |
| R11 | Does any change invalidate historical comparability? | Yes, deliberately, in the conservative direction: CH-1/CH-2/CH-5 marked INCOMPARABLE (§12 default); historical evidence preserved by identity; calibration reset rule applies (there is no old human calibration to lose). | SUPPORTED |
| R12 | Is the proposal's evidence sufficient? | External grounding: S1–S5 primary sources; audit findings; probes are paper-only. Construct improvements are EXPERT_JUDGMENT + PRIMARY_SOURCE — never PROOF. The proposal cannot claim the revised constructs ARE better measured — only that they are better specified for measurement. | PARTIALLY_SUPPORTED — inherently; empirical weight arrives only via future calibration |
| R13 | Any silent scope expansion? | CH-1 touches all three competencies' gate metadata (declared in targets); no new competency, no level-scale change, L5 untouched. | SUPPORTED |

## Ledger summary

proposal_status: **PARTIALLY_SUPPORTED** — no blocking finding; R2/R3/R7 require implementation-time wording/table discipline; R12 is an inherent epistemic limit of a proposal-stage artifact. Blocking conditions (§24) checked: none triggered — no unsupported technical assumption (CH-1/CH-2 grounded in S1–S5), L5 explicitly NOT made observable, no fabricated evidence required, no old-calibration reuse, no hard-gate weakening, no E→L inference introduced.
