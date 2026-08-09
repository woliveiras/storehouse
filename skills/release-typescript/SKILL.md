---
name: release-typescript
description: "Prepare and verify TypeScript or JavaScript package releases with package metadata, exports, types, semantic versions, packed artifacts, provenance, and registry-readiness evidence. Use when releasing an npm-compatible library, CLI, or package. Do not use for ordinary TypeScript CI or tag, push, npm publication, upload, or deployment without explicit authority."
---

# TypeScript Release

1. Inspect package manager/lockfile, package name/access, version source,
   engines, module formats, exports, types, files, lifecycle scripts, and target
   registry.
2. Require frozen install, types, lint, tests, security policy, and production
   build gates from CI.
3. Create the registry tarball without publishing; inspect contents, metadata,
   source maps, declarations, executable bits, licenses, and accidental secrets.
4. Install the tarball in representative clean consumers and test import,
   require, types, and CLI behavior as applicable.
5. Record hashes, packed size, compatibility changes, release notes, and a
   trusted-publishing/provenance design when supported.
6. Keep tags, pushes, npm-compatible publication, uploads, and deployment
   withheld until explicitly authorized.

