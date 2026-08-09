---
name: release-python
description: "Prepare and verify Python package releases with metadata, versions, sdists, wheels, compatibility, reproducible builds, and registry-readiness evidence. Use when releasing a Python library, CLI, or distributable application package. Do not use for ordinary Python CI or PyPI/TestPyPI upload, tag, push, publication, or deployment without explicit authority."
---

# Python Release

1. Inspect `pyproject.toml`, build backend, version source, Python classifiers,
   dependencies/extras, package data, license, and supported platforms.
2. Require locked CI checks and build the sdist and expected wheels in an
   isolated environment.
3. Inspect archive contents and metadata, then install artifacts into clean
   environments and run import/CLI smoke checks.
4. Validate sdist-to-wheel reproducibility expectations, compiled extension
   platform tags, and dependency floors/ceilings.
5. Record hashes, artifact sizes, build environment, changelog, and compatibility
   gaps; use a trusted-publishing design when the target registry supports it.
6. Keep tags, pushes, TestPyPI/PyPI upload, publication, and deployment withheld
   until explicitly authorized.

