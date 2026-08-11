# -*- coding: utf-8 -*-
"""Export Ghidra decompilation results without silently losing functions.

This script runs inside Ghidra's Jython environment.  It intentionally favors
reproducibility and an explicit failure report over maximum parallelism.

Arguments:
    selector       ALL, CLASS:<text>, NAME:<exact name>, ADDRESS:<address>,
                   or REPORT:<export report> to retry only failed functions.
    output_file    C output path.
    report_file    Optional JSON report path.

Environment variables:
    GHIDRA_EXPORT_THREADS          default: 4
    GHIDRA_DECOMPILE_TIMEOUT       default: 600 seconds
    GHIDRA_DECOMPILE_RETRY_TIMEOUT default: 1800 seconds
    GHIDRA_DECOMPILE_RETRIES       default: 2 retries after the first attempt
"""

import codecs
import json
import os

import java.lang
from java.util.concurrent import Executors, TimeUnit
from java.util.concurrent.atomic import AtomicInteger
from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.util.task import ConsoleTaskMonitor


def env_int(name, default_value, minimum=1, maximum=None):
    value = os.environ.get(name)
    if value is None:
        return default_value
    try:
        parsed = int(value)
    except Exception:
        return default_value
    if parsed < minimum:
        parsed = minimum
    if maximum is not None and parsed > maximum:
        parsed = maximum
    return parsed


def ensure_parent(path):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)


def replace_file(source, destination):
    if os.path.exists(destination):
        os.remove(destination)
    os.rename(source, destination)


def read_failed_selectors(report_path):
    with open(report_path, "rb") as report_file:
        report = json.loads(report_file.read().decode("utf-8"))

    selectors = set()
    for item in report.get("failed_functions", []):
        name = item.get("name")
        address = item.get("address")
        if name:
            selectors.add(("name", str(name)))
        if address:
            selectors.add(("address", str(address).lower()))
    return selectors


def function_matches(func, selector, failed_selectors):
    name = str(func.getName())
    address = str(func.getEntryPoint().toString()).lower()

    if selector == "ALL":
        return True
    if selector.startswith("CLASS:"):
        return selector[6:] in name
    if selector.startswith("NAME:"):
        return name == selector[5:]
    if selector.startswith("ADDRESS:"):
        wanted = selector[8:].lower()
        return address == wanted or address.lstrip("0") == wanted.lstrip("0")
    if selector.startswith("REPORT:"):
        return ("name", name) in failed_selectors or ("address", address) in failed_selectors
    return selector in name


def error_message(result):
    try:
        message = result.getErrorMessage()
        if message:
            return str(message)
    except Exception:
        pass
    return "Decompiler did not report a completed result."


def decompile_once(func, timeout_seconds, max_payload_mb):
    decomp = DecompInterface()
    try:
        options = DecompileOptions()
        options.setMaxPayloadMBytes(max_payload_mb)
        decomp.setOptions(options)
        decomp.openProgram(currentProgram)
        monitor = ConsoleTaskMonitor()
        result = decomp.decompileFunction(func, timeout_seconds, monitor)
        if result is not None and result.decompileCompleted():
            decompiled = result.getDecompiledFunction()
            if decompiled is not None:
                return {
                    "ok": True,
                    "code": str(decompiled.getC()),
                }
        return {
            "ok": False,
            "error": error_message(result) if result is not None else "No decompiler result.",
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": "{}: {}".format(exc.__class__.__name__, str(exc)),
        }
    finally:
        decomp.dispose()


def make_header(func):
    return (
        "// ==========================================================================================\n"
        "// Function: {}\n"
        "// Address: {}\n"
        "// ==========================================================================================\n"
    ).format(str(func.getName()), str(func.getEntryPoint().toString()))


args = getScriptArgs()
selector = args[0] if len(args) > 0 else "ALL"
out_file = args[1] if len(args) > 1 else os.path.join(
    os.path.dirname(getSourceFile().getAbsolutePath()), "Exported_Code.c"
)
report_file = args[2] if len(args) > 2 else out_file + ".report.json"

