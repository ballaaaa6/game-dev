# -*- coding: utf-8 -*-
"""
Auto_Annotator.py
=================
Layer 1: อ่าน dump.cs แล้วเปลี่ยนชื่อ offset ในโค้ด Ghidra C ให้เป็นชื่อฟิลด์จริง
เช่น *(int *)(param_1 + 0xd8)  →  this.state_  (GameForm.state_ at offset 0xD8)

ไม่ใช้ AI — ฟรี 100%
"""
import os
import re
import sys
import json
from collections import defaultdict

def parse_dump_cs(dump_path):
    """
    อ่าน dump.cs แล้วสกัดข้อมูลออกมาเป็น:
    {
        "GameForm": {
            "instance_fields": {"0xD8": "state_", "0xE0": "dialog_", ...},
            "static_fields": {"0x0": "softLabels_", "0x8": "VIEW_W", ...},
            "methods": ["ToString", "AddBodyFace", ...],
            "parent": "MyFormBase"
        },
        ...
    }
    """
    classes = {}
    current_class = None
    current_section = None  # "Fields" or "Methods"
    
    print(f"[WAIT] Parsing dump.cs ({os.path.getsize(dump_path) / 1024 / 1024:.1f} MB)...")
    
    with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.rstrip()
            
            # Detect class definitions
            # e.g. "public class GameForm : MyFormBase // TypeDefIndex: 3928"
            cls_match = re.match(
                r'\s*(?:public|private|internal|protected)?\s*(?:sealed\s+)?(?:abstract\s+)?'
                r'(?:class|struct|enum)\s+([^\s:{]+)(?:\s*:\s*([^\s/{]+))?\s*(?://.*)?$',
                line
            )
            if cls_match:
                raw_name = cls_match.group(1).strip()
                parent = cls_match.group(2).strip() if cls_match.group(2) else None
                # Skip compiler-generated classes like <>c
                if '<>' in raw_name:
                    current_class = None
                    continue
                current_class = raw_name
                classes[current_class] = {
                    "instance_fields": {},
                    "static_fields": {},
                    "methods": [],
                    "parent": parent
                }
                current_section = None
                continue
            
            if current_class is None:
                continue
                
            # Detect section headers
            if line.strip() == '// Fields':
                current_section = 'Fields'
                continue
            elif line.strip() == '// Methods':
                current_section = 'Methods'
                continue
            elif line.strip() == '// Properties':
                current_section = 'Properties'
                continue
            
            if current_section == 'Fields':
                # Match field declarations like:
                # public int state_; // 0xD8
                # internal static int CameraX; // 0x40
                field_match = re.match(
                    r'\s*(?:public|private|internal|protected)\s+'
                    r'((?:static|readonly|const)\s+)*'
                    r'(?:\S+\s+)+?'        # type (could be multi-word like "int[][]")
                    r'(\w+)\s*;'           # field name
                    r'\s*//\s*(0x[0-9A-Fa-f]+)',  # offset
                    line
                )
                if field_match:
                    modifiers = field_match.group(1) or ""
                    field_name = field_match.group(2)
                    offset = field_match.group(3).upper()
                    
                    is_static = 'static' in modifiers
                    if is_static:
                        classes[current_class]["static_fields"][offset] = field_name
                    else:
                        classes[current_class]["instance_fields"][offset] = field_name
                        
                # Match const fields (no offset, but useful for documentation)
                # public const int STATE_MAIN = 0;
                        
            elif current_section == 'Methods':
                # Match method declarations like:
                # public void AddBodyFace(...) { }
                method_match = re.match(
                    r'\s*(?:public|private|internal|protected)\s+'
                    r'(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:sealed\s+)?(?:abstract\s+)?'
                    r'(?:\S+\s+)'          # return type
                    r'(\w+)\s*\(',         # method name
                    line
                )
                if method_match:
                    classes[current_class]["methods"].append(method_match.group(1))
    
    # Count stats
    total_fields = sum(
        len(c["instance_fields"]) + len(c["static_fields"]) 
        for c in classes.values()
    )
    total_methods = sum(len(c["methods"]) for c in classes.values())
    
    print(f"[SUCCESS] Parsed {len(classes)} classes, {total_fields} fields, {total_methods} methods")
    return classes


def build_replacement_map(classes):
    """
    สร้าง lookup table สำหรับ find-and-replace ในโค้ด C
    
    เราต้องดูจากชื่อฟังก์ชันในโค้ด Ghidra ว่ามันอยู่ใน class ไหน
    เช่น "form_GameForm__ToString" → class = "GameForm"
    
    จากนั้นเอา instance_fields ของ class นั้นมาแทนที่:
    *(int *)(param_1 + 0xd8)  →  this.state_
    """
    # Build a map from Ghidra's "ClassName" pattern to our class data
    # Ghidra uses format like: form_GameForm, main_AppData, kairo_unity_ui_Graphics
    # The last part after the final _ before $$ is the class name
    return classes


