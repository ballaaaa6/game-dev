# -*- coding: utf-8 -*-
"""Export exact Ghidra disassembly for functions the C decompiler rejected.

This is a lossless fallback for very large/complex functions: it preserves
the function name, address, bytes, mnemonics, operands, and instruction
boundaries without waiting for the decompiler to produce C.
"""

import codecs
import json
import os


def safe_text(value):
    try:
        return str(value)
    except Exception:
        return "<unprintable>"


def address_from_report(value):
    value = safe_text(value).strip()
    try:
        return toAddr(value)
    except Exception:
        return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(value)


def byte_text(instruction):
    values = []
    for value in instruction.getBytes():
        values.append("%02x" % (int(value) & 0xff))
    return " ".join(values)


def operand_text(instruction):
    values = []
    for index in range(instruction.getNumOperands()):
        values.append(safe_text(instruction.getDefaultOperandRepresentation(index)))
    return ", ".join(values)


args = getScriptArgs()
report_path = args[0] if len(args) > 0 else os.path.join(
    os.path.dirname(getSourceFile().getAbsolutePath()), "Exported_ALL.report.json"
)
output_dir = args[1] if len(args) > 1 else os.path.join(
    os.path.dirname(report_path), "Failed_Functions_Assembly"
)

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

with open(report_path, "rb") as report_file:
    report = json.loads(report_file.read().decode("utf-8"))

listing = currentProgram.getListing()
function_manager = currentProgram.getFunctionManager()
combined_path = os.path.join(output_dir, "failed_functions.asm.txt")
summary = []

with codecs.open(combined_path, "w", "utf-8") as combined:
    combined.write("; Failed-function assembly fallback\n")
    combined.write("; Program: %s\n\n" % safe_text(currentProgram.getName()))

    for item in report.get("failed_functions", []):
        name = safe_text(item.get("name", "unnamed_function"))
        address_text = safe_text(item.get("address", ""))
        try:
            address = address_from_report(address_text)
            function = function_manager.getFunctionAt(address)
            if function is None:
                function = function_manager.getFunctionContaining(address)
            if function is None:
                raise RuntimeError("Ghidra function was not found at %s" % address_text)

            body = function.getBody()
            instructions = listing.getInstructions(body, True)
            safe_name = "".join(
                character if character.isalnum() or character in "._-$" else "_"
                for character in name
            ) or "unnamed_function"
            output_path = os.path.join(
                output_dir, "%s_%s.asm.txt" % (address_text, safe_name[:180])
            )

            lines = []
            lines.append("; Function: %s" % name)
            lines.append("; Address: %s" % address_text)
            lines.append("; Entry: %s" % safe_text(function.getEntryPoint()))
            lines.append("; Body bytes: %s" % safe_text(body.getNumAddresses()))
            lines.append("")

            while instructions.hasNext():
                instruction = instructions.next()
                lines.append(
                    "%s  %-12s %s    ; %s"
                    % (
                        safe_text(instruction.getAddress()),
                        byte_text(instruction),
                        safe_text(instruction.getMnemonicString()),
                        operand_text(instruction),
                    )
                )

            with codecs.open(output_path, "w", "utf-8") as output_file:
                output_file.write("\n".join(lines) + "\n")
            combined.write("\n".join(lines) + "\n\n")
            summary.append({
                "name": name,
                "address": address_text,
                "status": "ok",
                "instructions": len(lines) - 5,
                "file": output_path,
            })
        except Exception as exc:
            message = "%s: %s" % (exc.__class__.__name__, safe_text(exc))
            combined.write("; FAILED %s %s\n; %s\n\n" % (address_text, name, message))
            summary.append({
                "name": name,
                "address": address_text,
                "status": "error",
                "error": message,
            })

summary_path = os.path.join(output_dir, "failed_functions.asm.report.json")
with codecs.open(summary_path, "w", "utf-8") as summary_file:
    json.dump({"schema": 1, "source_report": report_path, "functions": summary}, summary_file, indent=2)
    summary_file.write("\n")

print("Assembly fallback finished: %d functions" % len(summary))
print("Assembly output: " + str(output_dir))
print("Assembly report: " + str(summary_path))
