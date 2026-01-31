@echo off
setlocal

:: Use pushd to handle UNC paths (e.g. \\wsl.localhost\...)
pushd "%~dp0"

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges to install dependencies...
    :: Re-launch self with pushd context wrapper
    powershell -Command "Start-Process cmd -ArgumentList '/c pushd ""%~dp0"" && ""%~dp0run_windows.bat""' -Verb RunAs"
    exit /b
)

echo Starting LMU Minimal Overlay Setup...
echo Working Directory: %CD%

:: 1. Check/Install Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python not found. Checking for Chocolatey...
        
        :: Check/Install Chocolatey
        choco --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo Installing Chocolatey...
            powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        )
        
        echo Installing Python 3.10 via Chocolatey...
        choco install python --version=3.10.11 -y
        
        echo Refreshing environment...
        call refreshenv 2>nul
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

if not defined PYTHON_CMD set PYTHON_CMD=python

:: 2. Setup Virtual Environment
if not exist "venv" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create venv. Ensure Python is in your PATH.
        echo You may need to restart this script after the first installation.
        pause
        exit /b 1
    )
)

:: 3. Activate and Install Deps
call venv\Scripts\activate
if not exist "venv\Lib\site-packages\pygame" (
    echo Installing project dependencies...
    pip install -r requirements-windows.txt
)

:: 4. Run Application
echo Launching LMU Overlay...
python -m src.main
if %errorlevel% neq 0 (
    echo Application closed with error code %errorlevel%.
    pause
)

deactivate
