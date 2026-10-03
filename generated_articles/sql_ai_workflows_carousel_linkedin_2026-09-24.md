# SQL's New Job in the AI Era: Powering Reliable AI Workflows

**Format:** LinkedIn carousel (10 slides, 1080 × 1350 portrait)
**Date:** 2026-09-24
**PDF:** `generated_articles/carousels/sql_ai_workflows_carousel_2026-09-24.pdf`
**Source:** `generated_articles/carousels/build_sql_ai_workflows_carousel.py` → `..._2026-09-24.html`
**Audience:** Analysts, analytics engineers, data engineers, data scientists, AI engineers, product managers, technical leaders
**Dedup note:** Avoids prior SQL topics (joins/grain, window functions, NULLs, grouping, CTEs, indexing, query plans, date/time, SQL safety, AI-query review). Slide 9 touches the semantic layer (covered in the 2026-09-02 text-to-SQL post) but frames it as metric ownership inside AI workflows, not text-to-SQL accuracy.

**Design system:** Editorial serif headlines (Georgia) + Segoe UI body, warm paper background. Every diagram color-codes who does the work: **SQL** (teal), **Vector/Search** (blue), **LLM** (violet), **App code** (slate), **Human** (amber).

---

## Slide-by-slide copy

### Slide 1 — Cover
**Eyebrow:** SQL × AI · FIELD GUIDE
**Title:** SQL's New Job in the **AI Era**
**Subtitle:** How the language behind dashboards is powering reliable AI workflows.
**Diagram:** Warehouse (orders · tickets · usage · CRM) → **SQL** (context · metrics · governance) → AI product (assistant · agent · copilot). Logs, feedback and outcomes flow back into SQL.
**Chips:** Trusted context · Data profiles · Observability · Quality evals · Experiments · Human review · Governance · Semantic layer
**Footer:** Sagar Rathkanthiwar, Data & AI Professional · 10 slides · save for later →

### Slide 2 — Trusted context for AI
**Headline:** Decide what the model sees, before it sees it
**Lead:** A support assistant drafting a reply for one customer doesn't need the warehouse. It needs *their* recent orders and open tickets, and nothing that belongs to anyone else.
**Pipeline:**
1. [SQL] **Scope**: this customer only, last 90 days, rows the requesting agent is allowed to see.
2. [SQL] **Clean & shape**: dedupe orders, drop test accounts, pick 12 useful columns instead of 80.
3. [VECTOR / SEARCH] **Retrieve policy text**: find the refund-policy passages that match the question by meaning.
4. [APP CODE] **Assemble the prompt**: template + SQL context + retrieved passages, within a token budget.
5. [LLM] **Draft the reply**: language, tone, summarisation.
6. [HUMAN] **Approve & send**: the agent owns what the customer receives.

**SQL is the right tool for:** exact filters, joins across systems, freshness checks, permission scoping, reproducible inputs you can audit later.
**SQL is not the tool for:** ranking free text by meaning, writing the reply, or deciding whether a reply is appropriate to send.
**Kicker:** The cheapest hallucination fix is better input. Every wrong row in the context is a fact the model will confidently repeat.

### Slide 3 — AI-ready data profiles
**Headline:** Compress each customer into one row a model can read
**Snippet 1: Compact customer context**
```sql
-- One compact, refreshable context record per customer
CREATE VIEW ai_customer_profile AS
SELECT
  c.customer_id,
  c.plan_tier,
  c.account_status,
  (SELECT SUM(o.amount) FROM orders o
    WHERE o.customer_id = c.customer_id)      AS lifetime_value,
  (SELECT MAX(o.ordered_at) FROM orders o
    WHERE o.customer_id = c.customer_id)      AS last_order_at,
  (SELECT COUNT(*) FROM product_events e
    WHERE e.customer_id = c.customer_id
      AND e.event_at >= CURRENT_DATE - 30)    AS events_30d,
  (SELECT COUNT(*) FROM support_tickets t
    WHERE t.customer_id = c.customer_id
      AND t.status = 'open')                  AS open_tickets
FROM customers c;
```
**What the assistant receives:** `{ plan_tier: "Pro", account_status: "active", lifetime_value: 4820, last_order_at: "2026-09-18", events_30d: 212, open_tickets: 1 }`
- **~60 tokens** instead of hundreds of raw order and event rows.
- **SQL does the arithmetic.** LLMs are unreliable at summing rows; they're good at explaining a number.
- **Materialise & refresh** on a schedule; add a `refreshed_at` stamp.

**Kicker:** Compute the facts in SQL. Let the model explain them, not invent them.

