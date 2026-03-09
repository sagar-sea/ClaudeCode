# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a collection of tools and documentation for working with Large Language Models (LLMs), particularly focusing on:

- **Ollama Integration**: A GUI launcher for managing Ollama models and launching Claude Code
- **Excel Automation**: Scripts for creating and analyzing Excel files with sample data
- **LLM Documentation**: Comprehensive guides on selecting and implementing LLMs

## Key Components

### Ollama Claude Launcher (`ollama_claude_launcher.py`)

A Tkinter-based GUI application that:
- Manages Ollama server lifecycle (start/stop)
- Lists available local and cloud models
- Launches Claude Code with selected models
- Provides logging and status monitoring

**Key Features:**
- Dark theme UI with scrollable interface
- Real-time server status monitoring
- Support for both local Ollama models and predefined cloud models
- Activity logging with timestamps

### Enhanced Ollama Claude Launcher (`ollama_claude_launcher_enhanced.py`)

An improved version of the launcher with additional features:
- Better error handling and logging
- Model information viewer
- Claude Code version checker
- Enhanced UI with utility buttons
- Color-coded log messages

**Common Commands:**
- Run original launcher: `python ollama_claude_launcher.py`
- Run enhanced launcher: `python ollama_claude_launcher_enhanced.py`
- Batch files: `ollama_claude_launcher.bat` or `ollama_claude_launcher_enhanced.bat`
- Create desktop shortcut: `cscript //nologo create_shortcut.vbs`

### Excel Automation Scripts

**create_excel.py**: Creates a sample Excel file with names data and concatenation formulas
**add_pivot_table.py**: Adds basic pivot table functionality to the Excel file
**add_analysis_fixed.py**: Performs data analysis with pandas and adds multiple analysis sheets

**Dependencies:**
- `openpyxl` for Excel file manipulation
- `pandas` for data analysis

**Usage:** Run scripts sequentially to build comprehensive Excel analysis:
```bash
python create_excel.py
python add_pivot_table.py
python add_analysis_fixed.py
```

## Environment and Permissions

**Claude Code Settings**: Permissions are configured in `.claude/settings.local.json` allowing:
- Execution of Python scripts with Excel dependencies
- Creation of desktop shortcuts
- Ollama server management

**Working Directory**: Defaults to `C:\Users\Sagar\ClaudeCode`

**Claude Path**: Configured as `C:\Users\Sagar\.local\bin\claude.exe`

## Setup and Troubleshooting

### PATH Configuration
Claude Code should be accessible via the command line. If not:
1. Run `setup_claude_path.ps1` to add Claude Code to your PATH
2. Restart your terminal/command prompt
3. Verify with `claude --version`

### Common Issues
See `TROUBLESHOOTING.md` for detailed solutions to common problems:
- Claude Code not found
- Ollama server won't start
- Model loading issues
- Image generation errors

### Testing Your Setup
Run `test_setup.bat` to verify:
- Ollama server status
- Claude Code accessibility
- Available models

## Architecture Notes

### LLM Selection Framework
The repository includes comprehensive guides (`how-to-choose-best-llm.md`, `llm-selection-blog-post.md`, `technical-llm-selection-guide.md`) covering:
- Local vs cloud model trade-offs
- Performance metrics and resource requirements
- Integration patterns and deployment strategies
- Cost optimization and security considerations

### Code Patterns
- **GUI Applications**: Uses Tkinter with modern dark theme styling
- **Excel Processing**: Combines openpyxl for basic operations with pandas for analysis
- **Subprocess Management**: Robust handling of Ollama processes and Claude Code launches
- **Error Handling**: Comprehensive exception handling with user-friendly messages

## Development Notes

- The Excel scripts demonstrate progressive enhancement of data files
- The launcher supports both interactive development and automated workflows
- All scripts include proper error handling and status feedback
- Desktop shortcuts can be created for quick access to the launcher

## Model Support

**Local Models**: Automatically detected via `ollama list` command
**Cloud Models**: Predefined list including qwen3-coder, llama3.1, codellama, deepseek-coder

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

Note: Avoid models with "mlx" tags unless using Apple Silicon Macs, as they require specific hardware support.