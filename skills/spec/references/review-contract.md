# Formal SDD review

Keep three review phases distinct. Record compact findings in the repository's normal review surface; create review files only when its SDD convention explicitly requires them.

1. **Specification review:** inspect the objective, complete specification, criteria, invariants, domain, scope, ambiguity, authority, and risk without using tests or implementation as justification. Establish or challenge the matrix.
2. **Test review:** inspect the approved specification, matrix, provenance, fail-first observation, and tests without using the new implementation as justification. Check mapping, assertion strength, edges, failure paths, and whether a plausible wrong implementation could pass.
3. **Implementation review:** inspect the governing artifacts, tests, complete diff, fresh results, documentation, unrelated changes, rollback, and residual risk.

Passing tests do not cancel a specification, standards, security, compatibility, or evidence finding.
