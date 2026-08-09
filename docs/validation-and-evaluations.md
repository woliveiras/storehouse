# Validation and evaluations

Run deterministic validation without provider calls:

```bash
pnpm run validate
pnpm run validate:official
pnpm run promptfoo:validate
pnpm run eval:dry-run
```

`validate` runs deterministic repository and evaluation-harness tests.
`validate:official` applies the official Agent Skills validator to every
directory under `skills/`. `promptfoo:validate` checks the configuration in
disposable local state without making provider calls. The Baseline commit in
`evals/config.py` freezes the optional composition condition so repeated runs do
not silently change when the sibling checkout advances.

Provider suites are deliberately separate: `eval:smoke`, `eval:routing`,
`eval:behavior`, `eval:composition`, `eval:security`, `eval:compare`, and
`eval:full`. Before any one can execute, run the matching suite-selectable dry
run, for example `pnpm run eval:dry-run --suite routing`, report its exact
target-call and secondary-judgment budget, obtain explicit human authorization,
and set the matching approval token described by the dry-run together with
`STOREHOUSE_EVAL_APPROVED_AT=$(date +%s)`. The runner rejects timestamps more
than ten minutes old and removes both variables from its own process before
authentication or provider startup. Use one-shot environment assignments on
the execution command; do not export reusable approval variables. Login is
also explicit through `eval:login`; inspect it with `eval:auth:status`.

The harness uses a dedicated absolute Codex home outside this checkout,
personal Codex state, and the optional Baseline source. It rejects symlinks and
unknown behavior-bearing configuration, constructs child environments from a minimal
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
Supporting another host OS requires an equivalently reviewed confinement
backend before those cases can pass.
