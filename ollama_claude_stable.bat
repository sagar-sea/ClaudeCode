@echo off
setlocal
cd /d "%~dp0"

set "OLLAMA_EXE=%USERPROFILE%\AppData\Local\Programs\Ollama\ollama.exe"
set "MODEL=qwen3-coder:latest"
set "WARMUP_PROMPT=Reply with only: ready"

if not exist "%OLLAMA_EXE%" (
  echo Ollama not found at:
  echo   %OLLAMA_EXE%
  echo Please install Ollama or update this script path.
  pause
  exit /b 1
)

echo Step 1/2: Running model first (warm-up)...
echo Model: %MODEL%
echo.
"%OLLAMA_EXE%" run "%MODEL%" "%WARMUP_PROMPT%"
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Model warm-up failed with code %ERRORLEVEL%.
  pause
  exit /b %ERRORLEVEL%
)

echo.
echo Step 2/2: Opening Claude...
"%OLLAMA_EXE%" launch claude --model "%MODEL%" -- --bare --disable-slash-commands --tools "" --effort low

endlocal
