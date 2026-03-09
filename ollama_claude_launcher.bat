@echo off
cd /d "C:\Users\Sagar\ClaudeCode"
python.exe "%~dp0ollama_claude_launcher.py"
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in current PATH
    echo Trying with full path...
    "C:\Users\Sagar\AppData\Local\Microsoft\WindowsApps\python.exe" "%~dp0ollama_claude_launcher.py"
)
pause