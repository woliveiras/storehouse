---
name: ci-game-dev-2d
description: "Design or review continuous integration for Phaser/Vite and Godot 2D projects, including deterministic tests, headless checks, exports, artifact validation, and safe caching. Use when adding or repairing game CI. Do not use for release versioning, publishing, store submission, gameplay implementation, or deployment."
---

# Game Development 2D CI

Build fast change validation without assuming release authority.

## Process

1. Inspect engine, exact version, package manager, lockfile, export templates,
   repository policy, target platforms, and current CI provider.
2. Separate fast source checks from slower headless/runtime and export checks.
3. For Phaser/Vite, preserve the locked install and run type, lint, unit,
   deterministic simulation, production build, and artifact inspection gates.
4. For Godot, pin the engine/export-template version and run import, headless
   tests, project validation, export, and artifact inspection gates.
5. Cache only rebuildable dependency/import state; keys must include the
   relevant lockfile, engine, and configuration fingerprints.
6. Treat forked or untrusted contributions as unable to access release secrets.
7. Upload only non-secret diagnostic or candidate artifacts with explicit
   retention.
8. Verify that the workflow actually exercises the produced build and reports
   actionable failures.

Keep versioning, signing, publishing, upload to stores, tags, and deployment in
`release-game-dev-2d` when that skill is installed, or explicitly out of scope.

