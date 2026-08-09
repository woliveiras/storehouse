# ChromaDB translation

Use ChromaDB when the target project selects its collection model and client.
Verify the installed client/server documentation before writing version-specific
code.

## Map the common RAG contract

- Represent environment/application boundaries with explicit tenants, databases,
  and collections when the deployment exposes them.
- Give every record a stable ID and intentional document, metadata, and embedding
  ownership. Do not let client-generated ordering become identity.
- Preserve the collection's embedding-function/model contract. A model change
  requires a new collection or a controlled re-embedding migration.
- Use metadata filters for tenant, authorization, document type, source version,
  and freshness before accepting vector similarity results.
- Treat collection or record deletion as data mutation. Confirm target and
  rebuild/retention policy before executing it.
- Test add/upsert semantics, duplicate IDs, filtered query, no-result behavior,
  delete/reingest, persistence, backup, and complete rebuild.

## Client choice

Select an in-process, persistent, HTTP, or managed client from the project's
deployment and lifecycle requirements. Do not silently replace a local durable
store with an ephemeral client or introduce a remote service.

## Primary references

- https://docs.trychroma.com/docs/overview/architecture
- https://docs.trychroma.com/docs/collections/manage-collections
- https://docs.trychroma.com/docs/querying-collections/query-and-get

