"""Build remediation views from executed receipts, never from guessed test outcomes."""
from pathlib import Path
import collections,datetime,hashlib,json,locale,os,platform,subprocess,sys,time,xml.etree.ElementTree as ET
import yaml
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
records=[json.loads(x) for x in (E/'command-records.jsonl').read_text().splitlines()]
by_label={r['label']:r for r in records}
source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert source=='b0582f61ae4fad99c02a262c9b27475330bd018e'
branch=subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()
assert branch=='arena/01a0dfcc-rfl-qa'
cases=list(ET.parse(E/'regressions.xml').iter('testcase'))
assert len(cases)==564 and not any(list(c) for c in cases)
new=[c for c in cases if c.attrib['classname']=='tests.test_remediation']
assert len(new)==445
ci=[json.loads(by_label[k]['stdout']) for k in ['ci-final-pull-request','ci-final-push']]
assert all(r['headSha']==source and r['status']=='completed' and r['conclusion']=='failure' for r in ci)
(E/'ci-results.json').write_text(json.dumps(ci,indent=2)+'\n')
def save(name,obj):(E/name).write_text(yaml.safe_dump(obj,sort_keys=False,allow_unicode=True))
save('environment.yaml',dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_commit=source,
    implementation_commit='3651ffbbf2487585d04c2e0e0ea9559baa3ea7ad',baseline_commit='e4f1611c245d5c001d29b5c4477dee088c3d7867',branch=branch,
    python=sys.version,executable=sys.executable,os=platform.platform(),architecture=platform.machine(),os_release=Path('/etc/os-release').read_text(),
    dependencies=subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True).splitlines(),
    environment_allowlist={k:os.environ.get(k) for k in ['LANG','LC_ALL','LC_CTYPE','TZ','PYTHONHASHSEED','CI','GITHUB_ACTIONS']},
    locale=locale.setlocale(locale.LC_ALL),effective_timezone=list(time.tzname),
    provenance_note='Source/test commit above is the executed revision; a later evidence-only receipt commit does not claim a new source execution. No unavailable historical commit was reconstructed.'))