### Slide 4 — Prompt and model observability
**Headline:** Log every AI call. Query it like any fact table.
**Diagram:** [APP CODE] Your app → [LLM] Model API → [SQL] `ai_request_log` (one row per call)
**Columns:** request_id · feature · prompt_version · model_version · input_tokens · output_tokens · latency_ms · cost_usd · status · feedback
**Snippet 2: Daily cost / quality monitor**
```sql
-- Daily cost, latency and quality by model + prompt version
SELECT
  CAST(created_at AS DATE)                   AS day,
  model_version,
  prompt_version,
  COUNT(*)                                   AS requests,
  SUM(cost_usd)                              AS cost_usd,
  AVG(latency_ms)                            AS avg_latency_ms,
  AVG(CASE WHEN status = 'error' THEN 1.0 ELSE 0 END) AS error_rate,
  AVG(CASE WHEN feedback = 'up'   THEN 1.0
           WHEN feedback = 'down' THEN 0.0 END)     AS thumbs_up_rate
FROM ai_request_log
WHERE created_at >= CURRENT_DATE - 14
GROUP BY CAST(created_at AS DATE), model_version, prompt_version
ORDER BY day DESC, cost_usd DESC;
```
**Questions this answers:** Which prompt version doubled cost? · Did the new model slow responses? · Where are errors spiking?
**Kicker:** Averages hide pain, so add p95 latency with your warehouse's percentile function. Logged prompts can also contain PII, so redact them and set retention like any customer data.

### Slide 5 — Quality evaluation at scale
**Headline:** Turn scattered feedback into a quality scorecard
**Lead:** Join four signals on `request_id`: user thumbs, human review labels, ticket outcomes, and confirmed hallucination tags. Then slice by intent.
**Diagram:** [APP] User thumbs · [HUMAN] Review labels · [APP] Ticket outcomes · [HUMAN] Hallucination tags → [SQL] Scorecard

| Support intent | Convos | Thumbs-up | Reviewed | Halluc. tag | Resolved, no escalation |
|---|---|---|---|---|---|
| Order status | 4,210 | 88% | 312 | 0.6% | 81% |
| Product how-to | 6,870 | 83% | 402 | 1.2% | 74% |
| Account access | 980 | 70% | 188 | 2.1% | 55% |
| **Billing dispute** | **1,145** | **61%** | **290** | **3.8%** | **42%** |

*Illustrative numbers. The overall average (~80% thumbs-up) looks healthy. The billing segment is where the assistant is failing.*
**SQL does:** aggregates, trends by version, segment slices, and stratified samples so reviewers see hard cases, not just easy ones.
**SQL can't:** judge whether an answer was actually correct. That takes human reviewers, or an LLM judge calibrated against them.
**Kicker:** Thumbs are biased: few users vote, and unhappy ones vote more. SQL won't tell you an answer was wrong. It tells you where to look, and whether it's improving.

### Slide 6 — Experiment analysis
**Headline:** Ship prompt v2 like a product change, not a vibe check
**Diagram:** Users randomly assigned → A (Model X · prompt v1) / B (Model Y · prompt v2) → assignments + outcome events → SQL scorecard

| Sales-assistant metric | A · v1 | B · v2 | Change |
|---|---|---|---|
| Adoption (reps who used it) | 34% | 37% | +3 pts |
| Task completion | 71% | 76% | +5 pts |
| Satisfaction (1–5) | 4.1 | 4.2 | +0.1 |
| Escalated to a human | 18% | 14% | −4 pts |
| Cost per completed task | $0.042 | $0.061 | +45% |

*Illustrative numbers.*
- **Analyse by assigned variant**, not by who happened to use the feature.
- **Check the split.** A 50/50 test that lands at 56/44 means broken assignment.
- **SQL builds the inputs;** the significance test belongs in a stats library or notebook.
- **Segment the result** (new vs tenured reps, small vs large deals). An average win can hide a segment loss.
- **+5 pts completion for +45% cost** is a business trade-off. Humans decide it.

**Kicker:** The winner isn't the variant that *feels* smarter. It's the one that clears your quality bar at a cost you'll accept at scale.

### Slide 7 — Human-in-the-loop workflows
**Headline:** Use SQL to decide which drafts a person must see
**Snippet 3: Route for human review**
```sql
-- Route risky AI drafts to a human review queue
INSERT INTO review_queue (response_id, reason)
SELECT response_id, reason
FROM (
  SELECT
    r.response_id,
    CASE
      WHEN r.topic IN ('legal', 'refund_over_limit') THEN 'high_risk_topic'
      WHEN r.confidence < 0.70                     THEN 'low_confidence'
      WHEN a.tier = 'enterprise'
       AND r.sentiment = 'negative'                THEN 'key_account'
      WHEN r.cost_usd > 0.50                       THEN 'expensive_request'
    END AS reason
  FROM ai_responses r
  JOIN accounts a ON a.account_id = r.account_id
  WHERE r.status = 'draft'
) flagged
WHERE reason IS NOT NULL;
```
**Diagram:** [LLM] AI draft → [SQL] Routing rules → [HUMAN] Review queue → [SQL] Decisions logged
- **"Confidence" is whatever your app produces**, such as a classifier score or a model self-rating. It is a signal, not a guarantee.
- **Calibrate thresholds with SQL:** how often did reviewers actually change a `low_confidence` draft?
- **Real-time routing often lives in app code.** SQL is where you design, backtest and audit the rules.

