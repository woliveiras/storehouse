# PostgreSQL query review

1. Confirm result semantics with representative rows, nulls, duplicates,
   boundaries, concurrency, and authorization/tenant predicates.
2. Review joins, filters, aggregation, windowing, ordering, limits, and pagination
   before looking for speedups.
3. Identify transaction/isolation assumptions and the locks produced by reads
   and writes.
4. Map predicates and orderings to existing indexes; do not prescribe an index
   without considering selectivity, write cost, and real plan evidence.
5. Prefer bound parameters and reviewed identifiers. Values can be parameterized;
   dynamic identifiers require a safe allowlist/composition boundary.
6. For writes, analyze affected rows, idempotency, conflict behavior, triggers,
   foreign keys, and rollback.
7. Return findings ordered by correctness, data loss/security, concurrency,
   operational risk, and measured performance.

Primary references:

- https://www.postgresql.org/docs/current/queries.html
- https://www.postgresql.org/docs/current/explicit-locking.html
- https://www.postgresql.org/docs/current/indexes.html

