# Google Cloud translation

## Establish identity and target

1. Inspect the active named configuration, authenticated account, project,
   region/zone, quota project, and impersonation before the resource command.
2. Prefer an explicit `--configuration`, `--project`, region/zone, and output
   format for repeatable commands instead of mutating global defaults.
3. Distinguish gcloud CLI credentials from Application Default Credentials.
4. Prefer user/workload federation and short-lived service-account
   impersonation over downloaded service-account keys.
5. Confirm both the caller's permission to impersonate and the impersonated
   service account's resource permissions.

## Operate safely

- Start with `describe`, `list`, or equivalent read-only commands.
- State project and resource identifiers in every mutating command where the CLI
  supports them.
- Treat IAM, service enablement, organization policy, billing, deploy, and delete
  as consequential operations requiring exact authority.
- Correlate automation evidence with Cloud Audit Logs when auditability matters.
- Do not use `--quiet` to conceal an unresolved destructive choice.

## Primary references

- https://docs.cloud.google.com/sdk/docs/configurations
- https://docs.cloud.google.com/docs/authentication/use-service-account-impersonation
- https://docs.cloud.google.com/iam/docs/best-practices-service-accounts

