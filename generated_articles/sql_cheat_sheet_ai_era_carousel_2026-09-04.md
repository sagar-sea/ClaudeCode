# SQL Cheat Sheet for the AI Era (LinkedIn Carousel)

**Created:** 2026-09-04
**Format:** LinkedIn Carousel (document post) — 12 slides, 1080×1350 (4:5 portrait)

**Files:**
- `carousels/sql_cheat_sheet_ai_era_carousel_2026-09-04.pdf` — upload directly to LinkedIn as a document post
- `carousels/sql_cheat_sheet_ai_era_carousel_2026-09-04.html` — editable source (Chrome → Print → Portrait, Margins **None**, Background graphics **ON**)
- `carousels/build_sql_cheat_sheet_carousel.py` — generator (edits copy + rebuilds the HTML, incl. SQL syntax highlighting)

**Re-render from the command line:**

```bash
chrome --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="sql_cheat_sheet_ai_era_carousel_2026-09-04.pdf" "sql_cheat_sheet_ai_era_carousel_2026-09-04.html"
```

---

## Differentiation vs. earlier SQL posts

| Prior piece | What it did | How this differs |
|---|---|---|
| `sql_fundamentals_ai_era_linkedin_2026-08-28.md` | Argued *that* SQL fundamentals still matter; a concept list (joins, windows, NULLs, GROUP BY, plans) | This is a **procedural cheat sheet**, not an argument: runnable diagnostic queries, a prompt template, a three-lane responsibility split, and a six-point ship checklist |
| `text_to_sql_accuracy_cliff_semantic_layer_linkedin_2026-09-02.md` | Benchmark cliff (Spider 1.0 vs 2.0) and semantic layers as the structural fix | Benchmark framing deliberately kept to **one qualitative line** — no repeat of the cliff numbers, no semantic-layer argument. Hook is DORA's verification tax instead |

Also aligned with the 2026-09-02 correction: the stale "21% / 10.1%" Spider 2.0 figures (late-2024 models) are **not** used anywhere in this deck.

---

## Design system

- **Palette:** ink `#0d1526`, body `#33415a`, accent blue `#2f5bea`, teal `#0e8177`, rose `#c8305c`, amber `#c07806`, soft `#f5f7fb`
- **Type:** Segoe UI (headlines 64px / 800, tight tracking), Consolas 22px for all code
- **Furniture:** 10px accent bar at slide top, dark footer strip with byline + `NN / 12` counter, accent-bordered "kicker" box pinned to the bottom of every slide
- **Code blocks:** dark navy panels with keyword / function / string / comment highlighting; every line kept under ~66 chars so nothing clips

---

## Slide-by-slide outline and copy

### Slide 1 — Cover (dark)
> **DATA & AI · PRACTICAL FIELD GUIDE**
> # SQL Cheat Sheet **for the AI Era**
> AI writes the first draft. You still own the number.
>
> Chips: Intent · Schema · Joins · NULLs · Aggregates · Windows · Performance · Privacy
> Sagar Rathkanthiwar — Data & AI Professional · *12 slides · save for later →*

### Slide 2 — The hook: the bottleneck moved
> ## The query runs. That doesn't make it right.
> - **90% use it · 30% don't trust it** — Nine in ten developers now work with AI. Nearly a third report little to no trust in the code it hands back (DORA).
> - **The verification tax** — DORA's finding: time saved writing gets spent auditing. AI raises the volume of code far faster than it raises your confidence in it.
> - **Your schema is the hard part** — On real enterprise warehouses rather than textbook databases, leading text-to-SQL systems still land well short of expert accuracy: undocumented columns and ambiguous join paths, not syntax.
>
> *Kicker:* The bottleneck moved from **writing** SQL to **checking** it. Everything after this slide is the checking part.

### Slide 3 — The frame: three lanes
> ## Split the work into three lanes
> - **ASK AI** — First drafts, dialect translation, boilerplate, alternate approaches, plain-English explanations of SQL you inherited.
> - **INSPECT YOURSELF** — Grain, keys, join cardinality, filter logic, date boundaries, and what the business actually means by "active customer."
> - **CATCH BEFORE SHIPPING** — Duplicated rows, NULL logic, averages at the wrong grain, unbounded scans, columns you shouldn't be reading.
>
> *Kicker:* AI is fast at SQL. You are accountable for the definition of **customer**, **active**, and **revenue**.

