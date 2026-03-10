# GenAI Weekly Research & Article Generation Prompts

This document contains a collection of optimized starting prompts to use alongside your `genai_weekly_research_prompt.md` workflow file. Depending on what you want to achieve in a given session, you can copy and paste one of these prompts to instantly kickstart the AI's process.

---

## 1. The Interactive Starter (General Purpose)
**What it does:** This is the improved version of your original prompt. It tells the AI to read the workflow and immediately execute Step 1 (Unified Assessment Phase) without you needing to repeat the workflow steps in the chat. It gives you the flexibility to decide your goal on the fly.

**The Prompt:**
```text
Act as my expert AI research assistant. I have provided the `genai_weekly_research_prompt.md` file which contains your strict workflow, research sources, and content constraints.

Please read and internalize the workflow. To kick off our session, execute **Step 1: Unified Assessment Phase** exactly as described. Ask me the single comprehensive question to determine my goal for today, and wait for my reply before you begin any research.
```

---

## 2. Direct-to-Content (Fast Track)
**What it does:** Bypasses Step 1 entirely. If you already know you want to create a specific piece of content (e.g., a LinkedIn post about a specific topic), use this prompt. It forces the AI straight into the Research Phase and Idea Generation Phase.

**The Prompt:**
```text
Act as my expert AI research assistant, following the rules in the attached `genai_weekly_research_prompt.md` file. 

We are skipping Step 1 today and going straight down **Pathway A (Content Creation)**. 
My goal is to create a [LinkedIn Post / Twitter Thread / Medium Article] focusing on [Insert Topic, e.g., "AI agent automation" or "general engineering takeaways"].

Please execute **Step 2 (Research Phase)** right now using your web browsing/search tools to find developments from the past 7-14 days. Once your research is complete, immediately execute **Step 4 (Idea Generation Phase)** and present me with ideas formatted according to your strict Idea/Topic Generation Strategy.
```

---

## 3. The Weekly Briefing (Information Only)
**What it does:** Bypasses Step 1 and forces the AI into "Pathway B". Perfect for when you just want to consume the news over your morning coffee without the pressure of creating content.

**The Prompt:**
```text
Act as my expert AI research assistant. Please review the attached `genai_weekly_research_prompt.md` file. 

Today, we are taking **Pathway B: Information Only**. I do not want to create any content. I am specifically interested in [general AI developments / new tooling / model updates].

Please execute **Step 2 (Research Phase)** using your live web search tools on the provided URLs for the past 7-14 days. After researching, immediately provide a concise, categorized summary highlighting the 3-5 key takeaways.
```

---

## 4. The Deep-Dive Failure Analysis
**What it does:** Directly leverages the "Contrarian / Failure Analysis" strategy from the workflow. Use this when you want to write a hard-hitting engineering article about why something in AI isn't working as nicely as the hype suggests.

**The Prompt:**
```text
Act as my expert AI research assistant relying on the `genai_weekly_research_prompt.md` workflow. We are taking **Pathway A (Content Creation)** specifically for a [Medium Article / LinkedIn post].

For your research (**Step 2**), I want you to focus strictly on "Real-world Scars" and "Failure Analysis". Search Hacker News, Latent Space, and Reddit for discussions about where GenAI tools/frameworks are currently failing in production, hitting rate limits, or costing too much.

Do the research, then present me with 4 highly contrarian, unconventional topics (**Step 4**) we can write about.
```

---

## 5. Instant Medium Article Generator
**What it does:** Use this when you already know you want a long-form Medium article. It bypasses the assessment and formatting questions, automatically telling the AI to look for deep "Second-Order Effects," generate specific article ideas, and wait for your selection.

**The Prompt:**
```text
Act as my expert AI research assistant using the `genai_weekly_research_prompt.md` workflow. 

Skip Steps 1-3. We are creating a **Medium Article**. 
Please begin immediately at **Step 2 (Research Phase)**. Focus your research on [specific topic, e.g., latest open-source model releases or agentic frameworks]. 

Once research is complete, execute **Step 4 (Idea Generation Phase)**. Give me 4-5 compelling article ideas focusing on "Cross-Pollination" or "Deep Structural Deconstruction." Wait for my selection before proceeding to Step 6.
```

---

## 6. Instant LinkedIn Post Generator
**What it does:** Use this when you want to create a high-impact, scannable LinkedIn post prioritizing engineering optimization or practical advice. It skips all onboarding steps.

**The Prompt:**
```text
Act as my expert AI research assistant using the `genai_weekly_research_prompt.md` workflow. 

Skip Steps 1-3. We are creating a **LinkedIn Post**. 
Please begin immediately at **Step 2 (Research Phase)**. Look for emerging trends around [specific topic, e.g., RAG optimization or prompt caching]. 

Once research is complete, execute **Step 4 (Idea Generation Phase)**. Generate 5 short-form topics focusing on "Unconventional Solutions" or "Micro-Optimizations" that engineers face. Highlight quantifiable metrics. Wait for my selection before proceeding to Step 6.
```

---

## 7. Instant Twitter / X Thread Generator
**What it does:** Ideal for quickly spinning up technical threads. This bypasses the onboarding and directs the AI to specifically generate punchy, high-signal topic ideas specifically formatted for X.

**The Prompt:**
```text
Act as my expert AI research assistant using the `genai_weekly_research_prompt.md` workflow. 

Skip Steps 1-3. We are creating a **Twitter / X Thread**. 
Please begin immediately at **Step 2 (Research Phase)**. Look for the latest developments regarding [specific topic/tool]. 

Once research is complete, execute **Step 4 (Idea Generation Phase)**. Generate 5 bold, controversial, or highly-technical topics that challenge the current hype cycle. Wait for my selection before creating the 7-tweet thread in Step 7.
```

---

## 8. The "Study & Pivot" Routine
**What it does:** Use this when you are just studying or browsing for your own personal engineering growth, but you want to leave the door open to writing an article if you stumble onto something genuinely cool. It runs an information-only briefing but explicitly triggers the new "Pivot" capability.

**The Prompt:**
```text
Act as my expert AI research assistant using the `genai_weekly_research_prompt.md` workflow. 

Today we are taking **Pathway B: Information Only**. I am just trying to study and understand the latest developments regarding [Insert Topic, e.g., memory management in local LLMs].

Please execute **Step 2 (Research Phase)** using your live web browsing. Provide me with a categorized briefing of what you find. When you are done, execute the **CRITICAL PIVOT STEP** defined in Step 3. Ask me if any of it caught my eye, and be prepared to instantly shift gears into Pathway A (Content Creation) if I decide I want to write a piece based on your briefing.
```
