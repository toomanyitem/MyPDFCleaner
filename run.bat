@echo off
setlocal
echo Starting MyPDFCleaner Web Server...
echo ==============================================

REM 0. Check for Ghostscript (Required for OCRmyPDF)
where gswin64c >nul 2>nul
if %errorlevel% EQU 0 goto :CHECK_TESS

echo [!] Ghostscript not found in PATH.
if exist "C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe" set "PATH=%PATH%;C:\Program Files\gs\gs10.04.0\bin" & echo Found Ghostscript in Program Files. & goto :CHECK_TESS

echo.
echo [!] Ghostscript is NOT installed.
echo Attempting to download and install automatically...

REM Download Ghostscript Installer using PowerShell
set "GS_URL=https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10040/gs10040w64.exe"
set "GS_INSTALLER=gs_installer.exe"

echo Downloading from %GS_URL%...
powershell -Command "try { Invoke-WebRequest -Uri '%GS_URL%' -OutFile '%GS_INSTALLER%' -ErrorAction Stop } catch { exit 1 }"

if %errorlevel% NEQ 0 goto :DL_FAILED

echo [V] Download complete. Installing (Silent Mode)...
start /wait %GS_INSTALLER% /S

if %errorlevel% NEQ 0 goto :INSTALL_FAILED

del %GS_INSTALLER%
echo [V] Ghostscript installed successfully.
echo.
echo [!] IMPORTANT: Please RESTART this script to apply the changes.
pause
exit

:DL_FAILED
echo [X] Download failed. Please check your internet connection.
goto :MANUAL_GS

:INSTALL_FAILED
echo [X] Installation failed.
del %GS_INSTALLER%
goto :MANUAL_GS

:MANUAL_GS
echo.
echo [!] Automatic installation failed.
echo Please install manually from: https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/latest
start https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/latest
pause
exit

:CHECK_TESS
REM 1. Check for Tesseract
where tesseract >nul 2>nul
if %errorlevel% EQU 0 goto :FOUND_TESS

echo [!] Tesseract OCR not found in PATH.
echo Checking common locations...

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" set "PATH=%PATH%;C:\Program Files\Tesseract-OCR" & echo Found in Program Files. & goto :FOUND_TESS
if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" set "PATH=%PATH%;C:\Program Files (x86)\Tesseract-OCR" & echo Found in Program Files (x86). & goto :FOUND_TESS

:INSTALL_TESS
echo.
echo [!] Tesseract is NOT installed.
echo Attempting to install automatically via Winget...
winget install -e --id UB-Mannheim.TesseractOCR --accept-source-agreements --accept-package-agreements

if %errorlevel% NEQ 0 (
    echo.
    echo [X] Automatic installation failed.
    echo Please download from: https://github.com/UB-Mannheim/tesseract/wiki
    echo Press any key to continue without OCR...
    pause
) else (
    echo [V] Installation complete. Adding to PATH...
    set "PATH=%PATH%;C:\Program Files\Tesseract-OCR"
)

:FOUND_TESS
echo.
REM 2. Activate Python Environment
if exist ".venv\Scripts\activate.bat" goto :ACTIVATE_VENV

echo Creating virtual environment...
python -m venv .venv
if %errorlevel% NEQ 0 (
    echo [X] Failed to create virtual environment. 
    echo Check your Python installation.
    pause
    exit /b
)
call .venv\Scripts\activate.bat
goto :INSTALL_DEPS

:ACTIVATE_VENV
call .venv\Scripts\activate.bat

:INSTALL_DEPS
echo Checking/Installing dependencies...
pip install -r requirements.txt

REM 3. Setup Local Tesseract Data (Fixes missing Thai language)
if not exist "tessdata" mkdir tessdata

if not exist "tessdata\eng.traineddata" (
    echo Downloading eng.traineddata...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata' -OutFile 'tessdata\eng.traineddata'"
)

if not exist "tessdata\tha.traineddata" (
    echo Downloading tha.traineddata...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tessdata/raw/main/tha.traineddata' -OutFile 'tessdata\tha.traineddata'"
)

REM Set TESSDATA_PREFIX to local folder
set "TESSDATA_PREFIX=%CD%\tessdata"
echo [V] TESSDATA_PREFIX set to %TESSDATA_PREFIX%

:RUN_APP
echo.
echo Launching Server...
python app.py

echo.
echo Application stopped.
pause
