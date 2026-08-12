# DoEvent — bounded assembly slice 01

อัปเดต: 2026-08-11

## ขอบเขต

- ฟังก์ชัน: `form.GameForm$$DoEvent`
- export namespace: `0x00f5d438`–`0x00f5d4d0`
- raw ELF namespace: `0x00e5d438`–`0x00e5d4d0`
- address delta: raw = export - `0x100000`
- basic blocks: `B0046`–`B0052` (`B0047`, `B0049`, `B0050`, `B0051` เป็น guard/helper blocks)
- alternate continuation ที่อยู่นอก slice: `B0053` ที่ `0x00f5d4d4`
- guard exits ที่อยู่นอก slice: `0x00f6ba04`, `0x00f6ba08`

หลักฐานตรงมาจาก `00f5c704_form_GameForm__DoEvent.asm.txt` และ `wave1_branch_index.json` ช่วงนี้เริ่มจากทางเดินที่ preceding state check ส่งเข้ามา และจบหลัง call `AddKaiwa` ที่ branch ไป continuation `0x00f5d5d8`

## สิ่งที่ยืนยันได้

1. ที่ `0x00f5d438` โหลด pointer จาก global storage, ตั้ง `x1 = 0` และเรียก export `0x00f83b80` raw=`0x00e83b80`
2. `script.json` map raw target เป็น `form.MyFormBase$$LT`; overload ที่ address นี้มี signature `System.String LT(string text)`
3. ที่ `0x00f5d468` อ่าน object จาก `[x9,#0xa88]`; ถ้า null ไป guard exit `0x00f6ba08`
4. index จาก `[x9,#0x878]` ถูกตรวจเทียบกับ array length `[x8,#0x18]`
5. object อีกชุดจาก `[x9,#0x910]` ถูกตรวจ null; element index ที่อ่านจาก array ถูกตรวจเทียบกับ `[x9,#0x18]`
6. string/payload ที่ `[element,#0x20]` ถูกส่งเข้า export `0x018ecc5c` raw=`0x017ecc5c`; `script.json` map เป็น `kairo.unity.util.StringUtil$$Replace`
7. ผลจาก `Replace` ถูกส่งเป็น `TK` เข้า export `0x00f1a908` raw=`0x00e1a908`; `script.json` map เป็น `form.GameForm$$AddKaiwa` overload `void AddKaiwa(GameForm*, string TK, int TModori)` โดย `w2 = 0`
8. หลัง call โหลด state value `3` แล้ว branch ไป continuation `0x00f5d5d8`; slice ไม่อ้างว่า branch นี้คือ event state โดย semantic

## Neutral pseudocode

```text
text = MyFormBase.LT(global_string_pointer, 0)

container = load_pointer(game_form_static + 0xb8)
array_a = load_pointer(container + 0xa88)
if array_a == null:
    goto guard_exit

i = load_i32(container + 0x878)
if unsigned(i) >= load_u32(array_a + 0x18):
    goto guard_exit

array_b = load_pointer(container + 0x910)
if array_b == null:
    goto guard_exit

j = load_i32(array_a[i] + 0x20)
if unsigned(j) >= load_u32(array_b + 0x18):
    goto guard_exit

payload = load_pointer(array_b[j] + 0x20)
replaced = StringUtil.Replace(text, payload, 0)
GameForm.AddKaiwa(game_form, replaced, 0)
store_or_prepare_state(3)
goto continuation(0x00f5d5d8)
```

ใน assembly ยังมี helper target raw=`0x00cb0cc0` ใน `B0047` สำหรับ type/guard path; ไม่ตั้งชื่อ semantic ให้ helper นี้ การเขียน `array_a[i]` และ `array_b[j]` เป็น shorthand ของ address arithmetic ที่เห็นจริง ไม่ใช่การตั้งชื่อชนิดข้อมูลใหม่

## ความหมายที่ยังสรุปไม่ได้

- ยืนยันได้ว่าเป็นทางเดินที่ format/replace string แล้ว enqueue ผ่าน `AddKaiwa`; ยังระบุไม่ได้ว่าเป็น event dispatch ชนิดใด
- ยังไม่ตั้งชื่อ offsets `0x878`, `0x910`, `0xa88` หรือ state `3` เป็น field semantic
- guard exits และ continuation อยู่ภายนอก slice จึงยังไม่สรุป cleanup/return behavior ของทั้ง `DoEvent`

## Confidence และผลต่อ Wave 2

`high` สำหรับ call targets, argument flow, null/bounds checks และ continuation; `medium` สำหรับการเรียกทางเดินนี้ว่า “dialogue/event preparation” ตามชื่อ `AddKaiwa` การ slice นี้เพียงพอให้ Wave 2 ใช้เป็น evidence boundary โดยไม่ต้องเดา selector หรือ asset filename
