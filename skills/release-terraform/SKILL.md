---
name: release-terraform
description: "Prepare and verify versioned Terraform module or provider releases, compatibility, documentation, artifacts, signatures, and registry-readiness evidence. Use when publishing a Terraform module/provider or designing its release automation. Do not use for ordinary Terraform CI, infrastructure apply, state mutation, or tag, push, signing, registry publication, or upload without explicit authority."
---

# Terraform Release

1. Determine module versus provider, registry target, semantic-version policy,
   Terraform/provider compatibility, platform targets, and signing ownership.
2. Require `fmt`, initialization/validation, lock consistency, tests, lint,
   security/policy checks, and documentation generation from CI.
3. For modules, inspect source layout, examples, inputs, outputs, provider
   constraints, submodule paths, license, and registry metadata.
4. For providers, build declared platform artifacts, verify schemas/tests,
   produce checksums, and keep signing keys behind the approved boundary.
5. Verify archives from clean inputs and record hashes, tool versions,
   compatibility changes, upgrade notes, and rollback/yank limitations.
6. Keep tags, pushes, signatures, registry publication, uploads, and release
   creation withheld until explicitly authorized.

