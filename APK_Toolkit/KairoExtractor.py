"""
╔══════════════════════════════════════════════════════════════╗
║  KAIROSOFT HARDCORE ASSET EXTRACTOR v1.0                     ║
║  สคริปต์สกัดภาพจากเกม Kairosoft แบบ "กดปุ่มเดียวจบ"          ║
║  เขียนขึ้นมาเองทั้งหมด เพื่อรันซ้ำได้กับทุกเกมของค่ายนี้      ║
╚══════════════════════════════════════════════════════════════╝

ขั้นตอนการทำงาน:
  1. อ่านไฟล์ Bundle จาก assets/bin/Data/ (Unity AssetBundle ที่ Kairosoft ดัดแปลง Header)
  2. ดึงไฟล์ TextAsset ดิบออกมา (ใช้ UnityPy + Force Version)
  3. ถอดรหัส XOR ด้วยกุญแจลับ 00112233...EEFF
  4. แยกไฟล์ PNG/INF จาก Kairosoft Virtual Archive

Kairosoft Archive Format (Big-Endian):
  [0x00] uint32 BE : Header/TOC size (offset to data start)  
  [0x04] uint32 BE : Total data payload size  
  [0x08] uint32 BE : File count (N)
  [0x0C] For each file:
         uint32 BE : Filename length
         bytes     : Filename (ASCII, no null terminator in the count)
  After filenames:
         N * uint32 BE : Cumulative data offsets (relative to data start)
  Data section:
         Raw file data for each entry
"""

import os
import sys
import struct
import argparse
import hashlib
import json
import re
import UnityPy
import UnityPy.config

# ============================================================
# CONFIG
# ============================================================
XOR_KEY = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
                 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF])

UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f2"


def safe_text(value):
    """Make UnityPy text safe for logs and filesystem paths.

    UnityPy may expose a binary TextAsset byte array as a Python string with
    surrogate code points.  ``surrogateescape`` recovers those code points
    back to their original byte values instead of raising UnicodeEncodeError.
    """
    value = str(value)
    return value.encode('utf-8', 'backslashreplace').decode('utf-8', 'replace')


def normalize_csv_for_excel(data: bytes, label: str):
    """Return a UTF-8/BOM CSV and repair only an incomplete trailing codepoint.

    Three language tables in this APK end with a partial UTF-8 sequence.  The
    bytes before that suffix are valid CSV, so dropping only the incomplete
    suffix is safer than exposing a replacement character (U+FFFD) to Excel.
    """
    bom = b'\xef\xbb\xbf'
    body = data[3:] if data.startswith(bom) else data
    repaired = False
    try:
        body.decode('utf-8')
    except UnicodeDecodeError as exc:
        trailing_bytes = len(body) - exc.start
        if exc.reason == 'unexpected end of data' and trailing_bytes <= 8:
            print("    [WARN] {} ends with an incomplete UTF-8 sequence; trimming {} trailing byte(s)".format(
                label, trailing_bytes
            ))
            body = body[:exc.start]
            body.decode('utf-8')
            repaired = True
        else:
            raise ValueError("CSV is not valid UTF-8: {} ({})".format(label, exc))
    return bom + body, repaired

# ============================================================
# STEP 1: XOR Decryption (จำลอง kairo.unity.util.Encrypter.Decode)
# ============================================================
def xor_decrypt(data: bytes, key: bytes = XOR_KEY) -> bytes:
    """ถอดรหัส XOR ตามแบบ Kairosoft Encrypter.Decode()
    
    จากโค้ด C (Ghidra decompiled):
      src[i] ^= key[i % key_len]
    """
    result = bytearray(len(data))
    key_len = len(key)
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % key_len]
    return bytes(result)


