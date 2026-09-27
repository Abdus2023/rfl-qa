import collections, datetime, json
from pathlib import Path
import yaml
A=Path(__file__).parent;R=A.parents[1]
F=[]
def finding(id,severity,status,classification,location,claim,observation,evidence,impact,action):
 F.append(dict(ID=id,SEVERITY=severity,STATUS=status,CLASSIFICATION=classification,LOCATION=location,CLAIM=claim,OBSERVATION=observation,EVIDENCE=evidence,IMPACT=impact,RECOMMENDED_ACTION=action))
finding('AUD-001','HIGH','OPEN','EVIDENCE_GAP',
 ['evidence/execution/ledger.yaml','Git source/evidence ancestry'],
 '993cf96 is the executed source and 50512a3 is the evidence commit.',
 'Both hashes fail git show after unshallow/fetch and GitHub commit API returns 422. Actual published evidence first appears in 1bfcdf9; remote head is e4f1611. Local HEAD remains 33e4d95 and execution sources are uncommitted. All 112 published files match the local pre-audit content; all 74 manifest files and 15 command-log hashes match. Three qualification outputs reproduce byte-for-byte.',
 ['evidence-chain.json','commands.log labels source-commit, evidence-commit, source-github, evidence-github, inspect-chain','remaining-results.json'],
 'Content-based reproduction succeeds, but the claimed historical commit chain and actual original command execution are not authenticated. Missing references are not proof that the historical run never happened.',
 'Publish a corrected provenance record referencing available source/evidence history and the content manifest; retain the old ledger rather than silently rewriting it.')
finding('AUD-002','HIGH','PROVED','IMPLEMENTATION_DEFECT',
 ['tools/validate.py:validate_dossier','tools/derive.py:derive','invariants/D-external/D01.yaml'],
 'An unresolved critical Type-D assumption always vetoes qualification.',
 'D01 is critical in the catalog. Setting the dossier copy critical=false while keeping OPEN changes the result from BLOCKED/REJECTED to PASS/PROVISIONAL. The validator compares class and required flag but not authoritative criticality.',
 ['engine-results.json:critical-open-control','counterexamples/critical-open-declared-noncritical.json','counterexamples/critical-open-declared-noncritical.result.json','commands.log:cli-critical-bypass'],
 'A caller-controlled Boolean disables a non-compensable veto. This is a metadata downgrade, not L/E compensation.',
 'Validate criticality against the existing authoritative invariant/rubric and reject weakening; derive safety criticality from that source. Add this exact regression without changing the taxonomy.')
finding('AUD-003','HIGH','PROVED','IMPLEMENTATION_DEFECT',
 ['tools/derive.py:required_refs','tools/validate.py:oracle result validation'],
 'The ceiling includes the weakest evidence needed by required qualification checks.',
 'TEST is OPEN and required=false, referenced by the five required teardown oracle checks but no longer by an invariant. The ceiling excludes it and the engine issues VERIFIED_WITHIN_SCOPE with VERIFIED ceiling.',
 ['counterexamples/oracle-open-evidence-not-in-ceiling.json','counterexamples/oracle-open-evidence-not-in-ceiling.result.json','commands.log:cli-oracle-ceiling-bypass'],
 'Required oracle evidence can be hidden from the ceiling by changing its flag/references, silently permitting an unjustified verified decision.',
 'Include the required-oracle evidence dependency closure in both adequacy validation and ceiling calculation, with a regression for this counterexample.')
finding('AUD-004','HIGH','PROVED','SCHEMA_DEFECT',
 ['tools/validate.py:scope constraints','competency/C047-callback-teardown.yaml:scope_constraints'],
 'Qualification cannot become broader by omitting scope restrictions.',
 'Complete missing fields and explicit out-of-scope additions are rejected. However environments=[x86_64], [PREEMPT_RT=y], or [CONFIG_RUST=y] are accepted and can receive VERIFIED_WITHIN_SCOPE. The set-subset test treats deleting a conjunctive architecture/config restriction as narrowing. Output copies the input exactly; this is not formatter extrapolation.',
 ['engine-results.json:scope-*','counterexamples/scope-erased-x86_64.json','counterexamples/scope-erased-PREEMPT_RT-y.json','counterexamples/scope-erased-CONFIG_RUST-y.json'],
 'The record no longer states the tested architecture/configuration combination. Interpreting omitted constraints as unrestricted would exceed the evidence.',
 'Enforce the frozen complete environment combination at validation. Record/resolve the whitelist-versus-conjunction ambiguity before allowing partial combinations; do not silently infer missing environments.')
