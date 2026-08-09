# AWS translation

## Establish identity and target

1. Resolve the account, principal/role, partition, region, profile, and resource
   before the service operation.
2. Use `sts get-caller-identity` or an equivalent read-only identity check and
   an explicit `--profile` and `--region` where ambiguity exists.
3. Prefer federation, IAM roles, STS, workload identity, and temporary
   credentials over long-lived access keys.
4. Review both the role trust policy and its permission policies, including
   resource and condition scope.
5. Never use or expose the root user credentials for ordinary operations.

## Operate safely

- Start with `list`, `describe`, or `get` operations and machine-readable output.
- Treat IAM, Organizations, billing, deploy, delete, key rotation, public access,
  and cross-account policy as consequential operations requiring exact authority.
- Apply least privilege and preserve a session name/audit trail for assumed roles.
- Avoid changing a default profile or region merely to make one command work.
- Verify final state with a read-only call in the same account and region.

## Primary references

- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html
- https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-options.html
- https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

