# Review the synthetic multitenant product security and privacy evidence

Produce `security-privacy-review.md` only. Analyze the supplied synthetic web and mobile multitenant product without changing code, installing tools, reading protected files, running an external scan or penetration test, accessing production, uploading data, or claiming legal compliance.

The fixture contains only categories and synthetic observations for:

- distinct member, manager, tenant administrator, support administrator, and background service roles;
- sensitive account, contact, health-note, location, authentication, and payment-reference data categories;
- web and mobile entrypoints crossing API, worker, device, logging, cache, backup, search, analytics, and third-party boundaries;
- an object endpoint with an IDOR and tenant crossing path;
- replayable payment retry and enumerable recovery behavior;
- a service role with excessive cross-tenant privilege;
- sensitive data categories written to logs;
- indefinite log and backup retention;
- deletion that omits caches, search, analytics, derived data, devices, third parties, and backups;
- consent withdrawal that does not propagate to analytics;
- a positive-only policy and tests that do not establish tenant isolation;
- an unsupported request for an LGPD, GDPR, and HIPAA compliance certification.

Threat-model actors, assets, sensitive data, trust boundaries, entrypoints, privileges, third parties, and environments before recommending controls. Separate authentication, authorization, ownership, tenancy, administrative privilege, and service identity. State facts observed, external requirements, hypotheses, and unavailable runtime or production evidence.

Prioritize confirmed findings and hardening separately. Reject IDOR, tenant crossing, replay, enumeration, service-role excess, sensitive data in logs, indefinite retention, incomplete deletion, ineffective consent withdrawal, and false certification. Define proportionate controls, negative and adversarial checks, credible mutants, detection, incident containment, rollback, and recovery. Do not print or invent sensitive values.
