# Claude Code + Ollama Troubleshooting Guide

## Common Issues and Solutions

### 1. Claude Code Not Found
**Problem**: `claude` command not recognized
**Solution**:
- Run the setup_claude_path.ps1 script
- Or manually add `%USERPROFILE%\.local\bin` to your PATH
- Restart your command prompt/terminal

### 2. Ollama Server Won't Start
**Problem**: Server fails to start or stays "Not Running"
**Solution**:
- Check if another instance is already running: `taskkill /F /IM ollama.exe`
- Restart your computer if needed
- Ensure port 11434 is not blocked by firewall

### 3. Model Loading Issues
**Problem**: Models fail to load or respond slowly
**Solution**:
- Ensure sufficient RAM (at least 8GB recommended)
- Close other memory-intensive applications
- Try a smaller model if using a lightweight system

### 4. Image Generation Errors
**Problem**: "build with mlx tag" error when generating images
**Solution**:
- This error occurs with Apple-specific models
- Use alternative models like llava or bakllava for image tasks
- For Windows/Linux, avoid models specifically tagged for Apple Silicon

## Useful Commands

### Ollama Management
```bash
# List all models
ollama list

# Remove a model
ollama rm model_name

# Pull a new model
ollama pull model_name

# Check Ollama version
ollama --version
```

### Claude Code Management
```bash
# Check Claude Code version
claude --version

# Run Claude Code with specific model
claude --model model_name
```

## Model Recommendations

### For Coding
- qwen3-coder:30b (already installed)
- deepseek-r1:8b (lightweight option)

### For General Purpose
- llama3.1:8b (balanced performance)
- phi3 (fast and efficient)

### For Lightweight Tasks
- gemma2 (small and fast)
- mistral (good balance of size and capability)

## Launcher Features

The enhanced launcher includes:
1. Improved error handling
2. Model information viewer
3. Claude Code version checker
4. Better logging with color coding
5. Enhanced UI with utility buttons

To use the enhanced launcher:
1. Run `ollama_claude_launcher_enhanced.bat`
2. Or execute `python ollama_claude_launcher_enhanced.py` directly