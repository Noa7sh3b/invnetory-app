@echo off
title Mini Inventory - Setup
color 0E
echo.
echo ========================================
echo    Mini Inventory Management System
echo    Installation Setup
echo ========================================
echo.

REM ============================================================
REM Step 1: Check Python
REM ============================================================
echo [Step 1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9+ from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python found!
echo.

REM ============================================================
REM Step 2: Create Virtual Environment
REM ============================================================
echo [Step 2/5] Creating virtual environment...

if exist "venv" (
    echo [INFO] Old virtual environment found. Removing it...
    echo [INFO] Stopping any running processes first...
    taskkill /F /IM streamlit.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
    rmdir /s /q venv
    if exist "venv" (
        echo [WARNING] Some files are locked. Retrying...
        timeout /t 3 /nobreak >nul
        rmdir /s /q venv
    )
    if exist "venv" (
        echo [ERROR] Cannot remove old venv. Please close all programs and try again.
        pause
        exit /b 1
    )
    echo [OK] Old environment removed.
    echo.
)

echo [INFO] Creating fresh virtual environment...
echo        Please wait...
echo.
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created!
echo.

REM ============================================================
REM Step 3: Activate Virtual Environment
REM ============================================================
echo [Step 3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated!
echo.

REM ============================================================
REM Step 4: Upgrade pip
REM ============================================================
echo [Step 4/5] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] Could not upgrade pip, continuing anyway...
)
echo [OK] pip is up to date!
echo.

REM ============================================================
REM Step 5: Install Dependencies
REM ============================================================
echo [Step 5/5] Installing dependencies from requirements.txt...
echo.

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

echo --------------------------------------------------------
echo  Installing packages - this may take 1-2 minutes...
echo --------------------------------------------------------
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install some packages
    echo.
    echo Troubleshooting:
    echo   1. Check your internet connection
    echo   2. Try again: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo All packages installed successfully.
echo.
echo Installed packages:
echo   - Streamlit    (Web Framework)
echo   - Pandas       (Data Processing)
echo   - Plotly       (Interactive Charts)
echo   - OpenPyXL     (Excel Export)
echo   - ReportLab    (PDF Export)
echo   - Pillow       (Image Processing)
echo.
echo To start the application, run:
echo   run.bat
echo.
echo ========================================
echo.
pause
