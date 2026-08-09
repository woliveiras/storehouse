---
name: release-ai-eng
description: "Prepare and verify versioned AI engineering release candidates spanning model integrations, agents, RAG pipelines, prompts, tool contracts, policies, evaluation evidence, and rollback controls. Use when packaging or assessing an AI-system release. Do not use for ordinary CI, model training, or tag, push, provider change, publication, rollout, deployment, or production mutation without explicit authority."
---

# AI Engineering Release

Release the complete AI behavior contract, not only the application binary or a
model name.

## Establish the release unit

1. Identify the user-visible capability, version source, target environments,
   owning services, supported providers/models, and deployment boundary.
2. Inventory prompts, routing/model configuration, structured-output and tool
   schemas, authority policies, agent state/checkpoint formats, retrieval schema
   and embedding versions, evaluation corpus/evaluators, application code, and
   infrastructure assumptions.
3. Classify each input as immutable release content, environment configuration,
   sensitive secret, external provider dependency, durable source data, or
   rebuildable derived artifact.
4. Define compatibility for API/tool schemas, persisted agent state, vector
   dimensions and embedding migrations, index rebuilds, clients, and previous
   application versions.

## Build and verify the candidate

1. Require the applicable CI gates and complete evaluation result for the exact
   candidate fingerprint. A partial or stale model evaluation is not release
   evidence.
2. Produce a manifest covering code, prompts, policies, model/router settings,
   schemas, data/index versions, dependencies, evaluator/corpus versions, and
   generated artifacts with hashes where the artifact is locally owned.
3. Verify representative quality, safety, privacy, prompt-injection, tenant
   isolation, tool-authority, failure/recovery, latency, throughput, and cost
   budgets at the depth required by the release risk.
4. Recheck provider/model availability, regional and data-processing constraints,
   rate limits, deprecations, fallback behavior, and quota assumptions without
   silently changing the approved candidate.
5. Inspect logs, traces, examples, and evaluation artifacts for secrets, personal
   data, protected prompts, canaries, and unsafe retention before distribution.
6. Define rollout controls: observability, alert thresholds, kill switch,
   provider/model fallback, configuration rollback, index/data recovery,
   checkpoint compatibility, and who may activate each action.
7. Record limitations, known regressions, manual acceptance, migration order,
   rollback constraints, and actions still withheld.

Live provider/model calls still require an explicit budget and authority. Keep
tag, push, publication, provider configuration mutation, traffic rollout,
deployment, and production data/index changes withheld until the user authorizes
that exact operation.

## Output

- Versioned AI release manifest and candidate fingerprint
- Compatibility, evaluation, safety, latency, and cost evidence
- Migration, rollout, observability, and rollback contract
- Explicitly authorized and withheld release actions
