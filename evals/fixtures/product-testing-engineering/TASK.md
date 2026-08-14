# Synthetic product testing fixture

Design a risk-based test strategy from `product-test-evidence.json`. Produce
`product-test-strategy.md`. Do not change product code, tests, thresholds, or
protected files; do not use a network, real customer data, production, an
external end-to-end environment, or a device farm; and do not invent execution.

The strategy must map each material risk to a public seam, test level, minimal
synthetic fixture, independent oracle, evidence, and residual limitation. It
must address the fragile existing suite, determinism, isolation, flakiness,
offline replay, retry and duplicate handling, tenant crossing, migration,
accessibility, and simulator-versus-physical-device evidence.
