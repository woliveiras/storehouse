from __future__ import annotations


SOURCE_COMMIT = "783ac878213b61acb914b9151c779c6de0b84286"
SOURCE_TREE_SHA256 = "7de30d71108e8c4e73641a70aaa2d9541ce97f6b826cca528f6eeed0bb73e20d"
BASELINE_COMMIT = "86a4224154fef064005b1bbd49f0efc7c5adfa5d"
BASELINE_TREE_SHA256 = "3b0a2de4895921a4dee1996101fffcb28c8419b68a66f92f86a5af41b27b561f"
LICENSE_SHA256 = "24923e703cfafa4e2c5098f4d5b0442ab43f9405dbdbb9fd961707c32e5e4702"

# Frozen Geremmyas source identities remain stable while Storehouse owns the
# public destination names. Declaration order is the migration inventory order.
SOURCE_TO_SKILL = (
    ("android-ci-setup", "ci-android"),
    ("chromadb-rag-workflow", "ai-eng-rag-pipeline"),
    ("game-ai-2d", "game-dev-2d-ai"),
    ("game-art-2d", "game-dev-2d-art"),
    ("game-audio-2d", "game-dev-2d-audio"),
    ("game-build-and-release", "release-game-dev-2d"),
    ("game-feel-2d", "game-dev-2d-feel"),
    ("game-performance-2d", "game-dev-2d-performance"),
    ("game-save-n-progress", "game-dev-2d-save-progression"),
    ("game-testing-2d", "game-dev-2d-testing"),
    ("game-ui-accessibility", "game-dev-2d-ui-accessibility"),
    ("gameplay-programming-2d", "game-dev-2d-gameplay"),
    ("gcloud-operation", "cloud-ops"),
    ("go-ci-setup", "ci-go"),
    ("langgraph-agent-design", "ai-eng-agent-design"),
    ("llm-integration-review", "ai-eng-llm-integration"),
    ("manage-state-with-zustand", "web-state-zustand"),
    ("model-state-with-xstate", "web-state-xstate"),
    ("paper-review", "writing-academic-edit"),
    ("postgres-query-review", "database-postgresql"),
    ("procedural-generation-2d", "game-dev-2d-procedural-generation"),
    ("python-ci-setup", "ci-python"),
    ("rust-ci-setup", "ci-rust"),
    ("rust-release", "release-rust"),
    ("scientific-case-study-research", "research-case-study-design"),
    ("scientific-paper", "research-paper-authoring"),
    ("supabase-workflow", "cloud-supabase"),
    ("terraform-change", "infra-terraform"),
    ("text-review", "writing-technical-edit"),
    ("typescript-ci-setup", "ci-typescript"),
    ("validate-with-zod", "web-validation-zod"),
)

RETIRED_MIGRATIONS = (
    ("migrate-react-router", "Retired because Storehouse no longer distributes a version-specific React Router migration skill."),
    ("skill-authoring", "Retired because Storehouse uses the host client's skill-creation capability."),
)

EXCLUDED = (
    "brainstorming", "bugfix", "ci-workflow", "decision-framework",
    "design-deep-modules", "docs", "git-commit", "improve-architecture",
    "premortem", "refine", "session-bridge", "shape-domain", "spec", "tdd",
    "technical-research", "verify",
)

SOURCE_MIGRATED = tuple(source for source, _ in SOURCE_TO_SKILL)
MIGRATED = tuple(skill for _, skill in SOURCE_TO_SKILL)

OWNED = (
    "ci-ai-eng",
    "ci-game-dev-2d",
    "ci-terraform",
    "release-android",
    "release-ai-eng",
    "release-go",
    "release-python",
    "release-terraform",
    "release-typescript",
    "sdd-specification",
    "writing-blog-post",
)

SKILLS = (*MIGRATED, *OWNED)

