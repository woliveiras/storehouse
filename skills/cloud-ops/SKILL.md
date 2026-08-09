---
name: cloud-ops
description: "Prepare, review, or perform scoped Google Cloud or AWS operations with explicit identity, target, authority, rollback, and verification. Use when inspecting or changing supported cloud resources through gcloud, Google Cloud APIs, AWS CLI, or AWS APIs. Do not use for provider-neutral Terraform changes, ambiguous accounts/projects, or production mutation without explicit authority."
---

# Cloud Operations

Operate supported cloud providers through one safety contract and a
provider-specific translation.

## Process

1. Identify provider, account or project, principal, region/zone, environment,
   resource, and requested outcome.
2. Inspect active configuration without assuming defaults are correct.
3. Start with read-only identity and resource discovery.
4. State the exact command or API operation, consequences, permission needs,
   billing impact, rollback, and verification.
5. Execute local, disposable, or explicitly authorized remote mutations only
   within the confirmed target. Treat ambiguity as protected.
6. Keep credentials, tokens, profiles, key files, and kubeconfigs out of source,
   logs, and generated artifacts.
7. Verify the observed resource state and report withheld production actions.

## Provider references

- For Google Cloud projects, accounts, impersonation, and `gcloud`, read
  [google-cloud.md](references/google-cloud.md).
- For AWS accounts, roles, profiles, regions, and the AWS CLI, read
  [aws.md](references/aws.md).

Other providers are outside the current supported contract.

## Authority

Production delete, deploy, IAM, organization policy, billing, service
enablement, key rotation, and other consequential remote mutations require
explicit authority for that exact operation.

