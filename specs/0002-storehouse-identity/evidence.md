# Storehouse identity evidence

## Preconditions and remote mutation

| Criterion | Evidence | Result |
| --- | --- | --- |
| SH-001, SH-006 | `git status --short`, branch, remote, and log inspection before mutation | Clean `main`; `origin` used the former repository URL; no unrelated destination changes |
| SH-001 | `gh auth status` and `gh repo view` before mutation | Authenticated as `woliveiras`; source was a private, non-archived repository; `woliveiras/storehouse` was not visible |
| SH-001 | `gh repo rename storehouse --repo <former-owner-source> --yes` | Authorized GitHub rename succeeded |
| SH-001 | `git remote set-url origin git@github.com:woliveiras/storehouse.git` followed by `gh repo view`, `git remote -v`, and `git ls-remote origin` | GitHub reports exact `nameWithOwner` `woliveiras/storehouse`; fetch and push URLs resolve directly to the canonical SSH URL |

The local checkout directory was deliberately not renamed. It is outside
tracked repository identity and outside the authorized write root for creating
a sibling checkout path.

## Fail-first and passing oracles

| Criterion | Command | Result | Provenance |
| --- | --- | --- | --- |
| SH-002-SH-005 fail-first | focused repository identity, stale-name scan, and README/catalog tests before implementation | Three failures on the former manifest identity, 35 stale tracked references, and former README source commands | spec-derived and independent |
| SH-002-SH-005 passing | same three focused tests after implementation | 3/3 pass | local deterministic run |
| SH-002-SH-005 | full-tree search for the constructed former hyphenated name and uppercase environment prefix | Zero tracked or untracked text occurrences | independent |

## Regression evidence

| Criterion | Command | Result |
| --- | --- | --- |
| SH-002-SH-005 | `pnpm run validate` | 48 tests pass with four expected source-free skips; 33 official validations and deterministic validation pass |
| SH-002-SH-005 | source-aware validation with absolute Storehouse source environment variables | 48 tests pass without skips; source reconciliation, clean-room installation, 33 official validations, and deterministic validation pass |
| SH-003 | `pnpm run validate:installation` | Locked CLI validates one individual skill and `game-core` in disposable project homes for the requested clients; personal configuration untouched |
| SH-004 | `pnpm run promptfoo:validate` | Configuration valid in disposable local state |
| SH-004 | `pnpm run eval:dry-run --suite full` | 332 target trials plus 33 secondary judgments; upper bound 365; no provider invocation |
| SH-002-SH-004 | `pnpm run validate:official` | 33/33 skills accepted by the official validator |
| SH-004 | AST parsing for repository Python plus shell-file discovery | 23 Python files parse; no shell files require syntax checking |
| SH-005-SH-006 | `git diff --check` and final Git/GitHub/source inspection | Diff check passes; target changes are task-owned; Storehouse remote/URL are canonical; Geremmyas and Tuxedo statuses remain clean |

Two preliminary dry-run invocations exited before execution because the suite
argument was absent or separated by an extra literal `--`. The documented PNPM
examples were corrected to the verified `pnpm run eval:dry-run --suite <name>`
form. Neither attempt reached authentication or a provider.

No model/provider evaluation, push, release, publication, or pull request was
performed.
