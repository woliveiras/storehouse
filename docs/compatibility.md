# Compatibility

All skills use the portable Agent Skills directory and frontmatter contract.
They are standalone: optional companion skills and Baseline workflows improve
composition but are never prerequisites.

Deterministic validation covers valid metadata and resource links. The official
`skills` CLI clean-room check lists the local repository and installs a single
skill plus a multi-skill collection into temporary Codex, Claude Code,
OpenCode, and GitHub Copilot targets when those targets are supported by the
pinned CLI. The validation report records the exact observed targets and does
not imply behavioral parity across clients.

Eleven Phaser/Godot skills retain `agents/openai.yaml` for intentional Codex
presentation metadata. Other clients may ignore it. `game-art-2d` treats Codex
image generation as an optional accelerator and retains a workflow for supplied
or externally generated assets. Model-backed compatibility remains unverified
until an explicit, budget-approved evaluation is run.

CI and migration examples never authorize rolling dependency selection. Skills
must preserve an existing project pin or propose an exact reviewed version;
GitHub Actions should use immutable commit SHAs when the project policy supports
them. Any example version is a reviewed baseline, not a claim that it is
perpetually current, and contributors must verify primary release sources before
updating it.