finding('AUD-005','HIGH','PROVED','SCHEMA_DEFECT',
 ['tools/validate.py:check_evidence','tools/derive.py:capability'],
 'No unperformed assessment can support a verified behavioral capability.',
 'An ARTIFACT record with method=not_tested, executed=0, and an explicit statement that no assessment occurred is accepted when labeled OBSERVATION/VERIFIED. It supports L3 and a VERIFIED_WITHIN_SCOPE decision. The validator checks ABSENCE_OF_EVIDENCE in one direction only.',
 ['counterexamples/not-tested-as-observation.json','counterexamples/not-tested-as-observation.result.json'],
 'Contradictory structured evidence can receive behavioral credit. This is not evidence-tier promotion.',
 'Enforce consistency between the existing not_tested method, absence strength and support eligibility; reject this contradictory record rather than guessing missing facts.')
finding('AUD-006','HIGH','PROVED','IMPLEMENTATION_DEFECT',
 ['tools/validate.py:Type-D checks','tools/derive.py:critical assumption checks'],
 'A VERIFIED critical Type-D invariant has adequate external support.',
 'D01 remains critical and VERIFIED while its only external source-audit record is OPEN. Validation accepts it; the aggregate ceiling becomes OPEN but the hard gate remains PASS and decision is PROVISIONAL rather than vetoing the unresolved critical contract.',
 ['counterexamples/critical-verified-with-open-support.json','counterexamples/critical-verified-with-open-support.result.json'],
 'Critical safety disposition trusts the invariant label despite unresolved supporting evidence.',
 'Reject the inconsistent critical VERIFIED assertion or apply the existing unresolved-critical-assumption veto based on its required support; preserve the raw disagreement rather than silently relabeling it.')
finding('AUD-007','MEDIUM','PARTIALLY_VERIFIED','EVIDENCE_GAP',
 ['tools/validate.py:external_evidence','schemas/invariant.schema.json'],
 'Structured external evidence is adequate evidence of the particular contract.',
 'Missing, Boolean, empty, dangling, wrong-method and unknown-assessor records are rejected. An unrelated source-audit statement about SATA registers still satisfies D01 callback-lifetime support if its ref/method fields match.',
 ['engine-results.json:type-d-*','counterexamples/type-d-unrelated_audit.json'],
 'Reference existence/method equality is not relevance, truth or artifact authentication. The implementation documents this human-review boundary; automated Type-D gate success must not be inflated into evidence adequacy.',
 'Require the existing independent review protocol to establish the explicit contract linkage and real source evidence. Do not claim automatic natural-language or authenticity verification.')
finding('AUD-008','HIGH','PROVED','ORACLE_DEFECT',
 ['tools/validate.py:check_oracle','tools/derive.py:oracle result loop','oracles/teardown/oracle.yaml'],
 'Teardown predicates and adversarial oracle conditions are actually evaluated.',
 'The engine checks check IDs, evidence refs and strength presence, then trusts result labels. An explicit FREE-with-live-callback counterexample in the evidence statement is accepted with PASS labels. In an isolated in-memory oracle catalog, replacing the state model with [FREE, ACTIVE] and safety predicate with looks correct also reaches a verified decision. Trusted-catalog mutation is a validator test, not an external code-write exploit.',
 ['counterexamples/contradictory-teardown-trace-with-pass-labels.json','counterexamples/oracle-invalid-state-model.catalog.json','engine-results.json:oracle-invalid-state-model','static-review.json'],
 'The current oracle gate verifies record shape/presence, not the specified safety predicates. No bounded trace evaluator or artifact check establishes that the declared PASS follows from observations.',
 'Implement/test evaluation or independently recorded adjudication of the already-frozen bounded predicates, and validate the required state model. Do not convert string presence into a proof or claim Python checks executed kernel behavior.')
