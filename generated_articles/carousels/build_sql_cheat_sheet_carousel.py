# -*- coding: utf-8 -*-
"""Builds the 'SQL Cheat Sheet for the AI Era' LinkedIn carousel HTML (1080x1350 slides)."""
import html, re, io, os

KEYWORDS = r"""SELECT|FROM|WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LEFT\s+JOIN|INNER\s+JOIN|JOIN|ON|AND|OR|NOT\s+EXISTS|EXISTS|NOT\s+IN|IN|IS\s+NULL|IS\s+NOT\s+NULL|NULL|AS|DISTINCT|OVER|PARTITION\s+BY|LIMIT|CASE|WHEN|THEN|ELSE|END|WITH|UNION\s+ALL|UPDATE|DELETE|INSERT|BEGIN|COMMIT|ROLLBACK|EXPLAIN|ANALYZE|DESC|ASC"""
FUNCS = r"""COUNT|SUM|AVG|MIN|MAX|COALESCE|ROW_NUMBER|RANK|DENSE_RANK|LAG|LEAD|DATE_TRUNC|NULLIF|CAST"""


def highlight(code: str) -> str:
    out = []
    for line in code.split("\n"):
        # split off trailing comment
        m = re.search(r"--.*$", line)
        comment = ""
        if m:
            comment = line[m.start():]
            line = line[:m.start()]
        s = html.escape(line)
        s = re.sub(r"(&#x27;[^&]*?&#x27;|&quot;[^&]*?&quot;|'[^']*')", r'<span class="s">\1</span>', s)
        s = re.sub(r"\b(" + FUNCS + r")\b(?=\s*\()", r'<span class="f">\1</span>', s, flags=re.I)
        s = re.sub(r"\b(" + KEYWORDS + r")\b", r'<span class="k">\1</span>', s, flags=re.I)
        if comment:
            s += '<span class="c">' + html.escape(comment) + "</span>"
        out.append(s)
    return "\n".join(out)


def code(src: str, cls: str = "", plain: bool = False) -> str:
    body = html.escape(src.strip("\n")) if plain else highlight(src.strip("\n"))
    return '<pre class="code %s">%s</pre>' % (cls, body)


# ---------------------------------------------------------------- slides
S = []

S.append(('cover', """
<div class="eyebrow light">DATA &amp; AI &middot; PRACTICAL FIELD GUIDE</div>
<h1 class="cover-title">SQL<br>Cheat Sheet<br><span class="hl">for the AI&nbsp;Era</span></h1>
<p class="cover-sub">AI writes the first draft.<br>You still own the number.</p>
<div class="chips">
  <span>Intent</span><span>Schema</span><span>Joins</span><span>NULLs</span>
  <span>Aggregates</span><span>Windows</span><span>Performance</span><span>Privacy</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">12 slides &middot; save for later &rarr;</div>
</div>
"""))

S.append(('std', """
<div class="eyebrow">THE HOOK</div>
<h2>The query runs.<br>That doesn't make it&nbsp;right.</h2>
<div class="stats">
  <div class="stat"><b>90% use it &middot; 30% don't trust it</b><span>Nine in ten developers now work with AI. Nearly a third report little to no trust in the code it hands back (DORA, State of AI-assisted Software Development).</span></div>
  <div class="stat"><b>The verification tax</b><span>DORA's finding: time saved writing gets spent auditing. AI raises the volume of code far faster than it raises your confidence in it.</span></div>
  <div class="stat"><b>Your schema is the hard part</b><span>On real enterprise warehouses rather than textbook databases, leading text-to-SQL systems still land well short of expert accuracy &mdash; undocumented columns and ambiguous join paths, not syntax.</span></div>
</div>
<p class="kicker">The bottleneck moved from <b>writing</b> SQL to <b>checking</b> it. Everything after this slide is the checking part.</p>
"""))

S.append(('std', """
<div class="eyebrow">THE FRAME</div>
<h2>Split the work into three lanes</h2>
<div class="lanes">
  <div class="lane blue"><div class="lane-tag">ASK AI</div>
    <p>First drafts, dialect translation, boilerplate, alternate approaches, and plain-English explanations of SQL you inherited.</p></div>
  <div class="lane teal"><div class="lane-tag">INSPECT YOURSELF</div>
    <p>Grain, keys, join cardinality, filter logic, date boundaries, and what the business actually means by "active customer."</p></div>
  <div class="lane rose"><div class="lane-tag">CATCH BEFORE SHIPPING</div>
    <p>Duplicated rows, NULL logic, averages at the wrong grain, unbounded scans, and columns you shouldn't be reading.</p></div>
</div>
<p class="kicker">AI is fast at SQL. You are accountable for the definition of <b>customer</b>, <b>active</b>, and <b>revenue</b>.</p>
"""))

