# Analyze the synthetic product performance evidence

Produce `performance-analysis.md` only. This is diagnosis-only work: do not modify code, install tools, send evidence to an external service, or execute load against production.

The evidence bundle contains measured laboratory regressions and bounded profile summaries for:

- web LCP and the critical rendering path;
- a web interaction degraded by a long task and main-thread contention;
- layout instability measured with CLS;
- Android startup with separate TTID and TTFD;
- Android jank and an ANR;
- iOS launch, a hang, and a hitch;
- mobile memory growth across lifecycle transitions;
- a cross-platform React Native path with Android/iOS and simulator limitations;
- a faster candidate that fails functional equivalence;
- a reported regression with missing measurement and no executable product.

Use repeated distributions rather than the best execution. Distinguish measured laboratory evidence, profile-supported causal inference, unsupported hypothesis, field evidence, and limitations. Preserve the existing 2500 ms TTFD budget; do not relax it to make a result pass. Reject the functionally changed candidate and state that a skeleton or animation cannot prove a technical improvement.

No field data or physical-device access is supplied. Do not claim field improvement, physical-device verification, or a technical root cause for the missing-profile case. Add a concrete measurement plan for that case and state the remaining browser, field, and device limitations.
