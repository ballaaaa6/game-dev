# Social Dev C# clean-room reset

Workspace สำหรับจัดระเบียบและสร้างระบบใหม่จาก Social Dev โดยยึด C#/APK/asset guide เป็นหลักฐาน แล้วแยก source, evidence, derived model และ runtime ออกจากกันอย่างชัดเจน

## โครงสร้างปัจจุบัน

- `knowledge/social-dev/` — active Social Dev evidence, candidate schemas และ provenance gates
- `knowledge/baseline/`, `knowledge/characters/`, `knowledge/language/`, `knowledge/reorganization/`, `knowledge/csharp/`, `knowledge/reverse-engineering/` และ `knowledge/world-assets/` — legacy/historical evidence ที่ถูกกั้น ไม่ใช่ source ใหม่
- `runtime/social-dev/` — active runtime boundary ที่จะสร้างจาก Social Dev contracts
- `runtime/office/` และ `runtime/dashboard/` — legacy runtime ที่หยุดรับ semantics ใหม่
- `tools/social-dev/` — active Social Dev inventory/validation tools
- `tools/` — active Social Dev tools only; legacy tools อยู่ใน `archive/pre-social-reset/tools/`
- `docs/` — Social Dev roadmap/reports และเอกสารเก่าที่ถูก freeze
- `archive/` — legacy tools และแนวคิด AI integration ที่ยังไม่เปิดใช้งาน

## แหล่งข้อมูลที่ห้ามแก้

- `social dev/` — Social Dev source inputs, read-only
- `archive/pre-social-reset/root-sources/` — archived GameDev source/extraction roots, APK toolkit, Ghidra bundle และ viewer

`knowledge/social-dev/evidence/` คือ Social Dev evidence boundary ชุดใหม่; `knowledge/csharp/primary/` เป็น legacy GameDev corpus ที่ถูก freeze และ `Assembly-CSharp/` จะไม่ถูกสร้างกลับ

## จุดเริ่มต้นสำหรับ session ถัดไป

อ่าน [AGENTS.md](AGENTS.md), [PROJECT_STATE.md](PROJECT_STATE.md), [TODO.md](TODO.md) แล้วดู [Social Dev roadmap](docs/roadmap/Roadmap_SocialDev_CSharp_Reset.md)

คำสั่งตรวจสอบหลัก:

```powershell
python -B tools/social-dev/stage_data_package.py
python -B tools/social-dev/build_legacy_reference_scan.py
```
