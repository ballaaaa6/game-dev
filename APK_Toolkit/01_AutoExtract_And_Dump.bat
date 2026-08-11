@echo off
setlocal EnableExtensions EnableDelayedExpansion
title APK Auto Extractor ^& Il2CppDumper

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%"
if errorlevel 1 (
    echo [ERROR] Could not enter toolkit directory: %SCRIPT_DIR%
    exit /b 1
)

if not defined FORCE_REBUILD set "FORCE_REBUILD=0"
if not defined KEEP_UNPACKED set "KEEP_UNPACKED=1"
set "DUMPER_DIR=%SCRIPT_DIR%Il2CppDumper"
set "DUMPER_EXE=%DUMPER_DIR%\Il2CppDumper.exe"
set "APK_COUNT=0"
set "LAST_DUMP_OUT="

echo ========================================================
echo   APK Auto Extractor ^& Il2CppDumper
echo ========================================================
echo [INFO] Force rebuild: !FORCE_REBUILD!
echo [INFO] Keep unpacked APK data: !KEEP_UNPACKED!
echo.

echo [WAIT] Checking system requirements...
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found on PATH.
    echo [INFO] Install Python 3.10+ and run this script again.
    popd
    exit /b 1
)

where java >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Java was not found on PATH.
    echo [INFO] Install a supported JDK and run this script again.
    popd
    exit /b 1
)

python -c "import UnityPy" >nul 2>&1
if errorlevel 1 (
    echo [WAIT] UnityPy is not installed. Installing it with the active Python...
    python -m pip install UnityPy
    if errorlevel 1 (
        echo [ERROR] UnityPy installation failed.
        popd
        exit /b 1
    )
)
echo [OK] Python, Java and UnityPy are ready.

if not exist "!DUMPER_EXE!" (
    echo [WAIT] Il2CppDumper not found. Preparing the local copy...
    if exist "..\Il2CppDumper_win.zip" (
        copy /y "..\Il2CppDumper_win.zip" "Il2CppDumper.zip" >nul
    ) else if exist "..\..\Il2CppDumper_win.zip" (
        copy /y "..\..\Il2CppDumper_win.zip" "Il2CppDumper.zip" >nul
    ) else (
        echo [WAIT] Downloading Il2CppDumper v6.7.46...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/Perfare/Il2CppDumper/releases/download/v6.7.46/Il2CppDumper-win-v6.7.46.zip' -OutFile 'Il2CppDumper.zip'"
    )
    if not exist "Il2CppDumper.zip" (
        echo [ERROR] Il2CppDumper archive was not obtained.
        popd
        exit /b 1
    )
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath 'Il2CppDumper.zip' -DestinationPath '!DUMPER_DIR!' -Force"
    if errorlevel 1 (
        echo [ERROR] Il2CppDumper archive could not be extracted.
        popd
        exit /b 1
    )
    del /q "Il2CppDumper.zip" >nul 2>&1
)
if not exist "!DUMPER_EXE!" (
    echo [ERROR] Il2CppDumper.exe is still missing after setup.
    popd
    exit /b 1
)

for %%F in (*.apk) do (
    if exist "%%~fF" (
        set /a APK_COUNT+=1
        set "APK_PATH=%%~fF"
        set "APK_BASE=%%~nF"
    )
)

if "!APK_COUNT!"=="0" (
    echo [ERROR] No .apk file was found in !SCRIPT_DIR!
    popd
    exit /b 1
)
if not "!APK_COUNT!"=="1" (
    echo [ERROR] Found !APK_COUNT! APK files. The master pipeline requires exactly one APK.
    echo [INFO] Keep one target APK in APK_Toolkit and run again.
    popd
    exit /b 1
)

set "WORKSPACE_DIR=!SCRIPT_DIR!.."
set "ZIP_NAME=!SCRIPT_DIR!!APK_BASE!.zip"
set "OUT_FOLDER=!WORKSPACE_DIR!\!APK_BASE!_Extracted"
set "DUMP_OUT=!WORKSPACE_DIR!\!APK_BASE!_Dumped"
set "SPRITE_OUT=!WORKSPACE_DIR!\!APK_BASE!_Sprites"

echo [OK] Target APK: !APK_PATH!
echo [INFO] Dump output: !DUMP_OUT!
echo [INFO] Sprite output: !SPRITE_OUT!

if "!FORCE_REBUILD!"=="1" (
    echo [WAIT] Removing only generated outputs for this APK...
    if exist "!OUT_FOLDER!" rmdir /s /q "!OUT_FOLDER!"
    if exist "!DUMP_OUT!" rmdir /s /q "!DUMP_OUT!"
    if exist "!SPRITE_OUT!" rmdir /s /q "!SPRITE_OUT!"
    if exist "!ZIP_NAME!" del /q "!ZIP_NAME!"
)

if not exist "!OUT_FOLDER!\assets\bin\Data" (
    echo [WAIT] Extracting APK contents...
    copy /y "!APK_PATH!" "!ZIP_NAME!" >nul
    if errorlevel 1 goto :extract_failed
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '!ZIP_NAME!' -DestinationPath '!OUT_FOLDER!' -Force"
    if errorlevel 1 goto :extract_failed
) else (
    echo [OK] Existing unpacked data has the expected Data directory.
)

