# APK Toolkit

โฟลเดอร์นี้เก็บเครื่องมือ extraction/decompile และ input APK/ZIP เดิม ไม่ใช่ที่เก็บ generated phase artifacts

- สคริปต์ `create_phase0_*`, `create_phase1_*`, `decode_seb.py` และ `validate_phase1.py` เขียนผลไปที่ `Phases/Phase0/` หรือ `Phases/Phase1/`
- batch/extraction scripts เก่าคงไว้เพื่อ compatibility กับ path เดิมและไม่ควรใช้แทน source roots ที่ freeze แล้ว
- `bodyface_records.json` ถูกย้ายไป `Phases/Phase2/references/`; batch extractor ถูกปรับให้หาไฟล์จากตำแหน่งใหม่
- APK/ZIP ในโฟลเดอร์นี้เป็น input เดิม ไม่ย้ายไปปะปนกับ artifacts

ให้รันคำสั่งจาก workspace root ตาม `Phases/README.md` เพื่อให้ default paths ถูกต้อง
