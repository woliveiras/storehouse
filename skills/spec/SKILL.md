---
name: spec
description: Create, discover, maintain, and formally reconcile software specifications through metadata-first routing, stable acceptance criteria, behavior/oracle matrices, explicit oracle provenance, durable evidence, and phased SDD review. Use when a user or repository explicitly chooses Specification-Driven Development; do not use for ordinary baseline implementation that does not request a persistent specification.
---

# Spec

Treat SDD as an optional methodology and keep the specification as the active source of intended behavior.

1. Discover candidate specifications metadata-first with [metadata guidance](./references/metadata.md), then read the complete governing specification before implementation or review.
2. Resolve or expose contradictions without letting tests or implementation silently redefine intent.
3. Maintain compact routing metadata, stable acceptance criteria, invariants, exclusions, authority, compatibility, recovery behavior, and unresolved decisions. Use [the spec template](./assets/spec-template.md) only when no repository convention exists.
4. Create the separate [behavior/oracle matrix](./references/behavior-matrix.md) before the new implementation is shown to its reviewer. Classify each oracle's provenance with [provenance guidance](./references/provenance.md).
5. Keep the specification, matrix, tests, implementation, durable documentation, and [evidence](./assets/evidence-template.md) reconciled through [formal SDD review](./references/review-contract.md) and [reconciliation](./references/reconciliation.md).
6. Preserve authority boundaries and report contradictions or missing decisions instead of inventing policy.

The skill works independently. When an installed TDD capability is available, hand it approved behavior, invariants, and matrix rows; when an installed review capability is available, hand it the governing input, expected behavior, tests, complete diff, fresh results, and risks. These optional capability handoffs create no runtime dependency and require no copied companion skill.