# ============================================================
# STEP 2: Parse Kairosoft Virtual Archive
# ============================================================
def parse_kairosoft_archive(data: bytes):
    """แยกไฟล์จาก Kairosoft Archive Format (Big-Endian)
    
    Returns:
        list of (filename, file_bytes)
    """
    if len(data) < 12:
        raise ValueError("Archive is smaller than its 12-byte header")

    pos = 0

    def read_u32(offset, label):
        if offset + 4 > len(data):
            raise ValueError("Archive ended while reading {}".format(label))
        return struct.unpack_from('>I', data, offset)[0]

    # Header
    toc_size = read_u32(pos, "TOC size")  # offset to data start
    pos += 4
    total_data_size = read_u32(pos, "payload size")
    pos += 4
    file_count = read_u32(pos, "file count")
    pos += 4
    
    print(f"  Archive Header:")
    print(f"    TOC size (data offset):  {toc_size}")
    print(f"    Total data payload size: {total_data_size:,}")
    print(f"    File count:              {file_count}")
    
    if file_count > 10000:
        print(f"  ERROR: File count too large ({file_count}), archive may be corrupt")
        return []
    
    if toc_size < 12 or toc_size > len(data):
        raise ValueError("Invalid TOC/data offset: {}".format(toc_size))
    if total_data_size > len(data) - toc_size:
        raise ValueError(
            "Payload exceeds archive size: offset={}, payload={}, archive={}"
            .format(toc_size, total_data_size, len(data))
        )

    # อ่านชื่อไฟล์ทั้งหมด
    filenames = []
    for i in range(file_count):
        name_len = read_u32(pos, "filename length")
        pos += 4
        if name_len > len(data) - pos:
            raise ValueError("Filename {} exceeds archive bounds".format(i))
        name = data[pos:pos+name_len].decode('ascii', errors='replace')
        filenames.append(name)
        pos += name_len
    
    # อ่าน offset table (cumulative offsets relative to data_start)
    offsets = []
    for i in range(file_count):
        offset = read_u32(pos, "file offset")
        offsets.append(offset)
        pos += 4
    
    # จุดเริ่มต้นของ data section
    data_start = pos
    print(f"    Data section starts at:  0x{data_start:06x} ({data_start})")
    print(f"    Expected data start:     0x{toc_size:06x} ({toc_size})")
    
    # ตรวจสอบว่า data_start ตรงกับ toc_size ไหม
    # ถ้าไม่ตรง อาจมี alignment padding
    if data_start != toc_size:
        print(f"    Adjusting data_start to match TOC size: {toc_size}")
        data_start = toc_size

    if offsets and offsets[0] != 0:
        raise ValueError("First archive offset is {}, expected 0".format(offsets[0]))
    for index in range(1, len(offsets)):
        if offsets[index] < offsets[index - 1]:
            raise ValueError("Archive offsets are not monotonic at {}".format(index))
    if offsets and offsets[-1] > total_data_size:
        raise ValueError("Last archive offset exceeds payload size")
    
    # แยกไฟล์แต่ละตัว
    files = []
    for i in range(file_count):
        start = data_start + offsets[i]
        if i + 1 < file_count:
            end = data_start + offsets[i + 1]
        else:
            end = data_start + total_data_size
        
        if start < data_start or end < start or end > len(data):
            raise ValueError("File {} points outside archive bounds".format(i))
        file_data = data[start:end]
        
        # Kairosoft adds an 8-byte header to ALL files inside the archive.
        # [0-3] File Hash / CRC
        # [4-7] File Size (this build stores payload+4, not payload+8)
        if len(file_data) >= 8:
            declared_be = struct.unpack_from('>I', file_data, 4)[0]
            declared_le = struct.unpack_from('<I', file_data, 4)[0]
            payload_size = len(file_data) - 8
            declared_sizes = (payload_size, len(file_data), len(file_data) - 4)
            if declared_be in declared_sizes or declared_le in declared_sizes:
                file_data = file_data[8:]
            else:
                # Preserve bytes when the size field does not validate instead
                # of silently discarding source data.
                print("    [WARN] File {} has an unverified 8-byte header; preserving bytes".format(i))
        
        files.append((filenames[i], file_data))
    
    return files


# ============================================================
# STEP 3: Extract TextAssets from Unity Bundle
# ============================================================
def extract_textassets_from_bundle(bundle_path: str):
    """ดึง TextAsset ทั้งหมดจากไฟล์ Unity Bundle ที่ Kairosoft ดัดแปลง Header
    
    Returns:
        list of (name, raw_bytes)
    """
    env = UnityPy.load(bundle_path)
    results = []
    
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            parsed = None
            try:
                parsed = obj.read()
            except Exception:
                parsed = None

            typed_name = getattr(parsed, "m_Name", None) if parsed else None
            typed_script = getattr(parsed, "m_Script", None) if parsed else None
            if typed_name is not None and typed_script is not None:
                name = safe_text(typed_name)
                if isinstance(typed_script, str):
                    # UnityPy can decode arbitrary binary TextAsset payloads
                    # into a str containing U+DCxx surrogate bytes.  Recover
                    # the original bytes rather than dropping this bundle.
                    script_bytes = typed_script.encode('utf-8', 'surrogateescape')
                else:
                    script_bytes = bytes(typed_script)
            else:
                # อ่าน raw bytes จาก reader โดยตรง (ไม่ผ่าน string decode)
                reader = obj.reader
                reader.Position = obj.byte_start

                # TextAsset format: string m_Name, byte[] m_Script
                name_len = reader.read_int()
                if name_len < 0 or name_len > 16 * 1024 * 1024:
                    raise ValueError("Invalid TextAsset name length: {}".format(name_len))
                name_bytes = reader.read_bytes(name_len)
                name = safe_text(name_bytes.decode('utf-8', errors='replace'))
                reader.align_stream()

                script_len = reader.read_int()
                if script_len < 0 or script_len > 1024 * 1024 * 1024:
                    raise ValueError("Invalid TextAsset data length: {}".format(script_len))
                script_bytes = reader.read_bytes(script_len)

            results.append((name, script_bytes))
            print(f"    TextAsset: '{name}' ({len(script_bytes):,} bytes)")
    
    return results


