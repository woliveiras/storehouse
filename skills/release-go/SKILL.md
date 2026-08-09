---
name: release-go
description: "Prepare and verify Go module or binary releases with semantic versions, module compatibility, reproducible cross-platform artifacts, checksums, and release notes. Use when releasing a Go library, CLI, or service artifact. Do not use for ordinary Go CI, a version bump alone, or tag, push, registry publication, upload, or deployment without explicit authority."
---

# Go Release

1. Determine module/library/binary shape, Go/tool pins, supported platforms,
   version source, compatibility policy, and distribution channels.
2. Require formatting, vet/static analysis, tests, vulnerability policy, and
   build gates from CI.
3. For modules, validate public API compatibility, module path, tags, examples,
   license, and proxy-visible contents.
4. For binaries, build declared target tuples from locked inputs and record
   embedded version/commit metadata without harming reproducibility.
5. Inspect archives, licenses, SBOM/provenance when required, checksums, and a
   minimal executable smoke path.
6. Prepare release notes and rollback/yank guidance appropriate to the channel.
7. Keep tags, pushes, Go proxy publication, GitHub releases, uploads, registries,
   and deployment withheld until explicitly authorized.

