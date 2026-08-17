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
- Put generated evidence for the active Social Dev project under `knowledge/fixtures/accepted`, runtime contracts under `knowledge/fixtures/accepted/runtime`, canonical brain artifacts under `knowledge/brain`, rebuildable outputs under `knowledge/generated`, source/extraction roots under `knowledge/sources`, K3 gap bookkeeping under `knowledge/gaps`, and reports/roadmaps under `docs/`.
- Do not create generated JSON/PNG/report files at the root.
- `knowledge/sources/` is the read-only C# discovery/source boundary for the active project. Accepted contracts and regression fixtures live under `knowledge/fixtures/accepted`; historical material is retained only under `legacy/`. The removed legacy corpus must not be recreated. Do not recreate `Assembly-CSharp/`.
- Keep evidence separate from runtime: use decompiled/C# evidence to analyze and create contracts, but do not execute it directly in the web runtime.

## Local Development Server Lifecycle

- Before starting a server, inspect existing listeners and process command lines for this repository.
- Reuse a healthy server already running for the repository; do not rely on automatic fallback ports.
- Track every process started during the task and stop its process tree after verification unless the user explicitly asks to keep it running.
- Do not terminate Codex-owned `mcp/server.mjs`, `node_repl`, or processes under `OpenAI\Codex\runtimes`.

## Current history policy

Use the canonical brain/database at `knowledge/brain/sqlite/social_dev_brain.sqlite`, generated packs under `knowledge/generated/`, accepted fixtures under `knowledge/fixtures/accepted/`, and read-only sources under `knowledge/sources/`. Historical K2/G1.5/visual material is under `legacy/` and is not an active runtime, test, build, or query dependency. K2.5, K3, K4, and K4.1 are closed; K4.1 is ready for a future explicitly authorized V8 phase, while V8, integrations, deployment, and persistence/backend work are not started.

## Git Closure Policy

After every user-authorized phase/task that reaches an accepted terminal state:

1. Run the required validation gates.
2. Update `knowledge/brain/exports/CURRENT_STATE.json`.
3. Append one compact milestone record to `docs/state/TASK_LEDGER.jsonl`.
4. Update `PROJECT_STATE.md` and `TODO.md` when the current status or next boundary changes.
5. Inspect `git status` and stage with an explicit allowlist mindset.
6. Audit staged file count, size, file types, and largest files.
7. Commit the completed phase.
8. Push the current `main` branch to the existing configured remote.

Mandatory rules:

- An accepted completed goal normally receives a commit and push to `main`.
- Failed, intermediate, or experimental work stays local unless the user explicitly requests a checkpoint publish.
- Never force-push or rewrite remote history merely to make a phase appear clean.
- Never use `git add .` blindly while forensic or local-only roots are present.
- Never commit original APK/RAR/source ZIP archives, extracted C#, `libil2cpp.so`, `global-metadata.dat`, raw game-source vaults, bulk original assets, `node_modules`, `dist`, caches, or temporary forensic output.
- Preserve read-only local forensic source roots.
- Small provenance/hash manifests are allowed when intentionally part of project evidence.
- Runtime-required promoted product assets and contracts may be committed when intentionally part of the product and reasonably sized.
- If a push is rejected because the remote advanced, do not force-push; fetch and report the divergence before any merge or rebase.
- If authentication is unavailable, keep the validated local commit and report `PUSH_BLOCKED_AUTH` with its commit SHA.
- Do not start the next phase merely because a push succeeded.
- A phase prompt may override automatic commit/push only when the user explicitly says not to commit or push.

## Future Session Startup

Before substantive work, read at minimum:

- `AGENTS.md`
- `knowledge/brain/exports/CURRENT_STATE.json`
- `PROJECT_STATE.md`
- `TODO.md`

Inspect the latest Git commit and history when needed to understand the shared repository baseline.