set "SO_FILE="
set "DAT_FILE="
if exist "!OUT_FOLDER!\lib\arm64-v8a\libil2cpp.so" set "SO_FILE=!OUT_FOLDER!\lib\arm64-v8a\libil2cpp.so"
if not defined SO_FILE if exist "!OUT_FOLDER!\lib\armeabi-v7a\libil2cpp.so" set "SO_FILE=!OUT_FOLDER!\lib\armeabi-v7a\libil2cpp.so"
if not defined SO_FILE for /r "!OUT_FOLDER!" %%S in (libil2cpp.so) do if not defined SO_FILE set "SO_FILE=%%~fS"

if exist "!OUT_FOLDER!\assets\bin\Data\Managed\Metadata\global-metadata.dat" set "DAT_FILE=!OUT_FOLDER!\assets\bin\Data\Managed\Metadata\global-metadata.dat"
if not defined DAT_FILE if exist "!OUT_FOLDER!\assets\bin\Data\Metadata\global-metadata.dat" set "DAT_FILE=!OUT_FOLDER!\assets\bin\Data\Metadata\global-metadata.dat"
if not defined DAT_FILE for /r "!OUT_FOLDER!" %%D in (global-metadata.dat) do if not defined DAT_FILE set "DAT_FILE=%%~fD"

if not defined SO_FILE (
    echo [ERROR] libil2cpp.so was not found in the extracted APK.
    goto :process_failed
)
if not defined DAT_FILE (
    echo [ERROR] global-metadata.dat was not found in the extracted APK.
    goto :process_failed
)
echo [OK] Found native binary: !SO_FILE!
echo [OK] Found metadata: !DAT_FILE!

if not exist "!DUMP_OUT!" mkdir "!DUMP_OUT!"
echo [WAIT] Running Il2CppDumper...
"!DUMPER_EXE!" "!SO_FILE!" "!DAT_FILE!" "!DUMP_OUT!"
if errorlevel 1 (
    echo [ERROR] Il2CppDumper returned a failure code.
    goto :process_failed
)

for %%R in (script.json dump.cs) do (
    if not exist "!DUMP_OUT!\%%R" (
        echo [ERROR] Il2CppDumper did not produce !DUMP_OUT!\%%R
        goto :process_failed
    )
)
if not exist "!DUMP_OUT!\ghidra.py" echo [INFO] Il2CppDumper did not generate ghidra.py; the toolkit's own Ghidra scripts will be used.
copy /y "!SO_FILE!" "!DUMP_OUT!\libil2cpp.so" >nul
if errorlevel 1 goto :process_failed

for %%R in (ghidra_headless.py ghidra_export_c.py split_exported_code.py validate_extraction.py validate_assets.py Extract_BodyFace_Records.py merge_exported_code.py 02_Launch_Ghidra.bat 03_Extract_Code_For_AI.bat 04_Recover_Failed_Functions.bat) do (
    if exist "!SCRIPT_DIR!%%R" copy /y "!SCRIPT_DIR!%%R" "!DUMP_OUT!\%%R" >nul
)
if exist "!SCRIPT_DIR!..\Phases\Phase2\references\bodyface_records.json" copy /y "!SCRIPT_DIR!..\Phases\Phase2\references\bodyface_records.json" "!DUMP_OUT!\bodyface_records.reference.json" >nul

echo [WAIT] Extracting Kairosoft assets...
python -u "!SCRIPT_DIR!KairoExtractor.py" "!OUT_FOLDER!\assets\bin\Data" "!SPRITE_OUT!" --csv-bom
if errorlevel 1 (
    echo [ERROR] Sprite extraction failed. Raw unpacked data was kept for diagnosis.
    goto :process_failed
)
if not exist "!SPRITE_OUT!\extraction_report.json" (
    echo [ERROR] Sprite extraction produced no extraction_report.json
    goto :process_failed
)
echo [WAIT] Validating PNG signatures and Excel-compatible CSV encoding...
python -u "!SCRIPT_DIR!validate_assets.py" "!SPRITE_OUT!"
if errorlevel 1 (
    echo [ERROR] Asset validation failed. The output is not trusted.
    goto :process_failed
)

if "!KEEP_UNPACKED!"=="0" (
    echo [WAIT] Removing raw unpacked APK data after successful extraction...
    rmdir /s /q "!OUT_FOLDER!"
)

>"!SCRIPT_DIR!.last_extraction.env" echo APK_BASE=!APK_BASE!
>>"!SCRIPT_DIR!.last_extraction.env" echo APK_PATH=!APK_PATH!
>>"!SCRIPT_DIR!.last_extraction.env" echo OUT_FOLDER=!OUT_FOLDER!
>>"!SCRIPT_DIR!.last_extraction.env" echo DUMP_OUT=!DUMP_OUT!
>>"!SCRIPT_DIR!.last_extraction.env" echo SPRITE_OUT=!SPRITE_OUT!

echo.
echo [SUCCESS] APK unpacking, Il2CppDumper and asset extraction completed.
echo   Dump:   !DUMP_OUT!
echo   Assets: !SPRITE_OUT!
popd
exit /b 0

:extract_failed
echo [ERROR] APK extraction failed. The unpacked folder was kept.
goto :process_failed

:process_failed
echo [ERROR] Stage 01 failed. No downstream stage should be trusted.
popd
exit /b 1
