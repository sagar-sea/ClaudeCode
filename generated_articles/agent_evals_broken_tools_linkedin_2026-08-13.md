# Agent Evals Must Test Broken Tools, Not Just Happy Paths

**Created:** 2026-08-13
**Last Updated:** 2026-08-13 21:54
**Format:** LinkedIn Post

---

Your AI agent passed every demo.

But what happens when a tool times out, returns last week's data, or has a poisoned description?

Most agent evaluations never find out. They test the happy path: valid tools, clean outputs, predictable APIs.

Production is the opposite.

A search API can return stale results. A CRM connector can deny a permission. A tool schema can change. And if the agent treats every response as trustworthy, a capable model can still make a bad decision.

Here's the shift teams need to make:

- Test tool failures deliberately, not incidentally.
- Replay real failure traces so a fix is reproducible.
- Verify recovery behavior: retry, escalate, switch tools, or stop safely.
- Make these scenarios release gates alongside task-success metrics.

Recent AgentCheck research frames this as a practical loop: reproduce a tool failure, intervene, then confirm the mitigation actually holds.

The goal isn't an agent that always completes the task.

It's an agent that knows when it no longer has trustworthy inputs.

If your agent can call tools in production, your eval suite should be able to break them first.

#AIAgents #AIEngineering #LLMOps #AIEvaluation #MCP

---
Source: AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP | https://arxiv.org/abs/2607.11098
Research date: 2026-08-13

---

## Image Generation Prompt

Create a clean, minimalist professional technical infographic titled **"Agent Evals Must Test Broken Tools"**. Directly beneath the title, place **"SAGAR RATHKANTHIWAR"** centered in smaller uppercase text. Use a two-panel before/after layout on a light dotted background. Left panel label: **"Happy-Path Eval"**. Show a cheerful AI agent connected to green tool boxes labeled "Search API," "CRM," and "Database," all returning checkmarks; add a small caption: "Valid tools. Clean outputs. Demo passes." Right panel label: **"Production-Ready Eval"**. Show the same AI agent encountering a red timeout clock on Search API, a yellow stale-data warning on CRM, a red shield warning labeled "Poisoned tool description," and a gray permission-denied lock on Database. Route these through a central evaluation harness with three numbered steps: "1. Reproduce", "2. Intervene", "3. Verify recovery". Show safe outcomes below it: "retry", "escalate", "switch tool", and "stop safely". Use restrained navy, teal, amber, and red accents; crisp sans-serif typography; high information hierarchy; no logos; no extraneous text. At the very bottom, include this exact footer text: **"Follow Sagar Rathkanthiwar | Repost to share with your network"**.