### Slide 4 — 01 · Intent
> ## Prompt the schema, not just the question
> *Weak prompt:* "Give me total revenue by customer."
>
> ```
> Tables + columns (with types):
>   orders(order_id PK, customer_id, order_ts, status, amount_usd)
>   refunds(refund_id PK, order_id FK, amount_usd)
>
> Grain I want:  one row per customer per month
> Revenue means: amount_usd minus refunds, excluding status='test'
> Dialect: Snowflake.  Window: last 12 full months.
>
> Write the query, then list every assumption you made.
> ```
>
> *Kicker:* **Catch:** an answer with no stated assumptions is an answer you have to reverse-engineer later. Make "list your assumptions" part of every prompt.

### Slide 5 — 02 · Schema
> ## Know the grain before you trust the join
> **Grain = what one row means.** Most wrong numbers are grain mistakes, not syntax mistakes — and the model can't see your data, only its names.
>
> ```sql
> -- 1. Is this column actually a key?
> SELECT COUNT(*) AS rows_total,
>        COUNT(DISTINCT order_id) AS distinct_ids
> FROM orders;              -- the two must match
>
> -- 2. Will this child table fan out my rows?
> SELECT order_id, COUNT(*) AS n
> FROM refunds
> GROUP BY order_id
> HAVING COUNT(*) > 1
> LIMIT 20;                 -- any result means one-to-many
> ```
>
> *Kicker:* **Ask AI:** "What grain does this query return, and which column makes it unique?" Then prove it with the two queries above.

### Slide 6 — 03 · Joins
> ## Duplicates don't announce themselves
> A one-to-many join silently multiplies rows — and every **SUM** that comes after it.
>
> ```sql
> -- WRONG: each order is counted once per refund row
> SELECT o.customer_id, SUM(o.amount_usd) AS revenue
> FROM orders o
> JOIN refunds r ON r.order_id = o.order_id
> GROUP BY 1;
>
> -- RIGHT: collapse the child table to the join grain first
> SELECT o.customer_id,
>        SUM(o.amount_usd) - SUM(COALESCE(r.refunded,0)) AS net_rev
> FROM orders o
> LEFT JOIN (SELECT order_id, SUM(amount_usd) AS refunded
>            FROM refunds GROUP BY order_id) r
>        ON r.order_id = o.order_id
> GROUP BY 1;
> ```
>
> *Kicker:* **Guard:** row count before the join should equal row count after. If it grew, you owe yourself an explanation — not a `DISTINCT`.

### Slide 7 — 04 · NULLs
> ## NULL isn't a value. It's "unknown."
> - `x = NULL` **is never true** — use `IS NULL`. Comparisons against unknown return unknown, not false.
> - `NOT IN (subquery)` **returns zero rows** if that subquery contains a single NULL. Use `NOT EXISTS` instead.
> - `COUNT(col)` **skips NULLs**, `COUNT(*)` doesn't. `AVG(col)` divides by the non-NULL count only.
> - **A LEFT JOIN plus a WHERE filter on the right table** quietly becomes an INNER JOIN. Move that filter into the `ON` clause.
>
> ```sql
> -- Safe anti-join: customers with no orders
> SELECT c.customer_id
> FROM customers c
> WHERE NOT EXISTS (SELECT 1 FROM orders o
>                   WHERE o.customer_id = c.customer_id);
> ```
>
> *Kicker:* **Catch:** ask AI "what happens here if this column is NULL?" — then test it with a row that actually is.

### Slide 8 — 05 · Aggregates
> ## Check the math, not just the output
> - **WHERE filters rows, HAVING filters groups.** Moving a row filter into HAVING changes the answer.
> - **An average of averages is not an average.** Re-aggregate from base rows, weighted properly.
> - **COUNT(DISTINCT user_id) is a different question** than COUNT(*). Decide which one you were asked.
> - **Empty groups vanish.** If "0 orders in July" must appear, join a date spine.
>
> ```sql
> SELECT d.month,
>        COUNT(DISTINCT o.customer_id) AS buyers,
>        COALESCE(SUM(o.amount_usd), 0) AS revenue
> FROM date_spine d
> LEFT JOIN orders o
>        ON DATE_TRUNC('month', o.order_ts) = d.month
>       AND o.status <> 'test'   -- filter goes in ON, not WHERE
> GROUP BY 1
> ORDER BY 1;
> ```
>
> *Kicker:* **Catch:** if a total looks too round or too small, check the filters before you check the data. Most "missing revenue" is a WHERE clause.

### Slide 9 — 06 · Window functions
> ## Rank, dedupe and compare without collapsing rows
> Window functions keep every row and add context. GROUP BY collapses them. Know which one you actually asked for.
>
> ```sql
> -- Latest order per customer (deterministic dedupe)
> SELECT * FROM (
>   SELECT o.*,
>          ROW_NUMBER() OVER (PARTITION BY customer_id
>            ORDER BY order_ts DESC, order_id DESC) AS rn
>   FROM orders o
> ) ranked
> WHERE rn = 1;
>
> -- Month over month change
> SELECT month, revenue,
>        revenue - LAG(revenue) OVER (ORDER BY month) AS mom_delta
> FROM monthly_revenue;
> ```
>
> *Kicker:* **Catch:** ties. Without a tiebreaker in ORDER BY, "latest" can change between runs. And `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` is a business decision, not a style choice.

