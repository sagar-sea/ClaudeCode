# Weekly GenAI Research and Article Writing Workflow

## What This Script Does

This workflow automates the process of researching the latest Generative AI topics and writing Medium articles. It consists of several components:

### 1. Main Python Script (`genai_weekly_research.py`)
- Collects research from multiple sources (Anthropic, Google AI, OpenAI, Medium, TLDR)
- Generates 5 article ideas based on the latest trends
- Allows you to select one idea for detailed exploration
- Writes a complete Medium article (7-8 minute read) on your chosen topic

### 2. Batch Runner (`run_genai_research.bat`)
- Checks for Python installation
- Installs required dependencies
- Executes the main workflow script

### 3. Prompt Template (`genai_weekly_research_prompt.md`)
- Contains the detailed prompt that defines the workflow behavior
- Can be used with Claude Code or other AI assistants

## How to Run the Workflow

### Option 1: Using the Batch Script (Recommended)
1. Double-click on `run_genai_research.bat` in Windows Explorer
2. Or run from Command Prompt:
   ```
   run_genai_research.bat
   ```

### Option 2: Direct Python Execution
1. Open Command Prompt or PowerShell
2. Navigate to the ClaudeCode directory:
   ```
   cd C:\Users\Sagar\ClaudeCode
   ```
3. Run the script:
   ```
   python genai_weekly_research.py
   ```

## How It Works

1. **Research Collection**: The script visits various AI research blogs and collects recent content
2. **Idea Generation**: Based on the research, it generates 5 compelling article ideas
3. **User Selection**: You choose which idea to develop into a full article
4. **Topic Explanation**: The script provides a detailed breakdown of your chosen topic
5. **Article Writing**: It creates a complete Medium article (~1,200-1,500 words) with proper formatting

## Output

- Articles are saved in the `generated_articles` folder
- Research data is cached in `genai_research_cache.json` to avoid repeated web requests
- Each article is named with the title and date (e.g., `The_Rise_of_Multimodal_AI_20260306.md`)

## Customization

You can modify:
- Research sources in the `RESEARCH_SOURCES` dictionary
- Article ideas generation logic in `generate_article_ideas()` function
- Article structure and content in `write_medium_article()` function
- The prompt in `genai_weekly_research_prompt.md` for use with Claude Code

## Scheduling for Weekly Execution

To run this automatically every week:

1. Open Task Scheduler (taskschd.msc)
2. Create a Basic Task
3. Set trigger to "Weekly"
4. Set action to start a program:
   - Program: `C:\Users\Sagar\ClaudeCode\run_genai_research.bat`
   - Start in: `C:\Users\Sagar\ClaudeCode`

## Requirements

- Python 3.7 or later
- Internet connection for research
- The following Python packages (installed automatically by the batch script):
  - requests
  - beautifulsoup4

## Notes

- The script respects website crawling policies and includes delays between requests
- Research data is cached for 24 hours to reduce load on servers
- All generated content is original and suitable for Medium publication
- The workflow is interactive - you'll need to select article ideas during execution