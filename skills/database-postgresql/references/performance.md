# PostgreSQL performance

- Reproduce on representative schema, data distribution, statistics, parameters,
  hardware class, concurrency, cache state, and PostgreSQL version.
- Read plan trees from actual row flow: estimates versus actuals, loops, buffers,
  scan/join type, sort/hash spill, filter removal, planning, and execution time.
- `EXPLAIN ANALYZE` executes the statement. Never use it for unsafe writes or an
  unapproved production workload; use a rollback-safe transaction only when its
  side effects and locks are understood.
- Investigate estimate errors and statistics before forcing plan types.
- Indexes can improve reads while increasing writes, storage, vacuum, cache, and
  migration costs. Test the complete workload.
- Include connection-pool saturation, transaction duration, lock waits,
  replication lag, vacuum/analyze health, and application retries in diagnosis.
- Compare before/after results with the same method and protect semantic parity.

Primary references:

- https://www.postgresql.org/docs/current/using-explain.html
- https://www.postgresql.org/docs/current/indexes.html
- https://www.postgresql.org/docs/current/sql-vacuum.html