threads = env_int("GHIDRA_EXPORT_THREADS", 4, 1, 32)
timeout_seconds = env_int("GHIDRA_DECOMPILE_TIMEOUT", 600, 1)
retry_timeout_seconds = env_int(
    "GHIDRA_DECOMPILE_RETRY_TIMEOUT", max(timeout_seconds, 1800), 1
)
retry_count = env_int("GHIDRA_DECOMPILE_RETRIES", 2, 0, 10)
max_payload_mb = env_int("GHIDRA_MAX_PAYLOAD_MB", 256, 16, 4096)

failed_selectors = set()
if selector.startswith("REPORT:"):
    failed_selectors = read_failed_selectors(selector[7:])

print("========================================")
print("Exporting functions with selector: " + str(selector))
print("Threads: {} | timeout: {}s | retry timeout: {}s | retries: {}".format(
    threads, timeout_seconds, retry_timeout_seconds, retry_count
))
print("Decompiler max payload: {} MB".format(max_payload_mb))
print("========================================")

function_manager = currentProgram.getFunctionManager()
target_functions = []
for function in function_manager.getFunctions(True):
    if function_matches(function, selector, failed_selectors):
        target_functions.append(function)

total_functions = len(target_functions)
print("Found {} functions to decompile.".format(total_functions))

results = [None] * total_functions
failures = [None] * total_functions
completed_count = AtomicInteger(0)


class DecompileTask(java.lang.Runnable):
    def __init__(self, index, func):
        self.index = index
        self.func = func

    def run(self):
        name = str(self.func.getName())
        address = str(self.func.getEntryPoint().toString())
        attempts = []
        success = None

        for attempt in range(retry_count + 1):
            limit = timeout_seconds if attempt == 0 else retry_timeout_seconds
            result = decompile_once(self.func, limit, max_payload_mb)
            if result.get("ok"):
                success = result
                break
            attempts.append({
                "attempt": attempt + 1,
                "timeout_seconds": limit,
                "error": result.get("error", "Unknown decompiler error."),
            })

        if success is not None:
            results[self.index] = make_header(self.func) + success["code"] + "\n\n"
        else:
            failures[self.index] = {
                "name": name,
                "address": address,
                "attempts": attempts,
            }

        count = completed_count.incrementAndGet()
        if count % 100 == 0 or count == total_functions:
            print("Progress: {} / {}".format(count, total_functions))


if total_functions > 0:
    executor = Executors.newFixedThreadPool(threads)
    for index, function in enumerate(target_functions):
        executor.execute(DecompileTask(index, function))
    executor.shutdown()
    executor.awaitTermination(7, TimeUnit.DAYS)

successful_functions = 0
failed_functions = []
ensure_parent(out_file)
ensure_parent(report_file)

partial_out = out_file + ".part"
if os.path.exists(partial_out):
    os.remove(partial_out)
with codecs.open(partial_out, "w", "utf-8") as output:
    for result in results:
        if result:
            output.write(result)
            successful_functions += 1

for failure in failures:
    if failure:
        failed_functions.append(failure)

report = {
    "schema": 1,
    "selector": str(selector),
    "total_functions": total_functions,
    "successful_functions": successful_functions,
    "failed_functions_count": len(failed_functions),
    "threads": threads,
    "timeout_seconds": timeout_seconds,
    "retry_timeout_seconds": retry_timeout_seconds,
    "retry_count": retry_count,
    "max_payload_mb": max_payload_mb,
    "failed_functions": failed_functions,
}

partial_report = report_file + ".part"
if os.path.exists(partial_report):
    os.remove(partial_report)
with codecs.open(partial_report, "w", "utf-8") as report_handle:
    json.dump(report, report_handle, indent=2, sort_keys=True)
    report_handle.write("\n")

replace_file(partial_out, out_file)
replace_file(partial_report, report_file)

print("========================================")
print("Export finished. Successful: {} / {}".format(
    successful_functions, total_functions
))
print("Failed: {}".format(len(failed_functions)))
print("Saved C: " + str(out_file))
print("Saved report: " + str(report_file))
print("========================================")
