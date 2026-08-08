# SPEC-0001 isolated specification review

## Context considered

- The complete user objective and authority boundaries.
- `spec.md`, `behavior-matrix.md`, `plan.md`, and `tasks.md` only.
- No tests, destination implementation, or implementation diff.
- Review performed by isolated runtime reviewer `/root/spec_review`.

## Initial findings and reconciliation

| Severity | Finding | Reconciliation |
| --- | --- | --- |
| P1 | Normative migrated, excluded, and collection sets were not enumerated | Added exact 33, 16, and 20 name sets and equality oracles |
| P1 | Composition variants omitted baseline, minimum/full Tuxedo, and current/proposed contracts | Added distinct variants, applicability, technical non-viability, and per-variant oracles |
| P1 | Behavior writes lacked protected hashes and outside sentinels | Added both controls to every write-capable behavior trial |
| P1 | Sensitivity could be under-classified | Added a complete normative 21-sensitive/12-non-sensitive classification with domains and rationale |
| P1 | Isolation did not enumerate contamination, cloud sharing, symlinks, or network | Added fail-closed surface list, real-entry rule, sharing prohibition, and per-case network declaration |
| P2 | Tree digests and initial worktree baselines were not reproducible | Added byte-exact digest algorithm and exact initial porcelain snapshots |
| P2 | Geremmyas-specific hooks/instructions/commands were not dispositioned | Expanded reference-disposition and portability oracles |
| P2 | Matrix required 33 implicit cases despite conditional applicability | Made implicit coverage conditional with a mandatory per-skill justification |
| P2 | MIT provenance was inferred from authorship | Added frozen Git-object license hash/scope inspection and notice exceptions |
| P1 | Repository-only write authority contradicted clean-room scratch and dedicated eval home requirements | Separated persistent product writes, disposable resolved scratch, and explicit-login-only dedicated home state |

## Final review

- Spec: no findings.
- Standards: no findings.
- Risk: no findings blocking fail-first test design.
- Decision: approved for fail-first verification and implementation.

The review record documents the reconstructed context and findings. It does not
mechanically prove semantic completeness or chronology.
