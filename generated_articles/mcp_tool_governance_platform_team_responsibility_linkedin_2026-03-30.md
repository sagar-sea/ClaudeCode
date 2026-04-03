# MCP/Tool Governance Is Now a Platform-Team Responsibility

**Created:** 2026-03-30
**Last Updated:** 2026-03-30 20:27
**Format:** LinkedIn Post

---

Your AI agents probably do not need better prompts first.
They need governance.

Most teams are wiring MCP connectors and tool permissions ad hoc across squads. It feels fast at first, but it quietly creates risk:
- Inconsistent tool allowlists
- Unclear approval paths
- No shared audit trail when an agent takes a high-impact action

The result: security reviews show up late, platform teams get pulled into firefighting, and launches slow down.

Here is the fix:
Treat agent tooling like core platform infrastructure, not app-level glue.

Start with:
- A centralized MCP/tool policy layer (what can run, by whom, in which environment)
- Scoped trust controls for CLI/tool execution
- Standard model-routing and logging rules across teams
- One owner team for governance changes and incident response

If every team has its own permission model, you do not have velocity. You have operational roulette.

When governance is centralized, approval and risk handling become predictable, and teams can ship agent workflows with much less friction.

This is where AI platform engineering is heading in 2026.

---
Source: Kiro Blog | https://kiro.dev/blog/enterprise-governance-mcp-and-models/
Additional source: Kiro CLI 1.27 Changelog | https://kiro.dev/changelog/cli/1-27/
Research date: 2026-03-30

#AIEngineering #PlatformEngineering #MCP #AIGovernance #LLMOps #DevSecOps

---

## Image Generation Prompt

Create a clean technical infographic titled "MCP/Tool Governance for AI Agents". Directly beneath the main title, place the name "SAGAR RATHKANTHIWAR" centered in smaller caps. Visual layout: left side shows a "Before" architecture with multiple teams connecting agents to tools independently (scattered lines, warning icons, inconsistent permissions); right side shows an "After" architecture with a centralized governance layer controlling MCP access, model routing, and execution trust policies. Include labeled components: "Tool Allowlist", "Approval Policy", "Audit Logs", "Environment Scoping", "Incident Response Owner". Use a professional palette (navy, slate, teal accents), minimal icons, and simple arrows to show controlled flow. Add a compact comparison strip: "Ad hoc governance -> unpredictable risk" vs "Central governance -> predictable delivery". At the very bottom footer of the image, include the text "Follow Sagar Rathkanthiwar | Repost to share with your network".
