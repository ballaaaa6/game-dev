"""Validate artifacts produced by the Ghidra export stage.

This is deliberately a separate process so a stale Exported_ALL.c cannot be
mistaken for a successful fresh export by a batch file.
"""

import json
import os
import re
import sys


def fail(message):
    print("[ERROR] " + message)
    return 1


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) < 3:
        print("Usage: python validate_extraction.py <dump_dir> <c_file> <report_file>")
        return 2

    dump_dir, c_file, report_file = [os.path.abspath(path) for path in argv[:3]]
    required = [
        os.path.join(dump_dir, "libil2cpp.so"),
        os.path.join(dump_dir, "script.json"),
        os.path.join(dump_dir, "dump.cs"),
        c_file,
        report_file,
    ]
    for path in required:
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            return fail("Missing or empty artifact: {}".format(path))

    try:
        with open(report_file, "r", encoding="utf-8") as handle:
            report = json.load(handle)
    except Exception as exc:
        return fail("Cannot read export report: {}".format(exc))

    total = int(report.get("total_functions", 0))
    successful = int(report.get("successful_functions", 0))
    failed = int(report.get("failed_functions_count", 0))
    if total == 0:
        return fail("Exporter selected zero functions.")

    with open(c_file, "r", encoding="utf-8", errors="ignore") as handle:
        code = handle.read()
    header_count = len(re.findall(r"^// Function:\s*.+$", code, re.MULTILINE))

    print("[INFO] Export report: {}/{} functions, {} failed".format(
        successful, total, failed
    ))
    print("[INFO] C function headers: {}".format(header_count))

    if header_count != successful:
        return fail(
            "C output/header count mismatch: report={}, C={}".format(
                successful, header_count
            )
        )
    if successful != total:
        return fail(
            "Exporter did not produce one successful result per selected function: "
            "successful={}, total={}".format(successful, total)
        )
    if failed:
        print("[ERROR] Export is incomplete. See failed_functions in {}".format(report_file))
        return 3

    print("[OK] Export artifacts are complete and internally consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