# ============================================================
# MAIN: Full Pipeline
# ============================================================
def is_bundle_candidate(filename: str):
    basename = os.path.basename(filename)
    stem = basename.rsplit('.', 1)[0]
    if len(stem) == 32 and re.match(r'^[0-9a-fA-F]{32}$', stem):
        return True
    return basename.lower().endswith(('.bundle', '.unity3d', '.assets'))


def safe_output_path(root: str, relative_name: str):
    relative_name = relative_name.replace('\\', '/')
    relative_name = relative_name.lstrip('/')
    relative_name = re.sub(r'^[A-Za-z]:', '', relative_name)
    parts = [part for part in relative_name.split('/') if part not in ('', '.', '..')]
    if not parts:
        parts = ['unnamed.bin']
    candidate = os.path.abspath(os.path.join(root, *parts))
    root_abs = os.path.abspath(root)
    if os.path.commonpath([root_abs, candidate]) != root_abs:
        raise ValueError("Unsafe output path: {}".format(relative_name))
    return candidate


def unique_output_path(path: str, content: bytes):
    if not os.path.exists(path):
        return path
    with open(path, 'rb') as existing:
        if existing.read() == content:
            return path
    digest = hashlib.sha1(content).hexdigest()[:10]
    root, extension = os.path.splitext(path)
    return root + '_' + digest + extension


