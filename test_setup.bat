@echo off
echo Testing Claude Code Setup
echo ========================
echo.

echo Checking Ollama status...
curl -s http://localhost:11434/api/version
if %ERRORLEVEL% EQU 0 (
    echo Ollama is running
) else (
    echo Ollama is not accessible
)
echo.

echo Checking Claude Code...
claude --version
if %ERRORLEVEL% EQU 0 (
    echo Claude Code is accessible
) else (
    echo Claude Code is not accessible - please restart your terminal
)
echo.

echo Listing available models...
ollama list
echo.

echo Setup verification complete!
pause