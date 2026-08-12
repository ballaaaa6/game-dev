# W4.5-R3 — MessageGraph และ audio

`form_GameForm___draw` อ่าน `MessageGraph`. ค่า `1` และ `2` เข้าสู่ image-draw path ของ
`imgMain` โดยใช้ crop ขนาด `0xe × 0xe`; พฤติกรรมการ render นี้ verified แต่ชื่อ graph
เชิง product ยังไม่ทราบ.

`MessageMaxTime - MessageTime == 1` เรียก `SoundPlay(param_1,1,3,0)`. threshold และ
call ถูกยืนยัน แต่ชื่อเสียง/ความหมาย UI ยังเปิด.
