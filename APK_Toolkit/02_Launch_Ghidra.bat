@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Ghidra Auto-Analyzer ^& Launcher

set "SCRIPT_DIR=%~dp0"
set "DUMP_DIR=%~1"
if not defined DUMP_DIR if exist "%~dp0libil2cpp.so" set "DUMP_DIR=%~dp0"
if not defined DUMP_DIR if exist "%~dp0game-dev-story-mod_Dumped\libil2cpp.so" set "DUMP_DIR=%~dp0game-dev-story-mod_Dumped"
if not defined DUMP_DIR if exist "%~dp0..\game-dev-story-mod_Dumped\libil2cpp.so" set "DUMP_DIR=%~dp0..\game-dev-story-mod_Dumped"
if not defined DUMP_DIR set "DUMP_DIR=%~dp0"
for %%D in ("!DUMP_DIR!") do set "DUMP_DIR=%%~fD"

rem Resolve Ghidra from the caller environment first.  When this script is
rem copied into *_Dumped, the toolkit root is two levels above this file;
rem when run from APK_Toolkit directly, it is one level above.
if not defined GHIDRA_DIR set "GHIDRA_DIR=%~dp0..\ghidra_11.0.1_PUBLIC"
if not exist "!GHIDRA_DIR!\support\analyzeHeadless.bat" set "GHIDRA_DIR=%~dp0..\..\ghidra_11.0.1_PUBLIC"
set "GHIDRA_ZIP=!GHIDRA_DIR!\..\ghidra_11.0.1.zip"
set "GHIDRA_URL=https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0.1_build/ghidra_11.0.1_PUBLIC_20240130.zip"
set "PROJECT_NAME=KairoHack"
set "PROJECT_PATH=!DUMP_DIR!\!PROJECT_NAME!.rep"
set "LOG_FILE=!DUMP_DIR!\ghidra_analysis.log"

pushd "!DUMP_DIR!"
if errorlevel 1 (
    echo [ERROR] Could not enter dump directory: !DUMP_DIR!
    exit /b 1
)

echo ========================================================
echo         Ghidra Auto-Analyzer (Headless)
echo ========================================================

for %%R in (libil2cpp.so script.json ghidra_headless.py) do (
    if not exist "!DUMP_DIR!\%%R" (
        echo [ERROR] Missing !DUMP_DIR!\%%R
        popd
        exit /b 1
    )
)

if not exist "!GHIDRA_DIR!\support\analyzeHeadless.bat" (
    echo [WAIT] Ghidra not found. Downloading the configured release...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '!GHIDRA_URL!' -OutFile '!GHIDRA_ZIP!'"
    if errorlevel 1 (
        echo [ERROR] Ghidra download failed.
        popd
        exit /b 1
    )
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '!GHIDRA_ZIP!' -DestinationPath '!DUMP_DIR!\..' -Force"
    if errorlevel 1 (
        echo [ERROR] Ghidra archive extraction failed.
        popd
        exit /b 1
    )
    del /q "!GHIDRA_ZIP!" >nul 2>&1
)

if defined FORCE_REANALYZE if "!FORCE_REANALYZE!"=="1" (
    if exist "!PROJECT_PATH!" rd /s /q "!PROJECT_PATH!"
    if exist "!DUMP_DIR!\!PROJECT_NAME!.gpr" del /q "!DUMP_DIR!\!PROJECT_NAME!.gpr"
)

if not exist "!PROJECT_PATH!" (
    echo [WAIT] Starting fresh Ghidra analysis...
    echo [INFO] Log: !LOG_FILE!
    if exist "!LOG_FILE!" del /q "!LOG_FILE!"
    "!GHIDRA_DIR!\support\analyzeHeadless.bat" "!DUMP_DIR!" "!PROJECT_NAME!" -import "!DUMP_DIR!\libil2cpp.so" -postScript "!DUMP_DIR!\ghidra_headless.py" "!DUMP_DIR!\script.json" "!DUMP_DIR!\ghidra_symbols.report.json" > "!LOG_FILE!" 2>&1
    if errorlevel 1 (
        echo [ERROR] Ghidra analysis failed. Read !LOG_FILE!
        popd
        exit /b 1
    )
) else (
    echo [OK] Ghidra project already exists: !PROJECT_PATH!
)

if not exist "!PROJECT_PATH!" (
    echo [ERROR] Ghidra returned but the project is missing.
    popd
    exit /b 1
)
if not exist "!DUMP_DIR!\ghidra_symbols.report.json" (
    echo [WARNING] ghidra_symbols.report.json is missing; inspect the log before trusting symbols.
)

echo [SUCCESS] Ghidra analysis is ready.
popd
exit /b 0
