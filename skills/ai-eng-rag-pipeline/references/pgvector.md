# pgvector translation

Use pgvector when PostgreSQL owns vector storage and retrieval. Verify the
installed PostgreSQL and pgvector versions before using version-specific index
or planner features.

## Map the common RAG contract

- Store the source/document/chunk identity, tenant, authorization metadata,
  embedding model/version, and vector in an explicit relational schema.
- Enforce tenant and lifecycle invariants with PostgreSQL constraints and policy,
  not only application filters.
- Choose the distance operator and operator class from the embedding metric;
  keep query and index semantics aligned.
- Establish an exact-search baseline before adding approximate indexes.
- Compare HNSW and IVFFlat on realistic rows, dimensions, filters, write rate,
  memory, latency, and recall. Do not select an index by popularity.
- Remember that approximate-index filtering can occur after candidate selection.
  Measure recall under real filters and consider ordinary indexes, partial
  indexes, partitioning, or supported iterative scans.
- Inspect `EXPLAIN (ANALYZE, BUFFERS)` only on an authorized environment where
  executing the query is safe.

## Operations

Plan extension upgrades, vector-dimension/model migrations, index build/rebuild,
replication, backup/restore, and rollback with the surrounding PostgreSQL
operations contract.

## Primary references

- https://github.com/pgvector/pgvector
- https://www.postgresql.org/docs/current/using-explain.html
- https://www.postgresql.org/docs/current/indexes.html

