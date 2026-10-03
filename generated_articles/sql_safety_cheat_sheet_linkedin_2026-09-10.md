# Before You Run AI-Generated SQL: The SQL Safety Cheat Sheet

**Format:** LinkedIn carousel (10 slides, 1080 × 1350 portrait)
**Date:** 2026-09-10
**PDF:** `generated_articles/carousels/sql_safety_cheat_sheet_carousel_2026-09-10.pdf`
**Source:** `generated_articles/carousels/build_sql_safety_carousel.py` → `..._2026-09-10.html`
**Audience:** SQL beginners, analysts, analytics engineers, data engineers, developers, technical managers, AI-assisted professionals

---

## Slide-by-slide copy

### Slide 1 — Cover

**Eyebrow:** SQL SAFETY · CHEAT SHEET

**Title:** Before you run **AI-generated SQL.**

**Subtitle:** A safety cheat sheet for queries that can change, expose, or break data.

**Chips:** Read before you run · Command types · Preview first · Blast radius · Transactions · Least privilege · Parameterized inputs · Prod checklist

**Footer:** Sagar Rathkanthiwar — Data & AI Professional · 10 slides · save for later →

---

### Slide 2 — Read before you run

**Eyebrow:** 01 · THE FIRST HABIT
**Headline:** Plausible is not the same as safe

AI writes SQL that **parses, runs, and looks right**. What it cannot know is which environment you're connected to, which table is the real one, or what the business considers safe to touch.

- **Wrong environment** — the statement was fine; the connection was production.
- **Wrong object** — `orders` vs `orders_archive` vs `orders_v2`. The model guessed.
- **Wrong scope** — a filter that matches 4 rows in your head and 400,000 in the table.

| STOP | CHECK | RUN |
|---|---|---|
| Read the whole statement before it touches a connection. | Which database? Which objects? How many rows? Reversible? | Only once all three answers are known — not assumed. |

**Kicker:** **Stop → Check → Run.** Ten seconds of reading is cheaper than any restore you will ever do.

---

### Slide 3 — Know the command type

**Eyebrow:** 02 · COMMAND TYPES
**Headline:** Know what the first word can do to you

| Command | Risk | What it does |
|---|---|---|
| `SELECT` | Low | Reads only. Can still be slow or expose data. |
| `INSERT` | Medium | Adds rows. Can duplicate or violate constraints. |
| `UPDATE` | Medium | Overwrites values. The old ones are gone. |
| `DELETE` | High | Removes rows. Logged and usually reversible inside a transaction. |
| `MERGE` | Medium–High | Insert + update + delete in one. Hardest to review. |
| `CREATE` | Low | Adds an object. Low risk — unless it replaces one. |
| `ALTER` | High | Changes structure. Can lock tables and break downstream code. |
| `DROP` | High | Destroys the object and its data. Often not reversible. |
| `TRUNCATE` | High | Empties a table fast. Frequently non-transactional. |

**Kicker:** **DDL (`CREATE / ALTER / DROP / TRUNCATE`) behaves very differently by engine.** PostgreSQL can roll most of it back; MySQL and Oracle commit it implicitly the moment it runs. Verify yours — don't assume.

---

### Slide 4 — Preview before modifying

**Eyebrow:** 03 · PREVIEW FIRST
**Headline:** Turn every write into a read — first

Before running a write, run the **exact same filter** as a `SELECT`. Same table, same predicate, no edits.

```sql
-- 1. COUNT the blast radius
SELECT COUNT(*) FROM orders
WHERE status = 'pending' AND created_at < '2026-01-01';

-- 2. LOOK at real rows before trusting the filter
SELECT order_id, status, created_at FROM orders
WHERE status = 'pending' AND created_at < '2026-01-01'
LIMIT 20;

-- 3. Only now, with the SAME predicate, write
UPDATE orders SET status = 'expired'
WHERE status = 'pending' AND created_at < '2026-01-01';
```

**Kicker:** If the count surprises you, **the filter is wrong — not the data.** Some engines also let you see exactly which rows a write touched: `RETURNING` (PostgreSQL), `OUTPUT` (SQL Server).

---

### Slide 5 — Constrain the blast radius

**Eyebrow:** 04 · BLAST RADIUS
**Headline:** A missing `WHERE` updates everything

```sql
-- The most expensive typo in SQL:
UPDATE customers SET tier = 'gold';  -- every customer. all of them.
DELETE FROM orders;                  -- the whole table.

-- Constrain by key, by partition, by date, by batch:
UPDATE customers SET tier = 'gold'
WHERE customer_id IN (101, 102, 103);

DELETE FROM events
WHERE event_date >= '2026-01-01' AND event_date < '2026-02-01';
```

- **Confirm the environment first** — `SELECT CURRENT_DATABASE(), CURRENT_USER;` costs nothing.
- **Filter on the partition key** on large or columnar warehouses — it caps cost and damage at once.
- **Delete in batches** instead of one giant statement; long writes hold locks and stall production.
- **Engine note:** `LIMIT` on `UPDATE`/`DELETE` works in MySQL, but **not** in PostgreSQL or most warehouses — bound the predicate instead.

**Kicker:** Ask of every write: **"If this matched ten times more rows than I expect, what breaks?"**

---

### Slide 6 — Use transactions

**Eyebrow:** 05 · TRANSACTIONS
**Headline:** Give yourself an undo button

```sql
BEGIN;                             -- open the transaction

UPDATE orders SET status = 'expired'
WHERE status = 'pending' AND created_at < '2026-01-01';

-- VALIDATE inside the transaction, before you commit:
SELECT status, COUNT(*) FROM orders GROUP BY status;

COMMIT;    -- numbers look right? make it permanent
ROLLBACK;  -- numbers look wrong? undo everything since BEGIN
```