old=yaml.safe_load((R/'evidence/adversarial-audit/findings.yaml').read_text())['findings']
notes={
1:('OPEN','UNRESOLVED_HISTORICAL_COMMIT: 993cf96/50512a3 remain unavailable after fetch. New receipts use available commits and content hashes; historical claims are not repaired.','initial history inspections'),
2:('FIXED_LOCALLY_CI_PENDING','Catalog criticality equality and authoritative derivation reject original false downgrade and inconsistent catalog metadata.','test_hg01*, test_catalog_*; current-provenance-results.json'),
3:('FIXED_LOCALLY_CI_PENDING','Closure includes optional-flagged material oracle/observation/assessor/behavior support. Original OPEN oracle support now produces PROVISIONAL/OPEN, not VERIFIED.','test_hg03*, test_hg05*; current-provenance-results.json'),
4:('FIXED_LOCALLY_CI_PENDING','Complete environment/task combinations and required exclusions enforced; all three original omission variants reject.','test_hg02*; current-provenance-results.json'),
5:('FIXED_LOCALLY_CI_PENDING','Method/strength compatibility rejects not_tested OBSERVATION; dynamic methods require a nonempty executed population.','test_hg04*, test_empty_dynamic_population_not_observation; current-provenance-results.json'),
6:('FIXED_LOCALLY_CI_PENDING','VERIFIED external invariants reject unresolved external support, with explicit binding requirements. This is not source-document authentication.','test_original_bypass_with_current_provenance_rejects[critical-verified-with-open-support]; current-provenance-results.json'),
7:('OPEN','Unrelated audit prose remains accepted when all declared bindings are fabricated consistently. Record bindings cannot establish source relevance or adequacy.','current-provenance-results.json:type-d-unrelated_audit.json'),
8:('OPEN','Partial correction: fixed bounded evaluator and ASSERTED_RESULT/DERIVED_RESULT provenance work for supplied structured traces; unsafe explicit transcription blocks. Contradictory prose paired with fabricated safe snapshots remains accepted. Full finding is NOT closed.','test_hg06*, test_hg07*, test_original_unsafe_narrative_explicitly_transcribed_to_trace; current-provenance-results.json'),
9:('FIXED_LOCALLY_CI_PENDING','Report validation recomputes qualification from retained input and rejects a rehashed contradictory decision.','test_aud009_contradictory_rehashed_report_rejected'),
10:('FIXED_LOCALLY_CI_PENDING','Standalone invariant validation applies context-free required evidence rules; original D VERIFIED without support rejects.','test_aud010_standalone_invariant_rules; post-fix-counterexamples.json'),
11:('FIXED_LOCALLY_CI_PENDING','Bounded parser rejects deep/recursive/ambiguous data with controlled Invalid errors. Supplemental baseline replay used exact e4f1611 common.py in isolation after patching; its old behavior was reproduced, not assumed.','test_aud011*, test_yaml_scalar_and_alias_boundaries; supplemental-checks command; trust-boundary-review.json'),
12:('OPEN','Structured synthetic fixtures are more executable as models, but substantive candidate/kernel artifacts for labs 001/002 remain unestablished. No real kernel/compiler/sanitizer execution was performed.','unchanged labs/001-pin-init and labs/002-rcu; synthetic fixture declarations'),
13:('SPECIFICATION_FAILURE','Outcome scope terminology conflict remains unresolved. No silent enum rename or expanded outcome interpretation was introduced.','immutable audit AUD-013; tests/test_outcomes.py only confirms current implementation'),
14:('OPEN','No independent human calibration, actual kernel execution or upstream criterion evidence was supplied or generated. Synthetic agreement does not satisfy these gates.','procedural-final/ledger.yaml; calibration fixtures remain synthetic'),
15:('EXTERNAL_FAILURE','Actual final CI runs/jobs observed: software steps succeed, overall workflows fail at procedural gate. Raw logs and artifact downloads return EOF. Successful whole-workflow CI is still absent; remote detailed failure cause is not independently confirmed.','ci-results.json; ci-final-raw-logs and ci-final-artifacts commands'),
}
findings=[]
for original in old:
 n=int(original['ID'].split('-')[1]);disposition,note,evidence=notes[n]
 findings.append(dict(id=original['ID'],severity=original['SEVERITY'],disposition=disposition,observation=note,
     baseline_evidence='pre-fix-counterexamples.json' if n in [2,3,4,5,6,7,8,9,10] else 'commands.log and immutable prior audit',
     regression_evidence=evidence,positive_control='Canonical/schema positive records and valid structured-trace control; full 564-test suite' if disposition.startswith('FIXED_') else 'No complete fix claimed',
     ci='Software step success observed; whole workflow FAIL. Successful-CI prerequisite still outstanding.',
     verified_fix_claim=False))
