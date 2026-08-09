# LangGraph translation

Use LangGraph when the project selects an explicit state graph.

## Map the common agent contract

- Define a typed state schema and reducers before nodes and edges.
- Keep each node responsible for one state transition and return updates instead
  of mutating hidden shared state.
- Compile with an appropriate checkpointer when the workflow needs persistence,
  human-in-the-loop, memory, replay, or fault recovery.
- Treat the thread identifier as a persistent execution cursor with an explicit
  owner, tenant boundary, retention policy, and collision strategy.
- Use dynamic interrupts for approval/review flows. Resume can restart the node,
  so work before an interrupt must be idempotent or moved to a separate node.
- Test routing, reducers, checkpoints, resume, replay, interrupts, tool errors,
  duplicate delivery, cancellation, and stale state.

Do not wrap interrupts in broad exception handling or assume execution resumes
at the exact source line after the interrupt.

## Primary references

- https://docs.langchain.com/oss/python/langgraph/persistence
- https://docs.langchain.com/oss/python/langgraph/interrupts

