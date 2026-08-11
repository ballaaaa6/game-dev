import sys
import os
import re
import argparse


FUNCTION_HEADER = re.compile(r'^// Function:\s*(.*)\s*$')
ADDRESS_HEADER = re.compile(r'^// Address:\s*(.*)\s*$')


def clean_generated_output(output_dir):
    """Remove generated C files while preserving unrelated files."""
    removed_files = 0

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        return removed_files

    if not os.path.isdir(output_dir):
        raise ValueError(f"Output path is not a directory: {output_dir}")

    for root, dirs, files in os.walk(output_dir, topdown=False):
        for filename in files:
            if filename.lower().endswith('.c'):
                os.remove(os.path.join(root, filename))
                removed_files += 1

        for dirname in dirs:
            directory = os.path.join(root, dirname)
            try:
                os.rmdir(directory)
            except OSError:
                # Keep directories that contain non-generated files.
                pass

    return removed_files


def dedupe_c_file(file_path):
    """Keep one copy of each decompiler function block in a C file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore', newline='') as f:
        lines = f.readlines()

    block_starts = [
        index for index, line in enumerate(lines)
        if FUNCTION_HEADER.match(line)
    ]
    if len(block_starts) < 2:
        return 0

    prefix = lines[:block_starts[0]]
    blocks = []
    for index, start in enumerate(block_starts):
        end = block_starts[index + 1] if index + 1 < len(block_starts) else len(lines)
        blocks.append(lines[start:end])

    seen = set()
    output = list(prefix)
    removed_blocks = 0

    for block in blocks:
        function_name = ''
        address = ''
        for line in block:
            function_match = FUNCTION_HEADER.match(line)
            if function_match:
                function_name = function_match.group(1)
                continue
            address_match = ADDRESS_HEADER.match(line)
            if address_match:
                address = address_match.group(1)
                break

        key = (function_name, address)
        if key in seen:
            removed_blocks += 1
            continue

        seen.add(key)
        output.extend(block)

    if removed_blocks:
        temp_path = file_path + '.tmp'
        try:
            with open(temp_path, 'w', encoding='utf-8', newline='') as f:
                f.writelines(output)
            os.replace(temp_path, file_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return removed_blocks


def dedupe_existing_output(output_dir):
    """Dedupe an already-generated Categorized_Code directory in place."""
    if not os.path.isdir(output_dir):
        raise ValueError(f"Existing output directory does not exist: {output_dir}")

    total_files = 0
    total_blocks = 0
    for root, _, files in os.walk(output_dir):
        for filename in files:
            if not filename.lower().endswith('.c'):
                continue
            total_files += 1
            total_blocks += dedupe_c_file(os.path.join(root, filename))

    print(f"Deduped {total_blocks} repeated function blocks across {total_files} C files.")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Split exported Ghidra C code or dedupe an existing generated output."
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Path to Exported_ALL.c',
    )
    parser.add_argument(
        'output_dir',
        nargs='?',
        help='Directory for categorized C files',
    )
    parser.add_argument(
        '--dedupe-existing',
        metavar='DIR',
        help='Dedupe an existing categorized output directory in place',
    )
    args = parser.parse_args(argv)

    if args.dedupe_existing:
        if args.input_file or args.output_dir:
            parser.error('--dedupe-existing cannot be combined with input/output positional arguments')
        return args

    if not args.input_file or not args.output_dir:
        parser.error('input_file and output_dir are required unless --dedupe-existing is used')

    return args

def split_exported_code(input_file, output_dir):
    input_file = os.path.abspath(input_file)
    output_dir = os.path.abspath(output_dir)

    if not os.path.isfile(input_file):
        raise ValueError(f"Input file does not exist: {input_file}")

    if os.path.commonpath([input_file, output_dir]) == output_dir:
        raise ValueError('Input file must not be inside output_dir')

    removed_files = clean_generated_output(output_dir)
    print(f"Reading massive file: {input_file}")
    print(f"Categorizing into: {output_dir}")
    if removed_files:
        print(f"Removed {removed_files} previous generated C files before writing.")

    current_class = "Unknown"
    current_file_handle = None
    file_handles = {}
    file_paths = {}

    # Pattern to extract Class name before $$ (Il2CppDumper format: ClassName$$MethodName)
    func_pattern = re.compile(r'// Function:\s+([^\$]+)\$\$')

    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Check if this line marks the start of a new function
                if line.startswith("// Function: "):
                    match = func_pattern.search(line)
                    if match:
                        new_class = match.group(1).strip()
                    else:
                        # If it doesn't have $$, just use the whole name or "Global"
                        raw_name = line.replace("// Function: ", "").strip()
                        new_class = raw_name.split('_')[0] if '_' in raw_name else "Global"

                    # Sanitize class name for valid filename
                    new_class = "".join(c for c in new_class if c.isalnum() or c in ('_', '-'))

                    if new_class != current_class:
                        current_class = new_class
                        # Group by primary namespace prefix
                        parts = current_class.split('_')
                        if len(parts) > 1 and parts[0] != "":
                            category_name = parts[0]
                        else:
                            category_name = "Global"

                        category_dir = os.path.join(output_dir, category_name)
                        os.makedirs(category_dir, exist_ok=True)

                        file_path = os.path.join(category_dir, f"{current_class}.c")
                        # Windows paths are case-insensitive.  Without a
                        # canonical key, names such as Mono/mono or
                        # System/system open two handles to the same file and
                        # one stream can overwrite the other, losing blocks.
                        file_key = os.path.normcase(os.path.abspath(file_path))
                        if file_key not in file_handles:
                            file_paths[file_key] = file_path
                            file_handles[file_key] = open(file_path, 'w', encoding='utf-8')
                        current_file_handle = file_handles[file_key]

                # Write line to the current file
                if current_file_handle:
                    current_file_handle.write(line)

    finally:
        for handle in file_handles.values():
            handle.close()

    # A fresh run already starts from an empty generated directory. Run the
    # same key-based dedupe once more so duplicate blocks inside a single
    # export cannot leak into the categorized output.
    dedupe_existing_output(output_dir)

    print("Splitting complete! Check the categorized folder.")


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    if args.dedupe_existing:
        dedupe_existing_output(os.path.abspath(args.dedupe_existing))
    else:
        split_exported_code(args.input_file, args.output_dir)
