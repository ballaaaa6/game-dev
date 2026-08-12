# C# Evidence Tools

The checker scripts in this directory are workspace-relative and can be run from any current directory:

```powershell
python tools/csharp-evidence/check_coverage.py
python tools/csharp-evidence/check_semantic_coverage.py
```

They read `game-dev-story-mod_Dumped/dump.cs` and `knowledge/csharp/primary/`, then write reports to `knowledge/csharp/coverage/`.

The checkers are diagnostic prototypes. Their aggregate results do not establish semantic completeness or C# build readiness.
