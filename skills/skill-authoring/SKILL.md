---
name: skill-authoring
description: "Create or revise portable Agent Skills with precise routing, progressive disclosure, bundled resources, and validation. Use when writing, renaming, or reviewing a skill. Do not use for general documentation or unrelated prompts."
---

# Skill Authoring

Create one self-contained capability that follows the Agent Skills format and
remains useful without a repository-specific installer or runtime.

## Define the contract

1. Collect concrete positive, implicit, negative, collision, and composition
   examples before writing instructions.
2. Choose one action-oriented lowercase kebab-case name of at most 64
   characters. Match the directory and frontmatter `name` exactly.
3. Write a routing `description` that says what the skill does, when to use it,
   and when not to use it. Keep all activation guidance in frontmatter.
4. Define observable completion, stop conditions, authority boundaries, and
   compatibility limits.

## Design progressive disclosure

1. Keep `SKILL.md` concise and imperative.
2. Put optional technical detail one level down in `references/` and link it
   directly from `SKILL.md` with a clear load condition.
3. Put deterministic reusable operations in `scripts/`; make dependencies and
   failure behavior explicit and test the scripts.
4. Put templates and output resources in `assets/`, not explanatory prose.
5. Put deliberate client metadata such as `agents/openai.yaml` under
   `agents/`; document its real compatibility instead of treating it as a
   portable guarantee.
6. Do not add a skill-local README, changelog, package manager, installer,
   daemon, telemetry, client generator, or consumer runtime.

## Preserve independence

- Include every resource necessary for the skill itself.
- Describe other skills as optional composition. Provide a useful local
  fallback when the companion is absent.
- Do not depend on a repository catalog, pack, manifest, target materializer,
  hook, or global instruction file to make the skill usable.
- Use relative paths from the skill root and avoid deep reference chains.

## Validate and forward-test

1. Validate YAML, required fields, naming, directory match, local links, and
   resource presence with the official Agent Skills validator.
2. Check that the description distinguishes the nearest semantic neighbor.
3. Forward-test complex skills with realistic inputs and isolated workspaces.
4. Reject no-op success: require the artifact or observable result promised by
   the task.
5. Recheck compatibility-specific claims in the clients that advertise them.

## Completion checklist

- The skill directory contains exactly one `SKILL.md`.
- Frontmatter contains only the portable fields the skill actually needs.
- The description carries positive and negative routing terms.
- Every linked file exists and every bundled script has executable evidence.
- No required behavior depends on another skill or distribution tool.
- Client-specific integrations are deliberate and documented.
- Validation and proportionate forward-test evidence are recorded.
