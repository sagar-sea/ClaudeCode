# Credit Optimization Guide for GenAI Research Workflow

## 🎯 Quick Reference: Expected Credit Usage

| Content Type | Current Usage | Optimized Usage | Savings |
|--------------|---------------|-----------------|---------|
| Twitter/X Thread | 8-10 credits | 1-2 credits | 80% |
| LinkedIn Post | 9-10 credits | 2-3 credits | 70% |
| Medium Article | 12-15 credits | 4-6 credits | 60% |
| Info Briefing | 5-7 credits | 1-2 credits | 70% |

---

## 📋 Key Optimization Strategies

### 1. **Snippet-First Research** (Saves 40% credits)

**Problem**: Fetching 5+ full articles at 15K+ bytes each
**Solution**: Leverage search result snippets before fetching

```markdown
✅ GOOD APPROACH:
1. Run 2-3 web searches
2. Analyze 20+ snippets from results (essentially free)
3. Only fetch 1-2 articles if snippets lack details
4. Use mode: "truncated" or "selective" (never "full" by default)

❌ BAD APPROACH:
1. Run web searches
2. Immediately fetch 5 full articles with mode: "full"
3. Process 75K+ bytes of content
```

**Web search snippets include:**
- Title
- URL
- 2-3 sentences of content
- Published date
- Domain

**For LinkedIn/Twitter, snippets are usually sufficient!**

---

### 2. **Content-Type Specific Limits** (Saves 20% credits)

**Twitter/X Threads:**
- Web Searches: 1-2 max
- Article Fetches: 0-1 max
- Collection Target: 3-5 items
- Skip: Content history, detailed scoring, topic explanation

**LinkedIn Posts:**
- Web Searches: 2-3 max
- Article Fetches: 1-2 max
- Collection Target: 5-8 items
- Skip: Detailed scoring (Step 3A), topic explanation (usually)

**Medium Articles:**
- Web Searches: 3-4 max
- Article Fetches: 3-4 max
- Collection Target: 8-12 items
- Use: Simplified scoring, brief explanation

---

### 3. **Conditional Content History** (Saves 5% credits)

**Current**: Always read full content_history.md file
**Optimized**: Conditional reading

```markdown
SKIP content history for:
- Twitter/X threads (rarely need duplicate checking)
- General topics
- When user doesn't mention avoiding duplicates

USE grepSearch instead of full file read:
grepSearch(query="LangChain|LangGraph", includePattern="content_history.md")

ONLY read full file when:
- User explicitly requests duplicate avoidance
- Very specific topic with high duplicate risk
```

---

### 4. **Simplified Scoring** (Saves 15% credits)

**For Short-Form Content (Twitter, LinkedIn):**

**Current Approach:**
- Collect 15-25 items
- Apply detailed scoring (recency + authority + impact)
- Track metadata for each item
- Formal ranking process

**Optimized Approach:**
- Collect 5-8 items
- Skip Step 3A (Hard Signal Filter) entirely
- Informal ranking: "Would an engineer care?"
- Pick top 3-5 by gut feel

**For Long-Form Content (Medium):**
- Collect 8-12 items (not 15-25)
- Apply simplified scoring
- Focus on top 8 items

---

### 5. **Fetch Mode Guidelines** (Saves 20% credits)

**Default Modes by Use Case:**

| Scenario | Mode | Reason |
|----------|------|--------|
| Initial exploration | `truncated` | 8KB preview sufficient |
| Need specific section | `selective` | Target exact content |
| Primary source only | `full` | When truncated insufficient |
| LinkedIn/Twitter | `truncated` or skip | Snippets usually enough |

**Rules:**
- **Never** use `mode: "full"` as default
- **Never** fetch more than 3 full articles per task
- **Always** try snippets first

---

### 6. **Skip Unnecessary Steps** (Saves 15% credits)

**Steps to Skip by Content Type:**

**Twitter/X Threads - Skip:**
- Step 0: Content history check
- Step 3A: Hard Signal Filter
- Step 7: Topic explanation
- Detailed tracking in Step 2

**LinkedIn Posts - Skip:**
- Step 3A: Hard Signal Filter (use informal ranking)
- Step 7: Topic explanation (unless complex)
- Detailed tracking in Step 2

**Medium Articles - Skip:**
- None (but simplify Step 3A)

---

### 7. **Batch Operations** (Saves 10% credits)

**Use:**
- `readMultipleFiles` instead of multiple `readFile` calls
- Group all file writes at the end
- Combine related operations in single turns

---

## 🔧 Implementation: Quick Changes to Make

### Change 1: Add Credit Budget Mode to Step 1

```markdown
### 1. Unified Assessment Phase

Determine from user response:
1. Pathway
2. Specific Interests
3. Target Format
4. **🆕 Credit Budget Mode** (auto-set based on format):
   - Twitter/X: Low (1-2 credits)
   - LinkedIn: Medium (2-3 credits)
   - Medium: High (4-6 credits)
```

