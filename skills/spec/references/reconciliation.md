# SDD reconciliation

When an accepted correction changes intent, update every affected artifact deliberately:

1. specification metadata, criteria, invariants, exclusions, and authority;
2. behavior/oracle matrix rows and provenance;
3. tests and implementation;
4. public, architectural, API, or operations documentation;
5. evidence and formal review findings.

Do not edit a governing request, bug report, or external contract merely to make implementation pass. If that input cannot be changed, record the conflict and required authority instead of manufacturing consistency.

Git history is the default archive. Keep active SDD artifacts while they govern current behavior or unresolved work; remove fully superseded specifications, matrices, evidence, and review bundles from the current tree when Git can reconstruct them completely.
