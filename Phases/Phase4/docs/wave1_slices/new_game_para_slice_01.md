# NewGamePara — bounded assembly slice 01

อัปเดต: 2026-08-11

## ขอบเขต

- ฟังก์ชัน: `form.GameForm$$NewGamePara`
- export namespace: `0x00f28148`–`0x00f281d0`
- raw ELF namespace: `0x00e28148`–`0x00e281d0`
- address delta: raw = export - `0x100000`
- basic blocks: `B0068`, `B0069`, `B0070`, `B0071`, `B0072`, `B0073`, `B0074`
- continuation ที่อยู่นอก slice: `B0075` ที่ `0x00f281d4`; exit labels `0x00f33b4c` และ `0x00f33b50`

หลักฐานตรงมาจาก `00f265b8_form_GameForm__NewGamePara.asm.txt` และ block metadata ใน `wave1_branch_index.json` การเลือกช่วงนี้ทำให้เห็น guard, field access, call ที่ map ได้ และ post-call checks โดยไม่ตีความทั้งฟังก์ชัน 13,671 instructions

## สิ่งที่ยืนยันได้

1. ที่ `0x00f28148` โหลด pointer จาก `[x0,#0xe0]` และถ้าเป็นศูนย์จะเรียก target `0x00db0cc0` ก่อนกลับมาอ่าน pointer อีกครั้ง
2. ที่ `0x00f28164` และ `0x00f28184` อ่าน base pointer จาก `[x0,#0xb8]` แล้วเขียนค่า `2` ไปที่ `[x8,#0x8c]` ในทางเดินแรก
3. ทางเดินที่ `0x00f28184` เตรียม argument constants (`4, 0xcc, 0x31, 0x1d, 0xf, 0x1b, 0`) และค่า `0x17` บน stack ก่อนเรียก `0x00f33b54` raw=`0x00e33b54`
4. `script.json` map raw target `0x00e33b54` เป็น `form.GameForm$$AddObjec` ด้วย signature `int AddObjec(GameForm*, int, int, int, int, int, int, int, int)`
5. ผลลัพธ์ `w0` จาก call ถูกเขียนไปที่ `[x21,#0x20]` หลังตรวจ `x21` และ `[x21,#0x18]`
6. ก่อนออกจาก slice มี null/bounds guards บน object ที่ `[x8,#0x308]`; ทางเดินปกติไปต่อที่ `B0075`

## Neutral pseudocode

```text
if guard_object_at(x0 + 0xe0) is null:
    call unresolved_helper(raw=0x00cb0cc0)

base = load_pointer(x0 + 0xb8)
if base_state_guard_requires_helper(base + 0xe0):
    call unresolved_helper(raw=0x00cb0cc0)

store_u32(base + 0x8c, 2)
result = GameForm.AddObjec(
    x0,
    4, 0xcc, 0x31, 0x1d, 0xf, 0x1b, 0,
    0x17,                 # stack argument observed at [sp]
)

if x21 == null or load_u32(x21 + 0x18) == 0:
    goto exit_label
store_u32(x21 + 0x20, result)

next_object = load_pointer(base + 0x308)
if next_object == null:
    goto exit_label
continue_at(B0075)
```

`base`, `x21`, `0x8c`, `0x308`, `0x18` และ `0x20` ถูกคงเป็น register/offset ตาม assembly ไม่ตั้งชื่อ field จาก offset เพียงอย่างเดียว `0x00cb0cc0` ยังไม่ถูกตั้งชื่อ semantic

## ความหมายที่ยังสรุปไม่ได้

- ยังระบุไม่ได้ว่าทางเดินนี้เป็น initialization, reset หรือ transition ของ gameplay
- constants ที่ส่งเข้า `AddObjec` ยืนยันได้ว่าเป็น literal arguments แต่ยังไม่ควรแปลงเป็นชื่อประเภท/พิกัดจากเลขอย่างเดียว
- ยังไม่เชื่อม `x21` หรือ object offset กับ selector `DDBody`, `DDPC`, `DDChair`, `DDDesk`

## Confidence และผลต่อ Wave 2

`medium-high` สำหรับ control-flow, offsets, literals และ `AddObjec` target; `low` สำหรับ semantic label ของ state/object การ slice นี้เพียงพอให้ Wave 2 อ้างถึง initialization-like bounded behavior ได้โดยไม่ต้องเดา resource index หรือ filename แต่ไม่ใช่ recovered source ของทั้งฟังก์ชัน
