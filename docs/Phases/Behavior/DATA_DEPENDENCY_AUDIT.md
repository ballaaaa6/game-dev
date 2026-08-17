# Data Dependency Audit

Status: `PASS_DATA_DEPENDENCY_FORENSIC_WITH_SOURCE_LIMITS`

This report is static/offline evidence only. No decompiled C# was executed and no runtime, renderer, MapChip, V8, emulator, server, network, or browser work was started.

Authority is the pinned APK/native set plus the original asset-guide ZIP table members. ZIP table roundtrip is exact for all eight locale/type members. Canonical counts: StaffData=141, JobData=30, SkillData=36, FurnitureData=103.

The machine package is under `knowledge/fixtures/accepted/data-dependency/`. Every record retains English and Japanese raw rows, parsed loader fields, row hashes, C# type refs, and archive provenance.

Resolved native formulas: JobData level interpolation, max-level bonus, Staff.GetSkill index lookup, Staff parameter component sum, and HP max consumer chain. Source limits remain tracked rather than filled with product guesses.
