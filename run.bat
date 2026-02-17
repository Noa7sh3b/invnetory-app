@echo off
title Mini Inventory Management System
color 0B
echo.
echo ========================================
echo    Mini Inventory Management System
echo ========================================
echo.

REM ============================================================
REM Check if virtual environment exists
REM ============================================================
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM ============================================================
REM Activate Virtual Environment
REM ============================================================
echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Environment activated!
echo.

REM ============================================================
REM Check if streamlit is installed
REM ============================================================
echo [2/2] Checking packages...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Required packages not installed!
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)
echo [OK] All packages ready!
echo.

REM ============================================================
REM Start Application
REM ============================================================
echo ========================================
echo    Starting Application...
echo ========================================
echo.
echo Your browser will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py

echo.
echo Application stopped.
pause
