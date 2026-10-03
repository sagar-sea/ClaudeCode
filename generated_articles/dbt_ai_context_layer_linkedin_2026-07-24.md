# dbt Is Becoming AI's Context Layer

**Created:** 2026-07-24
**Last Updated:** 2026-07-25 00:00 PDT
**Format:** LinkedIn Post
**Author:** Sagar Rathkanthiwar

---

AI has not made SQL the hard part.

It has made *context* the hard part.

For anyone new to it: **dbt is an open-source framework that data teams use to transform raw warehouse data into tested, documented models.** dbt Labs also offers a commercial platform built around that workflow.

An AI agent can generate a query in seconds. But ask, “What was monthly revenue?” and it still needs the institutional knowledge a good analyst carries around:

- Does revenue mean booked or recognized?
- Are refunds excluded?
- Which model is authoritative?
- Who owns the definition when it changes?

That is why dbt feels genuinely groundbreaking in the AI era. It is not just a transformation tool; it turns business logic into machine-readable infrastructure:

- models and tests establish quality;
- lineage and ownership make changes explainable;
- the Semantic Layer defines metrics once; and
- the dbt MCP server lets AI agents retrieve governed context instead of guessing from raw warehouse tables.

The newer Fusion engine completes the picture: it gives humans *and agents* richer project context and validates SQL changes before they reach the warehouse.

The more I follow agentic AI, the more convinced I am that reliable AI will not come from endlessly swapping models. It will come from engineering the context around them.

That is dbt’s moment: it captures how a business defines truth, versions it like software, and makes it available to every dashboard, application, and agent.

Before giving an AI analyst broader access, give it a contract for what the data means.

#dbt #DataEngineering #AI

---
Sources: [dbt Semantic Layer](https://www.getdbt.com/product/semantic-layer) | [dbt MCP Server](https://github.com/dbt-labs/dbt-mcp) | [dbt Fusion engine](https://www.getdbt.com/product/fusion) | [AI-ready data in practice](https://www.getdbt.com/blog/ai-ready-data-in-practice-what-dbt-semantic-layer-and-dbt-s-mcp-server-and-agent-skills-do-for)

Research date: 2026-07-25

---

## Image Generation Prompt

Create a clean, minimalist technical infographic titled “dbt: AI’s Context Layer”. Directly beneath the main title, center the text “SAGAR RATHKANTHIWAR” in smaller uppercase type. Show a left-to-right flow: on the left, an AI agent looking at a messy warehouse of unlabeled raw tables with question marks and conflicting definitions of “Revenue”; in the center, a clearly labeled dbt context layer containing four stacked blocks—“Tested models,” “Lineage & ownership,” “Governed metrics,” and “MCP interface”; on the right, trusted outputs for a dashboard, an application, and an AI agent, all displaying the same validated revenue metric. Use subtle navy, teal, and white on a light grid background. Include concise labels: “Raw data → governed meaning → reliable AI”. At the very bottom footer, include exactly: “Follow Sagar Rathkanthiwar | Repost to share with your network”.
