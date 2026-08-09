---
name: database-postgresql
description: "Design, review, diagnose, or evolve PostgreSQL schemas, queries, indexes, migrations, and operational behavior. Use when modeling relational data, reviewing SQL, interpreting EXPLAIN, improving performance, or planning safe PostgreSQL migrations. Do not use for non-PostgreSQL databases, unapproved production execution, or application-layer architecture unrelated to persistence."
---

# PostgreSQL Database Engineering

Choose the smallest PostgreSQL workflow that matches the request.

## Route the task

- Read [modeling.md](references/modeling.md) for tables, keys, constraints,
  normalization, tenancy, and lifecycle modeling.
- Read [query-review.md](references/query-review.md) for SQL correctness,
  indexes, transactions, locks, and review output.
- Read [performance.md](references/performance.md) for `EXPLAIN`, statistics,
  plan shapes, realistic data, pooling, and measurement.
- Read [migrations-and-operations.md](references/migrations-and-operations.md)
  for online changes, backfills, rollback, maintenance, backup, and recovery.

Load only the references needed for the selected task.

## Common process

1. Establish PostgreSQL version, schema, data scale, workload, latency/safety
   target, tenancy, and production authority.
2. Check correctness and data invariants before optimizing.
3. Use realistic plans and measurements; do not infer performance from SQL
   appearance alone.
4. Evaluate locks, rewrites, transaction duration, connection pressure,
   replication, rollback, and recovery for changes.
5. Prefer a reviewed SQL candidate or migration plan before any execution.
6. Report evidence, uncertainty, unsupported assumptions, and withheld remote
   operations.

