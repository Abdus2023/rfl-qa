# Behavioral rubric

The three `competency/*.yaml` matrices are authoritative. Read the artifact without the other assessor's evaluation. For each behavior, record its ID, DEMONSTRATED/FAILED finding and resolvable evidence references. Do not supply a level solely because an artifact is merged or a contributor has seniority.

Levels are cumulative. A level requires every behavior up to that level and no failed required behavior. The machine computes the highest fully supported level and preserves the assessor's original claim separately. E4 with L2 behaviors remains L2. Passing a lower level does not erase a higher-level failed behavior or a hard gate.

Classify each invariant's origin (A/B/C/D), knowledge state, and evidence strength separately. Pin provides address stability only under its API contract; refcounts require a correct acquisition/release protocol. Compiler acceptance alone does not prove a wrapper sound. Runtime diagnostics are observations over a population, not universal guarantees. Identify the external unregister/drain/allocator assumptions explicitly.

For every oracle check supply an executed finding with evidence or NOT_RUN. An unexecuted check cannot be represented as PASS. A finding of safety failure must be recorded in structured defect/hard-gate fields. Do not suppress findings because another test passed.

Training keys and examples are synthetic. For live assessment replace fixture:// references with reviewable artifacts; record kernel, toolchain, configuration, environment, workload and excluded contexts. The alpha fixtures' x86_64/PREEMPT_RT scope cannot justify ARM64, DMA, NMI or generic kernel expertise.
