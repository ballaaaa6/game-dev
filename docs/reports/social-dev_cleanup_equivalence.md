# Social Dev C# cleanup equivalence

This pass removes only standalone `Cpp2ILHelpers.NoteDecompilerIssue(...)` lines in memory, then compares hashes. It never changes source files.

| Result | Files | Meaning |
|---|---:|---|
| exact | 12 | raw/update bytes already equal |
| marker cleanup only | 60 | equal after removing marker lines |
| content change beyond markers | 0 | requires semantic review |
| missing | 0 | not comparable in both corpora |

## Gate

If all candidate files are exact or marker-cleanup-only, the update is a cleaner evidence presentation rather than a new semantic implementation. The raw baseline remains the provenance anchor.
