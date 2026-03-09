# Weekly GenAI Research and Article Writing Workflow

This repository contains a comprehensive workflow for researching the latest developments in Generative AI and automatically generating Medium articles.

## Features

- **Multi-source Research**: Collects information from leading AI research blogs and publications
- **Intelligent Idea Generation**: Uses keyword analysis to identify trending topics
- **Interactive Selection**: Allows users to choose which article idea to develop
- **Professional Article Writing**: Generates complete Medium-ready articles with proper formatting
- **Caching System**: Caches research data to avoid repeated web requests
- **Configurable Settings**: Customizable parameters for research depth and article length

## Sources

The workflow collects research from:

1. **Anthropic** - https://www.anthropic.com/research
2. **Google AI** - https://blog.google/technology/ai/
3. **OpenAI** - https://openai.com/research
4. **DeepSeek** - https://github.com/deepseek-ai/DeepSeek-Coder
5. **Medium GenAI** - https://medium.com/tag/generative-ai/latest
6. **TLDR Newsletter** - https://tldr.tech/newsletter/archive

## Requirements

- Python 3.7+
- Required Python packages (automatically installed by the batch script):
  - requests
  - beautifulsoup4
  - feedparser
  - schedule
  - nltk

## Usage

### Manual Execution

1. Double-click `run_genai_research.bat` or run from command line:
   ```
   python genai_weekly_research.py
   ```

2. The script will:
   - Collect recent research from all sources
   - Generate 4-5 article ideas based on trending topics
   - Prompt you to select an idea
   - Show detailed information about the selected topic
   - Generate a complete Medium article (7-8 minute read)
   - Save the article in the `generated_articles` folder

### Automated Scheduling

To schedule weekly execution:

1. Open Task Scheduler (taskschd.msc)
2. Create a new task
3. Set trigger to weekly
4. Set action to run `schedule_genai_research.bat`
5. Configure appropriate user permissions

## Configuration

The workflow can be customized using `config.json`:

- `article_word_count`: Target length for generated articles
- `research_depth`: Number of articles to analyze per source
- `cache_duration_hours`: How long to cache research data
- `retry_attempts`: Number of times to retry failed requests

## Output

Generated articles are saved in the `generated_articles` directory with filenames that include the article title and date.

## Troubleshooting

- If you encounter SSL certificate errors, update your Python certificates
- If certain sources fail to load, check if the website structure has changed
- For proxy issues, configure your system proxy settings
- If you get "ModuleNotFoundError" errors, ensure all dependencies are installed with:
  ```
  pip install -r requirements.txt
  ```
- If packages are installed but not found, check that you're using the correct Python interpreter:
  ```
  python -m pip install -r requirements.txt
  ```
- On Windows, you might need to use `py` instead of `python`:
  ```
  py -m pip install -r requirements.txt
  ```

## Contributing

Feel free to fork this repository and submit pull requests with improvements to the research sources, idea generation algorithms, or article templates.