---
name: ai-eng-agent-design
description: "Design or review stateful AI-agent workflows, tool boundaries, approvals, recovery, and tests across supported frameworks. Use when building agents, graphs, crews, resumable workflows, or human-in-the-loop control. Do not use for a simple model call, an ordinary deterministic workflow, or RAG-only retrieval design."
---

# AI Agent Design

Design the workflow before selecting framework primitives.

## Process

1. Define the goal, entrypoint, terminal states, and user-visible result.
2. Model explicit state, ownership, persistence, and data sensitivity.
3. Inventory tools and side effects with authority, idempotency, timeout, retry,
   compensation, and audit requirements.
4. Choose coordination only after the workflow shape is clear: sequential,
   branching, supervisor, peer delegation, or event-driven.
5. Place human approval before consequential or irreversible side effects.
6. Define cancellation, partial failure, resume, duplicate delivery, and stale
   state behavior.
7. Protect the boundary with deterministic tests for routing, state updates,
   tool failure, approval, retries, and recovery.
8. Add traces and evaluation signals that explain decisions without exposing
   private content by default.

## Framework references

- For LangGraph state graphs, checkpoints, interrupts, and subgraphs, read
  [langgraph.md](references/langgraph.md).
- For CrewAI crews, tasks, processes, and delegation, read
  [crewai.md](references/crewai.md).

Do not load a framework reference until the project or request selects it.

## Output

- State and coordination model
- Tool and authority inventory
- Failure and recovery contract
- Framework translation
- Test and observability plan

