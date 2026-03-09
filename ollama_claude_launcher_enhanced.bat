@echo off
cd /d "%~dp0"
python.exe "%~dp0ollama_claude_launcher_enhanced.py"
if %ERRORLEVEL% NEQ 0 (
    echo Python not found in current PATH
    echo Trying with Windows Store Python...
    "%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python.exe" "%~dp0ollama_claude_launcher_enhanced.py"
)
pause