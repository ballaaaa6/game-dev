# Social Dev C# boundary — first pass

## Evidence baseline

The immutable RAR extraction contains 5,568 files. The structural inventory currently targets the `data`, `game`, `game.routeSearch`, and `main` slices: 72 inputs, 82 discovered types, 3,430 fields, and 1,685 methods.

Structural fingerprint:

```text
1b2f9396f2768545d4f719022fb1b116df0de9a5347fb46337a8417e1257093a
```

The inventory is structural evidence only. It does not claim that every decompiled method body is correct or executable.

## Update corpus result

After removing the archive wrapper and the update-only `Dependencies/` and `KairoEngine/` layout wrappers:

| Result | Count | Meaning |
|---|---:|---|
| Exact canonical match | 4,980 | same canonical path and SHA-256 |
| Modified | 588 | same canonical path, different bytes |
| Update-only | 586 | not present in the RAR baseline; mostly split presentation files |

The update is therefore useful as a revision candidate, but it is not a clean replacement that can be promoted wholesale.

The candidate-slice diff shows that all 60 modified files remove the `Cpp2ILHelpers.NoteDecompilerIssue` calls: the raw slice has 16,699 such markers and the update has 0. The `//IL_...` annotations remain unchanged at 29,030, and the structural inventory is unchanged at 72 inputs, 82 types, 3,430 fields, and 1,685 methods. This is a cleanup of decompiler annotations, not proof that the bodies are repaired or buildable.

Standalone-marker normalization confirms all 60 modified candidate files become byte-equivalent after removing only those marker lines; there are zero content changes beyond markers. The update is therefore a cleaner presentation of the same decompiler evidence, while the RAR extraction remains the provenance anchor.

## Derived scaffold result

The human-authored derived scaffold was reviewed and removed before runtime work began. It was never extracted evidence and never became a state owner. Its historical disposition record is retained for provenance; no fields from it are eligible for the Social Dev model.

## Promotion order

1. Promote no code yet; finish semantic review of the display-relevant `data` and `game` slice.
2. Resolve the 588 modified files, starting with the 44 `data` files, 23 `game` files, and 2 route-search files.
3. Review the 3 lifecycle files under `main`/`KairoEngine/main` separately.
4. Keep all form and split-form files presentation evidence.
5. Use the ZIP guide and APK metadata to validate selectors and asset relationships after the data/entity boundary is stable.
