# Agent Instructions

This file applies to the workspace root and all subdirectories unless a nearer `AGENTS.md` defines more specific rules.

## Cross-Session Handoff

1. Before starting work, always read `AGENTS.md`, `PROJECT_STATE.md`, and any relevant handoff/state files.
2. If `TODO.md` or `DECISIONS.md` exists and is relevant, read it as well.
3. After reading state, inspect the actual codebase and files before continuing; never treat state as a substitute for repository verification.
4. `PROJECT_STATE.md` stores only completed work, current status, problems/constraints, decisions, changed files, and next work.
5. Update `PROJECT_STATE.md` and relevant `TODO.md` entries immediately when the project status changes materially.
6. Before ending a session or when the user requests a handoff, inspect the actual files and bring state documents up to date.
7. Keep handoffs concise; do not repeat details that can be recovered by reading the codebase.

## Engineering Loop — Persistent Delivery Rule

This rule is the default for every task in this workspace and every future session:

1. Use an end-to-end engineering loop: inspect real state/code → define acceptance criteria → implement → test/verify → fix and repeat until it passes.
2. Treat the available data and evidence as sufficient to begin. Ask for more information only when a blocker cannot be resolved from the repository or available tools.
3. Use any appropriate method, tool, or external service within the authorized scope and available budget to finish the work.
4. Do not hand off unfinished or partial work, and do not claim completion before all acceptance criteria pass. Deliver only when the result is usable and verified.
5. Before handoff, inspect the actual files and run verification proportionate to the risk, such as tests, builds, renders, smoke checks, or behavior checks, then report observable results.
6. If an unavoidable blocker remains, do not mark the task complete. State the exact blocker and what is required to continue.

## Language Policy — English-First Project Files

1. All new and modified project-owned prose, documentation, reports, roadmaps, state files, TODOs, code comments, test descriptions, and generated summaries must be written in English.
2. Preserve exact original-language strings, quoted source text, extracted values, identifiers, binary assets, raw datasets, source/extraction roots, and archived historical material when changing them would alter provenance.
3. In mixed evidence documents, translate only authored explanatory prose; keep source-derived values and quoted labels exact.
4. This language rule applies to files we author or modify. It does not authorize rewriting read-only source roots, raw evidence, or archived provenance.

## Workspace Conventions

- Base conclusions on the current source/extraction and code evidence; do not infer the meaning of anything that remains `unknown`.
- Keep the existing source roots read-only.
- Put generated evidence for the active Social Dev project under `knowledge/social-dev/evidence`, runtime contracts under `runtime/social-dev/evidence`, and reports/roadmaps under `docs/`.
- Do not create generated JSON/PNG/report files at the root.
- `knowledge/social-dev/evidence/` is the primary C# discovery evidence for the active project; legacy C# evidence remains under `archive/pre-social-reset/knowledge/`; do not recreate `Assembly-CSharp/`.
- Keep evidence separate from runtime: use decompiled/C# evidence to analyze and create contracts, but do not execute it directly in the web runtime.

## Local Development Server Lifecycle

- Before starting a server, inspect existing listeners and process command lines for this repository.
- Reuse a healthy server already running for the repository; do not rely on automatic fallback ports.
- Track every process started during the task and stop its process tree after verification unless the user explicitly asks to keep it running.
- Do not terminate Codex-owned `mcp/server.mjs`, `node_repl`, or processes under `OpenAI\Codex\runtimes`.