save('findings.yaml',{'disposition_semantics':'FIXED_LOCALLY_CI_PENDING means a local correction/regression exists but the required successful whole-workflow CI chain is still missing, despite observed successful software steps. No FIXED_AND_RETESTED or VERIFIED fix is asserted.','findings':findings})
contracts=[
 ('HG-01','AUD-002','PASS','Catalog true/false, upgrade/downgrade, missing metadata, identity and assessor downgrade'),
 ('HG-02','AUD-004','PASS','Exact/reordered scope; omitted environment/task; unsupported additions/exclusions/duplicates'),
 ('HG-03','AUD-003','PASS','Five epistemic states; oracle, behavioral and assessor closure independent of required flag'),
 ('HG-04','AUD-005','PASS','40 method/strength combinations; no not_tested observations; positive proof/coverage controls'),
 ('HG-05','AUD-003','PASS','Every canonical check x remove/unrelated/OPEN/absence/changed-strength/BLOCKED'),
 ('HG-06','AUD-008','FAIL','Structured result-label tests PASS; narrative artifact authenticity/provenance completeness remains unresolved'),
 ('HG-07','AUD-008','PASS','Bounded safe/unsafe/empty/incomplete/duplicate/reordered lifecycle evaluations; no real kernel execution'),
]
matrix=[
 ('Schema','PASS','Final --all and positive/negative schema regressions'),('Derivation','PASS','564-test suite; all 3 canonical CLI pipelines'),
 ('E→L separation','PASS','7 required pairs plus exhaustive 36-pair sweep'),('Invariant enforcement','PASS','Authoritative catalog and external support structure; document adequacy remains OPEN'),
 ('Scope enforcement','PASS','Both containment directions, exclusions, duplicates, order controls'),('Epistemic closure','PASS','All referenced material supports included; weakening cannot verify'),
 ('Evidence-strength separation','PASS','Compatibility matrix and independent epistemic states'),('Oracle integrity','FAIL','Executed adapted narrative cases still accept fabricated consistently bound source facts (AUD-007/008)'),
 ('Hard-gate veto','PASS','All 10 classes at L5/E5/VERIFIED and agreement: BLOCKED/REJECTED/BLOCKED'),
 ('Teardown evaluation','PASS','Finite structured model only, not external artifact authenticity'),('Canonical hashing','PASS','Full-record binding; serialization/key order stable; semantic changes differ'),
 ('Original regression suite','PASS','119 unchanged tests; separately rerun and included in final suite'),('Adversarial regression suite','PASS','445 additional tests; no skipped/xfail tests'),
 ('Determinism','PASS','16 final independent CLI processes, varied seed/CWD/locale/TZ/concurrency; key-order tests'),
 ('Remote CI','FAIL','Both final workflows completed failure; schema/tests/CLI steps success; logs/artifacts unavailable'),
 ('Human calibration','BLOCKED','NOT_RUN: no real independent dual-assessor exercise'),('Kernel execution','NOT_RUN','No kernel/compiler/KASAN/KCSAN/lockdep run'),
 ('Criterion validity','NOT_ESTABLISHED','No upstream outcome validation'),('Release','BLOCKED','Open authenticity/self-attestation gaps plus human/kernel/criterion/CI prerequisites'),
]
results={'source_commit':source,'rules_version':'1.1-alpha.2','baseline':{'passed':119,'failed':0,'schema':'PASS'},
    'full_suite':{'passed':564,'original':119,'additional':445,'failed':0,'errors':0,'skipped':0,'command':'completed-regression-suite'},
    'contracts':[dict(contract=a,finding=b,result=c,coverage=d) for a,b,c,d in contracts],
    'test_cases':[dict(name=c.attrib['classname']+'::'+c.attrib['name'],result='PASS') for c in cases],
    'canonical_outputs':json.loads((E/'canonical-cli-results.json').read_text()),
    'determinism':{'independent_processes':16,'all_byte_identical':True,'evidence':'determinism-results.json'},
    'final_matrix':[dict(gate=a,status=b,scope=c) for a,b,c in matrix],
    'release':'BLOCKED'}
