# Wave 1 resource-loading contract

เอกสารนี้สรุปเฉพาะ behavior ที่อ่านได้จาก recovered C และ manifest จริง ไม่ตีความชื่อไฟล์ที่ยังไม่มีหลักฐานรองรับ

## ภาพรวมการไหลของข้อมูล

```mermaid
flowchart LR
    A[img.inf / seb.inf] --> B[ResourceManager.LoadStart]
    B --> C[resource index]
    C --> D[img[] / seb[]]
    E[GameForm selector] --> F[AppData.GetImage]
    F --> G[list_ name match]
    G --> C
    H[archive path] --> I[JarInflater extension search]
    I --> J[extracted or archived bytes]
```

## Contract ที่ยืนยันได้

### ResourceManager list parser

หลักฐาน: `game-dev-story-mod_Dumped/Categorized_Code/Global/kairo.c`, `ResourceManager__LoadStart`, บรรทัด 108035 เป็นต้นไป

- รูปแบบที่มี TAB และ token แรกเป็นเลข: `index<TAB>filename[,option...]`
- รูปแบบไม่มีเลข: `filename[,option...]`
- explicit index คงค่าที่ประกาศไว้
- unindexed entry ได้ lowest unused index ตามลำดับใน manifest
- lookup รูปภาพใช้ resource index: `ResourceManager__GetImage(texId) -> img[texId]`

ตัวอย่างจาก manifest จริง:

| manifest | filename | resource index | เหตุผล |
|---|---:|---:|---|
| `game/img.inf` | `body0.png` | 1 | อยู่ที่บรรทัด/ตำแหน่งนั้นในรายการ |
| `game/img.inf` | `body10.png` | 3 | lexical manifest order ไม่ใช่เลขท้ายชื่อ |
| `office/img.inf` | `chair_000.png` | 10 | lowest index ที่ยังว่างหลัง explicit floor indices |
| `office/img.inf` | `chair_001.png` | 20 | lowest index ถัดไปตามลำดับ unindexed |

ดังนั้น `body10.png` ห้าม resolve ด้วยกฎ “suffix 10 = index 10”

### AppData.GetImage

หลักฐาน: `game-dev-story-mod_Dumped/Categorized_Code/Global/main.c`, `main_AppData__GetImage`, บรรทัด 6462

พฤติกรรมที่ยืนยันได้คือวนรายการชื่อ, แยกชื่อก่อน comma, compare กับ requested string และคืน resource-array item ตำแหน่งเดียวกัน หากไม่พบจะ log และคืน null/zero ตาม recovered C path

จึงต้องเก็บ mapping เป็นสองขั้น:

`selector string -> list position -> resource array index -> asset path`

ไม่ควรลดรูปเป็น `selector number -> filename number`

### Extension และ archive lookup

หลักฐาน: `kairo.c`, `JarInflater__ConvertExtension` บรรทัด 169781 และ search/get-data functions ใกล้เคียงกัน

- archive lookup ผ่าน `Config.ConvertExtension`
- รูปที่ source เรียกด้วย `.png` อาจถูก normalize เป็น `.png.bytes` ใน archive
- extraction root ใน Wave 1 ใช้ `.png` ที่อ่าน dimension/hash ได้; suffix `.bytes` เป็น storage/archive concern แยกต่างหาก
- search เป็น case-insensitive หลังสร้าง candidate paths แล้ว

## Selector trace

### imgFace

`Method_form_BootForm_GraphicLoad` (`Method.c`, ฟังก์ชันเริ่มบรรทัด 5184) allocate 36 slots และเขียนลง `GameForm.imgFace` offset `0x1150` โดย expression ที่ recovered C แสดงเป็น:

`StringLiteral_7514 + i + StringLiteral_833`

ค่า literal ที่ extract ได้คือ `StringLiteral_7514 = "false"` และ `StringLiteral_833 = ".png.bytes"` ขณะที่ asset family จริงมี `face_0.png` ถึง `face_35.png` ที่ resource indices 40–75 ใน `game/img.inf`. ความขัดแย้งนี้ถูกบันทึกเป็น `unknown`; ยังไม่แก้ recovered literal ด้วยการคาดเดา

### imgBody

function เดียวกัน allocate 25 slots และใช้:

`IMG_LIST[DDBody + i] + StringLiteral_833`

ปลายทางคือ `GameForm.imgBody` offset `0x1158`. Expression และ count ยืนยันได้ แต่ค่า static `DDBody` ยังไม่ยืนยัน จึงยังไม่ collapse เป็นชื่อไฟล์แน่นอน

### Bihin / floor / event

`LoadBihinImage` ใช้ `IMG_LIST[DDPC]`, `IMG_LIST[DDChair]`, `IMG_LIST[DDDesk]` แล้วเติม suffix เดียวกัน; `EventGChange` ใช้ index fields ของ floor/event และเขียนไปยัง `imgFloorMain`, `imgFloorParts`, `imgFloorCover`, `imgEvent`. Wave 1 จึงเก็บ expression และ destination offsets ไว้ก่อน ไม่ถือว่า selector-to-file mapping ปิดแล้ว

## Machine-readable artifacts

- `artifacts/resource_selector_map.json`: manifests, recovered `IMG_LIST`, selector contracts, source refs และ fixtures
- `artifacts/wave1_build_manifest.json`: source hashes และ count ที่ใช้ตรวจ reproducibility
- `artifacts/wave1_branch_index.json`: assembly CFG scaffold สำหรับเลือก lifecycle slices

## สถานะความมั่นใจ

| ชั้น | สถานะ |
|---|---|
| manifest explicit/implicit index rule | verified |
| `ResourceManager` array lookup | verified |
| `AppData.GetImage` name-to-list lookup | verified |
| archive `.bytes` normalization | verified at contract level |
| `imgFace` exact selector filename | unknown เพราะ recovered prefix conflict |
| `imgBody` exact selector filename | unknown เพราะ `DDBody` base ยังไม่ resolve |
| `NewGamePara`/`DoEvent` branch semantics | unknown; structural index only |