def annotate_c_file(c_file_path, classes, output_path):
    """
    อ่านไฟล์ .c แล้วเปลี่ยนชื่อ offset ให้เป็นชื่อฟิลด์จริง
    """
    with open(c_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_size = len(content)
    replacements_made = 0
    
    # 1. Find all function headers to determine which class we're in
    # Pattern: "// Function: form_GameForm$$AddBodyFace"
    # or the C function name: "void form_GameForm__AddBodyFace(...)"
    
    # Split content into function blocks
    func_blocks = re.split(r'(// Function: .+)', content)
    
    annotated_blocks = []
    current_class_name = None
    current_class_data = None
    
    for block in func_blocks:
        # Check if this is a function header
        func_header = re.match(r'// Function: (.+)', block)
        if func_header:
            func_full_name = func_header.group(1).strip()
            # Extract class name: "form_GameForm$$AddBodyFace" → try to find "GameForm"
            # Pattern: anything$$method  → class is the part before $$
            parts = func_full_name.split('$$')
            if parts:
                # The class part might be like "form_GameForm" or "main_AppData"
                class_part = parts[0]
                # Try to match to our known classes
                # Strategy: try progressively shorter suffixes
                segments = class_part.split('_')
                found = False
                for i in range(len(segments)):
                    candidate = '_'.join(segments[i:])
                    if candidate in classes:
                        current_class_name = candidate
                        current_class_data = classes[candidate]
                        found = True
                        break
                if not found:
                    # Try just the last segment
                    if segments[-1] in classes:
                        current_class_name = segments[-1]
                        current_class_data = classes[current_class_name]
            
            annotated_blocks.append(block)
            continue
        
        # For code blocks, do the replacement if we know the class
        if current_class_data:
            # Replace instance field accesses:
            # *(int *)(param_1 + 0xd8)  →  this.state_    /* 0xd8 */
            # *(long *)(param_1 + 0xe0) →  this.dialog_   /* 0xe0 */
            for offset_hex, field_name in current_class_data["instance_fields"].items():
                offset_lower = offset_hex.lower()
                # Pattern: (param_1 + 0xd8) or (param_1 + 0xD8)
                pattern = re.compile(
                    r'\(param_1\s*\+\s*' + re.escape(offset_lower) + r'\)',
                    re.IGNORECASE
                )
                new_block, count = pattern.subn(
                    f'(param_1 + {offset_lower}) /* this.{field_name} */',
                    block
                )
                if count > 0:
                    block = new_block
                    replacements_made += count
            
            # Replace static field accesses from the TypeInfo pointer:
            # These appear as offsets from the static field base
            # Less predictable pattern, so we add as comments where possible
        
        annotated_blocks.append(block)
    
    annotated_content = ''.join(annotated_blocks)
    
    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(annotated_content)
    
    return replacements_made


def process_all(dump_cs_path, code_dir, output_dir, target_folders=None):
    """
    ประมวลผลทั้งหมด: อ่าน dump.cs → annotate ทุกไฟล์ .c
    """
    if target_folders is None:
        target_folders = ['form', 'main', 'surface', 'data', 'cfg', 'panel', 'kfw', 'kairo', 'edition']
    
    # Step 1: Parse dump.cs
    classes = parse_dump_cs(dump_cs_path)
    
    # Save parsed class data as JSON for reuse
    meta_path = os.path.join(output_dir, '_class_metadata.json')
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert to serializable format
    serializable = {}
    for cls_name, cls_data in classes.items():
        serializable[cls_name] = {
            "instance_fields": cls_data["instance_fields"],
            "static_fields": cls_data["static_fields"],
            "methods": cls_data["methods"],
            "parent": cls_data["parent"]
        }
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Saved class metadata to {meta_path}")
    
    # Step 2: Process target folders
    total_replacements = 0
    total_files = 0
    
    for folder_name in target_folders:
        folder_path = os.path.join(code_dir, folder_name)
        if not os.path.exists(folder_path):
            print(f"[SKIP] Folder not found: {folder_name}")
            continue
            
        out_folder = os.path.join(output_dir, folder_name)
        
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if not filename.endswith('.c'):
                    continue
                    
                src_path = os.path.join(root, filename)
                rel_path = os.path.relpath(src_path, folder_path)
                dst_path = os.path.join(out_folder, rel_path)
                
                count = annotate_c_file(src_path, classes, dst_path)
                total_replacements += count
                total_files += 1
                
                if count > 0:
                    print(f"[OK] {filename}: {count} annotations")
    
    print(f"\n{'='*60}")
    print(f"[SUCCESS] Annotated {total_files} files with {total_replacements} field name replacements!")
    print(f"[OUTPUT] Results saved to: {output_dir}")


if __name__ == "__main__":
    # Default paths
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    
    dump_cs = os.path.join(base_dir, "game-dev-story-mod_Dumped", "dump.cs")
    code_dir = os.path.join(base_dir, "game-dev-story-mod_Dumped", "Categorized_Code")
    output_dir = os.path.join(base_dir, "Annotated_Code")
    
    if len(sys.argv) >= 4:
        dump_cs = sys.argv[1]
        code_dir = sys.argv[2]
        output_dir = sys.argv[3]
    
    process_all(dump_cs, code_dir, output_dir)
