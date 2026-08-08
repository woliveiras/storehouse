# Code review

## Spec

The diff makes Storehouse the visible product, repository slug, manifest name,
schema source, install source, maintenance namespace, evaluation namespace, and
temporary-state prefix. Generic Agent Skills format terminology remains intact.
No skill content, collection membership, dependency version, or consumer
runtime behavior changes.

## Standards

Install commands remain generated from `catalog/collections.json`; Node and
Python metadata agree; UV and PNPM remain the only maintenance package tools;
the official skill validator still accepts all 33 skills. The GitHub mutation
used the requested GH CLI, and `origin` resolves directly to the new SSH URL.

## Risk

No stale tracked identity, broken relative link, duplicated Tuxedo skill,
Geremmyas dependency, runtime dependency, or credential-bearing artifact was
found. The renamed evaluation namespace intentionally invalidates any ad hoc
shell environment using the former variable names; documentation and tests now
describe the canonical namespace. The repository remains private and has no
pushed branch, so live installation from GitHub is not yet available.
