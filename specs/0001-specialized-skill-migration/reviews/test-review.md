# SPEC-0001 isolated test review

## Context considered

- The complete specification and behavior/oracle matrix.
- Tests, eval catalogs, fixtures, independent verifiers, and maintenance gates.
- No new destination implementation was accepted as the source of truth.
- Review performed by isolated runtime reviewer `/root/test_review` across
  iterative frozen snapshots; the reviewer did not edit files or execute
  project code.

## Findings and reconciliation

| Severity | Finding | Reconciliation |
| --- | --- | --- |
| P1 | Behavior oracles trusted token samples and self-reported JSON | Added independent semantic inspection of implementation/configuration artifacts, no-op rejection, and mutants that corrupt implementation while leaving reports intact |
| P1 | Official CLI and validator tests were mocked only | Added real conditional external tests activated by the mandatory live-source gate; retained unit tests for command construction and exact 33-call routing |
| P1 | Security cases shared one generic canary attack | Added 21 domain-specific stimuli, protected every input, required structured action trajectories, and tested all 88 forbidden markers |
| P2 | Owned scripts were exercised only with `--help` | Added functional temporary-image executions for all five art scripts and a strict synthetic bibliography validation |
| P2 | Source reconciliation could skip and lacked a negative | Kept source-free unit mode explicit; the mandatory live-source command enables external tests and proves a mutated source skill is rejected |
| P2 | Portability and game-scope scans were narrow | Expanded scans to every decodable skill resource and every game-skill file |
| P2 | Eval-home allowlist, sanitization, and budget tests had gaps | Added allowed-entry symlink and unknown-config rejection, broader auth non-read guards, Promptfoo nested-secret probes, exact case-ID equality, and wrong/exact approval-token checks |
| P2 | A Gradle cache contaminated one controlled fixture | Moved `.gradle/` to Trash and added a fixture-wide generated-state prohibition |
| P1 | Several behavior tests were token-only or internally inconsistent | Added executable read-only Node drivers under a networkless macOS sandbox, strict Godot truth-table/ordering checks, self-contained save behavior, valid React Router/XState fixtures, and structural mutants |
| P1 | Terraform accepted malformed HCL | Added `terraform fmt -check` as an external syntax/format oracle and an invalid-HCL mutant |
| P1 | Executing generated tests could escape or mutate evidence | Denied network, process forks, HOME reads, and every file write in the driver sandbox; added outside-sentinel and intraworkspace mutation probes and repeated protected hashes after verification |

## Final review

## Spec

No material findings remain.

## Standards

No material findings remain. The behavior artifacts now have observable,
fail-closed checks proportional to the available local runtimes.

## Risk

No material findings remain in the static test review. The reviewer did not run
project code; the maintainer evidence records the fresh 45-test execution.

**Final verdict: approved.**
