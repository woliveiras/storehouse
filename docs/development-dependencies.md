# Development dependency evidence

No dependency in `pyproject.toml` or `package.json` is distributed inside a
skill or required by a consumer. Version constraints live only in those
manifests and their lockfiles so dependency updates have one source of truth.

| Dependency | Purpose | Provenance and maintenance | License/security evidence |
| --- | --- | --- | --- |
| PyYAML | Parse skill frontmatter in deterministic tests. | PyPI `PyYAML`, actively maintained upstream. | MIT; resolved by UV lock. |
| Pillow | Execute smoke checks for the optional game-art scripts. | PyPI `Pillow`, maintained fork of PIL. | MIT-CMU per installed package metadata; resolved by UV lock. |
| skills-ref | Official Agent Skills reference validator. | PyPI package from the Agent Skills reference implementation. | Apache-2.0; resolved by UV lock. |
| jsonschema | Validate committed catalogs against JSON Schema Draft 2020-12. | PyPI `jsonschema`, maintained reference implementation. | MIT; resolved by UV lock. |
| skills | Official documented project installer clean-room check. | npm `skills` from `vercel-labs/skills`. | MIT; PNPM production audit reported zero vulnerabilities. |
| Promptfoo | Development-only evaluation configuration and execution. | npm `promptfoo`; established evaluation project. | MIT; provider execution is explicit and isolated. |
| @openai/codex-sdk | Promptfoo's local Codex provider. | npm package from OpenAI. | Apache-2.0; no model is pinned and API keys are stripped. |

PNPM build policy allows only SWC, esbuild, protobufjs, and Sharp install
scripts needed by the development tooling. Playwright's browser download and
ONNX Runtime's native install are disabled because this harness does not use
those optional Promptfoo surfaces. Reviewed transitive overrides align with the
isolated Tuxedo evaluation toolchain. `pnpm audit --prod` is recorded with the
task evidence; transitive optional peer warnings are reported rather than
silently patched with new direct dependencies.
