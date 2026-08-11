@echo off
setlocal EnableExtensions
title 04 - Recover Failed Ghidra Functions

set "DUMP_DIR=%~1"
if not defined DUMP_DIR if exist "%~dp0libil2cpp.so" set "DUMP_DIR=%~dp0"
if not defined DUMP_DIR if exist "%~dp0game-dev-story-mod_Dumped\libil2cpp.so" set "DUMP_DIR=%~dp0game-dev-story-mod_Dumped"
if not defined DUMP_DIR set "DUMP_DIR=%~dp0..\game-dev-story-mod_Dumped"
for %%D in ("%DUMP_DIR%") do set "DUMP_DIR=%%~fD"

rem Reuse a valid caller path, then resolve Ghidra beside the workspace root.
if not defined GHIDRA_DIR set "GHIDRA_DIR=%~dp0..\ghidra_11.0.1_PUBLIC"
if not exist "%GHIDRA_DIR%\support\analyzeHeadless.bat" set "GHIDRA_DIR=%~dp0..\..\ghidra_11.0.1_PUBLIC"
set "PROJECT_NAME=KairoHack"
set "SOURCE_REPORT=%DUMP_DIR%\Exported_ALL.report.json"
set "RECOVERED_C=%DUMP_DIR%\Exported_FAILED.c"
set "RECOVERED_REPORT=%DUMP_DIR%\Exported_FAILED.report.json"
set "MERGED_C=%DUMP_DIR%\Exported_ALL.recovered.c"
set "LOG_FILE=%DUMP_DIR%\ghidra_recovery.log"

rem Fast recovery: the full export is already available; do not wait hours
rem retrying pathological functions.  Successful recovery blocks are still
rem merged into a separate candidate file and never overwrite Exported_ALL.c.
if not defined GHIDRA_EXPORT_THREADS set "GHIDRA_EXPORT_THREADS=2"
if not defined GHIDRA_DECOMPILE_TIMEOUT set "GHIDRA_DECOMPILE_TIMEOUT=180"
if not defined GHIDRA_DECOMPILE_RETRY_TIMEOUT set "GHIDRA_DECOMPILE_RETRY_TIMEOUT=180"
if not defined GHIDRA_DECOMPILE_RETRIES set "GHIDRA_DECOMPILE_RETRIES=0"
if not defined GHIDRA_MAX_PAYLOAD_MB set "GHIDRA_MAX_PAYLOAD_MB=512"

pushd "%DUMP_DIR%"
if errorlevel 1 (
    echo [ERROR] Could not enter dump directory: %DUMP_DIR%
    exit /b 1
)

if not exist "%DUMP_DIR%\%PROJECT_NAME%.rep" (
    echo [ERROR] Required recovery artifact is missing: %DUMP_DIR%\%PROJECT_NAME%.rep
    popd
    pause
    exit /b 1
)
if not exist "%DUMP_DIR%\ghidra_export_c.py" (
    echo [ERROR] Required recovery artifact is missing: %DUMP_DIR%\ghidra_export_c.py
    popd
    pause
    exit /b 1
)
if not exist "%SOURCE_REPORT%" (
    echo [ERROR] Required recovery artifact is missing: %SOURCE_REPORT%
    popd
    pause
    exit /b 1
)
if not exist "%DUMP_DIR%\Exported_ALL.c" (
    echo [ERROR] Required recovery artifact is missing: %DUMP_DIR%\Exported_ALL.c
    popd
    pause
    exit /b 1
)

for /f "usebackq tokens=1,* delims=:," %%A in (`powershell -NoProfile -Command "$r=Get-Content -Raw -LiteralPath '%SOURCE_REPORT%' | ConvertFrom-Json; Write-Output ('FAILED:' + $r.failed_functions_count)"`) do set "FAILED_COUNT=%%B"
if not defined FAILED_COUNT (
    echo [ERROR] Could not read failed_functions_count from %SOURCE_REPORT%
    popd
    pause
    exit /b 1
)
if "%FAILED_COUNT%"=="0" (
    echo [OK] The export report contains no failed functions.
    popd
    pause
    exit /b 0
)

echo [WAIT] Retrying %FAILED_COUNT% failed functions using the existing Ghidra project...
echo [INFO] Fast mode: 2 workers, 180s timeout, no long retries, 512 MB payload.
if exist "%RECOVERED_C%" del /q "%RECOVERED_C%"
if exist "%RECOVERED_REPORT%" del /q "%RECOVERED_REPORT%"
if exist "%LOG_FILE%" del /q "%LOG_FILE%"

set "GHIDRA_STATUS=0"
"%GHIDRA_DIR%\support\analyzeHeadless.bat" "%DUMP_DIR%" "%PROJECT_NAME%" -process -noanalysis -postScript "%DUMP_DIR%\ghidra_export_c.py" "REPORT:%SOURCE_REPORT%" "%RECOVERED_C%" "%RECOVERED_REPORT%" > "%LOG_FILE%" 2>&1
if errorlevel 1 set "GHIDRA_STATUS=1"
if not exist "%RECOVERED_C%" (
    echo [ERROR] Recovery produced no C output. Read %LOG_FILE%
    popd
    pause
    exit /b 1
)
if not exist "%RECOVERED_REPORT%" (
    echo [ERROR] Recovery produced no report. Read %LOG_FILE%
    popd
    pause
    exit /b 1
)

python "%DUMP_DIR%\merge_exported_code.py" "%DUMP_DIR%\Exported_ALL.c" "%RECOVERED_C%" "%MERGED_C%"
if errorlevel 1 (
    echo [ERROR] Recovery output could not be merged into a separate candidate file.
    popd
    pause
    exit /b 1
)

if "%GHIDRA_STATUS%"=="1" echo [WARNING] Some failed functions remain; partial recovery was merged safely.
echo [SUCCESS] Recovery finished with available results.
echo [INFO] Recovered functions: %RECOVERED_C%
echo [INFO] Candidate merged output: %MERGED_C%
echo [INFO] Original Exported_ALL.c was not overwritten.
popd
pause
exit /b 0
