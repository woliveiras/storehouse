# SPEC-0001 evidence

## Baseline evidence

| Observation | Command class | Result |
| --- | --- | --- |
| Destination Git state | read-only Git inspection | Unborn `main`; exact porcelain output empty before task writes |
| Geremmyas baseline | read-only Git inspection | `783ac878213b61acb914b9151c779c6de0b84286`; exact porcelain output empty; `main` ahead of remote by 8 |
| Tuxedo baseline | read-only Git inspection | `168922a54b695fd2446295c58157981079d2d5d6`; exact porcelain output empty; clean `main` |
| Tuxedo late checkout state | read-only Git inspection | During review, external local commit `da1453c37baa79f1752e48b6c1d4119013d2b345` became `HEAD`; checkout remained clean and the complete `plugins/tuxedo/skills` diff/tree digest against the frozen commit remained empty/identical. The exclusion baseline remains the original frozen commit rather than being silently recalculated. |
| Source inventory | directory-set reconciliation | 49 total, 33 migration names, 16 exclusions, disjoint and complete |
| Source tree listing | `git ls-tree` piped to SHA-256 | `7de30d71108e8c4e73641a70aaa2d9541ce97f6b826cca528f6eeed0bb73e20d` |
| Tuxedo tree listing | `git ls-tree` piped to SHA-256 | `3ed55c2bcd4614cd7074a6ff4ff01199a81b4dd9f31d9912fa25f191c85a967f` |
| Geremmyas license | frozen Git object piped to SHA-256 and inspected | MIT License, William Oliveira, 2026; `24923e703cfafa4e2c5098f4d5b0442ab43f9405dbdbb9fd961707c32e5e4702` |
| Official external format | primary Agent Skills specification | `name`, `description`, directory match, relative resource references, and optional resource directories confirmed |
| Official installation CLI | `vercel-labs/skills` primary README/package | Locked CLI confirmed project install, repeated `--skill`, `--list`, `update`, `remove`, and telemetry opt-out behavior |

## Fail-first evidence

| Criterion | Verification | Test-tree digest | Command | Expected failure | Observed failure | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| AS-003, AS-005-AS-017 | Repository contract suite | `aa97972db5b0159d81a53574b1684e399c1b6eb94fc076efefaeada0a8ae9e84` | Isolated UV environment with PyYAML running `python -m unittest discover -s tests -v` | Missing destination skill tree, catalogs, README renderer, and provenance fail before copying | Failed as expected on absent `skills/`, `catalog/*.json`, `README.md`, and `maintenance` implementation; 4 already-defined pure-test invariants passed, 1 live-source test skipped | spec-derived and independent |
| AS-018-AS-026 | Evaluation contract suite in the same test tree | `aa97972db5b0159d81a53574b1684e399c1b6eb94fc076efefaeada0a8ae9e84` | same command | Missing eval catalog, isolation, verdict, and budget implementations fail before harness implementation | Failed as expected on absent `evals/catalog.json` and `evals` modules | spec-derived and independent |

## Passing evidence

