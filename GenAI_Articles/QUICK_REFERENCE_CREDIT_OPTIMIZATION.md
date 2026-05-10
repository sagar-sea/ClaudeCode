# Quick Reference: Credit-Optimized Workflow

## 🎯 Target Credit Usage

| Format | Target | Max Searches | Max Fetches | Fetch Mode |
|--------|--------|--------------|-------------|------------|
| Twitter/X | 1-2 | 1-2 | 0-1 | truncated |
| LinkedIn | 2-3 | 2-3 | 1-2 | truncated |
| Medium | 4-6 | 3-4 | 3-4 | truncated/selective |
| Briefing | 1-2 | 2-3 | 1-2 | truncated |

---

## ⚡ The 3 Golden Rules

### 1. **Snippets First, Fetch Last**
- Web search results include 2-3 sentence snippets
- Analyze 20+ snippets before fetching anything
- For LinkedIn/Twitter, snippets are usually enough
- Only fetch when you need specific quotes or details

### 2. **Truncated by Default**
- Default: `mode: "truncated"` (8KB preview)
- Selective: When you need specific section
- Full: Only for primary sources (rare)
- **Never fetch more than 3 articles per task**

### 3. **Skip Steps for Short-Form**
- Twitter/LinkedIn: Skip content history, scoring, explanation
- Use informal ranking: "Would engineers care?"
- Pick top 3-5 items by judgment

---

## 📋 Step-by-Step Checklist

### Before Starting:
- [ ] Identify content type (Twitter/LinkedIn/Medium)
- [ ] Note credit budget (1-2 / 2-3 / 4-6)
- [ ] Set research limits (searches/fetches)

### During Research (Step 2):
- [ ] Start with 2-3 web searches
- [ ] Analyze all snippets first
- [ ] Only fetch if snippets insufficient
- [ ] Use `mode: "truncated"` or `"selective"`
- [ ] Stop at your fetch limit

### During Filtering (Step 3):
- [ ] Twitter/LinkedIn: Skip formal scoring
- [ ] Use informal ranking
- [ ] Pick top 3-5 items
- [ ] Medium: Use simplified scoring

### During Creation (Steps 5-8):
- [ ] Twitter/LinkedIn: Skip topic explanation
- [ ] Generate directly from research
- [ ] Batch all file operations

---

## 🚨 Red Flags (You're Wasting Credits)

❌ Fetching 5+ articles
❌ Using `mode: "full"` by default
❌ Reading full content history every time
❌ Detailed scoring for LinkedIn/Twitter
❌ Topic explanation for short-form
❌ Ignoring search snippets

---

## ✅ Green Flags (You're Optimized)

✅ Analyzing snippets before fetching
✅ Using `mode: "truncated"` by default
✅ Fetching 1-2 articles max for LinkedIn
✅ Skipping unnecessary steps
✅ Informal ranking for short-form
✅ Staying within credit budget

---

## 🔧 Quick Fixes

**If credits are too high:**

1. **Check fetch count**: Should be 1-2 for LinkedIn, 0-1 for Twitter
2. **Check fetch mode**: Should be "truncated" not "full"
3. **Check snippet usage**: Did you analyze them first?
4. **Check steps**: Did you skip scoring/explanation for short-form?

**Most common issue**: Fetching too many full articles

---

## 💡 Pro Tips

1. **Search snippets are gold**: They contain title, URL, 2-3 sentences, date, domain
2. **One good fetch > five mediocre ones**: Quality over quantity
3. **Trust your judgment**: For short-form, informal ranking is fine
4. **Batch operations**: Group file reads/writes together
5. **Skip when possible**: Not every step is needed for every format

---

## 📊 Success Metrics

After each task, check:
- **Credits used**: Within target range?
- **Fetch count**: Within limits?
- **Fetch modes**: Mostly truncated?
- **Steps skipped**: Appropriate for format?

**Target Achievement:**
- Twitter: 1-2 credits ✅
- LinkedIn: 2-3 credits ✅
- Medium: 4-6 credits ✅

---

## 🎓 Remember

**The workflow is a guide, not a prison.**

For short-form content:
- Less research is fine
- Informal ranking is fine
- Skipping steps is fine
- Trust your judgment

For long-form content:
- More research is justified
- Formal scoring helps
- Full workflow makes sense
- But still optimize fetches!

---

## 📞 Quick Troubleshooting

**Q: My LinkedIn post took 9 credits. Why?**
A: Probably fetched 5+ full articles. Use snippets + 1-2 truncated fetches.

**Q: Can I skip content history?**
A: Yes, for Twitter/general topics. Use grepSearch for specific topics.

**Q: When should I use mode: "full"?**
A: Rarely. Only for primary sources when truncated is insufficient.

**Q: How many snippets should I analyze?**
A: 15-20 from 2-3 searches is usually enough for LinkedIn.

**Q: Is informal ranking okay?**
A: Yes! For Twitter/LinkedIn, "would engineers care?" is sufficient.

---

**Remember: 60-70% credit savings is achievable with these simple changes!**