- **Verify your engine's behaviour.** Autocommit is on by default in many clients, and some tools commit each statement as it runs.
- **DDL is the exception.** MySQL and Oracle commit `CREATE`/`ALTER`/`DROP` implicitly — there's nothing left to roll back.
- **Don't leave it open.** An uncommitted transaction holds locks and can block everyone else.

**Kicker:** A transaction is not a substitute for a backup. **It protects the next five minutes, not the next five days.**

---

### Slide 7 — Protect sensitive data

**Eyebrow:** 06 · SENSITIVE DATA
**Headline:** The query ran fine. That's not the risk.

A `SELECT` can't corrupt a table — but it can move regulated data somewhere it was never approved to go.

```sql
-- RISKY: pulls every column, including ones you never asked for
SELECT * FROM customers;  -- email, dob, national_id, card_last4...

-- SAFER: name the columns, mask what you don't need in full
SELECT customer_id,
       LEFT(email, 2) || '***' AS email_hint,
       signup_date
FROM customers
WHERE signup_date >= '2026-01-01';
```

- **Least privilege** — analysts read from views, not base tables. Write access is granted, never assumed.
- **Never paste real PII, secrets or credentials into an AI prompt.** Share the schema, not the rows.
- **Exports are where data leaks** — a CSV in a downloads folder has left every control you have.

**Kicker:** `SELECT *` in a shared notebook or on a screen share is a **disclosure decision**, not a shortcut.

---

### Slide 8 — Parameterize inputs

**Eyebrow:** 07 · APPLICATION CODE
**Headline:** Never build SQL by gluing strings together

When AI generates **application** code, string-concatenated SQL is the classic injection hole: user input becomes executable syntax.

```python
# UNSAFE - the input becomes part of the statement
q = "SELECT * FROM users WHERE email = '" + user_input + "'"
#   user_input = "x' OR '1'='1"            -> returns every user
#   user_input = "x'; DROP TABLE users;--"  -> ends very badly

# SAFE - the value is sent separately from the SQL text
cur.execute(
    "SELECT id, email FROM users WHERE email = %s",
    (user_input,)
)
```

- Placeholders differ by driver (`%s`, `?`, `:name`) — the principle doesn't: **data is data, not syntax.**
- Table and column names can't be parameterized — validate them against an **allow-list**, never against user input.

**Kicker:** Ad-hoc analysis and shipped code are different risk classes. **Anything that accepts outside input must be parameterized** — no escaping by hand.

---

### Slide 9 — Production readiness checklist

**Eyebrow:** 08 · BEFORE PRODUCTION
**Headline:** The 8-point pre-flight check

Run this before any statement touches a production system — whoever, or whatever, wrote it.

1. **Environment** — confirmed dev, staging or prod. Say it out loud.
2. **Backup** — a recent snapshot, and a restore path you've tested.
3. **Peer review** — a second human has read the statement.
4. **Expected rows** — you predicted the count before running it.
5. **Query cost** — bytes scanned, locks, runtime, impact on others.
6. **Permissions** — least privilege; not connected as a superuser.
7. **Logging** — who ran what, when, against which objects.
8. **Rollback plan** — written down before the statement executes.

**Kicker:** If you can't answer **all eight**, the query isn't ready — no matter how good it looks.

---

### Slide 10 — Closing CTA

**Eyebrow:** THE TAKEAWAY
**Headline:** AI can write the statement. **You own the consequence.**

- A model has no idea which connection is open, who is on call, or what that table means to the business.
- Permissions, business impact, security and production safety are **human accountabilities**. They don't transfer.
- Safe SQL isn't a syntax skill. It's a **habit** — read, preview, constrain, wrap, verify.

**CTA:** What's the most dangerous SQL command you've seen run in production? Share it in the comments — someone is about to run it today.

**Note on dialects:** examples use generic SQL unless labelled otherwise. Transaction and DDL behaviour, `LIMIT` on writes, masking functions and driver placeholders vary across PostgreSQL, MySQL, SQL Server, Oracle, Snowflake and BigQuery — verify against your engine's documentation before running anything destructive.

---

## LinkedIn caption

AI can write a correct SQL statement in two seconds.

It cannot tell you which database you're connected to.

That gap is where the damage happens. The query parses. It runs. It looks completely reasonable — and it just updated every row in a production table, or pulled a column of national IDs into a CSV on someone's laptop.

Safe SQL isn't a syntax skill. It's a professional habit.

Read before you run. Know whether the first word reads or destroys. Preview every write as a SELECT first. Constrain the blast radius. Wrap it in a transaction when your engine supports one. Parameterize anything that touches user input. And answer the eight pre-flight questions before a statement goes near production.

None of that is hard. All of it is the part the model can't do for you — because permissions, business impact, security, and production safety are human accountabilities. They don't transfer to a tool.

This 10-slide cheat sheet is the version I wish someone had handed me early:

01 — Read before you run (Stop / Check / Run)
02 — Know the command type
03 — Preview before modifying
04 — Constrain the blast radius
05 — Use transactions for reversible changes
06 — Protect sensitive data
07 — Parameterize inputs
08 — The production readiness checklist

Save it. Send it to the teammate who just got write access.

AI can write the statement. You own the consequence.

What's the most dangerous SQL command you've seen run in production?

#SQL #DataEngineering #AnalyticsEngineering #Database #CyberSecurity #AI #DataGovernance