### Change 2: Add Research Limits to Step 2

```markdown
### 2. Research Phase

**🆕 RESEARCH LIMITS BY CONTENT TYPE:**

For LinkedIn Posts:
- Web Searches: 2-3 maximum
- Article Fetches: 1-2 maximum (use mode: "truncated")
- Collection Target: 5-8 items
- Leverage snippets first!

[Add similar blocks for other content types]
```

### Change 3: Simplify Step 3 for Short-Form

```markdown
### 3. Hard Signal Filter & Ranking

**🆕 FOR TWITTER/LINKEDIN: SKIP STEP 3A ENTIRELY**

Instead:
1. Review your 5-8 collected items
2. Pick top 3-5 most relevant to engineers
3. Use informal ranking - trust your judgment
4. No formal scoring needed

**FOR MEDIUM ARTICLES: Use standard scoring**
[Keep existing Step 3A/3B]
```

### Change 4: Add Skip Rules to Step 7

```markdown
### 7. Topic Explanation Phase

**🆕 SKIP FOR SHORT-FORM:**
- Twitter/X: Always skip, go to Step 8
- LinkedIn: Skip unless highly technical
- Medium: Brief explanation (2-3 paragraphs max)
```

---

## 📊 Credit Savings Breakdown

| Optimization | Credit Savings | Difficulty | Priority |
|--------------|---------------|------------|----------|
| Snippet-first research | 40% | Easy | HIGH |
| Fetch mode optimization | 20% | Easy | HIGH |
| Simplified scoring | 15% | Easy | HIGH |
| Skip unnecessary steps | 15% | Medium | MEDIUM |
| Conditional history check | 5% | Easy | MEDIUM |
| Batch operations | 10% | Medium | LOW |
| **TOTAL POTENTIAL** | **60-70%** | - | - |

---

## 🚀 Quick Start: Apply These 3 Changes First

### Priority 1: Snippet-First Research
- Always analyze search snippets before fetching
- Only fetch when snippets insufficient
- Use `mode: "truncated"` by default

### Priority 2: Content-Type Limits
- Set max searches/fetches based on format
- Twitter: 1-2 searches, 0-1 fetch
- LinkedIn: 2-3 searches, 1-2 fetches
- Medium: 3-4 searches, 3-4 fetches

### Priority 3: Skip Scoring for Short-Form
- Twitter/LinkedIn: Skip Step 3A entirely
- Use informal "would engineers care?" ranking
- Pick top 3-5 items by judgment

**These 3 changes alone will save 50-60% of credits.**

---

## 📝 Example: Optimized LinkedIn Post Workflow

**Old Workflow (9.85 credits):**
1. Read full content history
2. 3 web searches
3. Fetch 5 full articles (mode: "full")
4. Detailed scoring of 15+ items
5. Topic explanation
6. Generate content
7. Verification loop with more fetches

**New Workflow (2-3 credits):**
1. Skip content history (or use grepSearch)
2. 2 web searches
3. Analyze 20 snippets
4. Fetch 1-2 articles (mode: "truncated")
5. Informal ranking of 5-8 items
6. Skip topic explanation
7. Generate content directly

**Savings: 70% (7 credits)**

---

## 🎓 Training Your Workflow

Add this section at the top of your workflow file:

```markdown
## CREDIT EFFICIENCY MODE

Before starting any task, determine credit budget:
- Twitter/X: 1-2 credits (minimal research)
- LinkedIn: 2-3 credits (focused research)
- Medium: 4-6 credits (comprehensive research)

Then apply appropriate limits:
- Research: [X] searches, [Y] fetches
- Scoring: Simplified/Full
- Steps to skip: [List]
```

---

## ✅ Checklist: Is Your Workflow Optimized?

- [ ] Using snippet-first research approach
- [ ] Set content-type specific limits
- [ ] Using `mode: "truncated"` by default
- [ ] Skipping Step 3A for short-form content
- [ ] Conditional content history checks
- [ ] Skipping topic explanation for Twitter/LinkedIn
- [ ] Never fetching more than 3 full articles
- [ ] Batching file operations
- [ ] Analyzing snippets before fetching

**If you checked 7+, you're optimized!**

---

## 🔍 Monitoring Credit Usage

After each task, note:
- Content type created
- Credits consumed
- Number of web searches
- Number of article fetches
- Fetch modes used

Target ranges:
- Twitter: 1-2 credits ✅
- LinkedIn: 2-3 credits ✅
- Medium: 4-6 credits ✅

If exceeding targets, review which optimization you missed.

---

## 📞 Need Help?

If credit usage is still high:
1. Check how many full article fetches you're doing
2. Verify you're using snippets first
3. Confirm you're skipping unnecessary steps
4. Review fetch modes (should be mostly "truncated")

**Most common issue**: Fetching too many full articles instead of using snippets.
