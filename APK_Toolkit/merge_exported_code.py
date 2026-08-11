"""Merge decompiler outputs by Function + Address without duplicates."""

import argparse
import json
import os
import re


FUNCTION_HEADER = re.compile(r'^// Function:\s*(.*)\s*$')
ADDRESS_HEADER = re.compile(r'^// Address:\s*(.*)\s*$')


def read_blocks(path):
    with open(path, 'r', encoding='utf-8', errors='ignore', newline='') as handle:
        lines = handle.readlines()
    starts = [index for index, line in enumerate(lines) if FUNCTION_HEADER.match(line)]
    prefix = lines[:starts[0]] if starts else lines
    blocks = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        block = lines[start:end]
        name = ''
        address = ''
        for line in block:
            function_match = FUNCTION_HEADER.match(line)
            if function_match:
                name = function_match.group(1)
            address_match = ADDRESS_HEADER.match(line)
            if address_match:
                address = address_match.group(1)
        blocks.append(((name, address), block))
    return prefix, blocks


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base_file')
    parser.add_argument('additional_file')
    parser.add_argument('output_file')
    args = parser.parse_args(argv)

    base_prefix, base_blocks = read_blocks(args.base_file)
    _, additional_blocks = read_blocks(args.additional_file)
    seen = set()
    output = list(base_prefix)
    for key, block in base_blocks:
        if key not in seen:
            seen.add(key)
            output.extend(block)

    added = 0
    for key, block in additional_blocks:
        if key not in seen:
            seen.add(key)
            output.extend(block)
            added += 1

    output_file = os.path.abspath(args.output_file)
    parent = os.path.dirname(output_file)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    temp_file = output_file + '.part'
    with open(temp_file, 'w', encoding='utf-8', newline='') as handle:
        handle.writelines(output)
    if os.path.exists(output_file):
        os.remove(output_file)
    os.rename(temp_file, output_file)

    report = {
        'base_blocks': len(base_blocks),
        'additional_blocks': len(additional_blocks),
        'added_blocks': added,
        'output_blocks': len(seen),
        'output_file': output_file,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
