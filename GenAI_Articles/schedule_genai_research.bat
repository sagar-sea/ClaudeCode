@echo off
REM Weekly GenAI Research and Article Writing Workflow Scheduler
REM This script is designed to be run by Windows Task Scheduler

echo ================================================
echo Weekly GenAI Research Workflow - Scheduled Run
echo ================================================

REM Change to the script directory
cd /d "%~dp0"

REM Run the main workflow script
python genai_weekly_research.py

echo.
echo Scheduled workflow completed.
echo Check the generated_articles folder for output.

REM Keep window open for debugging (remove for fully automated runs)
REM pause