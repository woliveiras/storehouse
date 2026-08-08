# Specification review

## Spec

The specification names one canonical product, separates that identity from
the Agent Skills format, covers both remote and tracked local surfaces, and
keeps the repository's no-runtime product boundary intact. The acceptance
criteria are observable without relying on the proposed implementation.

## Standards

The change preserves the official `owner/repository --skill <name>` install
model and the existing UV/PNPM maintenance conventions. Remote mutation is
limited to the explicitly authorized GitHub rename.

## Risk

The main risks are stale install URLs, a redirected rather than canonical local
remote, and partial namespace changes in maintenance tooling. SH-001, SH-003,
SH-004, and SH-005 address those risks directly. Renaming the local checkout
directory is outside this specification because it is not part of GitHub or
tracked repository identity.
