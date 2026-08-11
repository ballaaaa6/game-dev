# 🛠️ In-Depth Guide (Step-by-Step): From APK to Source Code (C/C++) via Ghidra

This guide is designed as a **"hold-your-hand" step-by-step tutorial**. It will transform your game's `.apk` file (Unity IL2CPP) into readable C/C++ source code that allows you to trace 100% of the native logic.

---

## 📦 Required Tools
1. **Il2CppDumper**: [Download from Github](https://github.com/Perfare/Il2CppDumper/releases)
2. **Ghidra**: [Download from Official Website](https://ghidra-sre.org/) (Requires Java JDK 11 or higher)
3. **AutoExtract_APK.bat** (Provided in your workspace folder)

---

## 🚀 Step 1: Run the Shortcut Script (AutoExtract_And_Dump)
We will use the upgraded all-in-one script. It handles downloading dependencies, extracting the APK, finding the required files, and dumping the code automatically!

1. Place your target `.apk` file in the same folder as **`AutoExtract_And_Dump.bat`**.
2. Double-click to run **`AutoExtract_And_Dump.bat`**.
3. A command prompt window will appear and automatically perform the following:
   - Check if `Il2CppDumper` exists locally (if not, it downloads it from Github).
   - Copy the `.apk`, rename it to `.zip`, and extract its contents.
   - Search for the core logic file `libil2cpp.so` and the metadata map `global-metadata.dat`.
   - Run the dump process automatically!
4. When the program says `[SUCCESS] Done!`, press any key to close the window.
5. You will receive two new folders:
   - `[GameName]_Extracted`: Contains the raw files (you will need `libil2cpp.so` from here for Ghidra).
   - `[GameName]_Dumped`: Contains `dump.cs` (the C# headers/offsets) and the scripts needed for Ghidra.

Preparation is complete! Let's move on to Ghidra.

---

## 🧬 Step 2: Import to Ghidra and Run the Script
1. Open **Ghidra** (run `ghidraRun.bat`).
2. Create a new project: 
   - Go to the top-left menu, click **File -> New Project...**
   - Select **Non-Shared Project** -> Click **Next**
   - Enter any Project Name -> Click **Finish**
3. Import the game file:
   - Drag and drop **`libil2cpp.so`** (the original raw file) into the center of the Ghidra window.
   - An Import window will pop up. Leave the default settings and click **OK**.
   - A summary window will appear shortly after. Click **OK**.
4. Open the CodeBrowser:
   - Double-click the `libil2cpp.so` file in the active project window (the green dragon icon will launch).
   - Ghidra will ask: *"libil2cpp.so has not been analyzed. Would you like to analyze it now?"* 👉 Click **Yes**.
   - The Analysis Options window will appear 👉 Click the **Analyze** button at the bottom right.
   - ☕ **Warning:** Watch the progress bar at the bottom right corner. Ghidra is analyzing millions of lines of machine code! This step can take anywhere from **30 minutes to several hours**. Let it run until the progress bar disappears.

---

## 🔗 Step 3: Apply Symbols (Mapping Function Names)
After Ghidra finishes analysis (the bottom right progress bar is gone), function names will still look like gibberish (e.g., `FUN_01524330`). We need to run a python script to map the real names back.

1. In Ghidra's CodeBrowser window, click the top menu **Window -> Script Manager**.
2. The Script Manager window will open. Click the **"Create New Script"** button (document icon with a red symbol) at the top right.
3. Select **Python** as the script type.
4. Ghidra will open a Text Editor window.
   - Outside Ghidra, open the **`ghidra.py`** file (generated in the `_Dumped` folder from Step 1) using Notepad.
   - Copy all the code from Notepad and paste it over everything in the Ghidra Text Editor window.
   - Click **Save** and close the Text Editor window.
5. Back in the Script Manager, run the script we just saved (by double-clicking it).
6. The script will prompt you for a `script.json` file. Select the `script.json` file generated in the `_Dumped` folder from Step 1.
7. Wait for the script to finish running... Bingo! All function names are now restored to their original C# names (e.g., `GameForm$$Init` or `GameForm$$DrawFrame`)!

---

## 🔍 Step 4: How to Find Functions and Read C/C++ Code
1. Outside Ghidra 👉 Open the **`dump.cs`** file (using VS Code or Notepad).
2. Press `Ctrl + F` and search for the function you want to investigate, e.g., `DrawHuman`.
3. You will find a line that looks like this:
   `// RVA: 0x1783F94 Offset: 0x1783F94 VA: 0x1783F94`
   `public void DrawHuman(...)`
4. Copy the **Offset** number (e.g., `1783F94`).
5. Go back to Ghidra and press the **`G`** key (Go To command).
6. Paste the Offset number and click **OK**.
7. Ghidra will jump exactly to that memory address!
8. **The Magic Step:** Look at the right-hand window titled **"Decompile"**. You will see the assembly code translated back into readable C/C++ syntax, allowing you to trace and understand exactly how the engine's logic works!
