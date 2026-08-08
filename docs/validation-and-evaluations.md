# Validation and evaluations

Run deterministic validation without provider calls:

```bash
pnpm run validate
pnpm run validate:sources
pnpm run validate:official
pnpm run validate:installation
pnpm run promptfoo:validate
pnpm run eval:dry-run -- --suite full
```

`validate:sources` additionally requires absolute
`AGENT_SKILLS_GEREMMYAS_SOURCE` and `AGENT_SKILLS_TUXEDO_SOURCE` paths. The
frozen commits remain the provenance baseline; a clean later checkout is
accepted only when its governed tree is byte-identical. Installation validation
uses disposable homes and workspaces, disables external CLI telemetry, and
removes the scratch tree.

Provider suites are deliberately separate: `eval:smoke`, `eval:routing`,
`eval:behavior`, `eval:composition`, `eval:security`, `eval:compare`, and
`eval:full`. Before any one can execute, run the matching suite-selectable dry
run, for example `pnpm run eval:dry-run -- --suite routing`, report its exact
target-call and secondary-judgment budget, obtain explicit human authorization,
and set the matching approval token described by the dry-run together with
`AGENT_SKILLS_EVAL_APPROVED_AT=$(date +%s)`. The runner rejects timestamps more
than ten minutes old and removes both variables from its own process before
authentication or provider startup. Use one-shot environment assignments on
the execution command; do not export reusable approval variables. Login is
also explicit through `eval:login`; inspect it with `eval:auth:status`.

The harness uses a dedicated absolute Codex home outside this checkout,
personal Codex state, and Geremmyas/Tuxedo. It rejects symlinks and unknown
behavior-bearing configuration, constructs child environments from a minimal
allowlist (rather than inheriting cloud, registry, Git, or provider secrets),
requires the exact `Logged in using ChatGPT` status, gives each Promptfoo
process disposable state, and uses a fresh temporary Git workspace for every
writing case. Network is disabled unless a case explicitly requires synthetic
network behavior; fixtures never contain real credentials or projects.

Reports under `evals/promptfoo/results/` are append-only and sanitized to case
ID, verdict, bounded reason, and deterministic evidence. Prompts, raw responses,
traces, secrets, credentials, and canaries are never persisted. Deterministic
failures override semantic review; lack of required trajectory evidence yields
`needs-review`, never a pass.

Executable TypeScript behavior drivers are currently verified on macOS through
`sandbox-exec`; their profile denies network, process forks, HOME reads, and all
file writes. The oracle fails closed when Node or this sandbox is unavailable.
Supporting another maintainer OS requires an equivalently reviewed confinement
backend before those cases can pass.