S.append(('std', """
<div class="eyebrow">01 &middot; INTENT</div>
<h2>Prompt the schema,<br>not just the question</h2>
<div class="badline bad"><b>Weak prompt</b>&nbsp; "Give me total revenue by customer."</div>
""" + code("""
Tables + columns (with types):
  orders(order_id PK, customer_id, order_ts, status, amount_usd)
  refunds(refund_id PK, order_id FK, amount_usd)

Grain I want:  one row per customer per month
Revenue means: amount_usd minus refunds, excluding status='test'
Dialect: Snowflake.  Window: last 12 full months.

Write the query, then list every assumption you made.
""", plain=True) + """
<p class="kicker"><b>Catch:</b> an answer with no stated assumptions is an answer you have to reverse-engineer later. Make "list your assumptions" part of every prompt.</p>
"""))

S.append(('std', """
<div class="eyebrow">02 &middot; SCHEMA</div>
<h2>Know the grain before<br>you trust the join</h2>
<p class="lead"><b>Grain = what one row means.</b> Most wrong numbers are grain mistakes, not syntax mistakes &mdash; and the model can't see your data, only its names.</p>
""" + code("""
-- 1. Is this column actually a key?
SELECT COUNT(*) AS rows_total,
       COUNT(DISTINCT order_id) AS distinct_ids
FROM orders;              -- the two must match

-- 2. Will this child table fan out my rows?
SELECT order_id, COUNT(*) AS n
FROM refunds
GROUP BY order_id
HAVING COUNT(*) > 1
LIMIT 20;                 -- any result means one-to-many
""") + """
<p class="kicker"><b>Ask AI:</b> "What grain does this query return, and which column makes it unique?" Then prove it with the two queries above.</p>
"""))

S.append(('std', """
<div class="eyebrow">03 &middot; JOINS</div>
<h2>Duplicates don't<br>announce themselves</h2>
<p class="lead">A one-to-many join silently multiplies rows &mdash; and every <b>SUM</b> that comes after it.</p>
""" + code("""
-- WRONG: each order is counted once per refund row
SELECT o.customer_id, SUM(o.amount_usd) AS revenue
FROM orders o
JOIN refunds r ON r.order_id = o.order_id
GROUP BY 1;

-- RIGHT: collapse the child table to the join grain first
SELECT o.customer_id,
       SUM(o.amount_usd) - SUM(COALESCE(r.refunded,0)) AS net_rev
FROM orders o
LEFT JOIN (SELECT order_id, SUM(amount_usd) AS refunded
           FROM refunds GROUP BY order_id) r
       ON r.order_id = o.order_id
GROUP BY 1;
""") + """
<p class="kicker"><b>Guard:</b> row count before the join should equal row count after. If it grew, you owe yourself an explanation &mdash; not a <span class="mono">DISTINCT</span>.</p>
"""))

S.append(('std', """
<div class="eyebrow">04 &middot; NULLS</div>
<h2>NULL isn't a value.<br>It's "unknown."</h2>
<div class="rules">
  <div><b><span class="mono">x = NULL</span> is never true</b> &mdash; use <span class="mono">IS NULL</span>. Comparisons against unknown return unknown, not false.</div>
  <div><b><span class="mono">NOT IN (subquery)</span> returns zero rows</b> if that subquery contains a single NULL. Use <span class="mono">NOT EXISTS</span> instead.</div>
  <div><b><span class="mono">COUNT(col)</span> skips NULLs</b>, <span class="mono">COUNT(*)</span> doesn't. <span class="mono">AVG(col)</span> divides by the non-NULL count only.</div>
  <div><b>A LEFT JOIN plus a WHERE filter on the right table</b> quietly becomes an INNER JOIN. Move that filter into the <span class="mono">ON</span> clause.</div>
</div>
""" + code("""
-- Safe anti-join: customers with no orders
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id);
""") + """
<p class="kicker"><b>Catch:</b> ask AI "what happens here if this column is NULL?" &mdash; then test it with a row that actually is.</p>
"""))

