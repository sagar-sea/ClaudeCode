# ClaudeCode - AI Development Workspace

A collection of AI/GenAI tools, scripts, and resources for working with Large Language Models, automation, and Business Intelligence.

## 🚀 Features

- **GenAI Article Generator**: 8-step AI-assisted workflow for weekly GenAI research and content creation (LinkedIn posts, Medium articles, Twitter/X threads, Learning Documents). Includes two pathways (content creation vs. information briefing), ready-to-use starter prompts, and built-in handling for 23 edge cases.
- **GenAI Learning Reference**: Interactive HTML reference guide for AI/ML concepts
- **Ollama & Claude Launcher**: Automated launcher scripts for local AI development
- **Excel Automation**: Python scripts for data analysis and Excel manipulation
- **MCP Web Search Server**: Model Context Protocol server for web search capabilities

## 📁 Project Structure

```
ClaudeCode/
├── GenAI_Articles/          # Automated GenAI research and article generation
├── GenAI_Learning_Reference/ # Interactive learning resource for AI concepts
├── generated_articles/       # Output directory for generated content
├── web-search-mcp-server/   # MCP server implementation
└── *.py, *.bat, *.vbs       # Utility scripts and launchers
```

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Node.js (for MCP server)
- Ollama (optional, for local LLM)
- Claude CLI (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sagar-sea/ClaudeCode.git
cd ClaudeCode
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. For MCP server setup:
```bash
cd web-search-mcp-server
npm install
```

## 📚 Key Components

### GenAI Articles
Automated system for researching and generating articles about Generative AI topics.

- **Script**: `GenAI_Articles/genai_weekly_research.py`
- **Config**: `config.json`
- **Output**: `generated_articles/`

### GenAI Learning Reference
Interactive HTML-based reference guide covering AI/ML concepts from basics to advanced topics.

- **File**: `GenAI_Learning_Reference/index.html`
- **Topics**: Prompts, LLMs, RAG, Fine-tuning, Agents, and more

### Ollama Claude Launcher
Automated launcher for managing Ollama server and Claude CLI.

- **Enhanced**: `ollama_claude_launcher_enhanced.py`
- **Basic**: `ollama_claude_launcher.py`

## 📖 Documentation

- [CLAUDE.md](CLAUDE.md) - Claude CLI setup and usage
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [GenAI_Articles/GENAI_RESEARCH_README.md](GenAI_Articles/GENAI_RESEARCH_README.md) - Article generation guide

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available for personal and educational use.

## 👤 Author

**Sagar Rathkanthiwar**
- GitHub: [@sagar-sea](https://github.com/sagar-sea)
- Medium: [@sagar.rathkanthiwar](https://medium.com/@sagar.rathkanthiwar)

## 🔗 Related Resources

- [Medium Blog](https://medium.com/@sagar.rathkanthiwar) - AI/GenAI articles and insights
- [GenAI Learning Reference](GenAI_Learning_Reference/index.html) - Interactive learning guide
