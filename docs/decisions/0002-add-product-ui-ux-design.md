# Add product UI/UX design as a horizontal product capability

- Status: accepted
- Date: 2026-08-13
- Decision makers: @woliveiras
- Consulted: Codex
- Informed: Storehouse users
- Supersedes: none

## Context and Problem Statement

Storehouse needs a standalone capability for designing, auditing, redesigning,
specifying, implementing when authorized, and reviewing web and mobile product
experiences. The accepted flat, domain-first taxonomy does not yet have a
`product` namespace. The historical 42-skill inventory in ADR 0001 records the
coordinated taxonomy migration that established the current structure; changing
that record would obscure the decision it confirmed.

## Decision Drivers

- Preserve direct, independently installable `skills/<name>/` distribution.
- Keep the core workflow concise and client-neutral through conditional,
  first-level references.
- Cover web, mobile, accessibility, design systems, and the SaaS, e-commerce,
  CMS, CRM, and ERP domains without turning vendor conventions into universal
  rules.
- Make outputs traceable to inspected evidence and verifiable tasks, states,
  risks, and acceptance criteria.
- Preserve audit-only authority, domain vocabulary, permissions, and data-loss
  boundaries.
- Extend deterministic routing, behavior, composition, security, catalog, and
  clean-room installation evidence without provider execution.

## Decision Outcome

Add `product-ui-ux-design` as the first skill in the flat `product` namespace
and add the declarative `product-design` collection. This is a compatible
extension of ADR 0001's domain-first naming rule, not a retroactive change to
its migration decision. The distributed inventory ratchet advances from 42 to
43 skills and the current architecture, catalog documentation, README, tests,
and evaluation budgets advance with it.

The skill remains independent. Baseline review may be selected when separately
installed, but it is neither required nor copied into the skill.

## Stable Criteria and Behavior/Oracle Matrix

| ID | Expected behavior | Oracle | Provenance |
| --- | --- | --- | --- |
| PUD-001 | `product-ui-ux-design` has valid skill and OpenAI interface metadata and installs independently. | Official skill validation, metadata assertions, and clean-room official CLI smoke. | external |
| PUD-002 | The concise core routes directly to exactly the required first-level references and loads them conditionally. | File inventory, link, direct-reference, and line-budget assertions. | spec-derived |
| PUD-003 | The workflow inspects the real product and distinguishes observations, supplied evidence, heuristics, decisions, hypotheses, and limitations. | Core-contract token and section assertions. | spec-derived |
| PUD-004 | The workflow models complete flows, task-centered interaction, proportional artifacts, and multimodal verification. | Core and foundation/reference contract assertions. | spec-derived |
| PUD-005 | Accessibility guidance uses current WCAG, platform guidance, manual review, and explicit inclusive-design guardrails. | Accessibility reference source-class and behavior assertions. | external |
| PUD-006 | Web, mobile, design-system, SaaS, e-commerce, CMS, CRM, and ERP references provide concrete conditional guidance. | Exact reference inventory and domain-specific contract assertions. | independent |
| PUD-007 | Catalog, README, taxonomy, and architecture consistently expose 43 skills and the `product-design` collection. | Existing catalog renderer plus exact inventory assertions. | independent |
| PUD-008 | Positive product routing and negative game UI, promotional art, and backend-only routing are represented without leaking the answer. | `RT-043` catalog and runner case-expansion assertions. | implementation-aware |
| PUD-009 | A deterministic audit fixture covers SaaS onboarding, e-commerce checkout, CMS editorial flow, mobile CRM capture, dense ERP approval, accessibility/error states, and missing executable evidence. | `BH-043`, executable report oracle, calibrated sample, no-op, and targeted mutants. | independent |
| PUD-010 | Composition proves standalone behavior and optional Baseline review without dependency. | `CP-043` variants and repository dependency assertions. | independent |
| PUD-011 | Malicious product content cannot expand audit authority, expose protected content, or trigger remote/destructive actions. | `SEC-043`, protected hashes, outside sentinel, canary, and trajectory policy. | independent |
| PUD-012 | Deterministic validators, syntax checks, dry-run budgets, diff checks, and clean-room installation pass without model/provider execution. | Recorded local command results and provider gate assertions. | external |
| PUD-013 | Performance-sensitive product work defines observable web/mobile experience behavior under latency and constrained resources without claiming technical root cause or displacing engineering profiling and optimization. | Direct conditional reference, official-source and boundary assertions, strengthened `BH-043` oracle, and targeted root-cause mutant. | independent |

## Consequences

- Good: product experience work gains a task-centered, evidence-aware workflow
  that spans design through implementation review.
- Good: domain-specific detail remains optional and independently consumable.
- Good: the taxonomy and evaluation inventory retain exact ratchets.
- Bad: each future inventory-sensitive assertion and provider budget must now
  account for 43 skills.
- Neutral: source links guide current practice but do not replace product
  research, legal advice, accessibility expertise, or representative user
  testing.

## Confirmation

The decision is confirmed when PUD-001 through PUD-013 pass with no provider
execution and the final worktree contains only task-owned changes.
