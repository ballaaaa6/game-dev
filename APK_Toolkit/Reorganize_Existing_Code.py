import os
import shutil
import sys

def reorganize_folder(target_dir):
    print(f"Reorganizing files in {target_dir}...")
    
    if not os.path.exists(target_dir):
        print(f"[ERROR] Directory does not exist: {target_dir}")
        return
        
    moved_count = 0
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f)) and f.endswith(".c")]
    
    print(f"Found {len(files)} files to organize.")
    
    for filename in files:
        file_path = os.path.join(target_dir, filename)
        
        # Remove the .c extension to get the raw class name
        class_name = filename[:-2]
        
        parts = class_name.split('_')
        
        if len(parts) > 1 and parts[0] != "":
            category_name = parts[0]
        else:
            # Leave Global.c or FUN.c in the root, or move them to a Global folder
            category_name = "Global"
            
        category_dir = os.path.join(target_dir, category_name)
        
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
            
        new_file_path = os.path.join(category_dir, filename)
        
        # Move the file
        shutil.move(file_path, new_file_path)
        moved_count += 1
        
        if moved_count % 1000 == 0:
            print(f"Moved {moved_count} / {len(files)} files...")
            
    print(f"[SUCCESS] Reorganized {moved_count} files into categories!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game-dev-story-mod_Dumped", "Categorized_Code")
        
    reorganize_folder(target)
