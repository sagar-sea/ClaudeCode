# 📰 AI Digests — AI Skills

> Two AI skills that deliver daily digests of the latest AI papers and trending repos.
> Runs on Claude Code, Antigravity, Kiro IDE, Codex, and any AI agent with web access.
> No APIs, no keys — uses public RSS feeds and GitHub's trending page.

---

## 📦 Skills Included

| Skill | Command | Source | Output |
|-------|---------|--------|--------|
| Arxiv AI Digest | `/arxiv-digest` | arxiv.org RSS feeds | `arxiv-digest-YYYY-MM-DD.md` |
| GitHub AI Trending | `/github-ai-trending` | github.com/trending | `github-trending-YYYY-MM-DD.md` |

---

## 🚀 How to Run — By Platform

The skill logic lives in the SKILL.md files. Any AI agent that can read files and fetch URLs can execute it. Below are instructions for each platform.

---

### 🖥️ Claude Code (Slash Command)

**Best for:** Daily automated runs, staying in your terminal workflow.

1. Open a terminal and launch Claude Code in the workspace:
   ```powershell
   cd C:\Users\Sagar\ClaudeCode
   claude
   ```
2. Type the slash command inside the Claude Code session:
   ```
   /arxiv-digest
   ```
   or
   ```
   /github-ai-trending
   ```
3. Claude Code reads the SKILL.md, fetches live data, and saves the digest to:
   ```
   C:\Users\Sagar\ClaudeCode\ai-digests\arxiv-digest-YYYY-MM-DD.md
   ```

> **Note:** Skills must be in `.claude/skills/<skill-name>/SKILL.md` inside the workspace
> Claude Code is launched from. The MCP filesystem is sandboxed to that directory.

---

### 🤖 Antigravity (This Conversation)

**Best for:** On-demand runs, one-off digests, no terminal needed.