finding('AUD-009','MEDIUM','PROVED','SCHEMA_DEFECT',
 ['tools/report.py:report','tools/validate.py:qualification validation'],
 'A hash-checked qualification report cannot legitimize inconsistent derived fields.',
 'Genuine reports preserve all input states. But changing only decision status/ceiling to VERIFIED_WITHIN_SCOPE/VERIFIED in a PARTIALLY_VERIFIED record and recomputing its public checksum is accepted and presented. No cross-field consistency with the raw findings is checked.',
 ['counterexamples/report-rehashed-contradictory-decision.json','engine-results.json:report-rehashed-contradictory-decision','engine-results.json:report-purity-*'],
 'Report purity holds; hash authenticity was never provided. Separately, a semantically contradictory record is still accepted as a valid qualification. The report is not a derivation verifier.',
 'Reject demonstrably inconsistent decision/findings at qualification validation, while leaving presentation non-mutating. Do not treat recomputable checksums as signatures.')
finding('AUD-010','MEDIUM','PROVED','SCHEMA_DEFECT',
 ['tools/validate.py:validate_record invariant branch','schemas/invariant.schema.json'],
 'The Type-D evidence rule is enforced whenever an invariant is validated.',
 'A standalone D+VERIFIED invariant with empty evidence_refs and external_evidence passes validate_record. The same unsupported invariant fails inside a dossier. --all and catalogs use this shallow standalone path.',
 ['counterexamples/standalone-d-verified-no-evidence.yaml','format-determinism-results.json:standalone-d-verified-no-evidence'],
 'Validation assurance depends on entry point; standalone PASS does not establish the claimed invariant consistency rule.',
 'Apply context-free Type-D evidence shape requirements to standalone records, and state when reference validation requires dossier context.')
finding('AUD-011','MEDIUM','PROVED','IMPLEMENTATION_DEFECT',
 ['tools/common.py:load','tools/validate.py:CLI exception handling'],
 'Malformed inputs fail in a controlled, bounded manner.',
 '1500 nested JSON or YAML array levels produce uncaught RecursionError and a CLI traceback. No qualification is emitted. Duplicate keys, unsafe Python YAML tags and the tested recursive alias are rejected; benign aliases work.',
 ['format-determinism-results.json:json-deep,yaml-deep,cli-json-deep,cli-yaml-deep','commands.log:cli-json-deep,cli-yaml-deep'],
 'Availability/resource-boundary risk for untrusted dossiers. This audit does not demonstrate arbitrary code execution or a service-level exploit.',
 'Bound input depth/size and handle parser recursion errors explicitly; retain nonzero rejection rather than silently truncating inputs.')
finding('AUD-012','MEDIUM','PROVED','FIXTURE_DEFECT',
 ['labs/001-pin-init/task.yaml','labs/002-rcu/task.yaml','dossiers/examples/*.json'],
 'The meta-labs supply enough underlying artifact semantics for independent classification.',
 'Each lab contains only README/task/oracle/expected-observations files. All task inputs reuse a generic callback unregister/free scenario. Pin-init supplies no concrete self-referential layout/initializer; RCU supplies no implementation or RCU flavor contract; fixture:// compiler/audit/sanitizer refs are not attached artifacts. Labels describe the intended answer.',
 ['remaining-results.json:lab-inventory','labs/001-pin-init/expected-observations.yaml','labs/002-rcu/expected-observations.yaml'],
 'Useful schema/label fixtures, but no observed independent assessor performance on a substantive pin-init or RCU artifact. Correct classification of actual code cannot be inferred from these fixtures.',
 'Within the existing three labs, supply the promised bounded artifacts/contracts for future assessors, without claiming a kernel run or adding competencies.')
finding('AUD-013','LOW','OPEN','SPECIFICATION_INCONSISTENCY',
 ['GOVERNANCE.md:F-004','calibration/inter-rater.md','historical v1.1-alpha calibration definitions'],
 'VALIDATED_WITHIN_SCOPE describes a defect outside the assessed scope.',
 'The enum is preserved and validation does not auto-classify later bugs. Earlier prose equates an out-of-scope defect with validation, which does not establish correctness or predictive validity inside the scope. Governance already notes this ambiguity.',
 ['remaining-results.json:outcome-classification','GOVERNANCE.md'],
 'Potentially misleading outcome interpretation, not a demonstrated automatic classifier bug.',
 'Retain the enum during this audit. Resolve its interpretation through the existing governance process; use INCONCLUSIVE when the required evidence is absent.')
