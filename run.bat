@echo off
setlocal
cd /d "%~dp0"

echo === Namma Traffic AI: Setup & Run (Windows) ===

REM Create virtual environment if it doesn't exist
if not exist ".venv\Scripts\python.exe" (
  echo [1/4] Creating virtual environment...
  py -3.11 -m venv .venv || (echo Failed to create venv & pause & exit /b 1)
)

REM Activate venv
call ".venv\Scripts\activate"

REM Upgrade pip
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [3/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt || (echo Pip install failed. See errors above. & pause & exit /b 1)

REM Run the app
echo [4/4] Starting app...
python app.py

echo.
echo App exited. Press any key to close.
pause
