"""Extract numeric AddBodyFace records without inventing missing values.

The decompiler may emit expressions instead of constants.  Those records are
reported as unresolved and are not written with fake zeroes.
"""

import json
import os
import re
import sys


def parse_int(value):
    value = re.sub(r'^\s*(?:\([^)]+\)\s*)+', '', value).strip()
    value = re.sub(r'(?i)(?<=\d)[ul]+$', '', value)
    if not value:
        return None
    negative = value.startswith('-')
    if negative:
        value = value[1:].strip()
    try:
        parsed = int(value, 0)
    except ValueError:
        return None
    return -parsed if negative else parsed


def split_arguments(value):
    arguments = []
    current = []
    depth = 0
    for char in value:
        if char == '(':
            depth += 1
        elif char == ')' and depth > 0:
            depth -= 1
        if char == ',' and depth == 0:
            arguments.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
    arguments.append(''.join(current).strip())
    return arguments


def extract_records(code_content):
    records = []
    unresolved = []
    pattern = r'[A-Za-z0-9_]*AddBodyFace\s*\(([^;]+?)\)\s*;'

    for call_index, match in enumerate(re.finditer(pattern, code_content)):
        args = split_arguments(match.group(1))
        if len(args) < 15:
            unresolved.append({
                "call_index": call_index,
                "reason": "expected at least 15 arguments, found {}".format(len(args)),
                "arguments": args,
            })
            continue

        keys = [
            "face_src_x", "face_src_y", "face_width", "face_height",
            "face_dst_x", "face_dst_y", "body_src_x", "body_src_y",
            "body_width", "body_height", "body_dst_x", "body_dst_y",
        ]
        values = [parse_int(args[index]) for index in range(2, 14)]
        if any(item is None for item in values):
            unresolved.append({
                "call_index": call_index,
                "reason": "one or more arguments are not numeric constants",
                "arguments": args,
            })
            continue

        record = dict(zip(keys, values))
        record["source_call_index"] = call_index
        records.append(record)

    return records, unresolved


def scan_directory(code_dir):
    all_records = []
    unresolved = []
    files_scanned = 0
    for root, _, files in os.walk(code_dir):
        for filename in files:
            if not filename.lower().endswith('.c'):
                continue
            filepath = os.path.join(root, filename)
            files_scanned += 1
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as handle:
                    content = re.sub(r'[\r\n]+', ' ', handle.read())
                records, file_unresolved = extract_records(content)
                for record in records:
                    record["source_file"] = filepath
                all_records.extend(records)
                for issue in file_unresolved:
                    issue["source_file"] = filepath
                unresolved.extend(file_unresolved)
                if records:
                    print("[INFO] Found {} records in {}".format(len(records), filename))
            except Exception as exc:
                unresolved.append({
                    "source_file": filepath,
                    "reason": "file read failed: {}".format(exc),
                })
    return all_records, unresolved, files_scanned


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) < 2:
        print("Usage: python Extract_BodyFace_Records.py <Categorized_Code_Dir> <Output_Json_Path> [Report_Json_Path]")
        return 2

    code_dir = os.path.abspath(argv[0])
    out_file = os.path.abspath(argv[1])
    report_file = os.path.abspath(argv[2]) if len(argv) > 2 else out_file + '.report.json'

    if not os.path.isdir(code_dir):
        print("[ERROR] Directory does not exist: {}".format(code_dir))
        return 1

    print("[WAIT] Scanning {} for AddBodyFace calls...".format(code_dir))
    records, unresolved, files_scanned = scan_directory(code_dir)

    report = {
        "schema": 2,
        "files_scanned": files_scanned,
        "records_written": len(records),
        "unresolved_calls": len(unresolved),
        "unresolved": unresolved,
    }
    parent = os.path.dirname(out_file)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    report_parent = os.path.dirname(report_file)
    if report_parent and not os.path.isdir(report_parent):
        os.makedirs(report_parent)

    with open(report_file, 'w', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write('\n')

    if not records:
        print("[ERROR] No complete numeric AddBodyFace records found.")
        print("[INFO] Report: {}".format(report_file))
        return 3

    temp_file = out_file + '.part'
    with open(temp_file, 'w', encoding='utf-8') as handle:
        json.dump(records, handle, indent=2, ensure_ascii=False)
        handle.write('\n')
    if os.path.exists(out_file):
        os.remove(out_file)
    os.rename(temp_file, out_file)

    print("[SUCCESS] Wrote {} complete records to {}".format(len(records), out_file))
    if unresolved:
        print("[WARNING] {} calls were skipped; see {}".format(len(unresolved), report_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
