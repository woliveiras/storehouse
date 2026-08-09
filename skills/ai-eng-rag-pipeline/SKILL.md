---
name: ai-eng-rag-pipeline
description: "Design or review retrieval-augmented generation pipelines with durable ingestion, metadata, retrieval, evaluation, tenancy, and rebuild behavior. Use when building document ingestion, vector retrieval, filters, reranking, or grounded-answer evaluation with ChromaDB or pgvector. Do not use for general LLM integration, keyword search alone, or agent orchestration without retrieval."
---

# AI Engineering RAG Pipeline

Design retrieval behavior independently from the selected vector store.

## Process

1. Identify source documents, ownership, update cadence, deletion requirements,
   tenancy, sensitivity, and retrieval success criteria.
2. Define normalization, chunk boundaries, stable document/chunk IDs, metadata,
   and source-version tracking before ingestion.
3. Choose embedding and retrieval models with a versioned re-embedding plan.
4. Separate source-of-truth content from rebuildable vector representations.
5. Apply tenant, authorization, freshness, and document-type filters before
   treating similarity as relevance.
6. Define retrieval, optional reranking, context assembly, citation, and
   no-result behavior.
7. Test known matches, hard negatives, filters, stale/deleted content,
   cross-tenant isolation, and rebuild parity.
8. Record quality, latency, storage, and cost signals with a reproducible
   evaluation set.

## Storage references

- For ChromaDB clients, collections, metadata, and persistence, read
  [chromadb.md](references/chromadb.md).
- For PostgreSQL with pgvector, indexes, distance operators, filters, and query
  planning, read [pgvector.md](references/pgvector.md).

Load only the reference selected by the target system.

## Output

- Ingestion and metadata contract
- Retrieval and grounding flow
- Isolation, deletion, backup, and rebuild plan
- Evaluation dataset and acceptance measures

