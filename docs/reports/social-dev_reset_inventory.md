# Social Dev reset — source inventory

Generated: `2026-08-13T08:57:26.062902+00:00`

This is a read-only provenance pass over the active Social Dev source and evidence roots.

## Source summary

| Source | Files | Bytes | Initial role |
|---|---:|---:|---|
| RAR extraction | 5568 | 55,412,654 | immutable C# evidence baseline |
| C# update | 6154 | 64,609,265 | curated candidate corpus |

## C# update comparison

The comparison uses canonical paths: the archive's top-level `1_Click_CSharp_Code` directory is removed and layout-only `Dependencies/` and `KairoEngine/` wrappers in the update are removed. Split `form/SubForm_Split/` files remain explicit update-only candidates.

| Status | Files | Meaning |
|---|---:|---|
| exact_match | 4980 | same canonical path and SHA-256 |
| modified | 588 | same canonical path but different bytes; review before promotion |
| update_only | 586 | present only in the update corpus |

## Initial classification

| Scope | Update files | Treatment |
|---|---:|---|
| dependency_or_generated | 4770 | inventory only unless a bounded dependency is required |
| engine_or_framework | 612 | dependency evidence; exclude from game schema |
| extraction_support | 4 | retain for provenance, not gameplay semantics |
| gameplay_candidate | 69 | promote only after semantic/provenance review |
| lifecycle_candidate | 3 | save/load and lifecycle evidence; keep separate from entities |
| presentation_candidate | 603 | UI evidence; do not use as state owner |
| review_required | 93 | manual classification required |

## Next gate

Review modified/raw-only/update-only paths, then build the Social Dev canonical schema from `data`, `game`, and bounded `main` lifecycle evidence. Asset promotion remains blocked until the C# selectors and ZIP/APK provenance agree.