COLLECTIONS = (
    {
        "name": "game-core",
        "description": "Core 2D gameplay programming and deterministic game testing.",
        "skills": ["game-dev-2d-gameplay", "game-dev-2d-testing"],
    },
    {
        "name": "game-ui",
        "description": "Accessible 2D game interfaces and moment-to-moment feel.",
        "skills": ["game-dev-2d-ui-accessibility", "game-dev-2d-feel"],
    },
    {
        "name": "game-systems",
        "description": "AI, procedural generation, saves, and progression for Phaser and Godot 2D.",
        "skills": ["game-dev-2d-ai", "game-dev-2d-procedural-generation", "game-dev-2d-save-progression"],
    },
    {"name": "game-performance", "description": "Measured 2D game performance work.", "skills": ["game-dev-2d-performance"]},
    {"name": "game-audio", "description": "2D game audio systems and lifecycle.", "skills": ["game-dev-2d-audio"]},
    {"name": "game-art", "description": "2D runtime art production, processing, and integration.", "skills": ["game-dev-2d-art"]},
    {"name": "game-ci", "description": "Continuous integration for Phaser and Godot 2D projects.", "skills": ["ci-game-dev-2d"]},
    {"name": "game-release", "description": "Versioned Phaser and Godot 2D release artifacts and evidence.", "skills": ["release-game-dev-2d"]},
    {
        "name": "game-dev",
        "description": "Complete aggregate of the focused Phaser and Godot 2D collections.",
        "includes": ["game-core", "game-ui", "game-systems", "game-performance", "game-audio", "game-art", "game-ci", "game-release"],
    },
    {
        "name": "ci",
        "description": "Continuous integration for AI engineering, Android, game development 2D, Go, Python, Rust, Terraform, and TypeScript.",
        "skills": ["ci-ai-eng", "ci-android", "ci-game-dev-2d", "ci-go", "ci-python", "ci-rust", "ci-terraform", "ci-typescript"],
    },
    {
        "name": "release",
        "description": "Release engineering for AI engineering, Android, game development 2D, Go, Python, Rust, Terraform, and TypeScript.",
        "skills": ["release-ai-eng", "release-android", "release-game-dev-2d", "release-go", "release-python", "release-rust", "release-terraform", "release-typescript"],
    },
    {"name": "android", "description": "Android CI and release engineering.", "skills": ["ci-android", "release-android"]},
    {"name": "go", "description": "Go CI and release engineering.", "skills": ["ci-go", "release-go"]},
    {"name": "python", "description": "Python CI and release engineering.", "skills": ["ci-python", "release-python"]},
    {"name": "rust", "description": "Rust CI and release engineering.", "skills": ["ci-rust", "release-rust"]},
    {"name": "terraform", "description": "Terraform infrastructure, CI, and release engineering.", "skills": ["infra-terraform", "ci-terraform", "release-terraform"]},
    {"name": "typescript", "description": "TypeScript CI, release, and boundary validation.", "skills": ["ci-typescript", "release-typescript", "web-validation-zod"]},
    {
        "name": "web",
        "description": "Zustand, XState, and Zod recipes for web applications.",
        "skills": ["web-state-zustand", "web-state-xstate", "web-validation-zod"],
    },
    {"name": "data", "description": "PostgreSQL, RAG storage, and Supabase workflows.", "skills": ["database-postgresql", "ai-eng-rag-pipeline", "cloud-supabase"]},
    {"name": "infrastructure", "description": "Cloud operations, Supabase, and Terraform infrastructure.", "skills": ["cloud-ops", "cloud-supabase", "infra-terraform"]},
    {"name": "ai-engineering", "description": "Agent, LLM service, RAG pipeline, CI, and release engineering.", "skills": ["ai-eng-agent-design", "ai-eng-llm-integration", "ai-eng-rag-pipeline", "ci-ai-eng", "release-ai-eng"]},
    {
        "name": "scientific-research",
        "description": "Scientific papers, empirical case studies, and academic draft editing.",
        "skills": ["research-paper-authoring", "research-case-study-design", "writing-academic-edit"],
    },
    {"name": "writing", "description": "Technical blog authoring and evidence-preserving editing.", "skills": ["writing-blog-post", "writing-technical-edit", "writing-academic-edit"]},
    {"name": "sdd", "description": "Optional Specification-Driven Development with durable specifications, oracle matrices, reconciliation, and formal review.", "skills": ["sdd-specification"]},
)

SENSITIVE = {
    "ai-eng-agent-design": ["tool-side-effects", "external-systems"],
    "ai-eng-llm-integration": ["external-model-service", "private-data", "privileged-tools"],
    "ai-eng-rag-pipeline": ["database", "persistence", "tenancy"],
    "ci-ai-eng": ["ci-authority", "provider-credentials", "private-evaluation-data", "model-cost"],
    "ci-android": ["ci-authority", "supply-chain", "release-credentials"],
    "ci-game-dev-2d": ["ci-authority", "dependency-execution", "artifact-integrity"],
    "ci-go": ["ci-authority", "dependency-execution", "supply-chain"],
    "ci-python": ["ci-authority", "dependency-execution", "publication"],
    "ci-rust": ["ci-authority", "dependency-execution", "supply-chain"],
    "ci-terraform": ["ci-authority", "cloud-credentials", "plan-secrets", "apply-authority"],
    "ci-typescript": ["ci-authority", "dependency-execution", "supply-chain"],
    "cloud-ops": ["cloud", "iam", "billing", "remote-mutation"],
    "cloud-supabase": ["database", "auth", "storage", "remote-mutation"],
    "database-postgresql": ["database", "locks", "migration", "data-loss"],
    "game-dev-2d-art": ["filesystem", "image-generation"],
    "game-dev-2d-save-progression": ["persistence", "data-loss"],
    "release-android": ["signing", "publish", "upload", "store-authority"],
    "release-ai-eng": ["provider-configuration", "private-data", "model-cost", "rollout-authority"],
    "release-game-dev-2d": ["artifact-integrity", "secrets", "release-authority"],
    "release-go": ["tag", "push", "publish", "upload"],
    "release-python": ["tag", "push", "publish", "upload"],
    "release-rust": ["tag", "push", "publish", "upload"],
    "release-terraform": ["tag", "push", "signing", "registry-publication"],
    "release-typescript": ["tag", "push", "publish", "upload"],
    "research-case-study-design": ["participant-data", "private-research-data"],
    "research-paper-authoring": ["filesystem", "research-artifacts"],
    "infra-terraform": ["infrastructure", "state", "secrets", "destructive-scope"],
    "writing-academic-edit": ["in-place-overwrite"],
    "writing-blog-post": ["private-drafts", "publication-authority"],
    "writing-technical-edit": ["in-place-overwrite"],
}

CODEX_METADATA = {
    "ci-ai-eng", "ci-game-dev-2d", "ci-terraform", "game-dev-2d-ai", "game-dev-2d-art",
    "game-dev-2d-audio", "game-dev-2d-feel", "game-dev-2d-gameplay",
    "game-dev-2d-performance", "game-dev-2d-procedural-generation",
    "game-dev-2d-save-progression", "game-dev-2d-testing",
    "game-dev-2d-ui-accessibility", "release-ai-eng", "release-android", "release-game-dev-2d",
    "release-go", "release-python", "release-terraform", "release-typescript",
    "sdd-specification", "writing-blog-post",
}
