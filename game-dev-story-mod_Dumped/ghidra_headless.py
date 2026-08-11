# -*- coding: utf-8 -*-
"""Apply Il2CppDumper symbols and create every known native function entry."""

import json
import os
import re

process_fields = [
    "ScriptMethod",
    "ScriptString",
    "ScriptMetadata",
    "ScriptMetadataMethod",
    "Addresses",
]

function_manager = currentProgram.getFunctionManager()
base_address = currentProgram.getImageBase()
USER_DEFINED = ghidra.program.model.symbol.SourceType.USER_DEFINED


def get_addr(value):
    return base_address.add(int(value))


def text(value):
    try:
        return str(value)
    except Exception:
        return "<unprintable>"


def safe_label(value):
    """Convert a recovered IL2CPP name into a valid Ghidra symbol name.

    Il2CppDumper can emit generic/signature names such as
    ``System.String$$Create<ValueTuple<object, int, int>>``.  Those are
    useful as metadata, but angle brackets, commas, and spaces are rejected
    by Ghidra's symbol table.  Keep the original name in the error/report
    context and use a deterministic, conservative symbol spelling here.
    """
    original = text(value).replace("\x00", "")
    label = re.sub(r"[^A-Za-z0-9_]", "_", original)
    label = label.strip("_") or "unnamed_symbol"
    if label[0].isdigit():
        label = "_" + label
    return label[:240]


def set_name(addr, name, report, kind):
    try:
        label = safe_label(name)
        createLabel(addr, label, True, USER_DEFINED)
        report["labels_created"] += 1
    except Exception as exc:
        report["label_errors"].append({
            "kind": kind,
            "address": text(addr),
            "name": text(name),
            "error": "{}: {}".format(exc.__class__.__name__, text(exc)),
        })


def make_function(start, report):
    try:
        existing = function_manager.getFunctionAt(start)
        if existing is not None:
            report["functions_existing"] += 1
            return
        created = createFunction(start, None)
        if created is None:
            report["function_errors"].append({
                "address": text(start),
                "error": "createFunction returned no function",
            })
        else:
            report["functions_created"] += 1
    except Exception as exc:
        report["function_errors"].append({
            "address": text(start),
            "error": "{}: {}".format(exc.__class__.__name__, text(exc)),
        })


def write_report(path, report):
    if not path:
        return
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(path, "w") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")


args = getScriptArgs()
json_path = args[0] if len(args) > 0 else os.path.join(
    os.path.dirname(getSourceFile().getAbsolutePath()), "script.json"
)
report_path = args[1] if len(args) > 1 else os.path.join(
    os.path.dirname(json_path), "ghidra_symbols.report.json"
)

print("Loading script.json from: " + str(json_path))
with open(json_path, "rb") as json_file:
    data = json.loads(json_file.read().decode("utf-8"))

report = {
    "schema": 1,
    "script_json": str(json_path),
    "labels_created": 0,
    "label_errors": [],
    "functions_created": 0,
    "functions_existing": 0,
    "function_errors": [],
    "address_count": 0,
}

if "ScriptMethod" in data and "ScriptMethod" in process_fields:
    script_methods = data["ScriptMethod"]
    monitor.initialize(len(script_methods))
    monitor.setMessage("Methods")
    for script_method in script_methods:
        try:
            addr = get_addr(script_method["Address"])
            set_name(addr, script_method["Name"], report, "ScriptMethod")
        except Exception as exc:
            report["label_errors"].append({
                "kind": "ScriptMethod",
                "error": "{}: {}".format(exc.__class__.__name__, text(exc)),
            })
        monitor.incrementProgress(1)

if "ScriptString" in data and "ScriptString" in process_fields:
    index = 1
    script_strings = data["ScriptString"]
    monitor.initialize(len(script_strings))
    monitor.setMessage("Strings")
    for script_string in script_strings:
        try:
            addr = get_addr(script_string["Address"])
            label = "StringLiteral_" + str(index)
            createLabel(addr, label, True, USER_DEFINED)
            setEOLComment(addr, text(script_string["Value"]))
            report["labels_created"] += 1
        except Exception as exc:
            report["label_errors"].append({
                "kind": "ScriptString",
                "error": "{}: {}".format(exc.__class__.__name__, text(exc)),
            })
        index += 1
        monitor.incrementProgress(1)

if "ScriptMetadata" in data and "ScriptMetadata" in process_fields:
    script_metadata = data["ScriptMetadata"]
    monitor.initialize(len(script_metadata))
    monitor.setMessage("Metadata")
    for metadata in script_metadata:
        try:
            addr = get_addr(metadata["Address"])
            set_name(addr, metadata["Name"], report, "ScriptMetadata")
            setEOLComment(addr, text(metadata["Name"]))
        except Exception as exc:
            report["label_errors"].append({
                "kind": "ScriptMetadata",
                "error": "{}: {}".format(exc.__class__.__name__, text(exc)),
            })
        monitor.incrementProgress(1)

if "ScriptMetadataMethod" in data and "ScriptMetadataMethod" in process_fields:
    metadata_methods = data["ScriptMetadataMethod"]
    monitor.initialize(len(metadata_methods))
    monitor.setMessage("Metadata Methods")
    for metadata_method in metadata_methods:
        try:
            metadata_addr = get_addr(metadata_method["Address"])
            method_addr = get_addr(metadata_method["MethodAddress"])
            name = metadata_method["Name"]
            set_name(metadata_addr, name, report, "ScriptMetadataMethod")
            setEOLComment(metadata_addr, text(name))
            set_name(method_addr, name, report, "ScriptMetadataMethodAddress")
        except Exception as exc:
            report["label_errors"].append({
                "kind": "ScriptMetadataMethod",
                "error": "{}: {}".format(exc.__class__.__name__, text(exc)),
            })
        monitor.incrementProgress(1)

if "Addresses" in data and "Addresses" in process_fields:
    addresses = data["Addresses"]
    report["address_count"] = len(addresses)
    monitor.initialize(len(addresses))
    monitor.setMessage("Addresses")
    seen = set()
    for address in addresses:
        address_key = int(address)
        if address_key not in seen:
            seen.add(address_key)
            make_function(get_addr(address_key), report)
        monitor.incrementProgress(1)

write_report(report_path, report)
print("Script finished!")
print("Addresses processed: " + str(report["address_count"]))
print("Functions created: " + str(report["functions_created"]))
print("Function errors: " + str(len(report["function_errors"])))
print("Symbol report: " + str(report_path))
