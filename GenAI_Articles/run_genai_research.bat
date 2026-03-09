@echo off
echo Weekly GenAI Research and Article Writing Workflow
echo ==================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Python is not installed or not in PATH
        echo Please install Python 3.7 or later and try again
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

REM Install required packages from requirements.txt
echo Installing required Python packages...
%PYTHON_CMD% -m pip install -r "%~dp0requirements.txt" >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Could not install required packages automatically
    echo Please run: %PYTHON_CMD% -m pip install -r requirements.txt
    echo Press any key to continue anyway...
    pause >nul
)

REM Run the main script
echo Starting GenAI research workflow...
%PYTHON_CMD% "%~dp0genai_weekly_research.py"

echo.
echo Workflow completed. Check the generated_articles folder for output.
pause