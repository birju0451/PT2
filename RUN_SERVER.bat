@echo off
REM Possum Regression Predictor - Development Server Startup
REM Run this file to start the server on Windows

echo.
echo ============================================================
echo  Possum Regression Predictor - Development Server
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ first
    pause
    exit /b 1
)

REM Check virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
pip install -q -r requirements.txt

REM Start server
echo.
echo ============================================================
echo Starting server on http://localhost:5000
echo Press CTRL+C to stop
echo ============================================================
echo.

python app.py

pause

REM Start Flask server
echo.
echo [3/3] Starting Flask server...
echo.
echo ====================================
echo Server starting on: http://localhost:5000
echo ====================================
echo.
echo Once the server is running, open your browser and go to:
echo   http://localhost:5000
echo.
echo To stop the server, press Ctrl+C
echo.

python app.py
