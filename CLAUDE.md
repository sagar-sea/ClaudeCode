# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ClaudeCode** is a GenAI development workspace focused on AI-assisted content creation, research, and automation. The core system is an **8-step article generation workflow** that combines live web research with structured content creation for multiple formats (Medium articles, LinkedIn posts, Twitter/X threads, learning documents).

## Architecture & Key Components

### 1. GenAI Article Generation System
The heart of this project — a prompt-based workflow that lives in `GenAI_Articles/`:
- **Master Workflow**: `genai_weekly_research_prompt.md` — 8-step instruction set for AI assistants
- **Quick-Start Prompts**: `article_generation_prompts.md` — 7 pre-built starter templates for different session types
- **Optimized Variants**: Several prompt versions optimized for specific AI models (Claude, ChatGPT)
- **Credit Guides**: `CREDIT_OPTIMIZATION_GUIDE.md` and `QUICK_REFERENCE_CREDIT_OPTIMIZATION.md` for managing API costs

**Two Pathways**:
- **Pathway A** (Content Creation): Generates publishable content (Medium, LinkedIn, Twitter, Learning Docs)
- **Pathway B** (Information Briefing): Weekly GenAI development briefing, with ability to pivot to content creation mid-session

**Key Design**: The workflow handles 23 edge cases including unfilled topics, mid-session pathway changes, sparse news weeks, and inaccessible sources. It's designed to be stateless — can skip steps, iterate freely, and doesn't loop back.

### 2. Research Configuration (`config.json`)
Defines research parameters and sources:
- `article_word_count`: Target output length (1400)
- `research_depth`: Research iteration count (5)
- `cache_duration_hours`: Caching window (24)
- `sources`: 6+ curated sources (Anthropic, Google AI, OpenAI, DeepSeek, Medium, TLDR)

The workflow uses **live web research** across 20+ sources including company blogs, AI research aggregators (The Rundown, TLDR AI, Ben's Bites), engineering communities (Hacker News, r/MachineLearning), and expert blogs (Pragmatic Engineer, Chip Huyen).

### 3. Article Output System
- **Output Directory**: `generated_articles/` — Contains all generated content (markdown files with metadata like `_linkedin_2026-05-15` in filename)
- **Content History**: `generated_articles/content_history.md` — Tracks all created content for deduplication and reference

### 4. Supporting Systems
- **Ollama Launcher** (`ollama_claude_launcher_enhanced.py`): Automated management of local Ollama server + Claude CLI
- **MCP Web Search Server** (`web-search-mcp-server/`): Node.js-based Model Context Protocol server for web search capabilities
- **Excel Utilities** (`add_analysis.py`, `add_pivot_table.py`, etc.): Data analysis and Excel automation helpers
- **Learning Reference** (`GenAI_Learning_Reference/`): Interactive HTML guide covering AI/ML concepts

## How to Work with This Repository

### Article Generation Workflow
This is a **prompt-driven, human-in-the-loop** system — not automated:

1. **Start a Session**: Open one of the ready-to-use prompts from `article_generation_prompts.md` in Claude or your preferred AI assistant
2. **Pick Your Pathway**:
   - Use **Interactive Starter** if you're unsure of your goal
   - Use **Direct-to-Content** if you know exactly what you want (Medium article, LinkedIn post, etc.)
   - Use **Weekly Briefing** for information-only sessions
3. **Follow the 8 Steps**: The master prompt in `genai_weekly_research_prompt.md` guides you through research → idea generation → selection → writing → revision
4. **Iterate Freely**: You can skip steps, request revisions, pivot pathways mid-session
5. **Save Output**: Generated content is meant to be saved to `generated_articles/` with naming convention `<topic>_<platform>_<date>.md`
6. **Track in History**: Update `generated_articles/content_history.md` to prevent duplicate topic coverage

### Key Workflows by Task
- **Create a LinkedIn Post**: Use `article_generation_prompts.md` → "Instant LinkedIn Post Generator"
- **Create a Medium Article**: Use → "Instant Medium Article Generator"  
- **Weekly Research Brief**: Use → "Weekly Briefing" (Pathway B)
- **Production Postmortem Article**: Use → "Deep-Dive Failure Analysis" (contrarian edge cases)
- **Stay Current Without Publishing**: Use → "Weekly Briefing" (Pathway B)

### Development Commands

**Python Dependencies**:
```bash
pip install -r requirements.txt
```

**MCP Server Setup**:
```bash
cd web-search-mcp-server
npm install
```

**Run Ollama Launcher** (for local AI development):
```bash
python ollama_claude_launcher_enhanced.py
# Or via batch file: ollama_claude_launcher_enhanced.bat
```

**Common Ollama Commands** (see TROUBLESHOOTING.md for details):
```bash
ollama list                    # List installed models
ollama pull model_name         # Download a model
ollama rm model_name          # Remove a model
```

## Important Context for Claude

### When Working on Article Generation
- The workflow is **not code-based** — it's a series of structured prompts in markdown files
- The 8 steps have a specific order and rationale (research → ideas → selection → writing ensures quality)
- Edge cases are explicitly documented (unfilled topics, pathway changes, sparse news weeks) — follow them
- Output should be saved with `_<platform>_<date>` naming convention to `generated_articles/`
- Check `content_history.md` before suggesting topics to avoid duplicates

### When Modifying Prompts
- The workflow handles 23 edge cases explicitly — don't remove or simplify them
- Both Pathway A (content) and Pathway B (briefing) branches must be present and clear
- The "Critical Pivot Step" at the end of Pathway B (ability to switch to content creation) is load-bearing
- Optimized variants exist for Claude, ChatGPT, etc. — preserve these as separate files

### When Adding Content Types
- The current 4 formats are: Medium articles (~1200–1500 words), LinkedIn posts (~150–250 words), Twitter/X threads (5–7 tweets), and Learning Documents (deep-dive reference)
- New formats should include: word count/length target, structure/sections, tone, and example output format

### Configuration Notes
- `config.json` drives research depth and source selection — check it before expanding research sources
- `cache_duration_hours` and `retry_attempts` control API efficiency and resilience
- Research sources must be accessible and regularly updated (some may drift over time)

## File Organization Notes
- `GenAI_Articles/`: Master prompts, edge-case guides, credit optimization guides
- `generated_articles/`: Output only — don't edit manually (track changes in version control instead)
- Root-level Python scripts: Utility scripts and launchers (not part of core workflow)
- `GenAI_Learning_Reference/`: Self-contained HTML reference guide
- `web-search-mcp-server/`: Separate Node.js project

## See Also
- `TROUBLESHOOTING.md` — Common issues with Ollama, Claude CLI, and model selection
- `README.md` — High-level project overview and features
- `GenAI_Articles/GENAI_RESEARCH_README.md` — Detailed workflow guide
- `GenAI_Articles/CREDIT_OPTIMIZATION_GUIDE.md` — Cost management for API calls
