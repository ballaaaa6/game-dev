@echo off
setlocal EnableExtensions
title 05 - Export Failed Functions Assembly

set "SCRIPT_DIR=%~dp0"
set "DUMP_DIR=%~1"
if not defined DUMP_DIR if exist "%SCRIPT_DIR%game-dev-story-mod_Dumped\libil2cpp.so" set "DUMP_DIR=%SCRIPT_DIR%game-dev-story-mod_Dumped"
if not defined DUMP_DIR if exist "%SCRIPT_DIR%libil2cpp.so" set "DUMP_DIR=%SCRIPT_DIR%"
if not defined DUMP_DIR if exist "%SCRIPT_DIR%..\game-dev-story-mod_Dumped\libil2cpp.so" set "DUMP_DIR=%SCRIPT_DIR%..\game-dev-story-mod_Dumped"
if not defined DUMP_DIR set "DUMP_DIR=%SCRIPT_DIR%game-dev-story-mod_Dumped"
for %%D in ("%DUMP_DIR%") do set "DUMP_DIR=%%~fD"

set "GHIDRA_DIR=%SCRIPT_DIR%..\ghidra_11.0.1_PUBLIC"
if not exist "%GHIDRA_DIR%\support\analyzeHeadless.bat" set "GHIDRA_DIR=%SCRIPT_DIR%..\..\ghidra_11.0.1_PUBLIC"
set "PROJECT_NAME=KairoHack"
set "REPORT_FILE=%DUMP_DIR%\Exported_ALL.report.json"
set "SCRIPT_FILE=%SCRIPT_DIR%Export_Failed_Functions_Assembly.py"
set "OUT_DIR=%DUMP_DIR%\Failed_Functions_Assembly"
set "LOG_FILE=%DUMP_DIR%\ghidra_assembly.log"

if not exist "%DUMP_DIR%\%PROJECT_NAME%.rep" (
    echo [ERROR] Ghidra project is missing: %DUMP_DIR%\%PROJECT_NAME%.rep
    if not defined AUTO_RUN pause
    exit /b 1
)
if not exist "%REPORT_FILE%" (
    echo [ERROR] Export report is missing: %REPORT_FILE%
    if not defined AUTO_RUN pause
    exit /b 1
)
if not exist "%GHIDRA_DIR%\support\analyzeHeadless.bat" (
    echo [ERROR] Ghidra was not found: %GHIDRA_DIR%
    if not defined AUTO_RUN pause
    exit /b 1
)

if exist "%OUT_DIR%" rmdir /s /q "%OUT_DIR%"
mkdir "%OUT_DIR%"
echo [WAIT] Exporting exact assembly for failed functions...
"%GHIDRA_DIR%\support\analyzeHeadless.bat" "%DUMP_DIR%" "%PROJECT_NAME%" -process -noanalysis -postScript "%SCRIPT_FILE%" "%REPORT_FILE%" "%OUT_DIR%" > "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] Assembly export failed. Read: %LOG_FILE%
    if not defined AUTO_RUN pause
    exit /b 1
)
if not exist "%OUT_DIR%\failed_functions.asm.report.json" (
    echo [ERROR] Assembly report was not created. Read: %LOG_FILE%
    if not defined AUTO_RUN pause
    exit /b 1
)

echo [SUCCESS] Assembly fallback completed.
echo [INFO] Output: %OUT_DIR%
echo [INFO] Log: %LOG_FILE%
if not defined AUTO_RUN pause
exit /b 0