S.append(('std', """
<div class="eyebrow">05 &middot; AGGREGATES</div>
<h2>Check the math,<br>not just the output</h2>
<div class="rules tight">
  <div><b>WHERE filters rows, HAVING filters groups.</b> Moving a row filter into HAVING changes the answer.</div>
  <div><b>An average of averages is not an average.</b> Re-aggregate from base rows, weighted properly.</div>
  <div><b>COUNT(DISTINCT user_id) is a different question</b> than COUNT(*). Decide which one you were asked.</div>
  <div><b>Empty groups vanish.</b> If "0 orders in July" must appear, join a date spine.</div>
</div>
""" + code("""
SELECT d.month,
       COUNT(DISTINCT o.customer_id) AS buyers,
       COALESCE(SUM(o.amount_usd), 0) AS revenue
FROM date_spine d
LEFT JOIN orders o
       ON DATE_TRUNC('month', o.order_ts) = d.month
      AND o.status <> 'test'   -- filter goes in ON, not WHERE
GROUP BY 1
ORDER BY 1;
""") + """
<p class="kicker"><b>Catch:</b> if a total looks too round or too small, check the filters before you check the data. Most "missing revenue" is a WHERE clause.</p>
"""))

S.append(('std', """
<div class="eyebrow">06 &middot; WINDOW FUNCTIONS</div>
<h2>Rank, dedupe and compare<br>without collapsing rows</h2>
<p class="lead">Window functions keep every row and add context. GROUP BY collapses them. Know which one you actually asked for.</p>
""" + code("""
-- Latest order per customer (deterministic dedupe)
SELECT * FROM (
  SELECT o.*,
         ROW_NUMBER() OVER (PARTITION BY customer_id
           ORDER BY order_ts DESC, order_id DESC) AS rn
  FROM orders o
) ranked
WHERE rn = 1;

-- Month over month change
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS mom_delta
FROM monthly_revenue;
""") + """
<p class="kicker"><b>Catch:</b> ties. Without a tiebreaker in ORDER BY, "latest" can change between runs. And <span class="mono">RANK</span> vs <span class="mono">DENSE_RANK</span> vs <span class="mono">ROW_NUMBER</span> is a business decision, not a style choice.</p>
"""))

S.append(('std', """
<div class="eyebrow">07 &middot; PERFORMANCE</div>
<h2>Correct and expensive<br>is still a problem</h2>
<div class="rules">
  <div><b>Read the plan, not the vibes.</b> <span class="mono">EXPLAIN</span> / <span class="mono">EXPLAIN ANALYZE</span>, and check bytes scanned on cloud warehouses where you pay per scan.</div>
  <div><b>Keep predicates sargable.</b> <span class="mono">WHERE order_ts &gt;= '2026-01-01'</span> can use an index or partition; <span class="mono">WHERE YEAR(order_ts) = 2026</span> usually can't.</div>
  <div><b>Filter partition and cluster keys early</b>, and stop selecting <span class="mono">*</span> from tables that run to hundreds of columns.</div>
  <div><b>Treat a stray DISTINCT as a smell.</b> It's often patching a fan-out join instead of fixing it.</div>
</div>
<p class="kicker"><b>Ask AI:</b> "Rewrite this to scan fewer partitions and explain the tradeoff." Then read the plan yourself &mdash; cost estimates are the one thing the model genuinely cannot see.</p>
"""))

S.append(('std', """
<div class="eyebrow">08 &middot; SECURITY &amp; PRIVACY</div>
<h2>Review what the<br>query exposes</h2>
<div class="rules">
  <div><b>Never concatenate user input into SQL.</b> Parameterize. A generated f-string that "works" is an injection waiting for its first quote character.</div>
  <div><b>Least privilege by default.</b> Analysis runs on a read-only role. Write credentials don't belong in a notebook or an agent's environment.</div>
  <div><b>Don't paste real PII or secrets into a prompt</b> to "help it understand the data." Share column names, types and synthetic rows instead.</div>
  <div><b>Query only what you're entitled to</b> &mdash; prefer masked or governed views, and re-check access before sharing an export.</div>
  <div><b>No UPDATE or DELETE</b> until you've run the identical predicate as a SELECT, inside a transaction you can roll back.</div>
</div>
<p class="kicker"><b>Catch:</b> generated SQL inherits whatever access you hand it. The model has no idea which of your columns are regulated &mdash; that judgement is entirely yours.</p>
"""))

