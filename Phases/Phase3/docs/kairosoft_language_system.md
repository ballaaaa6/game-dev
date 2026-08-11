# Language System — Current Extraction Reference

สถานะเอกสาร: อ้างอิงจาก CSV และ dump ชุดปัจจุบัน

คู่มือเดิมมีการอ้าง `GameDevStory_EN.csv`, การแบ่งช่วง ID และตัวอย่างข้อความที่
ยังไม่ได้ตรวจเทียบกับ extraction ปัจจุบัน เอกสารนี้จึงแยก “สิ่งที่พบจริง” ออกจาก
“สิ่งที่ต้องตรวจต่อ”

## Source of truth ปัจจุบัน

ไฟล์ภาษาที่พบจริงใน `game-dev-story-mod_Sprites/language/` มี 12 ภาษา:

`de`, `es`, `fr`, `hi`, `it`, `ko`, `pt`, `ru`, `SC`, `TC`, `TH`, `tr`

ไม่มี `GameDevStory_EN.csv` ในโฟลเดอร์ language ของ extraction ปัจจุบัน
แม้ dump จะมี function ชื่อ `Language__English` อยู่ก็ตาม ซึ่งอาจเป็น enum,
fallback หรือ runtime support และยังไม่ควรสรุปว่าเป็น asset ภาษาอังกฤษที่แกะได้

## โครงสร้าง CSV ที่ยืนยันได้

แต่ละไฟล์มี metadata เช่น:

- `@title`
- `@language`
- `@scale`
- `@appli`
- `@version`
- `@author`

หลัง metadata เป็น record ที่มี language ID เช่น `#00000` และข้อความ
CSV ชุดปัจจุบันถูกแก้ให้:

- ตัด Kairosoft per-file header 8 ไบต์
- ใช้ UTF-8 BOM สำหรับ Excel
- คง ID และ placeholder เดิม
- ซ่อม trailing UTF-8 sequence ที่ไม่สมบูรณ์ 3 ไฟล์ โดยไม่เติมข้อความเดา

สถานะจาก `extraction_report.json`: archives 7, extracted files 436,
errors 0, warnings 3

## Function entry points ที่ควร trace

จาก dump ปัจจุบันพบ function ที่เกี่ยวข้องกับ language และข้อความ เช่น:

- `kairo_unity_util_Language__Get`
- `kairo_unity_util_Language__GetLanguageCode`
- `kairo_unity_util_Language__SetTextTable`
- `kairo_unity_util_Language__TranslateText`
- `kairo_unity_util_Language__English`
- `kairo_unity_util_Language__Japanese`
- `form_GameForm__DrawFukidashi`
- `form_GameForm__GetTalkIndex`
- `form_GameForm__GetHumanTalkName`

ต้องอ่าน callsite และ arguments เพิ่มเติมก่อนสรุปว่า function ใดเป็น lookup,
formatter, language selector หรือ chat bubble provider

## สิ่งที่ยังไม่ยืนยัน

อย่าใช้ข้อสรุปต่อไปนี้จากเอกสารเก่าโดยตรง:

- ID ช่วง `#00000–#00043` เป็น chat bubble ทั้งหมด
- ID ช่วง `#00994–#01003` เป็น news/sales ทั้งหมด
- ID `#01008–#01010` เป็น employee request ทั้งหมด
- ทุกข้อความถูกเรียกด้วย `Language.GetString` รูปแบบเดียวกัน
- placeholder ทุกตัวใช้ index ตามลำดับแบบ JavaScript

ให้พิสูจน์ด้วยการค้น ID ใน CSV, `script.json`, `dump.cs`, C output และ callsite
ที่เรียก language functions

## Runtime adapter สำหรับเว็บ

เมื่อ trace เสร็จแล้วจึงสร้าง JSON locale และ adapter ลักษณะนี้:

```ts
type LanguageEntry = {
  id: string;
  text: string;
  locale: string;
  placeholders: number[];
  sourceFile: string;
  confidence: 'verified' | 'csv-only' | 'inferred';
};
```

ฟังก์ชันเว็บควรทำสิ่งต่อไปนี้:

1. รับ `id` และ locale
2. fallback เมื่อไม่มี locale หรือ ID
3. ตรวจ placeholder ก่อนแทนค่า
4. ไม่ทำลาย `<0>`, `<1>` หรือ token พิเศษ
5. เก็บ source ID เพื่อย้อนกลับไปหา CSV ได้

## ลำดับการแปลสำหรับ AI Agent Office

เริ่มจากข้อความที่เกี่ยวกับ runtime ใหม่:

1. idle/chat bubble
2. working, done, blocked และ break
3. task assignment และ approval request
4. notification และ activity log

ข้อความเกมที่เกี่ยวกับยอดขาย เงิน ranking และ progression ยังไม่ต้องแปลจนกว่า
จะมีคำสั่งให้นำระบบนั้นกลับมาใช้ใน dashboard

## Excel rule

ให้แก้ CSV ที่ `game-dev-story-mod_Sprites/language/` ได้โดยตรงใน Excel แต่ต้อง:

- ห้ามเปลี่ยน language ID
- ห้ามลบ metadata
- ห้ามเปลี่ยน placeholder
- บันทึกเป็น UTF-8 CSV
- ตรวจว่าไฟล์ยังเปิดด้วย UTF-8 BOM และไม่มี formula/format ที่ Excel เติมเอง
