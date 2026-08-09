# PostgreSQL migrations and operations

## Migration review

- Determine the lock level, table/index rewrite, scan, transaction duration,
  replication effect, disk headroom, and rollback/recovery path for every DDL or
  backfill step.
- Separate expand, bounded backfill, application cutover, constraint validation,
  and contract/removal when a one-step migration would block or be irreversible.
- Use concurrent index operations only after checking their restrictions,
  failure artifacts, extra scans, and version support.
- Make backfills resumable, observable, rate-limited, and safe under concurrent
  writes. State how old/new application versions coexist.
- Set and justify lock/statement timeouts at the execution boundary; a timeout is
  not a rollback strategy.

## Operations

- Define backup ownership, encryption, retention, restore verification, recovery
  point/time objectives, and disaster procedure.
- Monitor connections, locks, long transactions, replication, disk growth,
  autovacuum/analyze, bloat indicators, and failed maintenance.
- Remember that `VACUUM FULL`, destructive DDL, failover, restore, extension
  upgrade, and production migration are consequential operations.
- Verify rollback against data written by the newer schema; binary rollback alone
  may not restore compatibility.

Primary references:

- https://www.postgresql.org/docs/current/explicit-locking.html
- https://www.postgresql.org/docs/current/sql-createindex.html
- https://www.postgresql.org/docs/current/backup.html