S.append(('close', """
<div class="eyebrow">SHIP CHECKLIST</div>
<h2>Six checks before you<br>trust the number</h2>
<ol class="checks">
  <li><b>Row counts</b> are sane before and after every join.</li>
  <li><b>Grain matches the ask</b> &mdash; one row per ______.</li>
  <li><b>Three records traced end-to-end</b> back to the source system.</li>
  <li><b>Totals reconcile</b> with a known report or last month's figure.</li>
  <li><b>Edge cases handled</b>: no orders, refunds only, NULLs, future dates.</li>
  <li><b>Re-run is stable</b> &mdash; same input, same output, no random ties.</li>
</ol>
<div class="cta">
  <div class="cta-line">Save this, then run check #1 on the query you shipped yesterday.</div>
  <div class="cta-by">Follow <b>Sagar Rathkanthiwar</b> for practical Data &amp; AI</div>
</div>
<div class="srcs"><b>Sources:</b> DORA, State of AI-assisted Software Development &amp; ROI of AI-assisted Software Development (dora.dev) &middot; Spider 2.0 enterprise text-to-SQL benchmark and leaderboards (spider2-sql.github.io, arXiv 2411.07763). SQL behaviour described here is standard-SQL; syntax details vary by dialect.</div>
"""))

# ---------------------------------------------------------------- template
CSS = """
:root{
  --ink:#0d1526; --body:#33415a; --muted:#64748b; --line:#e4e8ef;
  --accent:#2f5bea; --teal:#0e8177; --rose:#c8305c; --amber:#c07806;
  --paper:#ffffff; --soft:#f5f7fb;
}
*{box-sizing:border-box;margin:0;padding:0;}
@page{ size:810pt 1012.5pt; margin:0; }
html,body{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ font-family:"Segoe UI","Inter",Arial,sans-serif; color:var(--body); background:#fff; }
.slide{
  position:relative; width:1080px; height:1350px; overflow:hidden;
  padding:84px 78px 132px; background:var(--paper);
  page-break-after:always; display:flex; flex-direction:column;
}
.slide:last-child{ page-break-after:auto; }

/* footer */
.foot{ position:absolute; left:0; right:0; bottom:0; height:76px; background:var(--ink);
  display:flex; align-items:center; justify-content:space-between; padding:0 78px; }
.foot span{ color:#fff; font-size:21px; letter-spacing:.045em; font-weight:600; }
.foot .r{ color:#8ea2c9; font-weight:500; letter-spacing:.12em; }
.accentbar{ position:absolute; top:0; left:0; width:100%; height:10px; background:var(--accent); }

/* type */
.eyebrow{ font-size:22px; font-weight:700; letter-spacing:.2em; color:var(--accent); margin-bottom:26px; }
.eyebrow.light{ color:#9db4f7; }
h2{ font-size:64px; line-height:1.1; letter-spacing:-.02em; color:var(--ink); font-weight:800; margin-bottom:34px; }
.lead{ font-size:30px; line-height:1.45; color:var(--body); margin-bottom:30px; }
.lead b{ color:var(--ink); }
.kicker{ margin-top:auto; font-size:27px; line-height:1.5; color:var(--body);
  border-left:8px solid var(--accent); background:var(--soft); padding:26px 30px; border-radius:0 14px 14px 0; }
.kicker b{ color:var(--ink); }
.mono{ font-family:Consolas,"Cascadia Mono",monospace; font-size:.92em; background:#eef1f7; color:#1b2a4a;
  padding:2px 8px; border-radius:6px; }

/* code */
.code{ font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:22px; line-height:1.6;
  background:#0d1526; color:#dbe4f5; padding:32px 34px; border-radius:16px; white-space:pre;
  margin-bottom:30px; overflow:hidden; }
.code .k{ color:#7fb0ff; font-weight:600; }
.code .f{ color:#f2b45c; }
.code .s{ color:#7fd6a5; }
.code .c{ color:#7d8db0; font-style:italic; }

/* cover */
.cover{ background:var(--ink); color:#fff; padding:96px 78px 132px; }
.cover .accentbar{ background:linear-gradient(90deg,#2f5bea,#22b3a4); }
.cover-title{ font-size:112px; line-height:1.02; font-weight:800; letter-spacing:-.035em; color:#fff; }
.cover-title .hl{ color:#7fb0ff; }
.cover-sub{ margin-top:40px; font-size:38px; line-height:1.35; color:#b9c6e0; font-weight:400; }
.chips{ margin-top:52px; display:flex; flex-wrap:wrap; gap:14px; max-width:820px; }
.chips span{ border:2px solid #33456d; color:#9db4f7; border-radius:999px; padding:10px 22px;
  font-size:23px; font-weight:600; }
.cover-foot{ margin-top:auto; }
.cover-foot .rule{ height:3px; background:#2a3a5e; margin-bottom:34px; }
.cover-by{ font-size:32px; font-weight:700; color:#fff; }
.cover-by span{ display:block; font-size:24px; font-weight:500; color:#8ea2c9; margin-top:6px; }
.cover-meta{ margin-top:26px; font-size:23px; color:#7fb0ff; font-weight:600; letter-spacing:.03em; }

/* stats */
.stats{ display:flex; flex-direction:column; gap:22px; margin-bottom:34px; }
.stat{ background:var(--soft); border-radius:16px; padding:28px 32px; border-left:8px solid var(--accent); }
.stat b{ display:block; font-size:46px; color:var(--ink); font-weight:800; letter-spacing:-.02em; }
.stat span{ display:block; margin-top:10px; font-size:25px; line-height:1.45; color:var(--body); }
.stat:nth-child(2){ border-color:var(--teal); }
.stat:nth-child(3){ border-color:var(--amber); }

/* lanes */
.lanes{ display:flex; flex-direction:column; gap:26px; margin-bottom:34px; }
.lane{ border:3px solid var(--line); border-radius:18px; padding:30px 34px; }
.lane-tag{ display:inline-block; font-size:21px; font-weight:800; letter-spacing:.16em;
  padding:8px 18px; border-radius:999px; color:#fff; margin-bottom:18px; }
.lane p{ font-size:27px; line-height:1.5; }
.lane.blue{ border-color:#c9d8ff; } .lane.blue .lane-tag{ background:var(--accent); }
.lane.teal{ border-color:#bde3de; } .lane.teal .lane-tag{ background:var(--teal); }
.lane.rose{ border-color:#f3ccda; } .lane.rose .lane-tag{ background:var(--rose); }

/* rule lists */
.rules{ display:flex; flex-direction:column; gap:22px; margin-bottom:30px; }
.rules.tight{ gap:18px; }
.rules div{ font-size:27px; line-height:1.45; padding-left:34px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:12px; width:16px; height:16px;
  border-radius:5px; background:var(--accent); }
.rules div b{ color:var(--ink); }

.badline{ font-size:26px; padding:20px 26px; border-radius:12px; margin-bottom:26px; }
.badline.bad{ background:#fdf0f4; color:#8d2242; }
.badline b{ letter-spacing:.06em; }

/* checks */
.checks{ list-style:none; counter-reset:c; margin-bottom:34px; }
.checks li{ counter-increment:c; position:relative; padding-left:74px; margin-bottom:22px;
  font-size:28px; line-height:1.45; }
.checks li:before{ content:counter(c); position:absolute; left:0; top:-2px; width:50px; height:50px;
  border-radius:14px; background:var(--accent); color:#fff; font-weight:800; font-size:26px;
  display:flex; align-items:center; justify-content:center; }
.checks li b{ color:var(--ink); }
.cta{ background:var(--ink); border-radius:18px; padding:34px 36px; margin-top:auto; }
.cta-line{ font-size:31px; line-height:1.35; color:#fff; font-weight:700; }
.cta-by{ margin-top:14px; font-size:25px; color:#9db4f7; }
.cta-by b{ color:#fff; }
.srcs{ margin-top:22px; font-size:17px; line-height:1.5; color:var(--muted); }
.srcs b{ color:var(--body); }
"""

BODY = []
for i, (kind, content) in enumerate(S, start=1):
    cls = "slide" + (" cover" if kind == "cover" else "")
    foot = '' if kind == 'cover' else (
        '<div class="foot"><span>Sagar Rathkanthiwar &nbsp;|&nbsp; Data &amp; AI Professional</span>'
        '<span class="r">%02d / %02d</span></div>' % (i, len(S)))
    if kind == 'cover':
        foot = ('<div class="foot"><span>SQL Cheat Sheet for the AI Era</span>'
                '<span class="r">SWIPE &rarr;</span></div>')
    BODY.append('<section class="%s"><div class="accentbar"></div>%s%s</section>' % (cls, content, foot))

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>SQL Cheat Sheet for the AI Era</title><style>%s</style></head><body>%s</body></html>""" % (
    CSS, "\n".join(BODY))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql_cheat_sheet_carousel.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
