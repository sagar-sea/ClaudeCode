# Weekly GenAI Research and Content Creation Workflow

This folder contains a comprehensive AI-assisted workflow for researching the latest developments in Generative AI and creating various types of content including Medium articles and LinkedIn posts.

## Overview

This is a prompt-based workflow designed to be used with AI assistants (Claude, ChatGPT, Gemini, etc.) to streamline the process of staying current with GenAI developments and creating engaging content.

## What's Included

- **genai_weekly_research_prompt.md** - Complete workflow instructions for AI assistants
- **genai_research_cache.json** - Cache file for storing research data (auto-generated)

## Features

- **Flexible Intent Assessment**: Determines whether you want to create content or just get information
- **Multi-source Research**: Guides research from leading AI blogs and publications
- **Multiple Content Types**: 
  - Medium articles (1,200-1,500 words)
  - LinkedIn posts (300-500 words, engineering-focused)
  - Learning documents
- **LinkedIn Post Topics**: Generates practical, developer-focused topics similar to:
  - "Async Python for AI Engineers"
  - "Prompt Caching: Stop Paying to Recompute the Same Tokens"
  - "RAG Pipeline Optimization"
  - And more engineering-focused insights
- **Image Generation Prompts**: Creates detailed prompts for technical diagrams and infographics

## Research Sources

The workflow covers:

1. **Anthropic** - https://www.anthropic.com/research
2. **Google AI** - https://blog.google/technology/ai/
3. **Google Research** - https://research.google/
4. **OpenAI** - https://openai.com/research
5. **DeepSeek Papers** - https://huggingface.co/collections/Presidentlin/deepseek-papers
6. **Kiro Blogs** - https://kiro.dev/blog/
7. **Medium AI** - https://medium.com/tag/ai
8. **TLDR Newsletter** - https://tldr.tech/ (special focus on AI/ML section)

## How to Use

### With Claude/ChatGPT/Gemini

1. Open your AI assistant
2. Upload or paste the content from `genai_weekly_research_prompt.md`
3. Tell the assistant what you want to do:
   - "I want to create a LinkedIn post about recent AI developments"
   - "Give me a weekly update on GenAI news"
   - "Help me write a Medium article about [topic]"
4. Follow the interactive workflow

### Workflow Steps

1. **Intent Assessment** - AI determines if you want content creation or just information
2. **Research Phase** - AI researches the specified sources
3. **Content Type Selection** - Choose between:
   - Medium article
   - LinkedIn post
   - Learning document
   - Information summary only
4. **Topic Generation** - AI generates relevant topics based on research
5. **Selection & Creation** - Choose a topic and AI creates the content
6. **Image Prompts** - Get detailed prompts for creating visuals

## Content Types

### Medium Articles
- 7-8 minute read (~1,200-1,500 words)
- Professional formatting with sections
- Technical depth with accessibility
- Includes references and further reading

### LinkedIn Posts
- 300-500 words
- Engineering-focused and practical
- Problem → Solution → Impact structure
- Includes image generation prompts for technical diagrams
- Examples:
  - Performance optimization techniques
  - Cost-saving strategies
  - Architecture best practices
  - Production engineering insights

### Learning Documents
- Comprehensive explanations
- Step-by-step guides
- Visual diagrams
- Best practices and troubleshooting

## Output Location

Generated content is typically saved in the `generated_articles` folder (created automatically when needed).

## Tips for Best Results

- Be specific about your content goals
- Mention if you want focus on specific AI tools or developments
- Request information-only mode if you just want updates
- Ask for topic refinement if the generated ideas don't match your needs
- Use the image generation prompts with tools like DALL-E, Midjourney, or NotebookLM

## Customization

You can modify `genai_weekly_research_prompt.md` to:
- Add or remove research sources
- Adjust content length requirements
- Change the tone or style guidelines
- Add specific topics of interest
- Customize LinkedIn post categories

## Notes

- Research data is cached in `genai_research_cache.json` to avoid redundant lookups
- The workflow adapts based on your stated goals
- Not all sessions need to result in content creation
- Focus is on practical, actionable insights for AI engineers and developers