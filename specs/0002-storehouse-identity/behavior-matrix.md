# SPEC-0002 behavior and oracle matrix

| Criterion | Scenario | Observable oracle | Provenance | Verification |
| --- | --- | --- | --- | --- |
| SH-001 | Rename the GitHub source | `gh repo view woliveiras/storehouse` succeeds with that exact `nameWithOwner`; `origin` fetch and push URLs are the canonical SSH URL | external | GitHub CLI and local Git inspection |
| SH-002 | Read repository metadata | Node and Python project names equal `storehouse`; schema IDs and human-facing descriptions use Storehouse | spec-derived | Manifest and repository contract tests |
| SH-003 | Copy an install command | Every repository-owned source argument is `woliveiras/storehouse`, and the README collection block equals the catalog renderer | independent | Full-tree identity scan and README snapshot test |
| SH-004 | Run maintenance or an eval dry-run | Repository-specific configuration uses only the `STOREHOUSE`/`storehouse` namespace while generic Agent Skills terminology remains intact | spec-derived | Unit tests, dry-run, config validation, full-tree scan |
| SH-005 | Search the tracked product | The former hyphenated name and uppercase environment prefix have zero occurrences in tracked text | independent | Git-aware text scan with deliberately constructed forbidden tokens |
| SH-006 | Inspect external and Git effects | One authorized GitHub rename and one local commit occur; no push, release, PR, publication, or model call occurs | diagnostic-probe | GitHub metadata, reflog/log, status, and command record inspection |
