@echo off
setlocal EnableExtensions EnableDelayedExpansion
title 00 - Complete APK Extraction Pipeline

set "SCRIPT_DIR=%~dp0"
set "GHIDRA_DIR=%~dp0..\ghidra_11.0.1_PUBLIC"
set "PROJECT_NAME=KairoHack"
set "FORCE_REBUILD=1"
set "KEEP_UNPACKED=1"

pushd "%SCRIPT_DIR%"
if errorlevel 1 (
    echo [ERROR] Could not enter toolkit directory: %SCRIPT_DIR%
    pause
    exit /b 1
)

echo ========================================================
echo        COMPLETE APK EXTRACTION PIPELINE
echo ========================================================
echo [INFO] This run rebuilds generated output for the target APK.
echo [INFO] Raw unpacked APK data will be kept for diagnosis.
echo [INFO] Logs and failure reports will be saved beside the dump.
echo [INFO] Asset extraction includes Kairosoft header removal and UTF-8 CSV validation.
echo.

if not exist "!GHIDRA_DIR!\support\analyzeHeadless.bat" (
    echo [ERROR] Ghidra was not found at !GHIDRA_DIR!
    echo [INFO] Run 02_Launch_Ghidra.bat once or place Ghidra beside APK_Toolkit.
    pause
    popd
    exit /b 1
)

echo ========================================================
echo [STEP 1] APK unpacking, Il2CppDumper and asset extraction
echo ========================================================
call "!SCRIPT_DIR!01_AutoExtract_And_Dump.bat"
if errorlevel 1 (
    echo [ERROR] Step 1 failed. Stop here; no Ghidra output is trusted.
    pause
    popd
    exit /b 1
)

if not exist "!SCRIPT_DIR!.last_extraction.env" (
    echo [ERROR] Step 1 did not produce .last_extraction.env
    pause
    popd
    exit /b 1
)
for /f "usebackq tokens=1,* delims==" %%A in ("!SCRIPT_DIR!.last_extraction.env") do set "%%A=%%B"

if not defined DUMP_OUT (
    echo [ERROR] DUMP_OUT was not recorded by Step 1.
    pause
    popd
    exit /b 1
)
if not exist "!DUMP_OUT!\libil2cpp.so" (
    echo [ERROR] Native binary is missing from !DUMP_OUT!
    pause
    popd
    exit /b 1
)
if not exist "!DUMP_OUT!\script.json" (
    echo [ERROR] script.json is missing from !DUMP_OUT!
    pause
    popd
    exit /b 1
)

echo.
echo ========================================================
echo [STEP 2] Fresh Ghidra analysis and symbol application
echo ========================================================
echo [WAIT] Analyzing libil2cpp.so. This is the long step.
echo [INFO] Ghidra log: !DUMP_OUT!\ghidra_analysis.log

if exist "!DUMP_OUT!\!PROJECT_NAME!.rep" rd /s /q "!DUMP_OUT!\!PROJECT_NAME!.rep"
if exist "!DUMP_OUT!\!PROJECT_NAME!.gpr" del /q "!DUMP_OUT!\!PROJECT_NAME!.gpr"
if exist "!DUMP_OUT!\ghidra_symbols.report.json" del /q "!DUMP_OUT!\ghidra_symbols.report.json"
if exist "!DUMP_OUT!\ghidra_analysis.log" del /q "!DUMP_OUT!\ghidra_analysis.log"

"!GHIDRA_DIR!\support\analyzeHeadless.bat" "!DUMP_OUT!" "!PROJECT_NAME!" -import "!DUMP_OUT!\libil2cpp.so" -postScript "!DUMP_OUT!\ghidra_headless.py" "!DUMP_OUT!\script.json" "!DUMP_OUT!\ghidra_symbols.report.json" > "!DUMP_OUT!\ghidra_analysis.log" 2>&1
if errorlevel 1 (
    echo [ERROR] Ghidra analysis failed. Read !DUMP_OUT!\ghidra_analysis.log
    pause
    popd
    exit /b 1
)
if not exist "!DUMP_OUT!\KairoHack.rep" (
    echo [ERROR] Ghidra returned success but the project was not created.
    echo [INFO] Read !DUMP_OUT!\ghidra_analysis.log
    pause
    popd
    exit /b 1
)
if not exist "!DUMP_OUT!\ghidra_symbols.report.json" (
    echo [ERROR] Symbol application report was not created.
    echo [INFO] Read !DUMP_OUT!\ghidra_analysis.log
    pause
    popd
    exit /b 1
)

echo [OK] Ghidra analysis and symbol application completed.

echo.
echo ========================================================
echo [STEP 3] Full decompilation, validation and categorization
echo ========================================================
call "!SCRIPT_DIR!03_Extract_Code_For_AI.bat" "!DUMP_OUT!"
if errorlevel 1 (
    echo [ERROR] Step 3 is incomplete. Read the export report and log in !DUMP_OUT!
    pause
    popd
    exit /b 2
)

echo.
echo ========================================================
echo [SUCCESS] COMPLETE EXTRACTION PIPELINE FINISHED
echo ========================================================
echo [INFO] Dump:   !DUMP_OUT!
echo [INFO] Assets: !SPRITE_OUT!
echo [INFO] The next analysis must use the reports, not assumptions.
popd
exit /b 0
