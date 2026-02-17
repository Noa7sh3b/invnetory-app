@echo off
title Clean Installation - Reset Everything
color 0C
echo.
echo ========================================
echo    CLEAN ALL - Reset Everything
echo ========================================
echo.
echo This will delete:
echo   - Virtual environment (venv)
echo   - Database (data)
echo   - Log files (logs)
echo   - Python cache (__pycache__)
echo.

set /p confirm="Are you sure? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo.
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo [INFO] Stopping any running processes...
taskkill /F /IM streamlit.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo.

echo [1/4] Removing virtual environment...
if exist "venv" (
    rmdir /s /q venv
    if exist "venv" (
        echo       [RETRY] Some files locked, retrying...
        timeout /t 3 /nobreak >nul
        rmdir /s /q venv
    )
    if exist "venv" (
        echo       [ERROR] Cannot delete venv. Close all programs and try again.
        pause
        exit /b 1
    )
    echo       [OK] Deleted
) else (
    echo       [SKIP] Not found
)

echo [2/4] Removing database...
if exist "data" (
    rmdir /s /q data
    echo       [OK] Deleted
) else (
    echo       [SKIP] Not found
)

echo [3/4] Removing logs...
if exist "logs" (
    rmdir /s /q logs
    echo       [OK] Deleted
) else (
    echo       [SKIP] Not found
)

echo [4/4] Removing cache...
for /d /r %%i in (__pycache__) do (
    if exist "%%i" rmdir /s /q "%%i"
)
echo       [OK] Done
echo.

echo ========================================
echo    Cleanup Complete!
echo ========================================
echo.
echo To reinstall, run:
echo   1. setup.bat  (install dependencies)
echo   2. run.bat    (start application)
echo.
pause
