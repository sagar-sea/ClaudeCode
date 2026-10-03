# Model Routing: Why Your Agent Costs 4x More Than It Should

**Created:** 2026-08-20
**Last Updated:** 2026-08-20 17:28 PDT
**Format:** LinkedIn Post

---

Your AI agents are probably using the wrong model for 80% of their tasks.

Not because you chose badly. Because you're routing everything to one model.

Glean's co-founder Tony Gentilcore recently shared a data point worth stopping on: Glean averages $0.45 per task. Claude Code averages $1.84. The difference isn't model quality — it's routing.

The logic is straightforward. A 15-step support agent doesn't need a frontier model for all 15 steps. Entity extraction, classification, summarization — small models handle these just as well, at a fraction of the cost. Route those to a mid-tier model. Reserve the frontier model for the steps where reasoning depth actually matters: multi-document synthesis, policy interpretation, complex planning.

Glean's internal model (Waldo) does exactly this before any frontier model is invoked — reduces latency 50%, tokens 25% — by deciding *what* to retrieve and *which* model actually needs it.

And research backs this at scale. UC Berkeley, Anyscale, and Canva published results at ICLR 2025 showing trained routers achieve 85% cost reduction while maintaining 95% of GPT-4-level performance.

The routing layer isn't an optimization. It's an architecture decision most teams are skipping.

If your agent stack sends every call to the same model, you're not overpaying for AI. You're overpaying for the wrong abstraction.

---
Source: Latent Space — "Frontier Model Cost and Open-Weights Popularity is Driving Demand for Model Routing" | https://www.latent.space/p/glean-model-routing
Research date: 2026-08-20

---

## Image Generation Prompt

Create a high-value, editorial-quality LinkedIn technical infographic titled: "The Model Routing Gap: Why Your Agent Costs 4x More Than It Should."

The one idea this visual must communicate within three seconds: Most agent costs come from sending all tasks to the same frontier model — routing separates simple tasks (cheap models) from complex reasoning (frontier models) to cut cost 4–5x without quality loss.

Use a **Before → After** narrative structure. **4:5 vertical LinkedIn graphic, optimized for mobile readability.**

**Left — "Before: Single-Model Stack":** Show an AI agent at the top dispatching 6 task cards in a vertical stack — entity extraction, classification, summarization, document retrieval, policy check, final answer synthesis — all connected by arrows to a single large "Frontier Model" block at the bottom. Label it `Every call. Same model. $1.84/task avg.` Use a neutral gray palette for this side. Add a subtle red cost meter in the corner.

**Right — "After: Routed Stack":** Show the same 6 task cards, now split by a central routing decision node. Top 4 tasks (extraction, classification, summarization, retrieval) route left to a small "Lightweight Model" block. Bottom 2 tasks (policy check, synthesis) route right to a "Frontier Model" block. Label the routing node: `Task Complexity Classifier`. Below, show `$0.45/task avg` in teal/green. Add an amber "85% cost reduction" badge with a footnote: `ICLR 2025 — UC Berkeley, Anyscale, Canva.`

**Center separator:** A clean vertical dividing line with a bold label: `Architecture Change, Not Model Change.`

**Bottom takeaway strip:** "Don't only ask which model is best. Ask which model each step actually needs." — in crisp sans-serif, full width.

Design: premium editorial-tech aesthetic. Light off-white background with subtle dot-grid texture. Navy, teal, amber palette. Thin connectors, rounded cards, generous whitespace. No robots, circuit boards, or generic AI imagery.
