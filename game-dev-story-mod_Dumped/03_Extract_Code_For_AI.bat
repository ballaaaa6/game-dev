@echo off
setlocal EnableExtensions EnableDelayedExpansion
title AI Code Extractor ^& Splitter (Ghidra)

set "SCRIPT_DIR=%~dp0"
set "DUMP_DIR=%~1"
if not defined DUMP_DIR if exist "%~dp0libil2cpp.so" set "DUMP_DIR=%~dp0"
if not defined DUMP_DIR set "DUMP_DIR=%~dp0..\game-dev-story-mod_Dumped"
for %%D in ("!DUMP_DIR!") do set "DUMP_DIR=%%~fD"

set "GHIDRA_DIR=!DUMP_DIR!\..\ghidra_11.0.1_PUBLIC"
set "PROJECT_NAME=KairoHack"
set "CLASS_NAME=ALL"
set "OUT_FILE=!DUMP_DIR!\Exported_ALL.c"
set "REPORT_FILE=!DUMP_DIR!\Exported_ALL.report.json"
set "OUT_DIR=!DUMP_DIR!\Categorized_Code"
set "SCRIPT_FILE=!DUMP_DIR!\ghidra_export_c.py"
set "SPLITTER_FILE=!DUMP_DIR!\split_exported_code.py"
set "VALIDATOR_FILE=!DUMP_DIR!\validate_extraction.py"
set "RECORDS_SCRIPT=!DUMP_DIR!\Extract_BodyFace_Records.py"
set "EXPORT_LOG=!DUMP_DIR!\ghidra_export.log"
set "INCOMPLETE=0"

if not defined GHIDRA_EXPORT_THREADS set "GHIDRA_EXPORT_THREADS=4"
if not defined GHIDRA_DECOMPILE_TIMEOUT set "GHIDRA_DECOMPILE_TIMEOUT=600"
if not defined GHIDRA_DECOMPILE_RETRY_TIMEOUT set "GHIDRA_DECOMPILE_RETRY_TIMEOUT=1800"
if not defined GHIDRA_DECOMPILE_RETRIES set "GHIDRA_DECOMPILE_RETRIES=2"

pushd "!DUMP_DIR!"
if errorlevel 1 (
    echo [ERROR] Could not enter dump directory: !DUMP_DIR!
    exit /b 1
)

echo ========================================================
echo        AI Code Extractor ^& Categorizer
echo ========================================================
echo [INFO] Dump: !DUMP_DIR!
echo [INFO] Threads: !GHIDRA_EXPORT_THREADS!
echo [INFO] Timeout: !GHIDRA_DECOMPILE_TIMEOUT!s + retries
echo [INFO] Export log: !EXPORT_LOG!

for %%R in ("!DUMP_DIR!\!PROJECT_NAME!.rep" "!DUMP_DIR!\libil2cpp.so" "!DUMP_DIR!\script.json" "!SCRIPT_FILE!" "!SPLITTER_FILE!" "!VALIDATOR_FILE!") do (
    if not exist "%%~R" (
        echo [ERROR] Required extraction artifact is missing: %%~R
        popd
        exit /b 1
    )
)

if exist "!OUT_FILE!" del /q "!OUT_FILE!"
if exist "!REPORT_FILE!" del /q "!REPORT_FILE!"
if exist "!OUT_FILE!.part" del /q "!OUT_FILE!.part"
if exist "!REPORT_FILE!.part" del /q "!REPORT_FILE!.part"
if exist "!EXPORT_LOG!" del /q "!EXPORT_LOG!"

echo [WAIT] Decompiling every Ghidra function. Do not close this window.
"!GHIDRA_DIR!\support\analyzeHeadless.bat" "!DUMP_DIR!" "!PROJECT_NAME!" -process -noanalysis -postScript "!SCRIPT_FILE!" "!CLASS_NAME!" "!OUT_FILE!" "!REPORT_FILE!" > "!EXPORT_LOG!" 2>&1
if errorlevel 1 (
    echo [ERROR] Ghidra export process failed. Read !EXPORT_LOG!
    popd
    exit /b 1
)
if not exist "!OUT_FILE!" (
    echo [ERROR] Ghidra returned success but no C output was created.
    echo [INFO] Read !EXPORT_LOG!
    popd
    exit /b 1
)
if not exist "!REPORT_FILE!" (
    echo [ERROR] Export report was not created. A stale/partial C file is not trusted.
    echo [INFO] Read !EXPORT_LOG!
    popd
    exit /b 1
)

echo [WAIT] Validating export completeness...
python "!VALIDATOR_FILE!" "!DUMP_DIR!" "!OUT_FILE!" "!REPORT_FILE!"
if errorlevel 1 set "INCOMPLETE=1"

echo [WAIT] Splitting fresh C output into categorized files...
python "!SPLITTER_FILE!" "!OUT_FILE!" "!OUT_DIR!"
if errorlevel 1 (
    echo [ERROR] C categorization failed.
    popd
    exit /b 1
)

if exist "!RECORDS_SCRIPT!" (
    echo [WAIT] Extracting only verified numeric BodyFace records...
    set "RECORDS_OUT=!DUMP_DIR!\bodyface_records.generated.json"
    set "RECORDS_REPORT=!DUMP_DIR!\bodyface_records.generated.report.json"
    if exist "!RECORDS_OUT!" del /q "!RECORDS_OUT!"
    python "!RECORDS_SCRIPT!" "!OUT_DIR!" "!RECORDS_OUT!" "!RECORDS_REPORT!"
    if errorlevel 1 echo [WARNING] BodyFace records are incomplete; the C export report remains authoritative.
)

echo.
if "!INCOMPLETE!"=="1" (
    echo [ERROR] C export is incomplete. Successful functions were split for diagnosis only.
    echo [INFO] Use !REPORT_FILE! to see every failed function and retry after reviewing the log.
    popd
    exit /b 2
)

echo [SUCCESS] C export, validation and categorization completed.
echo [INFO] Categorized code: !OUT_DIR!
popd
exit /b 0
