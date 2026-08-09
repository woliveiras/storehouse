# PostgreSQL modeling

- Model domain identity and lifecycle before tables. Distinguish natural,
  surrogate, tenant-scoped, external, and idempotency keys.
- Use `NOT NULL`, primary/unique keys, foreign keys, and `CHECK` constraints for
  invariants PostgreSQL can enforce reliably.
- Normalize duplicated facts until a measured read or lifecycle requirement
  justifies a documented denormalization and synchronization owner.
- Choose types from semantics and range. Avoid unbounded text conventions for
  finite states when a checked domain is required.
- Model timestamps, time zones, money/precision, soft deletion, retention, and
  ownership explicitly.
- Include tenant keys in uniqueness, foreign-key, index, and policy reasoning.
- Treat JSON/arrays as intentional boundaries, not escape hatches from modeling.
- Add indexes for demonstrated access and integrity needs; every index has write,
  storage, vacuum, and maintenance cost.

Primary references:

- https://www.postgresql.org/docs/current/ddl-constraints.html
- https://www.postgresql.org/docs/current/indexes.html

