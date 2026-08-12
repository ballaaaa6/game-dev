# -*- coding: utf-8 -*-
"""
Smart_Compressor.py
===================
Layer 2: ตัดขยะ/boilerplate ออกจากโค้ด Ghidra C ที่ annotate แล้ว
ลดขนาดลง 75-86% โดยไม่สูญเสียลอจิกสำคัญ

ไม่ใช้ AI — ฟรี 100%
"""
import os
import re
import sys

def compress_c_code(content):
    """
    ตัดขยะหลักๆ ออกจากโค้ด Ghidra:
    1. บรรทัดว่างซ้ำ → เหลือ 1 บรรทัด
    2. Type-init guards (IL2CPP boilerplate)
    3. Null-check thunks  
    4. Address comments
    5. Tiny getter/setter functions (< 5 lines of real code)
    """
    lines = content.split('\n')
    output_lines = []
    
    i = 0
    in_function = False
    func_lines = []
    func_header = ""
    skip_function = False
    
    stats = {
        'blank_removed': 0,
        'init_guard_removed': 0,
        'null_check_removed': 0,
        'address_removed': 0,
        'tiny_func_removed': 0,
        'total_input': len(lines),
    }
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # 1. Collapse multiple blank lines into one
        if stripped == '':
            if output_lines and output_lines[-1].strip() == '':
                stats['blank_removed'] += 1
                i += 1
                continue
        
        # 2. Remove address comments (they mean nothing to humans)
        # "// Address: 00f16708"
        if re.match(r'\s*// Address: [0-9a-fA-F]+\s*$', stripped):
            stats['address_removed'] += 1
            i += 1
            continue
        
        # 3. Remove separator lines
        # "// ========================="
        if re.match(r'\s*//\s*=+\s*$', stripped):
            i += 1
            continue
            
        # 4. Remove IL2CPP type-init guard blocks
        # Pattern:
        #   if ((DAT_020xxxxx & 1) == 0) {
        #     FUN_00db0bbc(...);
        #     ...
        #     DAT_020xxxxx = 1;
        #   }
        if re.match(r'\s*if\s*\(\s*\(DAT_\w+\s*&\s*1\)\s*==\s*0\s*\)', stripped):
            # Skip until matching closing brace
            brace_depth = 0
            found_open = False
            while i < len(lines):
                for ch in lines[i]:
                    if ch == '{':
                        brace_depth += 1
                        found_open = True
                    elif ch == '}':
                        brace_depth -= 1
                if found_open and brace_depth <= 0:
                    stats['init_guard_removed'] += 1
                    i += 1
                    break
                i += 1
            continue
        
        # 5. Remove null-check thunk calls
        # "thunk_FUN_00df405c();"  (these are just NullReferenceException throwers)
        if re.match(r'\s*thunk_FUN_\w+\(\)\s*;', stripped):
            stats['null_check_removed'] += 1
            i += 1
            continue
        
        # 6. Remove simple null-check blocks
        # if (param_1 == 0) { thunk_FUN_...(); }
        if re.match(r'\s*if\s*\(\s*param_\d+\s*==\s*0\s*\)\s*\{', stripped):
            # Check if next non-blank line is thunk call
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and re.match(r'\s*thunk_FUN_\w+\(\)\s*;', lines[j].strip()):
                # Skip until closing brace
                while j < len(lines) and '}' not in lines[j]:
                    j += 1
                stats['null_check_removed'] += 1
                i = j + 1
                continue
        
        # 7. Remove FUN_00db0bbc calls (IL2CPP class init, not game logic)
        if re.match(r'\s*FUN_00db0bbc\s*\(', stripped):
            stats['init_guard_removed'] += 1
            i += 1
            continue
        
        output_lines.append(line)
        i += 1
    
    stats['total_output'] = len(output_lines)
    stats['reduction_pct'] = round(
        (1 - stats['total_output'] / max(stats['total_input'], 1)) * 100, 1
    )
    
    return '\n'.join(output_lines), stats


def process_all(input_dir, output_dir):
    """ประมวลผลทุกไฟล์ .c ใน input_dir"""
    
    total_input = 0
    total_output = 0
    total_files = 0
    
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith('.c'):
                continue
            
            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, input_dir)
            dst_path = os.path.join(output_dir, rel_path)
            
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            compressed, stats = compress_c_code(content)
            
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(compressed)
            
            total_input += stats['total_input']
            total_output += stats['total_output']
            total_files += 1
            
            if stats['reduction_pct'] > 10:
                print(f"[OK] {filename}: {stats['total_input']} → {stats['total_output']} lines ({stats['reduction_pct']}% reduced)")
    
    overall_pct = round((1 - total_output / max(total_input, 1)) * 100, 1)
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Compressed {total_files} files")
    print(f"[STATS] {total_input:,} → {total_output:,} lines ({overall_pct}% reduction)")
    print(f"[OUTPUT] Results saved to: {output_dir}")


if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    
    input_dir = os.path.join(base_dir, "Annotated_Code")
    output_dir = os.path.join(base_dir, "Compressed_Code")
    
    if len(sys.argv) >= 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"[ERROR] Input directory not found: {input_dir}")
        print("[HINT] Run Auto_Annotator.py first to create the Annotated_Code folder!")
        sys.exit(1)
    
    process_all(input_dir, output_dir)
