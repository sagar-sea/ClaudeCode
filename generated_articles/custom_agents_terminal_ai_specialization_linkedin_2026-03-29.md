# Custom Agents - Structure for Terminal AI

**Created:** 2026-03-29
**Last Updated:** 2026-03-29 (Initial creation)
**Format:** LinkedIn Post

---

Your terminal AI agent just wasted 30 seconds thinking about frontend code when you asked it to fix a backend API bug.

It loaded your entire codebase into context. Considered files it shouldn't touch. Suggested changes that violate your team's standards. Then asked for permission to run a command it runs 50 times a day.

This is the "generic agent" problem.

**Here's what's actually happening:**

Generic AI agents treat every task the same. They load everything, consider everything, and ask about everything. It's like hiring a generalist for every job instead of calling in a specialist.

The result? Slower responses. Inconsistent output. Wasted tokens on irrelevant context. And you, constantly re-explaining your project setup.

**The fix: Custom Agents**

Custom agents bring specialization to terminal AI. Instead of one agent doing everything, you create focused agents for specific workflows:

- A **backend specialist** that only touches `src/api/**`, auto-loads your API standards, and knows your error handling patterns
- A **DevOps agent** pre-approved to run deployment commands, with access to your infrastructure docs
- A **code review agent** that enforces your team's style guide and runs linters automatically

Each agent has:
→ **Restricted file access** - can't accidentally break unrelated code  
→ **Pre-loaded context** - your standards, docs, and patterns are always remembered  
→ **Pre-approved tools** - no permission prompts for routine operations  
→ **Focused scope** - only thinks about what matters for that task

**The impact:**

Benchmarks show specialized multi-agent systems hit 72.2% on SWE-bench Verified vs 65% for generic single agents using the same model. The gains come from focus, not from using a better model.

In practice, this means:
- Faster responses (no time wasted on irrelevant context)
- Consistent output (standards are baked in, not repeated)
- Better accuracy (agent isn't distracted by unrelated code)
- Less friction (routine tools run without prompts)

**Who has this?**

Custom agents are rolling out across leading CLI tools:
- **Kiro CLI** - JSON-based agent configs with file restrictions and auto-loaded docs
- **Claude Code** - Markdown-based custom agents in `.claude/agents/`
- **VS Code Copilot** - Agent plugins with custom configurations
- **GitHub Copilot** - Custom agents via repository config files

Kiro CLI's implementation stands out for its structure: you define tools, permissions, context paths, and file restrictions in one clean JSON file. Drop it in `.kiro/agents/`, and you've got a specialist.

**The shift:**

We're moving from "one AI that does everything poorly" to "specialized AIs that do specific things well."

It's the same principle that makes microservices work. Focused responsibility. Clear boundaries. Better results.

If you're still using a generic agent for everything, you're leaving speed and accuracy on the table.

---

**Source Attribution:**

Sources: 
- Kiro CLI Blog: https://kiro.dev/blog/introducing-kiro-cli/
- Kiro CLI Documentation: https://kiro.dev/docs/cli/custom-agents/
- ArXiv: https://arxiv.org/html/2602.14690v1
- VibeCoding.app: https://vibecoding.app/blog/multi-agent-vs-single-agent-coding
- The Neuron AI: https://www.theneuron.ai/explainer-articles/claude-code-automations-complete-guide/

Research date: 2026-03-29

---

**Hashtags:**

#AIAgents #DeveloperTools #CodingAgents #SoftwareEngineering #DevOps

---

## Image Generation Prompt

Create a technical comparison infographic titled "Generic Agent vs Custom Agents: The Specialization Advantage". 

**MANDATORY BRANDING:** Place the text "SAGAR RATHKANTHIWAR" centered directly beneath the main title in clean, professional typography. At the bottom of the infographic, add a footer reading "Follow Sagar Rathkanthiwar | Repost to share with your network".

**Left side - Generic Agent (Problem):**
- Single large circle labeled "Generic Agent"
- Arrows pointing to scattered file icons (frontend, backend, config, tests)
- Visual indicators of "wasted context" (faded/grayed files)
- Text: "Loads everything, considers everything, asks about everything"
- Performance metric: "65% accuracy"

**Right side - Custom Agents (Solution):**
- Three focused circles: "Backend Specialist", "DevOps Agent", "Code Review Agent"
- Each connected to specific file types only
- Visual indicators of "focused context" (highlighted relevant files)
- Icons showing: file restrictions, pre-loaded docs, pre-approved tools
- Performance metric: "72.2% accuracy"

**Bottom comparison bar:**
- Speed: Generic (slow) vs Custom (fast)
- Consistency: Generic (variable) vs Custom (high)
- Token efficiency: Generic (wasteful) vs Custom (optimized)

Style: Clean, modern, technical diagram with a professional color scheme (blues, greens, grays). Use icons for files, locks for permissions, and checkmarks for pre-approved tools. Make the performance difference visually obvious.
