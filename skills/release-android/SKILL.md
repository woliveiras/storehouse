---
name: release-android
description: "Prepare and verify Android application release candidates, versioning, signing boundaries, AAB/APK artifacts, obfuscation outputs, and store-readiness evidence. Use when creating an Android release or release automation. Do not use for ordinary Android CI, debug builds, or signing, uploading, publishing, rollout, or production deployment without explicit authority."
---

# Android Release

1. Confirm application ID, variant, version code/name, SDK/toolchain pins,
   distribution channel, signing owner, and rollback/update constraints.
2. Run the required CI gates and build the release AAB or APK from locked inputs.
3. Keep signing material outside source and logs; use the repository's approved
   local, CI, or store-managed signing boundary.
4. Inspect manifest, permissions, native ABIs, resources, R8 mapping, dependency
   metadata, artifact size, and accidental secrets.
5. Verify signatures and install or inspect a representative generated APK when
   the release contract requires device-level evidence.
6. Record artifact hashes, mapping/native symbol files, tool versions, CI source
   revision, and manual store/device checks.
7. Keep Google Play or other Android-store upload, track rollout, promotion,
   tag, push, and publication withheld until explicitly authorized.
