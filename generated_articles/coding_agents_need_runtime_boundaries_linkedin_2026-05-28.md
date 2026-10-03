# Coding Agents Need Runtime Boundaries

**Created:** 2026-05-28
**Last Updated:** 2026-05-27 23:19
**Format:** LinkedIn Post

---

I used to think the hardest part of using coding agents was writing better prompts: better repo context, clearer instructions, sharper acceptance criteria, and more examples of the style I wanted. All of that still matters, but the more I work with coding agents, the more I think prompts are only the entry point.

The real shift happens when the agent stops being a code suggestion tool and starts becoming an actor inside the development workflow. That is when it can inspect files, run commands, modify code, coordinate across branches, open pull requests, and ask for approvals while work is already moving.

At that point, "better prompting" is not enough. The question changes from "How do I get better code out of the model?" to "What should this agent be allowed to touch, execute, call, change, and ship?"

That is the part I think many teams will underestimate. They will keep tuning prompts when they actually need runtime boundaries:

- sandboxed file and command access
- approval gates for risky actions
- network restrictions
- logs for commands, tool calls, approvals, and blocked steps
- normal PR review before merge

OpenAI's write-up on running Codex safely points directly at this pattern: bounded execution, explicit approvals, managed network policy, and agent-native audit trails. Kiro Web shows the same direction from the product side: autonomous coding agents running in isolated sandboxes, coordinating repository changes, and handing back pull requests for review.

My takeaway: if I let an AI coding agent behave like a junior engineer, I should manage it like one. Not just with instructions, but with permissions, observability, review, and clear production boundaries.

#AIAgents #SoftwareEngineering #GenAI #AgenticAI #AIEngineering

---
Source: OpenAI - Running Codex safely at OpenAI | https://openai.com/index/running-codex-safely/
Additional source: Kiro - Introducing Kiro Web | https://kiro.dev/blog/introducing-kiro-web/
Research date: 2026-05-28

---

## Image Generation Prompt

Create a bold LinkedIn infographic with very little text.

Main title, large and centered: "PROMPTS ARE NOT ENOUGH"

Directly below the title, centered in smaller uppercase text: "SAGAR RATHKANTHIWAR"

Visual concept: Split the image into two strong halves.

Left side: an AI coding agent standing in front of an open terminal and code repository, with loose arrows pointing to "files", "commands", "network", and "PRs". The left side should feel uncontrolled and risky, but clean and professional, not chaotic.

Right side: the same AI coding agent inside a clear protective boundary labeled "RUNTIME BOUNDARY". Around the boundary, show five simple icon labels only:
- Sandbox
- Approvals
- Network Policy
- Audit Logs
- PR Review

Use large icons, thick lines, high contrast, and generous spacing. Avoid paragraphs, small captions, dense diagrams, or tiny UI text. The image should be readable in 2 seconds on a LinkedIn mobile feed.

Style: modern technical poster, bold typography, clean light background, black/charcoal text, one strong accent color such as electric blue or signal green. Professional engineering aesthetic. No decorative clutter.

Bottom footer text, centered: "Follow Sagar Rathkanthiwar | Repost to share with your network"