save('regression-results.yaml',results)
workflow=list((R/'.github/workflows').glob('*'))
(E/'workflow-review.md').write_text('''# Workflow and trust boundary review

The existing workflow was inspected, not weakened or changed: Python 3.11; pinned requirements; schema/reference CLI; full pytest; derive/report CLI; full release runner (which includes deterministic reproduction); upload-artifact with always(). It intentionally retains a nonzero human-calibration release gate. Dependency/schema/test/CLI and upload step success are observed in the run/job API; source inspection alone is not used as execution evidence. Exact remote test counts and procedural ledger details are unavailable because downloads return EOF.

Production source review: no eval/exec/pickle, dynamic imports, network, candidate shell execution, arbitrary expressions, or new framework. YAML uses a strict SafeLoader subclass, with document bounds and controlled parser errors; not an unsafe object loader. CLI reads supplied files and trusted repository catalogs; derivation does not execute candidate artifacts or use current time/random/environment as qualification facts. New oracle payloads have a closed schema and a ≤9-state trace; general parsed documents have 2 MB/depth64/node100000 bounds. The existing release runner uses subprocess with fixed trusted CLI/test commands and writes only its selected evidence directory. New remediation harnesses likewise run trusted git/pytest/CLI/gh commands, not candidate code. No shell=True was found in production AST inspection. This source review is not a security certification.

The deliberate remaining trust boundary is supplied observation truth versus external reality: hashes bind records but authenticate neither a trace producer nor a narrative source. AUD-007/008 remain OPEN. Complete-record hashes bind timestamps, limitations, scope, observations, array order, evidence and behavior facts. YAML/JSON serialization and mapping-key order are irrelevant presentation; array order is intentionally NOT canonicalized away.

Workflow file hashes:\n'''+''.join(f'- `{p.relative_to(R)}`: `{hashlib.sha256(p.read_bytes()).hexdigest()}`\n' for p in workflow))
text=f'''# Adversarial remediation report — RELEASE BLOCKED

**No evidence → no VERIFIED claim. Software consistency is not human reliability or criterion validity.**

Executed source/test revision: `{source}` on `{branch}`. Implementation commit: `3651ffb`; baseline: `e4f1611`. Rules: **1.1-alpha.2**. Later evidence-only receipt commits do not assert a different source execution. Prior `evidence/adversarial-audit/` and `evidence/execution/` were preserved (97 files verified against the pre-remediation SHA256 snapshot).

## Outcome

- **564 passed, 0 failed, 0 skipped**: all **119 original tests unchanged**, plus **445 new regressions**. The unchanged baseline was 119/119 before patching. Original-only rerun: 119/119. Final fresh procedural runner independently reports 564/564 and release BLOCKED.
- Final schema/reference validation PASS. All three canonical dossiers derived and reported successfully. Sixteen final independent CLI executions produced identical bytes/hashes under varied hash seeds, directories, locale, timezone and concurrency. All remain synthetic qualifications, not human/kernel evidence.
- **Eight findings locally corrected, successful whole-workflow CI prerequisite outstanding** (`FIXED_LOCALLY_CI_PENDING`). **AUD-007 and AUD-008 remain OPEN**: consistent fabricated bindings and safe snapshots can coexist with unrelated or contradictory prose. The bounded evaluator is a partial correction, not artifact authentication.
- Actual final CI workflows both **FAIL** at the procedural release-gate step. Dependency, schema, automated tests, CLI and artifact-upload steps are **success** per GitHub job API. Logs/artifact download EOF prevents independent confirmation of remote procedural details; local human-calibration blockage is not substituted for the missing remote ledger.
- **No finding is FIXED_AND_RETESTED; no VERIFIED fix or release eligibility is claimed.** No release/tag was created.

## Baseline → reproduction → contract → patch

The original source/schema suite was executed unchanged. All 12 saved counterexample inputs (including injected bad catalog and forged report) reproduced acceptance before implementation changes; see `pre-fix-counterexamples.json` and command receipts. Seven contracts were written in `regression-contracts.md` before patching. Available published files were byte-checked before aligning the local index/HEAD to the already published e4f1611 history; no force push or reconstructed commits were used. Historical 993cf96/50512a3 remain UNRESOLVED_HISTORICAL_COMMIT.

Minimal production changes enforce authoritative criticality, complete scope, material support closure, method/strength compatibility, explicit observation/result provenance, fixed teardown predicates, qualification rederivation, standalone invariant rules and bounded strict parsing. Existing canonical/synthetic fixtures were explicitly migrated; arbitrary old inputs receive no defaults or repairs. Frozen axes, statuses, three labs/competencies and release gates remain unchanged. SPEC.md and CHANGELOG.md document the stricter alpha profile.

AUD-011 supplemental baseline reproduction was performed **after** implementation using the exact recorded baseline `tools/common.py` in an isolated temporary directory. Old JSON/YAML depth1500 raises RecursionError; patched CLI rejects cleanly. This is evidence about baseline-version behavior, not a falsely backdated command.

## Counterexample replay and positive controls

All 12 frozen old inputs now reject, mostly for missing required provenance. **That alone is not a semantic fix.** Current-schema replay adds explicitly synthetic template observations and bindings while retaining old fields; it is NOT a transcription/authentication of narrative source facts:

- Criticality downgrade; VERIFIED external invariant with OPEN support; not_tested-as-observation; and all three omitted environment attacks: reject at their intended semantic boundaries.
- Required oracle support with OPEN status and optional flag: accepts only as **PROVISIONAL / OPEN**, never VERIFIED. This is the expected conservative result, not an input-format rejection requirement.
- Unrelated external audit and contradictory teardown prose paired with safe fabricated snapshots: **still accepted**. These are retained as OPEN counterexamples, not hidden behind old-schema rejection.
- Explicitly transcribing the original `FREE(target)` with possible callback/live reference into the bounded trace causes **BLOCKED / REJECTED / signature BLOCKED**. Unsafe traces fail regardless of submitted PASS/BLOCKED; the same safe trace has the same derived result for both labels, while a submitted BLOCKED remains a separate conservative veto.
- Bad state-model catalog, standalone D VERIFIED/no support and current-format rehashed report contradiction reject in dedicated regressions.

Controls include all canonical derive/report pipelines, safe modeled trace → DERIVED_RESULT/PASS, exact/permuted scope, catalog-consistent criticality, compatible method/strength pairs, valid standalone records, and complete VERIFIED support closure. Tests never interpret these synthetic positive controls as real human qualifications.

## Regression matrix

| Contract | Finding | Result | Executed boundary |
|---|---|---|---|
'''
text+=''.join(f'| {a} | {b} | {c} | {d} |\n' for a,b,c,d in contracts)
text+='''
The suite additionally retains seven specified E/L pairs plus all 36 pairs, A/B/C/D × VERIFIED/OPEN, all ten hard-gate classes at L5/E5/VERIFIED and assessor agreement, schema/format/alias/numeric attacks and hash sensitivity/equivalence tests. Every generated test case is listed in `regression-results.yaml`; actual JUnit receipts are retained. No xfail, skip or original test weakening was used.

Earlier failed runs remain in the log: diagnostic-order mismatch (118/119), a no-op PROOF→PROOF mutation (522/523), and a new test reading the evidence list as a dict (554/564). Those test/diagnostic issues were corrected without weakening intended failure oracles, then full suites rerun. The final 564-test suite is green.

## Canonical outputs and determinism

| Dossier | Decision | Ceiling | Assessment hash |
|---|---|---|---|
'''
for row in results['canonical_outputs']:
 text+=f"| {Path(row['dossier']).stem} | {row['decision']['status']} | {row['decision']['epistemic_ceiling']} | `{row['assessment_hash']}` |\n"
