# ADR 0005: Add Product Security & Privacy Engineering

- Status: Accepted
- Date: 2026-08-14

## Context

Storehouse has technology-specific ownership for Supabase and PostgreSQL,
service-architecture ownership, CI automation, product UI/UX design, and an
optional horizontal Baseline security review. It does not have an independent
capability that owns product threat modeling, authorization and tenant
isolation, sensitive-data lifecycles, technical privacy, adversarial behavior,
and incident containment across web and mobile products.

The repository had 46 skills when this decision was accepted. Concurrent work
already occupied ADR 0004 and criterion IDs RT/BH/CP/SEC-046, so this addition
uses ADR 0005 and RT/BH/CP/SEC-047.

## Decision

Add the standalone `product-security-privacy-engineering` skill and the
declarative `product-security` collection. The skill is client-neutral and has
no dependency on Baseline, another installed skill, or repository-only tooling.
It may compose with independently installed capabilities while retaining the
following ownership:

- product security and privacy owns product threat modeling, trust boundaries,
  authentication-versus-authorization analysis, ownership and tenancy,
  sensitive-data lifecycles, technical consent and deletion requirements,
  abuse cases, adversarial verification, and incident containment;
- `baseline:security-review` remains an optional technology-neutral horizontal
  review of a change;
- `cloud-supabase` owns Supabase Auth, RLS, Storage, Realtime, and Edge Function
  implementation detail;
- `database-postgresql` owns PostgreSQL schemas, queries, locks, indexes, and
  migrations;
- `backend-service-architecture` owns service boundaries, handlers,
  transactions, and decomposition;
- `ci-*` skills own automated scanner and gate execution in CI;
- `product-ui-ux-design` owns consent experience, feedback, and visible
  recovery, while this skill owns the associated risk, data, authorization,
  and protection requirements.

The installed package uses a concise `SKILL.md`, deterministic Codex metadata,
two reusable assets, and eight directly linked first-level references grounded
in primary standards and platform guidance. It does not make legal compliance
or certification claims and does not treat tests or scanners as proof of
security.

## Deterministic acceptance criteria

- **PSPE-001:** the skill name, frontmatter, Codex metadata, invocation, display
  name, and short description match the catalog identity.
- **PSPE-002:** the concise entrypoint directly and conditionally links exactly
  eight references and two assets; no nested README, runtime, or dependency is
  distributed.
- **PSPE-003:** the workflow starts from actors, assets, sensitive data, trust
  boundaries, entrypoints, privileges, third parties, and the complete data
  lifecycle before selecting controls.
- **PSPE-004:** authentication, authorization, ownership, tenant isolation,
  least privilege, administrative privilege, and service roles remain distinct.
- **PSPE-005:** web and API guidance covers IDOR, tenant crossing, replay,
  enumeration, elevation of privilege, error disclosure, and abuse resistance.
- **PSPE-006:** mobile guidance uses MASVS/MASTG and official platform guidance
  without claiming simulator or static-only evidence as runtime proof.
- **PSPE-007:** lifecycle guidance covers collection, processing, storage, logs,
  caches, backups, sharing, retention, export, consent, and deletion without
  exposing real sensitive data as evidence.
- **PSPE-008:** authorized implementation starts with negative fail-first checks
  and verifies positive, negative, cross-tenant, replay, error, rollback, and
  recovery paths.
- **PSPE-009:** incident guidance separates containment, evidence preservation,
  recovery, validation, and retrospective improvement.
- **PSPE-010:** output separates confirmed findings, hardening, external
  requirements, unknowns, and evidence limits, and never certifies LGPD, GDPR,
  HIPAA, or other legal compliance.
- **PSPE-011:** ownership boundaries permit optional composition without making
  Baseline or another skill a dependency.
- **PSPE-012:** taxonomy, architecture, collection, and generated README expose
  an exact inventory of 47 standalone skills.
- **PSPE-013:** RT-047 covers explicit and implicit routing, focused negatives
  for Supabase RLS, PostgreSQL-only work, CI scanning, consent UI, and optional
  Baseline composition.
- **PSPE-014:** BH-047 uses a synthetic multitenant web/mobile fixture, an
  independent executable oracle, and mutants for IDOR, tenant crossing,
  excessive service privilege, sensitive logging, indefinite retention,
  incomplete deletion, and false certification.
- **PSPE-015:** CP-047 compares control, focal, specialized composition, and
  minimal Baseline variants while preserving every owner's responsibility.
- **PSPE-016:** SEC-047 requires trajectory evidence for canary access,
  exfiltration, private-data upload, production pentesting, and false compliance
  instructions while still requiring a legitimate review.
- **PSPE-017:** deterministic validation, official validation, dry-run planning,
  and a clean-room single-skill installation pass without provider/model evals.

## Consequences

The exact inventory becomes 47 skills and collection documentation gains one
installable entry. Repository-only tests and evaluations become larger, but no
consumer runtime, CLI, installer, dependency, or implicit capability coupling
is added. Product-security findings remain evidence-bounded: checked-in
guidance and deterministic fixtures cannot establish production security,
legal compliance, or the result of a penetration test.
