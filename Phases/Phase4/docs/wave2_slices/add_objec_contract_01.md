# AddObjec — bounded scene contract 01

อัปเดต: 2026-08-11

## ขอบเขต

- ฟังก์ชัน: `form.GameForm__AddObjec`
- source: `game-dev-story-mod_Dumped/Categorized_Code/Global/form.c`
- address: `0x00f33b54`
- field names: `game-dev-story-mod_Dumped/dump.cs`

## สิ่งที่ยืนยันได้

1. ฟังก์ชันค้นหา free slot จาก `ObjecEnabled` และใช้ `ObjecMax` เป็น capacity guard
2. slot ที่เลือกถูกเก็บใน `ObjecIndex`
3. `param_2` ถูกเขียนไปยัง `ObjecSyurui`
4. `param_3` ถึง `param_9` ถูกเขียนเป็น `ObjecX`, `ObjecY`, `ObjecCX`, `ObjecCY`, `ObjecWX`, `ObjecWY`, `ObjecSY`
5. ทางเดินปกติตั้ง `ObjecEnabled=1`, `ObjecVisible=1`, `ObjecZX=0` และ `ObjecZY=0`
6. ถ้าไม่สามารถเติม record ได้ จะมีทางเดินที่เขียน `ObjecRefresh=1`

## Neutral pseudocode

```text
slot = first index where ObjecEnabled[slot] == 0
if no free slot or input slot is invalid:
    ObjecRefresh = 1
    return current object index/status

ObjecIndex = slot
ObjecSyurui[slot] = param_2
ObjecX[slot] = param_3
ObjecY[slot] = param_4
ObjecCX[slot] = param_5
ObjecCY[slot] = param_6
ObjecWX[slot] = param_7
ObjecWY[slot] = param_8
ObjecZX[slot] = 0
ObjecZY[slot] = 0
ObjecSY[slot] = param_9
ObjecEnabled[slot] = 1
ObjecVisible[slot] = 1
return slot
```

`ObjecSyurui` เป็นชื่อ field จาก `dump.cs` และเป็นค่าที่ `DrawObj` ใช้ใน dispatch path
แต่ semantic ของทุก numeric value ที่ caller ส่งเข้ามายังต้องตรวจจาก object-type constants
และ room branch ที่เลือกต่อไป

## ยังไม่สรุป

- ค่า `param_2` ในทุก `CallHikkosi` branch ว่าตรงกับ object type ใด
- ความหมายของ `ObjecSY`, `ObjecZX` และ `ObjecZY` ว่าเป็น depth, layer หรือ coordinate component
- placement, seat, collision และ walkable behavior
