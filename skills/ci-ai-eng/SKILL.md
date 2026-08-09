---
name: ci-ai-eng
description: "Design or review continuous integration for AI engineering systems, including model integrations, agents, RAG pipelines, prompts, tool schemas, evaluation suites, safety checks, and bounded provider tests. Use when adding or repairing CI for AI behavior or artifacts. Do not use for ordinary application CI alone, model training infrastructure, release promotion, deployment, or live provider/model calls without an explicit budget and authority."
---

# AI Engineering CI

Validate AI-system changes without turning ordinary CI into an unbounded model
experiment or a release path.

## Process

1. Inventory the changed AI contract: prompts, model/router configuration,
   structured outputs, tools and authority, agent state, retrieval/ingestion,
   evaluation corpus, policies, and user-visible fallbacks.
2. Record exact dependency, prompt/configuration, schema, corpus, fixture, and
   evaluator revisions so results identify what was tested.
3. Run deterministic gates first: formatting, types, unit/integration tests,
   prompt/template parsing, schema compatibility, tool-policy checks, retrieval
   invariants, fixture integrity, secret scanning, and build/package checks.
4. Exercise model boundaries offline with fakes, recorded responses, or local
   deterministic fixtures where they preserve the behavior under test. Never
   present mocks as provider-quality evidence.
5. Define provider/model evaluation cases from independent expected behavior,
   including normal, edge, failure, adversarial, privacy, refusal, tool-denial,
   cross-tenant, and recovery scenarios as applicable.
6. Require an exact call and cost ceiling, explicit execution flag, isolated
   credentials, sanitized inputs, concurrency limit, timeout, and matching human
   authorization before any live provider/model evaluation.
7. Treat nondeterminism explicitly: predefine scoring, aggregation, sample size,
   retry policy, thresholds, and incomplete-result handling. Do not retry until a
   preferred answer appears or weaken an oracle to accept current behavior.
8. Store only bounded, sanitized evidence with configuration fingerprints,
   per-case outcomes, aggregate results, unavailable checks, and retention.
9. Keep secrets and privileged tools unavailable to fork-controlled code; use
   least privilege and protect any authorized provider-evaluation environment.
10. Verify that a failed, partial, timed-out, or unevaluated suite cannot be
    reported as green.

Keep versioning, release manifests, signing, publication, rollout, and deployment
in `release-ai-eng` when that skill is installed, or explicitly out of scope.

## Output

- Trigger, trust, permission, secret, cache, and artifact boundaries
- Deterministic and model-backed check mapping
- Evaluation budget, oracle, aggregation, and incomplete-result contract
- Sanitized evidence and explicit withheld actions
