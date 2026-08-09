---
name: cloud-supabase
description: "Design, build, review, diagnose, or operate Supabase applications across Postgres, Auth, Storage, Realtime, Edge Functions, local development, migrations, and security. Use when the target system depends on Supabase platform behavior. Do not use for generic PostgreSQL work with no Supabase boundary, unrelated cloud platforms, or unapproved remote or production mutation."
---


# Supabase Platform Engineering

Treat database, identity, object access, realtime delivery, functions, generated
types, and environment lifecycle as one platform contract.

## Route the task

- For Postgres schema, queries, indexes, migrations, functions, and RLS, establish
  ownership, roles, exposed schemas, tenancy, and rollback before implementation.
- For Auth, define identity providers, redirect/session behavior, account linking,
  claims, authorization ownership, and recovery flows.
- For Storage, define buckets, object paths, MIME/size constraints, ownership,
  signed/public access, policies, and deletion lifecycle.
- For Realtime, define channels, authorization, ordering/duplication behavior,
  reconnection, and client state reconciliation.
- For Edge Functions, define runtime/configuration, secrets, authentication,
  timeouts, retries, idempotency, observability, and external side effects.
- For local/remote operations, identify the exact project, environment, migration
  history, CLI configuration, authority, and recovery path before mutation.

## Common process

1. Inventory tables, policies, functions, buckets, clients, user roles, generated
   types, Edge Functions, and integration boundaries affected by the task.
2. Decide what belongs in checked-in migrations/configuration, application code,
   platform secrets, or an explicitly documented manual operation.
3. Design authorization before frontend access. Test anonymous, authenticated,
   tenant-crossing, owner, privileged backend, and failure paths separately.
4. Keep service-role credentials on trusted backends only; anon/publishable keys
   rely on grants and RLS and are not authorization controls by themselves.
5. Add indexes for real policy, join, filter, and ownership predicates, then
   verify query and lock behavior proportionally.
6. Regenerate typed clients when schema changes affect consumers and verify the
   compile/runtime boundary.
7. Prefer local or synthetic verification. Require exact authority before link,
   push, deploy, secret change, production SQL, data migration, or destructive
   remote operation.
8. Report the Supabase surfaces affected, security boundary, checks run,
   rollback/recovery, and remote actions withheld.

Do not use dashboard-only changes as the source of truth. Write both `USING` and
`WITH CHECK` where PostgreSQL policy read and write rules differ.
