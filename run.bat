@echo off
setlocal
echo Starting MyPDFCleaner Web Server...
echo ==============================================

REM 1. Check for Tesseract
where tesseract >nul 2>nul
if %errorlevel% EQU 0 goto :FOUND_TESS

echo [!] Tesseract OCR not found in PATH.
echo Checking common locations...

if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    set "PATH=%PATH%;C:\Program Files\tesseract-OCR"
    echo Found in Program Files.
    goto :FOUND_TESS
)
if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" (
    set "PATH=%PATH%;C:\Program Files (x86)\tesseract-OCR"
    echo Found in Program Files (x86).
    goto :FOUND_TESS
)

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

:RUN_APP
echo.
echo Launching Server...
python app.py

echo.
echo Application stopped.
pause