Antigravity (the AI you're talking to right now) can run the skill directly — it has
web access to fetch arXiv RSS and GitHub trending, and can write files to your workspace.

Just say:
```
run arxiv-digest
```
or
```
run github-ai-trending
```

Antigravity will:
1. Read the config from `C:/Users/Sagar/ClaudeCode/.claude/ai-digests/config.md`
2. Fetch and process live data following the SKILL.md pipeline
3. Write the digest file directly to `C:/Users/Sagar/ClaudeCode/ai-digests/`

> **Note:** No setup needed beyond what's already installed. Works in any conversation
> as long as your workspace is `C:\Users\Sagar\ClaudeCode`.

---

### 🪐 Kiro IDE (Agent Task)

**Best for:** Running inside your IDE without switching windows, integrating with your dev workflow.

Kiro IDE supports agent tasks that can read files and call web endpoints.

1. Open Kiro IDE with `C:\Users\Sagar\ClaudeCode` as your workspace root.
2. Open the **Agent** panel and start a new task.
3. Paste this prompt:
   ```
   Read the skill instructions from .claude/skills/arxiv-digest/SKILL.md and execute
   them exactly. Use the config at .claude/ai-digests/config.md. Save the digest
   output to the ai-digests/ folder with today's date in the filename.
   ```
4. Kiro's agent will follow the SKILL.md steps and write the file.

> **Note:** Kiro must have filesystem write access and web fetch capability enabled
> in its agent settings. The output path is relative to your workspace root.

---

### ⚡ OpenAI Codex (Prompt-based)

**Best for:** Running via the Codex CLI or API with a custom system prompt.

Codex (o3/o4 series via API or CLI) can execute the skill by reading the SKILL.md as
a system prompt and running it as a task.

**Option A — Codex CLI:**
```powershell
# From your workspace directory
codex "Read .claude/skills/arxiv-digest/SKILL.md and execute it. Use config at .claude/ai-digests/config.md. Save output to ai-digests/arxiv-digest-$(Get-Date -Format yyyy-MM-dd).md"
```

**Option B — API (Python):**
```python
import openai, pathlib, datetime

skill = pathlib.Path(".claude/skills/arxiv-digest/SKILL.md").read_text()
config = pathlib.Path(".claude/ai-digests/config.md").read_text()

client = openai.OpenAI()
response = client.responses.create(
    model="o4-mini",
    tools=[{"type": "web_search_preview"}],
    input=[
        {"role": "system", "content": skill},
        {"role": "user",   "content": f"Config:\n{config}\n\nToday: {datetime.date.today()}. Run the digest now."}
    ]
)
print(response.output_text)
```

> **Note:** Codex needs the `web_search_preview` or `browser` tool enabled to fetch
> arXiv RSS feeds. File writing must be handled by your script — Codex returns the
> digest content as text; save it yourself.

---

### 🆚 Platform Comparison

| Platform | Trigger | File Write | Web Fetch | Best For |
|----------|---------|------------|-----------|----------|
| **Claude Code** | `/arxiv-digest` slash cmd | ✅ Auto | ✅ Auto | Daily terminal workflow |
| **Antigravity** | Natural language request | ✅ Auto | ✅ Auto | On-demand, no setup |
| **Kiro IDE** | Agent task prompt | ✅ Auto | ✅ Auto | IDE-integrated workflow |
| **Codex CLI** | Shell command | ⚠️ Manual save | ✅ With tool | CI/CD or scripted runs |
| **Codex API** | Python script | ⚠️ Manual save | ✅ With tool | Automation & scheduling |

---

## 🗂️ File Structure (Windows)

```
C:\Users\Sagar\ClaudeCode\
├── .claude\
│   ├── ai-digests\
│   │   └── config.md                  ← Edit this to customize behavior
│   └── skills\
│       ├── arxiv-digest\
│       │   └── SKILL.md               ← Skill instructions for /arxiv-digest
│       └── github-ai-trending\
│           └── SKILL.md               ← Skill instructions for /github-ai-trending
├── ai-digests\                         ← Digest output files are saved here
│   ├── arxiv-digest-2026-03-17.md
│   └── github-trending-2026-03-17.md
└── arxiv_readme.md                     ← This file
```

> **Note:** All files live inside `C:\Users\Sagar\ClaudeCode` so that Claude Code's MCP
> filesystem server (which is sandboxed to this workspace) can read and write them.

---

## ⚙️ Configuration

Edit `.claude/ai-digests/config.md` to customize both skills:

```
C:\Users\Sagar\ClaudeCode\.claude\ai-digests\config.md
```

### Full Config Reference

```markdown
## Output
output_dir: C:/Users/Sagar/ClaudeCode/ai-digests

## Arxiv Digest
categories: cs.AI, cs.LG, cs.CL
results: 5           # final digest count
filter_size: 10      # pool after hard signal filter (range: 5–15)
fetch_pool_size: 25  # initial fetch width (range: 15–50)
lookback_days: 3     # range: 1–7

## GitHub Trending
topics: AI, LLM, machine-learning, agents
results: 5           # final digest count
filter_size: 10      # pool after hard signal filter (range: 5–15)
fetch_pool_size: 25  # initial fetch width (range: 15–50)
time_window: 3       # range: 1–7 days
```

### Config Options Explained

#### Shared
| Option | Default | Description |
|--------|---------|-------------|
| `output_dir` | `C:/Users/Sagar/ClaudeCode/ai-digests` | Where digest `.md` files are saved |
| `results` | `5` | Number of items in the final digest |
| `filter_size` | `10` | Items kept after the hard signal scoring filter |
| `fetch_pool_size` | `25` | Items fetched initially before any filtering |

#### Arxiv Digest
| Option | Default | Description |
|--------|---------|-------------|
| `categories` | `cs.AI, cs.LG, cs.CL` | arXiv categories to pull from ([full list](https://arxiv.org/category_taxonomy)) |
| `lookback_days` | `3` | Discard papers older than this many days |

**Popular categories to add:**
- `cs.CV` — Computer Vision
- `cs.NE` — Neural and Evolutionary Computing
- `cs.RO` — Robotics
- `stat.ML` — Machine Learning (Statistics)

#### GitHub Trending
| Option | Default | Description |
|--------|---------|-------------|
| `topics` | `AI, LLM, machine-learning, agents` | Keywords to filter repos by description/tags |
| `time_window` | `3` | 1–2 uses daily trending, 3–7 uses weekly trending |

---

## 🔍 How It Works — 3-Stage Pipeline

Both skills use the same pipeline:

```
Stage 1: Fetch Wide
  └─ Pull fetch_pool_size candidates from the source
       (arXiv RSS per category, or GitHub trending page)

Stage 2: Hard Signal Filter
  └─ Narrow to filter_size using objective signals:
       • arXiv: recency score + lab affiliation + keyword density
       • GitHub: star growth score + total star count score

Stage 3: Claude Relevance Ranking
  └─ Score remaining candidates on practical engineering value
       Select top results items

Output: Dated markdown file saved to output_dir
```

### Scoring Details

#### arXiv Hard Signal Filter
| Signal | Points |
|--------|--------|
| Published today | +3 |
| Published yesterday | +2 |
| Published 2 days ago | +1 |
| Published 3+ days ago | 0 |
| Author from Google/DeepMind/Meta/OpenAI/Anthropic/Stanford/MIT/CMU/Berkeley/Apple/MSFT | +2 |
| Each keyword match (LLM, agent, RAG, reasoning, etc.) | +1 (max +5) |

#### GitHub Hard Signal Filter
| Signal | Points |
|--------|--------|
| Star growth ≥ 1,000 | +4 |
| Star growth 500–999 | +3 |
| Star growth 200–499 | +2 |
| Star growth 50–199 | +1 |
| Total stars ≥ 10,000 | +3 |
| Total stars 1,000–9,999 | +2 |
| Total stars 100–999 | +1 |

---

## 📄 Output Format

### arxiv-digest-YYYY-MM-DD.md

```markdown
# Arxiv AI Digest — 2026-03-17

> 62 papers fetched · 10 passed hard signal filter · 5 selected by relevance
> Categories: cs.AI, cs.LG, cs.CL · Lookback: 3 days

---

## 1. Paper Title Here
**Authors:** First Author et al. · Google DeepMind
**Link:** https://arxiv.org/abs/2501.12345

**What they built:** Plain-English description of the research...

**What this means for you:** Concrete takeaway for engineers building with AI...

---
```

### github-trending-YYYY-MM-DD.md

```markdown
# GitHub AI Trending — 2026-03-17

> 25 repos fetched · 10 passed hard signal filter · 5 selected by relevance
> Topics: AI, LLM, machine-learning, agents · Time window: 3 days

---

## 1. owner/repo-name
**Stars:** 12,400 · **3-day growth:** +1,800
**Link:** https://github.com/owner/repo-name

**What it does:** One clear sentence describing the repo.

**Worth your time?** Yes — explanation of practical use...

---
```

---

## 🛠️ Customization Examples

### More arXiv categories + larger digest
```markdown
categories: cs.AI, cs.LG, cs.CL, cs.CV, cs.RO
results: 8
fetch_pool_size: 40
lookback_days: 2
```

### Broader GitHub topics + daily window
```markdown
topics: AI, LLM, machine-learning, agents, RAG, fine-tuning, inference
results: 7
time_window: 1
fetch_pool_size: 30
```

---

## 📅 Last Updated

- **Setup date:** 2026-03-17
- **Last updated:** 2026-03-17 — Added multi-platform run instructions
- **Original repo:** [Ubajaj1/ai-digests-skill](https://github.com/Ubajaj1/ai-digests-skill)
- **Adapted for:** Windows / workspace at `C:\Users\Sagar\ClaudeCode`
- **Platforms tested:** Claude Code ✅ · Antigravity ✅ · Kiro IDE (instructions adapted) · Codex (instructions adapted)

---

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| `Access denied - path outside allowed directories` | Make sure you run Claude Code from `C:\Users\Sagar\ClaudeCode` |
| No papers found in arXiv digest | Increase `lookback_days` (arXiv doesn't publish on weekends) |
| No repos matched topic filter | Broaden `topics` list or increase `fetch_pool_size` |
| Skill command not recognized | Confirm `SKILL.md` is in `.claude/skills/<skill-name>/SKILL.md` |
