# Arxiv AI Digest — 2026-03-17

> 30 papers fetched · 10 passed hard signal filter · 5 selected by relevance
> Categories: cs.AI, cs.LG, cs.CL · Lookback: 3 days

---

## 1. Think First, Diffuse Fast: Improving Diffusion Language Model Reasoning via Autoregressive Plan Conditioning
**Authors:** Earl J St Sauver et al.
**Link:** https://arxiv.org/abs/2603.13243

**What they built:** Diffusion large language models (dLLMs) generate text by iteratively denoising all token positions simultaneously — unlike autoregressive models that build left-to-right. This makes them fast but bad at multi-step reasoning, because tokens can't build on each other. The authors hypothesize this is a "coordination problem": without a shared scaffold, positions conflict. Their fix is dead-simple — prepend a short (~100-token) natural-language plan from a regular AR model before the diffusion model starts denoising. This frozen plan gives every position something to coordinate around. Result: LLaDA-8B jumps from 75.6% to 87.2% on GSM8K (+11.6pp), matching a same-size LLaMA 3.1 8B (87.7%). On HumanEval code, the gain is +12.8pp. Diffusion models benefit 2–10x more from plans than AR models do, validating the hypothesis. Cost: ~$0.002/problem, ~2s extra latency.

**What this means for you:** If you're using or evaluating diffusion LLMs (like LLaDA or MDLM) for reasoning tasks and finding them underwhelming, this is a training-free drop-in fix. Just generate a short plan with any capable AR model and prepend it. The technique works for both math and code. Watch out: planner quality matters a lot — smaller Llama-class planners actually hurt performance, so you need a frontier model as the planner.

---

## 2. Training-Free Agentic AI: Probabilistic Control and Coordination in Multi-Agent LLM Systems
**Authors:** Mohammad Parsa Hosseini et al.
**Link:** https://arxiv.org/abs/2603.13256

**What they built:** Multi-agent LLM systems typically route tasks to sub-agents randomly or by simple rules, wasting tokens on bad agents. REDEREF is a training-free controller that uses Thompson sampling — a Bayesian approach — to route tasks to agents with the best historical track record. It also adds reflection-driven re-routing (a judge LLM decides if an agent's answer is good), evidence-based selection (pick the best answer, don't average them), and memory-aware priors to cold-start new agents intelligently. Tested on multi-agent split-knowledge tasks: 28% token reduction, 17% fewer agent calls, 19% faster time-to-success vs. random delegation — with no training or fine-tuning needed.

**What this means for you:** If you're building multi-agent pipelines (LangGraph, CrewAI, AutoGen, etc.) and struggling with efficiency or inconsistent results, REDEREF's pattern is directly applicable. The Thompson sampling approach can be implemented in ~50 lines on top of any existing framework. The 28% token savings translates directly to cost savings at production scale.

---

## 3. Explain in Your Own Words: Improving Reasoning via Token-Selective Dual Knowledge Distillation
**Authors:** Minsang Kim, Seung Jun Baek
**Link:** https://arxiv.org/abs/2603.13260

**What they built:** Knowledge distillation (KD) compresses a large "teacher" model into a smaller "student" by having the student mimic the teacher's output distribution. The problem: a weak student overwhelmed by imitating every teacher token learns poorly. TSD-KD takes a dual approach — indirect distillation lets the student generate its own candidate answers, and the teacher just re-ranks them (no full distribution imitation); direct distillation selectively matches distributions only on tokens where the teacher and student confidence gap is large. They also add entropy regularization. Remarkably, students trained with TSD-KD beat their own teachers in 4 out of 10 benchmarks by up to 20.3%, and outperform baselines by up to 54.4%. Code released at github.com/kmswin1/TSD-KD.

**What this means for you:** If you're fine-tuning or distilling small models for reasoning tasks (math, coding, QA), TSD-KD is worth adopting over standard KD. The key insight — let the student explain in its own words rather than blindly copying the teacher — generalizes to any scenario where you're distilling chain-of-thought reasoning. Code is available, making this immediately usable.

---

## 4. ILION: Deterministic Pre-Execution Safety Gates for Agentic AI Systems
**Authors:** Florin Adrian Chitan
**Link:** https://arxiv.org/abs/2603.13247

**What they built:** As AI agents gain the ability to call APIs, modify files, and run code, existing content-safety infrastructure (OpenAI Moderation API, Llama Guard) fails badly — it was designed to flag harmful *language*, not dangerous *actions*. ILION is a deterministic execution gate that classifies proposed agent actions as BLOCK or ALLOW using a 5-component cascade (identity imprinting, semantic reference frames, drift control, resonance scoring, consensus veto). Zero training data needed, sub-millisecond latency (143µs mean). On a 380-scenario benchmark covering 8 attack categories: F1=0.8515, 91% precision. Compared to OpenAI Moderation API (F1=0.1188) and Llama Guard 3 (F1=0.0105), it's not even close — text-safety tools systematically fail at action safety.

**What this means for you:** If you're shipping AI agents that execute real-world actions (shell commands, database writes, API calls), you need an action-level safety layer — and this paper proves you cannot rely on your LLM provider's content moderation for it. ILION's architecture is a directly implementable pattern: classify the *action*, not the *text*. The F1=0.85 at 143µs is practical for production.

---

## 5. Your Code Agent Can Grow Alongside You with Structured Memory
**Authors:** Yi-Xuan Deng et al.
**Link:** https://arxiv.org/abs/2603.13258

**What they built:** Current code agents only see the current codebase snapshot — they have no memory of why code evolved the way it did, or what past PRs tried that didn't work. MemCoder addresses this by (1) mining git commit history to extract intent-to-code mappings as structured memory, (2) using verification feedback to self-correct in real time, and (3) crystallizing human-validated solutions back into long-term memory (experience self-internalization). On SWE-bench Verified — the industry-standard benchmark for real-world GitHub issue resolution — MemCoder achieves SOTA performance and a 9.4% improvement in resolved rate over DeepSeek-V3.2 as the base model.

**What this means for you:** For teams using AI coding assistants on large, long-running codebases, this is the architecture you want. The git-history-as-memory approach is brilliant and underexplored — your commit log is effectively a labeled dataset of "problem → solution" pairs. If you're building internal dev tooling, mining PRs and commits for agent context is a high-leverage, zero-cost data source.

---
