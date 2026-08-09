---
name: release-game-dev-2d
description: "Prepare and verify versioned Phaser/Vite or Godot 2D release artifacts, packaging, delivery configuration, and artifact smoke evidence. Use when producing a candidate build, checksums, export packages, web delivery evidence, or release readiness. Do not use for ordinary CI, gameplay implementation, or publication, upload, tag, push, store submission, or deployment without explicit authority."
---

# Game Development 2D Release

Produce a reproducible candidate artifact and verify the artifact users would
receive.

## Establish the release contract

1. Inspect engine and exact version, package manager, lockfile, export presets,
   target platforms, version source, hosting/store constraints, and secrets.
2. Define artifact names, supported platforms, public configuration, acceptance,
   rollback, and save/cache compatibility.
3. Read [release-pipeline.md](references/release-pipeline.md).
4. For Phaser, read [phaser.md](references/phaser.md); for Godot, read
   [godot.md](references/godot.md).

## Build and verify

1. Require the relevant source checks and CI result; rerun only what the release
   contract needs locally.
2. Build from declared inputs with production configuration.
3. Inspect contents, licenses, sizes, accidental secrets, hashes, and provenance.
4. Serve, install, or unpack the artifact through the real delivery path.
5. Run the minimal playable smoke route and inspect logs, assets, input, audio,
   saves, resize/focus, and exit behavior as applicable.
6. Record artifact paths, checksums, tool versions, gaps, and manual acceptance.

Keep publish, upload, tag, push, store submission, and deployment withheld until
the user authorizes that exact operation.

