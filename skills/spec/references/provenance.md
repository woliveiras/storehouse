# Oracle provenance

Classify each oracle, not each file:

- `spec-derived`: follows an identifiable approved criterion or invariant.
- `independent`: derived without exposure to the new implementation.
- `implementation-aware`: authored after exposure to the new implementation.
- `external`: comes from a protocol, standard, upstream contract, or verified reference system.
- `diagnostic-probe`: reproduces or localizes a problem but does not establish the final contract alone.

For material testable behavior, include at least one `spec-derived`, `independent`, or `external` oracle. Provenance estimates shared-error exposure; it does not prove correctness.