### Slide 8 — Data governance and access
**Headline:** An AI tool should never get every column

| customers column | AI assistant gets |
|---|---|
| customer_id | Yes |
| plan_tier | Yes |
| region | Row filter |
| email | Masked (j***@acme.com) |
| phone | Excluded |
| date_of_birth | Excluded |
| internal_notes | Excluded |

- **Least-privilege views:** grant the AI service account a purpose-built view, never base tables.
- **Row-level security:** the assistant inherits the *end user's* access, so an EMEA agent sees EMEA customers.
- **Masking:** mask or tokenise PII at the column; don't hope the model ignores it.
- **Auditability:** log which identity queried what and when, and join it to the AI request log.

**Same idea, different syntax:** PostgreSQL row-level security · SQL Server RLS & dynamic data masking · Snowflake row access & masking policies · BigQuery authorized views & policy tags.
**Warning box:** A prompt that says "don't reveal emails" is not access control. Instructions can be ignored or bypassed by prompt injection. Permissions enforced in the database can't be talked out of.
**Kicker:** Rule of thumb: if a column would be a problem in a screenshot, it's a problem in a prompt.

### Slide 9 — The semantic layer matters
**Headline:** One definition of "active," before AI answers anything
**Lead:** "How many active customers do we have?" Three teams, three honest answers:

| Team | "Active customer" means | Answer |
|---|---|---|
| Marketing | Logged in during the last 30 days | 18,400 |
| Finance | Paid an invoice in the last 90 days | 11,250 |
| Product | ≥ 3 key actions in the last 28 days | 7,900 |

*Illustrative numbers. The same trap hides in every business noun:*
- **"Resolved ticket":** closed by an agent? Or closed *and* not reopened within 7 days?
- **"Qualified lead":** filled in a form? Or matches the ideal-customer profile *and* accepted by sales?

**Diagram:** [LLM] Maps the question to a named metric → [SQL] Governed metric (one definition, owner, version) → [APP CODE] Answer + definition cited back to the user
- **Metric owners (humans)** agree the definition; the semantic layer or governed views encode it once.
- **The LLM translates language to metric names.** It should not re-derive the business logic on every question.

**Kicker:** AI doesn't resolve ambiguity in your metrics. It automates it, at the speed of chat.

### Slide 10 — Closing CTA
**Headline:** AI makes answers faster. **SQL makes the inputs, measurements, and decisions trustworthy.**
**Who does what:**
- **SQL:** select, measure, govern. Trusted context, cost and quality metrics, access rules, one metric definition.
- **Vector / Search:** find relevant unstructured text (policies, docs, past tickets) by meaning.
- **LLM:** understand and generate language. Summarise, draft, classify, translate intent.
- **App code:** orchestrate and enforce in real time. Prompts, retries, routing, guardrails.
- **Human:** define, judge, decide. Metric definitions, quality calls, trade-offs, accountability.

**CTA:** Where could SQL make your AI workflow more reliable?
Share your most valuable SQL-for-AI use case in the comments, and save this for your next AI project review.
**Implementation note:** Table names are generic and the examples use broadly portable SQL. Date arithmetic, percentile functions, row-level security, masking policies and semantic-layer tooling differ across PostgreSQL, SQL Server, Snowflake, BigQuery, Databricks and others. Details vary by warehouse and product architecture.

---

## LinkedIn caption

SQL isn't being replaced by AI. Its job is getting bigger.

Every week I see AI demos that look great, then struggle in production. The model is rarely the problem. The trouble is almost always upstream or downstream of it:

→ The assistant got the wrong context, or too much of it
→ Nobody could say what the new prompt version cost, or whether it was better
→ "Active customer" meant three different things depending on who asked
→ The AI tool could see columns it never should have

Reliable AI needs three things: trusted context, measurable outcomes, and governed data. All three live where SQL already works.

This carousel walks through 8 practical jobs SQL does in AI workflows:

1. Scoping permission-aware context before anything reaches a model
2. Compressing customers into compact, AI-ready profiles
3. Monitoring cost, latency and errors by model and prompt version
4. Turning feedback and review labels into a quality scorecard
5. Analysing A/B tests of prompts and models
6. Routing risky or low-confidence outputs to a human
7. Enforcing least-privilege views, row-level security and masking
8. Giving every business metric one trusted definition

It also marks where SQL stops: finding text by meaning (vector search), writing language (LLM), real-time orchestration (app code), and judgement calls (people).

AI makes answers faster. SQL makes the inputs, measurements, and decisions trustworthy.

📌 Save this for your next AI project review.
💬 What's your most valuable SQL-for-AI use case? Share it in the comments.

#SQL #AI #DataEngineering #AnalyticsEngineering #MLOps #DataScience #GenerativeAI