text+='''
RCU's required absence-classification evidence now participates in closure, changing its ceiling to OPEN; its decision remains PROVISIONAL. Other canonical ceilings remain PARTIALLY_VERIFIED. Provenance fields/rules intentionally change output hashes. Hashes bind recorded timestamps/limitations and array order; presentation indentation/key order do not. No wall-clock value participates in derivation. Final deterministic results are in `determinism-results.json`; three reports and records in `outputs/`. The fresh procedural ledger is `procedural-final/ledger.yaml`.

## CI authority

'''
for run in ci:
 text+=f"- [{run['event']} run {run['databaseId']}]({run['url']}), head `{run['headSha']}`, completed **{run['conclusion']}**; job {run['jobs'][0]['databaseId']}.\n"
text+='''
The workflow was inspected and left unchanged; see `workflow-review.md` and `ci-results.json`. API success on automated steps is real execution evidence, but is not a successful whole-workflow conclusion. Raw logs and uploaded artifacts could not be downloaded (EOF; actual nonzero exits recorded, signed URLs redacted). No exact remote test count, kernel run or detailed remote procedural cause is asserted. The successful-CI prerequisite for a VERIFIED fix remains outstanding; the prescribed pending disposition is used conservatively even though the current attempt has completed FAIL.

## Finding dispositions

'''
text+='| Finding | Disposition | Observation |\n|---|---|---|\n'+''.join(f"| {f['id']} | {f['disposition']} | {f['observation']} |\n" for f in findings)
text+='''
## Final gate matrix

| Gate | Status | Scope / executed evidence |
|---|---|---|
'''+''.join(f'| {a} | {b} | {c} |\n' for a,b,c in matrix)
text+='''
## Evidence and next boundary

`environment.yaml` records exact Python/OS/architecture/dependencies, source commit/branch and an allowlisted environment; `commands.log` and `command-records.jsonl` contain command, stdout, stderr and actual exit information. `hash-manifest.yaml` covers remediation evidence and qualification outputs, plus relevant source files; it explicitly excludes itself to avoid recursive hashing. `preserved-evidence.json` is the original immutability snapshot. Source AST/boundary review is in `trust-boundary-review.json`; it is not a security certification. Repeatable harnesses write only remediation output, never frozen prior evidence.

Next work must establish authentic, relevant observation/source artifacts and reconcile contradictory facts; obtain independent human calibration and real scoped kernel/compiler/sanitizer observations; resolve outcome scope terminology and historical provenance; and establish upstream criterion validity. A general evaluator or an NLP heuristic is not silently added to pretend those gaps are solved. Release remains BLOCKED even though the executed bounded software regressions pass.
'''
(E/'REPORT.md').write_text(text)
print('Built required environment/findings/regression-results/REPORT from observed receipts: 564 tests, 445 new, 15 dispositions, release BLOCKED.')
