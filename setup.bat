@echo off
REM Setup script for CodeMentor AI
REM Windows batch file

echo ==========================================
echo  CodeMentor AI - Setup Script
echo ==========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)
echo Python found!
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Check for .env file
echo [5/5] Checking API key configuration...
if exist .env (
    echo .env file found!
) else (
    echo WARNING: .env file not found!
    echo Creating .env from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your Google Gemini API key
    echo Get your API key from: https://aistudio.google.com/app/apikey
    echo.
    notepad .env
)
echo.

echo ==========================================
echo  Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Make sure your Google Gemini API key is in .env file
echo 2. Run the demo: python demo\demo_script.py
echo 3. Launch the app: streamlit run app.py
echo.
echo To activate virtual environment later, run:
echo    venv\Scripts\activate
echo.
pause