finding('AUD-014','INFORMATIONAL','BLOCKED','EVIDENCE_GAP',
 ['tests/fixtures/calibration','tools/release_gates.py','calibration/inter-rater.md'],
 'Calibration is a completed executable release gate.',
 'Synthetic comparisons preserve raw findings and halt all five tested disagreement axes. The release runner then hardcodes human calibration BLOCKED and returns 1; it does not conduct human assessments. No independent human run or criterion-validity study is supplied.',
 ['engine-results.json:assessor-disagreement-*','reproduced-release/ledger.yaml','tools/release_gates.py'],
 'Six machine gate commands are executable; the human component is a correctly blocked procedural prerequisite, not an executed reliability experiment. Kernel execution remains NOT_RUN and criterion validity NOT_ESTABLISHED.',
 'Do not release or equate synthetic agreement with independence. Perform the existing blind dual-assessment protocol on real artifacts before claiming calibration.')
finding('AUD-015','INFORMATIONAL','PARTIALLY_VERIFIED','ENVIRONMENTAL_BLOCKER',
 ['GitHub Actions runs 36280520784 and 36280518710'],
 'REMOTE_CI remains NOT_RUN.',
 'GitHub API now shows both runs completed with failure at e4f1611. Dependency/schema/test/CLI steps are success; full procedural gate is failure; artifact upload is success. Full log downloads failed twice with EOF. Final remote job state is observed, but remote stdout/test count/installed patch-version cannot be independently extracted here.',
 ['commands.log:ci-runs,ci-details,ci-other-details,ci-log,ci-job-log'],
 'Fresh REMOTE_CI is FAIL, not NOT_RUN. Local reproduction corroborates the expected procedural block but cannot substitute for unavailable remote logs.',
 'Retain API observations and obtain GitHub log/artifact downloads when accessible. Do not alter historical NOT_RUN evidence or assert the remote failure is a test failure.')
(A/'findings.yaml').write_text(yaml.safe_dump({'status_semantics':'PROVED denotes the bounded reproducible observation/counterexample only, not universal code correctness. Finding statuses do not alter the engine VERIFIED vocabulary.','findings':F},sort_keys=False))
legacy=yaml.safe_load((A/'reproduced-release/ledger.yaml').read_text())['execution']
gates={}
issues={'schema':['AUD-004','AUD-005','AUD-009','AUD-010'],'derivation':['AUD-003','AUD-005'],
        'invariant':['AUD-002','AUD-006','AUD-010'],'oracle':['AUD-008','AUD-012'],'hard_gate':['AUD-002','AUD-006'],
        'calibration':['AUD-014'],'reproducibility':[]}
for name,ids in issues.items():
 disposition='BLOCKED' if name=='calibration' else 'FAIL' if ids else 'PASS'
 gates[name]={'claimed': 'BLOCKED' if name=='calibration' else 'PASS',
              'observed_legacy_command_result':legacy['gates'][name],
              'audit_disposition':disposition,
              'claim_progression':['CLAIMED','OBSERVED','REPRODUCED']+(['VERIFIED_WITHIN_EXECUTION_SCOPE'] if name=='reproducibility' else []),
              'execution_scope':'Original machine tests rerun with pinned Python 3.11.2 environment; not human or kernel validation.',
              'findings':ids,'evidence':['reproduced-release/'+('calibration_automated' if name=='calibration' else name)+'.log','engine-results.json']}
gates['reproducibility']['execution_scope']='Three old outputs reproduced byte-identically; 100 original repeated derivations plus 16 independent subprocess variants (seeds, CWD, TZ, locale, concurrency). Fixed source/dependencies/catalogs only.'
gates.update({'remote_ci':{'claimed':'NOT_RUN','audit_disposition':'FAIL','claim_progression':['CLAIMED','OBSERVED'],
                          'evidence':['commands.log:ci-details','commands.log:ci-other-details'],'logs_available':False},
              'human_calibration':{'audit_disposition':'NOT_RUN'},'kernel_execution':{'audit_disposition':'NOT_RUN'},
              'criterion_validity':{'audit_disposition':'NOT_ESTABLISHED'}})
(A/'gate-results.yaml').write_text(yaml.safe_dump({'gates':gates,'release':'BLOCKED','note':'Legacy PASS means the existing tests ran successfully. Adversarial FAIL means broader frozen assurance was refuted. NOT_RUN and NOT_ESTABLISHED are not test failures.','original_suite':legacy['tests'],'adversarial_engine':{'probes':150,'boundary_held':139,'counterexamples_or_evidence_limitations':11},'implementation_modified':False},sort_keys=False))
print(json.dumps({'findings':len(F),'severity_counts':dict(collections.Counter(f['SEVERITY'] for f in F)),'release':'BLOCKED'},indent=2))