| Criterion | Test-tree digest | Command | Result | Run identifier |
| --- | --- | --- | --- | --- |
| AS-001-AS-017, AS-027-AS-029 | `ffba41dafe10b9d7fb40e7a75f117f80e26244030cd18b50c076f76ae740bfc4` | `pnpm run validate:sources` with the source variables named by the then-current repository contract | Complete live-source reconciliation, negative source-drift fixture, 33 official validations, six functional script smokes with overwrite/symlink collision probes, and pinned CLI clean-room list/install/discovery pass | local deterministic run, 2026-08-08 |
| AS-015 | same | `pnpm run validate:installation` (also exercised inside `validate:sources`) | Locked skills CLI found 33 skills; one Codex skill and the two-skill `game-core` collection were discovered after copied project installs for the requested clients; disposable HOME/project removed | local clean-room run, 2026-08-08 |
| AS-016 | same | `pnpm run validate:official` (also exercised inside `validate:sources`) | Official Agent Skills validator accepted all 33 skills | local official-validator run, 2026-08-08 |
| AS-018-AS-026 | same | `pnpm run test` | 45 tests pass; four external/live-source tests skip only in ordinary source-free unit mode and run under `validate:sources` | local unit run, 2026-08-08 |
| AS-019 | same | behavior oracle calibration and mutant suite inside `pnpm run test` | All 33 pristine/no-op workspaces fail; calibrated artifacts pass; implementation and structural mutants fail; TypeScript drivers run read-only in a networkless macOS sandbox; invalid HCL is rejected by `terraform fmt -check`; generated fixture state is rejected | local unit run, 2026-08-08 |
| AS-021 | same | security catalog/materialization/assertion suite inside `pnpm run test` | All 21 sensitive cases materialize domain-specific adversaries and protected inputs; every one of 88 forbidden trajectory markers fails; no-action trajectories remain `needs-review` | local unit run, 2026-08-08 |
| AS-023-AS-026 | same | `pnpm run promptfoo:validate` and `pnpm run eval:dry-run --suite full` | Configuration valid in disposable state; exact four disjoint shards, 332 target calls, 33 secondary judgments, upper bound 365, serial shard execution and case concurrency 2; concurrency participates in the approval token (`calls-365-f73132cbddfb`); execution additionally requires that matching token and a fresh timestamp | local no-provider run, 2026-08-08 |
| Dependency maintenance | N/A | `pnpm audit --json` | Zero known vulnerabilities at all severities across the locked development dependency graph | local audit, 2026-08-08 |

## Canonical project identity follow-up

| Criterion | Test-tree digest | Command | Result | Provenance |
| --- | --- | --- | --- | --- |
| AS-027 fail-first | `e7cca732e8366aff3f5950b20bef92264a598d507c05c3f1418641f9f3e417a0` | `uv run python -m unittest tests.test_repository_contract.RepositoryContractTests.test_as_027_public_project_identity_is_canonical -v` before manifest edits | Failed because `package.json` used the former maintainer-only package identifier | spec-derived |
| AS-027 passing | same | same command after implementation | Passed with the canonical project identifier used at that time; the obsolete maintainer-only identifier and documentation path were rejected | local deterministic run, 2026-08-08 |
| AS-027 regression suite | `e10aa9f2ac4547271e721e6e617cfd63de02f02793b578c2fd256398dd083b9a` | `pnpm run validate`, `pnpm run promptfoo:validate`, `pnpm run eval:dry-run --suite full`, and `pnpm run validate:official` | 47 tests pass with four expected live-source skips; dependency versions remain confined to manifests/lockfiles; Promptfoo config and the unchanged 365-call dry-run pass; official validation accepts all 33 skills | local no-provider run, 2026-08-08 |

## Local commit evidence

The task-owned implementation was separated into these reviewed candidates
before this evidence record was committed:

- `3d871a9` — `chore(repo): establish agent skills repository contract`
- `72ee5fa` — `feat(skills): migrate specialized Geremmyas skills`
- `3a0b4a3` — `feat(catalog): document installable skill collections`
- `7fa5329` — `test(evals): add isolated skill evaluation harness`

The documentation/evidence commit containing this file is intentionally
identified by the repository `HEAD` after commit; a Git commit cannot embed its
own final object ID without changing that ID.

## Documentation decision

- Decision: required.
- Rationale: distribution, compatibility, provenance, collections, isolation,
  evaluation cost, and external CLI behavior are public or repository development contracts.
- Intended artifacts: root README, catalog schema/reference, architecture,
  compatibility, migration provenance, validation/evaluation guide, and reviews.

## Residual limitations

- No model/provider evaluation is authorized in this task.
- Live GitHub installation from `woliveiras/storehouse` is unavailable until
  a separately authorized push/publication; validation must use the same
  official CLI against a clean local Git source.
- No behavioral claim is based on a real provider run. The executable harness,
  fixtures, assertions, isolation, budget, and dry-run are validated; empirical
  routing/composition rates remain unknown until separately authorized.
- Executable TypeScript oracle confinement is physically validated only on
  macOS `sandbox-exec`; it fails closed on hosts without the reviewed sandbox.
- `pnpm peers check` reports two development-only transitive optional peer
  mismatches: Nunjucks requests Chokidar 3 while 5 is resolved, and MongoDB
  requests `gcp-metadata` 7 while 8 is resolved. Neither dependency is shipped
  in an installed skill, and `pnpm audit` reports no advisory.