def extract_all(apk_data_dir: str, output_dir: str, csv_bom: bool = False):
    """
    Pipeline หลัก: 
      APK data dir → Unity Bundle → TextAsset → XOR Decrypt → Kairosoft Archive → PNG/INF files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print(" KAIROSOFT HARDCORE ASSET EXTRACTOR v1.0")
    print("=" * 70)
    print(f" Input:  {apk_data_dir}")
    print(f" Output: {output_dir}")
    print()
    
    # สแกนหาไฟล์ Bundle ทั้งหมด (ชื่อเป็น 32-char hex hash)
    bundle_files = []
    for root, _, filenames in os.walk(apk_data_dir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if is_bundle_candidate(filename):
                bundle_files.append(path)
    bundle_files.sort()
    
    print(f"[1/4] สแกนไฟล์ Bundle... พบ {len(bundle_files)} ไฟล์")
    print()
    
    total_extracted = 0
    total_archives = 0
    errors = []
    csv_repairs = []
    raw_assets = 0
    total_textassets = 0
    
    for bundle_name in sorted(bundle_files):
        bundle_path = bundle_name
        bundle_size = os.path.getsize(bundle_path)

        print(f"[2/4] Processing Bundle: {os.path.relpath(bundle_path, apk_data_dir)} ({bundle_size:,} bytes)")
        
        # Step 2.1: ดึง TextAssets
        try:
            bundle_textassets = extract_textassets_from_bundle(bundle_path)
        except Exception as e:
            print(f"  ⚠ Skip (cannot parse bundle): {e}")
            errors.append({"stage": "bundle", "path": bundle_path, "error": str(e)})
            print()
            continue
        
        if not bundle_textassets:
            print(f"  ⚠ Skip (no TextAssets found)")
            print()
            continue
        
        total_textassets += len(bundle_textassets)
        for asset_name, raw_bytes in bundle_textassets:
            print(f"\n[3/4] ถอดรหัส XOR: '{asset_name}' ({len(raw_bytes):,} bytes)")
            
            # Step 3: XOR Decrypt
            decrypted = xor_decrypt(raw_bytes)
            
            # Step 4: ลองแยกไฟล์จาก archive
            try:
                # ตรวจสอบว่า header สมเหตุสมผลไหม
                file_count = struct.unpack_from('>I', decrypted, 8)[0]
                if file_count == 0 or file_count > 10000:
                    print(f"  ⚠ ไม่ใช่ Kairosoft Archive (file_count={file_count})")
                    # บันทึกเป็นไฟล์ดิบ
                    raw_out = safe_output_path(output_dir, f"{asset_name}_raw.bin")
                    raw_out = unique_output_path(raw_out, decrypted)
                    os.makedirs(os.path.dirname(raw_out), exist_ok=True)
                    with open(raw_out, 'wb') as f:
                        f.write(decrypted)
                    print(f"  → Saved raw: {raw_out}")
                    raw_assets += 1
                    continue
                
                print(f"\n[4/4] แยกไฟล์จาก Kairosoft Archive: '{asset_name}'")
                files = parse_kairosoft_archive(decrypted)
                
                if not files:
                    print(f"  ⚠ ไม่พบไฟล์ใน archive")
                    continue
                
                total_archives += 1
                
                # สร้างโฟลเดอร์ย่อยตามชื่อ archive
                archive_dir = safe_output_path(output_dir, asset_name)
                os.makedirs(archive_dir, exist_ok=True)
                
                for fname, fdata in files:
                    out_path = safe_output_path(archive_dir, fname)

                    # Excel-compatible mode strips malformed trailing UTF-8
                    # bytes and writes a BOM so non-ASCII languages open cleanly.
                    if csv_bom and fname.lower().endswith('.csv'):
                        fdata, repaired = normalize_csv_for_excel(fdata, fname)
                        if repaired:
                            csv_repairs.append({
                                "archive": asset_name,
                                "file": fname,
                                "reason": "incomplete trailing UTF-8 sequence",
                            })

                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    out_path = unique_output_path(out_path, fdata)
                    with open(out_path, 'wb') as f:
                        f.write(fdata)
                    total_extracted += 1
                
                print(f"  ✓ แยกไฟล์สำเร็จ {len(files)} ไฟล์ → {archive_dir}")
                
            except Exception as e:
                print(f"  ⚠ Error parsing archive: {e}")
                errors.append({"stage": "archive", "asset": asset_name, "bundle": bundle_path, "error": str(e)})
                # บันทึกเป็นไฟล์ดิบ
                raw_out = safe_output_path(output_dir, f"{asset_name}_raw.bin")
                raw_out = unique_output_path(raw_out, decrypted)
                os.makedirs(os.path.dirname(raw_out), exist_ok=True)
                with open(raw_out, 'wb') as f:
                    f.write(decrypted)
                print(f"  → Saved raw: {raw_out}")
                raw_assets += 1
        
        print()
    
    summary = {
        "schema": 1,
        "input": os.path.abspath(apk_data_dir),
        "output": os.path.abspath(output_dir),
        "bundle_candidates": len(bundle_files),
        "textassets": total_textassets,
        "archives": total_archives,
        "files_extracted": total_extracted,
        "raw_assets": raw_assets,
        "warnings": csv_repairs,
        "errors": errors,
    }
    report_path = os.path.join(output_dir, "extraction_report.json")
    with open(report_path, 'w', encoding='utf-8') as report_file:
        json.dump(summary, report_file, indent=2, ensure_ascii=False)
        report_file.write('\n')

    print("=" * 70)
    print(f" สรุปผล:")
    print(f"   Archives ที่แกะสำเร็จ: {total_archives}")
    print(f"   ไฟล์ที่สกัดได้ทั้งหมด: {total_extracted}")
    print(f"   Raw assets: {raw_assets}")
    print(f"   Warnings: {len(csv_repairs)}")
    print(f"   Errors: {len(errors)}")
    print(f"   Output: {output_dir}")
    print(f"   Report: {report_path}")
    print("=" * 70)
    return summary


# ============================================================
# Entry Point
# ============================================================
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Extract Kairosoft assets from a Unity Data directory."
    )
    parser.add_argument(
        "apk_data_dir",
        help="Path to the extracted APK's assets/bin/Data directory",
    )
    parser.add_argument(
        "output_dir",
        help="Directory where extracted assets will be written",
    )
    parser.add_argument(
        "--csv-bom",
        action="store_true",
        help="Add UTF-8 BOM to CSV files (changes extracted bytes; default is exact bytes)",
    )
    args = parser.parse_args(argv)

    apk_data_dir = os.path.abspath(os.path.expanduser(args.apk_data_dir))
    output_dir = os.path.abspath(os.path.expanduser(args.output_dir))

    if not os.path.isdir(apk_data_dir):
        parser.error(f"Input directory does not exist: {apk_data_dir}")

    os.makedirs(output_dir, exist_ok=True)
    summary = extract_all(apk_data_dir, output_dir, csv_bom=args.csv_bom)
    if summary["bundle_candidates"] == 0:
        print("[ERROR] No Unity bundle candidates found.")
        return 2
    if summary["archives"] == 0 and summary["files_extracted"] == 0 and summary["raw_assets"] == 0:
        print("[ERROR] No assets were extracted.")
        return 3
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
