# GitHub AI Trending — 2026-03-17

> 25 repos fetched · 10 passed hard signal filter · 5 selected by relevance
> Topics: AI, LLM, machine-learning, agents · Time window: 3 days

---

## 1. microsoft/BitNet
**Stars:** 35,289 · **3-day growth:** high weekly momentum
**Link:** https://github.com/microsoft/BitNet

**What it does:** The official inference framework for 1-bit LLMs — models where every weight is stored as -1, 0, or +1 instead of a 16/32-bit float, making them dramatically smaller and cheaper to run.

**Worth your time?** Yes — Microsoft Research built this, and 1-bit quantization is one of the most promising paths to running capable LLMs on edge hardware (laptops, phones, embedded devices). If you're building anything that needs local inference without a GPU, this is the framework to benchmark against. It's not a toy — this is production-grade inference code backed by published research.

---

## 2. promptfoo/promptfoo
**Stars:** 17,236 · **3-day growth:** strong
**Link:** https://github.com/promptfoo/promptfoo

**What it does:** A testing and evaluation framework for prompts, agents, and RAG pipelines — with built-in red teaming, vulnerability scanning, and performance comparison across GPT, Claude, Gemini, Llama and more.

**Worth your time?** Yes — if you're shipping LLM-powered features, this fills the gap between "vibes" and actual regression testing. Declarative YAML configs mean you can drop evals into CI/CD without writing test harnesses from scratch. The red-teaming / pentesting capability is particularly valuable for teams under compliance pressure. Actively maintained with 1,491 forks.

---

## 3. alibaba/page-agent
**Stars:** 10,624 · **3-day growth:** rising fast
**Link:** https://github.com/alibaba/page-agent

**What it does:** A JavaScript in-page GUI agent that lets you control web interfaces with natural language — it runs directly in the browser, reads the DOM, and takes actions on your behalf.

**Worth your time?** Yes — this is a practical building block for browser automation without Playwright/Puppeteer brittle selectors. If you're building customer support bots, RPA-style workflows, or AI copilots that interact with existing web UIs, page-agent gives you a language-native action layer. Alibaba engineering behind it means the foundations are solid. Worth cloning and testing against your own web apps immediately.

---

## 4. volcengine/OpenViking
**Stars:** 15,274 · **3-day growth:** strong
**Link:** https://github.com/volcengine/OpenViking

**What it does:** An open-source context database purpose-built for AI agents — it unifies memory, resources, and skills into a filesystem-like hierarchy, enabling agents to store, retrieve, and evolve their context across sessions.

**Worth your time?** Yes — the "memory problem" in agentic AI (agents forgetting everything between runs) is one of the hardest unsolved practical issues. OpenViking tackles this with a structured, hierarchical approach rather than just dumping embeddings into vector search. The self-evolving context model is novel. If you're building multi-session agents, this is worth architecturally studying even if you don't adopt it directly.

---

## 5. vectorize-io/hindsight
**Stars:** 4,623 · **3-day growth:** very strong for its size
**Link:** https://github.com/vectorize-io/hindsight

**What it does:** Agent memory that learns — Hindsight analyzes past agent interactions and automatically extracts, consolidates, and updates what an agent should remember for future runs.

**Worth your time?** Yes — this is the practical implementation of what people call "long-term memory" for agents. Rather than manually curating what the agent remembers, Hindsight automatically distills lessons from past sessions. 4,600+ stars for a focused infrastructure tool is a strong signal. Good fit for anyone building agents that do repetitive tasks and should improve over time (code agents, research agents, customer service bots).

---
