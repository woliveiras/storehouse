---
id: SPEC-0002
title: Rename the repository product identity to Storehouse
summary: Make Storehouse the canonical repository identity and installation source without changing the Agent Skills format or consumer runtime boundary.
status: active
risk: medium
change_surfaces:
  - GitHub repository identity
  - Git remote configuration
  - repository manifests
  - installation documentation
  - maintenance and evaluation configuration
authority:
  granted:
    - rename the former GitHub repository to woliveiras/storehouse through the GitHub CLI
    - update the local origin to the renamed repository
    - edit task-owned files in this checkout
    - create one atomic local Conventional Commit
  withheld:
    - push
    - release
    - publication
    - pull-request creation
    - model or provider calls
---

# Intent

Adopt **Storehouse** as the single product and repository name. The repository
is the source from which project-specific capabilities are selected through the
official `skills` CLI. “Agent Skills” remains the name of the external format,
not the product name.

This identity change must not add a registry, installer, package manager,
runtime, synchronization layer, or dependency for skill consumers.

# Acceptance criteria

- **SH-001 — Remote identity:** GitHub reports the repository as
  `woliveiras/storehouse`, and local `origin` fetch/push URLs resolve directly
  to that repository.
- **SH-002 — Manifest identity:** Node, Python, UV, schema titles, and repository
  descriptions identify the product as `storehouse` or `Storehouse` as
  grammatically appropriate.
- **SH-003 — Installation identity:** Every repository-owned installation,
  listing, and telemetry example uses `woliveiras/storehouse`; collection
  commands remain deterministically rendered from the catalog.
- **SH-004 — Maintenance identity:** Repository-specific environment variables,
  temporary paths, evaluation homes, canaries, and evaluation labels use the
  `STOREHOUSE`/`storehouse` namespace. Generic references to the Agent Skills
  specification and format remain unchanged.
- **SH-005 — No stale identity:** No tracked text file retains the former
  hyphenated repository name or its former uppercase environment prefix.
- **SH-006 — Authority:** The task performs the authorized repository rename
  and local commit only. It does not push commits, publish, release, create a
  pull request, or call a model/provider.

# Verification

The deterministic repository suite checks SH-002 through SH-005. Fresh `gh`
and `git remote` inspection establish SH-001. Full repository validation,
Promptfoo configuration validation, evaluation dry-run, official validation,
syntax checks, `git diff --check`, and final Git inspection establish that the
identity change preserves existing behavior and SH-006.
