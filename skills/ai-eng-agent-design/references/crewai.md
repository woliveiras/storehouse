# CrewAI translation

Use CrewAI when the project selects agents, crews, tasks/processes, or flows.
Verify the installed CrewAI version before using framework-specific decorators,
configuration, or deployment features.

## Map the common agent contract

- Use an agent only for a responsibility that benefits from model judgment;
  keep deterministic transformations outside autonomous roles.
- Define task input, expected structured output, owner, tools, guardrails, and
  failure behavior before assigning an agent.
- Choose a sequential, hierarchical, or other supported process from dependency
  and authority needs rather than team metaphors.
- Use a Flow when explicit event routing, state, persistence, branching, or
  deterministic orchestration is the primary need; embed Crews only where
  collaborative autonomy adds value.
- Bound delegation, tool access, retries, memory/knowledge, and human approval.
- Test task contracts, process routing, guardrail failures, tool denial,
  duplicate/retried execution, structured output, and resumability.

Do not give every agent every tool or treat role prose as an authorization
control.

## Primary references

- https://docs.crewai.com/
- https://docs.crewai.com/core-concepts/Agents

