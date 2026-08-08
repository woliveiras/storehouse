# Test review

## Spec

The tests cover manifest identity, schema URLs, human-facing README identity,
generated collection commands, the repository-specific environment namespace,
and complete removal of the former tracked text identity. Remote identity is
correctly left to an external GitHub oracle rather than simulated locally.

## Standards

The stale-name oracle constructs its forbidden tokens independently instead of
copying a value from production code. It scans tracked and untracked task files,
skips only non-UTF-8 content, and cannot pass merely because the README changed.
The existing catalog renderer remains an independent oracle for every
collection command.

## Risk

No circular oracle or no-op path was found. The test intentionally distinguishes
generic “Agent Skills” terminology from the former hyphenated product name, so
valid references to the public format are not rejected. A standard unit suite
cannot prove the remote rename; the separate `gh repo view` and `git remote`
checks supply that evidence.
