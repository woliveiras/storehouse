---
name: ci-terraform
description: "Design or review continuous integration for Terraform configuration with formatting, initialization, validation, lint/security policy, plans, artifacts, and approval boundaries. Use when adding or repairing Terraform CI. Do not use for infrastructure design, direct apply, state mutation, module/provider publication, or non-Terraform IaC."
---

# Terraform CI

Validate proposed infrastructure changes without granting CI implicit apply
authority.

## Process

1. Inspect the pinned Terraform version, providers, lockfile, modules, backend,
   workspaces, environments, and CI trust model.
2. Run formatting, dependency-lock consistency, initialization, validation, and
   repository-selected lint/security/policy checks.
3. Use `terraform init -backend=false` for static validation when backend access
   is unnecessary; use a reviewed isolated backend only when a real plan needs it.
4. Authenticate through short-lived, scoped federation where supported. Never
   expose long-lived cloud credentials to untrusted contributions.
5. Generate plans only for explicit environments and record configuration,
   provider-lock, variable, and source-revision fingerprints.
6. Treat plan files as potentially sensitive; control artifact access and
   retention, and provide a redacted human summary.
7. Require a protected, separately authorized deployment path for apply.
8. Verify failure behavior, concurrency, superseded plans, and stale approvals.

If `infra-terraform` is installed, compose with it for change semantics. This
skill remains standalone and owns only the CI boundary.