### Slide 10 — 07 · Performance
> ## Correct and expensive is still a problem
> - **Read the plan, not the vibes.** `EXPLAIN` / `EXPLAIN ANALYZE`, and check bytes scanned on cloud warehouses where you pay per scan.
> - **Keep predicates sargable.** `WHERE order_ts >= '2026-01-01'` can use an index or partition; `WHERE YEAR(order_ts) = 2026` usually can't.
> - **Filter partition and cluster keys early**, and stop selecting `*` from tables that run to hundreds of columns.
> - **Treat a stray DISTINCT as a smell.** It's often patching a fan-out join instead of fixing it.
>
> *Kicker:* **Ask AI:** "Rewrite this to scan fewer partitions and explain the tradeoff." Then read the plan yourself — cost estimates are the one thing the model genuinely cannot see.

### Slide 11 — 08 · Security & privacy
> ## Review what the query exposes
> - **Never concatenate user input into SQL.** Parameterize. A generated f-string that "works" is an injection waiting for its first quote character.
> - **Least privilege by default.** Analysis runs on a read-only role. Write credentials don't belong in a notebook or an agent's environment.
> - **Don't paste real PII or secrets into a prompt** to "help it understand the data." Share column names, types and synthetic rows instead.
> - **Query only what you're entitled to** — prefer masked or governed views, and re-check access before sharing an export.
> - **No UPDATE or DELETE** until you've run the identical predicate as a SELECT, inside a transaction you can roll back.
>
> *Kicker:* **Catch:** generated SQL inherits whatever access you hand it. The model has no idea which of your columns are regulated — that judgement is entirely yours.

### Slide 12 — Ship checklist + CTA
> ## Six checks before you trust the number
> 1. **Row counts** are sane before and after every join.
> 2. **Grain matches the ask** — one row per ______.
> 3. **Three records traced end-to-end** back to the source system.
> 4. **Totals reconcile** with a known report or last month's figure.
> 5. **Edge cases handled**: no orders, refunds only, NULLs, future dates.
> 6. **Re-run is stable** — same input, same output, no random ties.
>
> **Save this, then run check #1 on the query you shipped yesterday.**
> Follow **Sagar Rathkanthiwar** for practical Data & AI
>
> *Sources:* DORA, State of AI-assisted Software Development & ROI of AI-assisted Software Development (dora.dev) · Spider 2.0 enterprise text-to-SQL benchmark and leaderboards (spider2-sql.github.io, arXiv 2411.07763). SQL behaviour described here is standard-SQL; syntax details vary by dialect.

---

## LinkedIn post caption

AI can write a query in three seconds. It cannot tell you whether the number is right.

That's not a knock on the tools — it's where the job moved. DORA's research calls it the verification tax: the time you save generating code comes back as time spent auditing it. Nine in ten developers now work with AI; close to a third say they have little or no trust in what it produces. Both of those things are true at once, and SQL is where it bites hardest, because a wrong query doesn't throw an error. It returns a number, and the number goes in the deck.

So I put together a cheat sheet for the part nobody prompts their way out of: reviewing.

12 slides, three lanes — what to ask AI, what to inspect yourself, and the mistakes to catch before you ship:

→ Prompting the schema and the grain, not just the question
→ Proving a column is actually a key (two queries, ten seconds)
→ Fan-out joins that silently multiply every SUM after them
→ NULL semantics: NOT IN, COUNT(col), and the LEFT JOIN that quietly turns INNER
→ WHERE vs HAVING, averages of averages, groups that vanish
→ Window functions, deterministic dedupe, and tie-breaking
→ Sargable predicates and reading the plan instead of the vibes
→ Injection, least privilege, and what not to paste into a prompt
→ A six-point checklist before you trust the number

Useful whether you're writing your first SELECT or reviewing someone else's — or an AI's.

Save it, then run check #1 on the query you shipped yesterday. Row count before the join, row count after. If it grew and you can't say why, you just found something.

What's the check you never skip? I'm collecting them.

---
Sources: DORA — State of AI-assisted Software Development / ROI of AI-assisted Software Development | https://dora.dev/ · Spider 2.0 | https://spider2-sql.github.io/
Research date: 2026-09-04

#SQL #DataEngineering #DataAnalytics #Analytics #DataScience #AIEngineering #TechLeadership #CodeReview
