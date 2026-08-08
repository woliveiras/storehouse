# SPEC-0001 implementation plan

1. Freeze and reconcile the three-repository baseline; record primary external
   contracts for Agent Skills and the `skills` CLI.
2. Review this specification without tests or implementation, reconcile all
   actionable findings, and keep the approved criteria stable.
3. Write fail-first deterministic tests for inventory, skill format, recursive
   disposition, collections, README commands, isolation, eval coverage, and
   verdict privacy.
4. Migrate and adapt the 33 specialized skill trees; record provenance and
   compatibility per skill.
5. Add the declarative collections catalog, README command block, architecture,
   compatibility, migration, and validation documentation.
6. Add the maintainer-only evaluation catalog, fixtures, mocks, provider bridge,
   Promptfoo configuration, isolated runner, budget gate, sanitized checkpoints,
   and all requested command aliases.
7. Run official validators, deterministic suites, clean-room CLI discovery,
   dry-runs, syntax/link checks, and `git diff --check` without model calls.
8. Reconstruct test review without implementation, then code review from the
   complete candidate and fresh evidence. Repair in-scope findings.
9. Commit coherent task-owned slices locally with Conventional Commits and
   verify all three final Git states.
