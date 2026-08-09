from __future__ import annotations


SOURCE_COMMIT = "783ac878213b61acb914b9151c779c6de0b84286"
SOURCE_TREE_SHA256 = "7de30d71108e8c4e73641a70aaa2d9541ce97f6b826cca528f6eeed0bb73e20d"
TUXEDO_COMMIT = "168922a54b695fd2446295c58157981079d2d5d6"
TUXEDO_TREE_SHA256 = "3ed55c2bcd4614cd7074a6ff4ff01199a81b4dd9f31d9912fa25f191c85a967f"
LICENSE_SHA256 = "24923e703cfafa4e2c5098f4d5b0442ab43f9405dbdbb9fd961707c32e5e4702"
SDD_ORIGIN_COMMIT = "27ef05b97211b74845af78095ce7d5d852358dbf"

MIGRATED = (
    "android-ci-setup", "chromadb-rag-workflow", "game-ai-2d", "game-art-2d",
    "game-audio-2d", "game-build-and-release", "game-feel-2d",
    "game-performance-2d", "game-save-n-progress", "game-testing-2d",
    "game-ui-accessibility", "gameplay-programming-2d", "gcloud-operation",
    "go-ci-setup", "langgraph-agent-design", "llm-integration-review",
    "manage-state-with-zustand", "migrate-react-router", "model-state-with-xstate",
    "paper-review", "postgres-query-review", "procedural-generation-2d",
    "python-ci-setup", "rust-ci-setup", "rust-release",
    "scientific-case-study-research", "scientific-paper", "skill-authoring",
    "supabase-workflow", "terraform-change", "text-review",
    "typescript-ci-setup", "validate-with-zod",
)

EXCLUDED = (
    "brainstorming", "bugfix", "ci-workflow", "decision-framework",
    "design-deep-modules", "docs", "git-commit", "improve-architecture",
    "premortem", "refine", "session-bridge", "shape-domain", "spec", "tdd",
    "technical-research", "verify",
)

# The bootstrap migration remains a frozen 33 + 16 inventory. `spec` was
# subsequently adapted into a Storehouse-owned optional methodology.
OWNED = ("spec",)
SKILLS = (*MIGRATED, *OWNED)

COLLECTIONS = (
    {
        "name": "game-core",
        "description": "Core 2D gameplay programming and deterministic game testing.",
        "skills": ["gameplay-programming-2d", "game-testing-2d"],
    },
    {
        "name": "game-ui",
        "description": "Accessible 2D game interfaces and moment-to-moment feel.",
        "skills": ["game-ui-accessibility", "game-feel-2d"],
    },
    {
        "name": "game-systems",
        "description": "AI, procedural generation, saves, and progression for Phaser and Godot 2D.",
        "skills": ["game-ai-2d", "procedural-generation-2d", "game-save-n-progress"],
    },
    {"name": "game-performance", "description": "Measured 2D game performance work.", "skills": ["game-performance-2d"]},
    {"name": "game-audio", "description": "2D game audio systems and lifecycle.", "skills": ["game-audio-2d"]},
    {"name": "game-art", "description": "2D runtime art production, processing, and integration.", "skills": ["game-art-2d"]},
    {"name": "game-delivery", "description": "Reproducible Phaser and Godot build and release evidence.", "skills": ["game-build-and-release"]},
    {
        "name": "game-dev",
        "description": "Complete aggregate of the seven focused Phaser and Godot 2D collections.",
        "includes": ["game-core", "game-ui", "game-systems", "game-performance", "game-audio", "game-art", "game-delivery"],
    },
    {"name": "android", "description": "Android CI and delivery checks.", "skills": ["android-ci-setup"]},
    {"name": "go", "description": "Go CI and supply-chain checks.", "skills": ["go-ci-setup"]},
    {"name": "python", "description": "Python CI, validation, and publishing preparation.", "skills": ["python-ci-setup"]},
    {"name": "rust", "description": "Rust CI and release engineering.", "skills": ["rust-ci-setup", "rust-release"]},
    {"name": "typescript", "description": "TypeScript CI and boundary validation.", "skills": ["typescript-ci-setup", "validate-with-zod"]},
    {
        "name": "web",
        "description": "React Router migration plus Zustand, XState, and Zod recipes.",
        "skills": ["migrate-react-router", "manage-state-with-zustand", "model-state-with-xstate", "validate-with-zod"],
    },
    {"name": "data", "description": "PostgreSQL, ChromaDB/RAG, and Supabase workflows.", "skills": ["postgres-query-review", "chromadb-rag-workflow", "supabase-workflow"]},
    {"name": "infrastructure", "description": "Google Cloud and Terraform operations.", "skills": ["gcloud-operation", "terraform-change"]},
    {"name": "ai", "description": "LangGraph, LLM service, and RAG design and review.", "skills": ["langgraph-agent-design", "llm-integration-review", "chromadb-rag-workflow"]},
    {
        "name": "scientific-research",
        "description": "Scientific papers, empirical case studies, and academic draft review.",
        "skills": ["scientific-paper", "scientific-case-study-research", "paper-review"],
    },
    {"name": "writing", "description": "Evidence-preserving technical blog review.", "skills": ["text-review"]},
    {"name": "skill-maintenance", "description": "Portable Agent Skill authoring and review.", "skills": ["skill-authoring"]},
    {"name": "sdd", "description": "Optional Specification-Driven Development with durable specs, oracle matrices, reconciliation, and formal review.", "skills": ["spec"]},
)

SENSITIVE = {
    "android-ci-setup": ["ci-authority", "supply-chain", "release-credentials"],
    "chromadb-rag-workflow": ["database", "persistence", "tenancy"],
    "game-art-2d": ["filesystem", "image-generation"],
    "game-build-and-release": ["artifact-integrity", "secrets", "release-authority"],
    "game-save-n-progress": ["persistence", "data-loss"],
    "gcloud-operation": ["cloud", "iam", "billing", "remote-mutation"],
    "go-ci-setup": ["ci-authority", "dependency-execution", "supply-chain"],
    "langgraph-agent-design": ["tool-side-effects", "external-systems"],
    "llm-integration-review": ["external-model-service", "private-data", "privileged-tools"],
    "migrate-react-router": ["dependency-mutation", "filesystem-rewrite"],
    "paper-review": ["in-place-overwrite"],
    "postgres-query-review": ["database", "locks", "migration", "data-loss"],
    "python-ci-setup": ["ci-authority", "dependency-execution", "publication"],
    "rust-ci-setup": ["ci-authority", "dependency-execution", "supply-chain"],
    "rust-release": ["tag", "push", "publish", "upload"],
    "scientific-case-study-research": ["participant-data", "private-research-data"],
    "scientific-paper": ["filesystem", "research-artifacts"],
    "supabase-workflow": ["database", "auth", "storage", "remote-mutation"],
    "terraform-change": ["infrastructure", "state", "secrets", "destructive-scope"],
    "text-review": ["in-place-overwrite"],
    "typescript-ci-setup": ["ci-authority", "dependency-execution", "supply-chain"],
}

CODEX_METADATA = {
    "game-ai-2d", "game-art-2d", "game-audio-2d", "game-build-and-release",
    "game-feel-2d", "game-performance-2d", "game-save-n-progress",
    "game-testing-2d", "game-ui-accessibility", "gameplay-programming-2d",
    "procedural-generation-2d", "spec",
}
