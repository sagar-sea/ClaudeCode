# Weekly GenAI Research and Content Creation Workflow

This folder contains a comprehensive AI-assisted workflow for researching the latest developments in Generative AI and creating content including Medium articles, LinkedIn posts, and Twitter/X threads.

## Overview

A prompt-based workflow designed to be used with AI assistants (Claude, ChatGPT, Gemini, etc.) to stay current with GenAI developments and create high-quality, engineering-focused content. The workflow is split into two pathways based on your intent.

## What's Included

| File | Description |
|------|-------------|
| `genai_weekly_research_prompt.md` | The master workflow — 8-step instruction set for AI assistants |
| `article_generation_prompts.md` | Ready-to-use starter prompts to rapidly kick off specific session types |

## Two Pathways

| Pathway | When to Use | Output |
|---------|-------------|--------|
| **Pathway A – Content Creation** | You want to publish something | Medium article, LinkedIn post, Twitter/X thread, or Learning Document |
| **Pathway B – Information Only** | You just want to stay informed | Categorized briefing of the latest GenAI developments |

Both pathways always end with a **Critical Pivot Step** — if you're on Pathway B and something catches your eye, you can instantly shift into content creation without restarting.

## Workflow Steps (Pathway A)

1. **Unified Assessment** — Determine goal, pathway, and format
2. **Research Phase** — Live web research across 20+ curated sources
3. **Pathway Decision** — Route to content creation or information briefing
4. **Idea Generation** — 5–8 unique, engineering-focused topic ideas with hooks and angles
5. **User Selection** — Pick one (or let the AI choose)
6. **Topic Explanation** — Deep dive into the selected topic before writing
7. **Content Creation** — Full post/article/thread in the chosen format
8. **Revision & Iteration** — Request unlimited targeted edits until satisfied

## Research Sources

**Primary AI Research & Company Blogs:**
- Anthropic (https://www.anthropic.com/research, https://www.anthropic.com/news)
- Google DeepMind / Gemini (https://blog.google/technology/ai/)
- Google Research (https://research.google/)
- OpenAI (https://openai.com/research)
- DeepSeek Papers (https://huggingface.co/collections/Presidentlin/deepseek-papers)
- Kiro (https://kiro.dev/blog/)

**AI News Aggregators & Newsletters:**
- The Rundown AI, TLDR AI, Ben's Bites, AI News Guru
- The Batch (DeepLearning.AI), Import AI, Alpha Signal
- The Neuron, GenAI.works, Latent Space

**Engineering & Community:**
- Hacker News, r/MachineLearning, r/LocalLLaMA
- Pragmatic Engineer, Simon Willison, Eugene Yan, Chip Huyen
- Hugging Face Blog

## Content Types

### Medium Articles
- ~1,200–1,500 words (7–8 min read)
- Full Markdown formatting
- Includes infographic image generation prompt with author branding
- Accompanied by a LinkedIn promotional post

### LinkedIn Posts
- 150–250 words (ruthlessly concise and scannable)
- Structure: Hook → Problem → Fix → How It Works → Impact
- Includes a detailed infographic/diagram generation prompt
- No hashtags, no emojis (unless contextually appropriate)

### Twitter / X Threads
- 5–7 tweets, each under 280 characters
- Strong hook → Problem → Solution → Quantifiable impact → Takeaway

### Learning Documents
- Comprehensive deep-dive reference documents
- Step-by-step guides, comparison tables, troubleshooting sections
- Designed to be saved and referenced long-term

## Quick-Start Prompts (`article_generation_prompts.md`)

Instead of writing your own prompt from scratch, use one of these ready-to-go starters:

| Prompt | Best For |
|--------|----------|
| **Interactive Starter** | General sessions — AI asks your goal first |
| **Direct-to-Content (Fast Track)** | You know exactly what you want to create |
| **Weekly Briefing** | Information-only, no content creation |
| **Deep-Dive Failure Analysis** | Contrarian / production war stories |
| **Instant Medium Article Generator** | Long-form, second-order effects focus |
| **Instant LinkedIn Post Generator** | Engineering micro-optimizations |
| **Instant Twitter/X Thread Generator** | Bold, controversial technical threads |

## Edge Case Handling

The workflow includes explicit rules for 23 identified edge cases, including:
- Unfilled/vague topic placeholders → clarify before researching
- User skips steps → honor the skip, never loop back
- Mid-session pathway changes → adapt without restarting
- All ideas rejected → regenerate with completely different strategy angles
- Unsupported output formats → adapt closest structural equivalent
- Inaccessible source URLs → fallback to web search with noted limitations
- Sparse news weeks → auto-widen to 30-day window with user notice

## Tips for Best Results

- Use the ready-made prompts from `article_generation_prompts.md` to fast-track sessions
- If you don't specify a topic, the AI will do a broad sweep across all GenAI categories
- You can skip any step by explicitly saying so (e.g., "skip the explanation")
- Request edits after the content is generated — the revision loop has no limit
- Use the image generation prompts in ChatGPT, Gemini, or Midjourney for visuals

## Notes

- Not all sessions need to result in content creation
- Always uses live web search — not cached training data
- Focus is on practical, actionable insights for AI engineers and developers
- Author branding (Sagar Rathkanthiwar) is automatically included in image prompts