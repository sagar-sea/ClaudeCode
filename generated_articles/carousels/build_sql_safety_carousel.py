# -*- coding: utf-8 -*-
"""Builds the 'Before You Run AI-Generated SQL' LinkedIn carousel HTML (1080x1350, 10 slides)."""
import html, re, io, os

KEYWORDS = r"""SELECT|FROM|WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LEFT\s+JOIN|INNER\s+JOIN|JOIN|ON|AND|OR|NOT|BETWEEN|IN|IS\s+NULL|NULL|AS|DISTINCT|SET|VALUES|INTO|LIMIT|CASE|WHEN|THEN|ELSE|END|WITH|UNION\s+ALL|INTERVAL|BEGIN|COMMIT|ROLLBACK|SAVEPOINT|START\s+TRANSACTION|UPDATE|DELETE|INSERT|MERGE|CREATE|ALTER|DROP|TRUNCATE|TABLE|GRANT|REVOKE|EXPLAIN|RETURNING|USING|DESC|ASC|LIKE"""
FUNCS = r"""COUNT|SUM|AVG|MIN|MAX|COALESCE|DATE_TRUNC|CAST|CURRENT_DATE|CURRENT_USER|CURRENT_DATABASE|CURRENT_SCHEMA|NOW|LEFT"""


def highlight(code_src):
    out = []
    for line in code_src.split("\n"):
        m = re.search(r"--.*$", line)
        comment = ""
        if m:
            comment = line[m.start():]
            line = line[:m.start()]
        s = html.escape(line)
        s = re.sub(r"(&#x27;[^&]*?&#x27;|&quot;[^&]*?&quot;|'[^']*')", r'<span class="s">\1</span>', s)
        s = re.sub(r"\b(" + FUNCS + r")\b", r'<span class="f">\1</span>', s, flags=re.I)
        s = re.sub(r"\b(" + KEYWORDS + r")\b", r'<span class="k">\1</span>', s, flags=re.I)
        if comment:
            s += '<span class="c">' + html.escape(comment) + "</span>"
        out.append(s)
    return "\n".join(out)


def code(src, cls="", plain=False):
    body = html.escape(src.strip("\n")) if plain else highlight(src.strip("\n"))
    return '<pre class="code %s">%s</pre>' % (cls, body)


S = []

# ---------------------------------------------------------------- 01 cover
S.append(('cover', """
<div class="eyebrow light">SQL SAFETY &middot; CHEAT SHEET</div>
<h1 class="cover-title">Before you run<br><span class="hl">AI-generated<br>SQL.</span></h1>
<p class="cover-sub">A safety cheat sheet for queries that can<br>change, expose, or break data.</p>
<div class="chips">
  <span>Read before you run</span><span>Command types</span><span>Preview first</span>
  <span>Blast radius</span><span>Transactions</span><span>Least privilege</span>
  <span>Parameterized inputs</span><span>Prod checklist</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">10 slides &middot; save for later &rarr;</div>
</div>
"""))

# ---------------------------------------------------------------- 02 read before you run
S.append(('std', """
<div class="eyebrow">01 &middot; THE FIRST HABIT</div>
<h2>Plausible is not<br>the same as safe</h2>
<p class="lead">AI writes SQL that <b>parses, runs, and looks right</b>. What it cannot know is which environment you're connected to, which table is the real one, or what the business considers safe to touch.</p>
<div class="rules tight">
  <div><b>Wrong environment</b> &mdash; the statement was fine; the connection was production.</div>
  <div><b>Wrong object</b> &mdash; <span class="mono">orders</span> vs <span class="mono">orders_archive</span> vs <span class="mono">orders_v2</span>. The model guessed.</div>
  <div><b>Wrong scope</b> &mdash; a filter that matches 4 rows in your head and 400,000 in the table.</div>
</div>
<div class="framework">
  <div class="fw"><b>STOP</b><i>Read the whole statement before it touches a connection.</i></div>
  <div class="fw amber"><b>CHECK</b><i>Which database? Which objects? How many rows? Reversible?</i></div>
  <div class="fw teal"><b>RUN</b><i>Only once all three answers are known &mdash; not assumed.</i></div>
</div>
<p class="kicker"><b>Stop &rarr; Check &rarr; Run.</b> Ten seconds of reading is cheaper than any restore you will ever do.</p>
"""))

# ---------------------------------------------------------------- 03 command types
S.append(('std', """
<div class="eyebrow">02 &middot; COMMAND TYPES</div>
<h2>Know what the first<br>word can do to you</h2>
<div class="cmdgrid">
  <div class="cmd safe"><b>SELECT</b><span>Reads only. Can still be slow or expose data.</span></div>
  <div class="cmd warn"><b>INSERT</b><span>Adds rows. Can duplicate or violate constraints.</span></div>
  <div class="cmd warn"><b>UPDATE</b><span>Overwrites values. The old ones are gone.</span></div>
  <div class="cmd danger"><b>DELETE</b><span>Removes rows. Logged and usually reversible inside a transaction.</span></div>
  <div class="cmd warn"><b>MERGE</b><span>Insert + update + delete in one. Hardest to review.</span></div>
  <div class="cmd safe"><b>CREATE</b><span>Adds an object. Low risk &mdash; unless it replaces one.</span></div>
  <div class="cmd danger"><b>ALTER</b><span>Changes structure. Can lock tables and break downstream code.</span></div>
  <div class="cmd danger"><b>DROP</b><span>Destroys the object and its data. Often not reversible.</span></div>
  <div class="cmd danger"><b>TRUNCATE</b><span>Empties a table fast. Frequently non-transactional.</span></div>
</div>
<p class="kicker"><b>DDL (<span class="mono">CREATE / ALTER / DROP / TRUNCATE</span>) behaves very differently by engine.</b> PostgreSQL can roll most of it back; MySQL and Oracle commit it implicitly the moment it runs. Verify yours &mdash; don't assume.</p>
"""))

# ---------------------------------------------------------------- 04 preview before modifying
S.append(('std', """
<div class="eyebrow">03 &middot; PREVIEW FIRST</div>
<h2>Turn every write into<br>a read &mdash; first</h2>
<p class="lead">Before running a write, run the <b>exact same filter</b> as a <span class="mono">SELECT</span>. Same table, same predicate, no edits.</p>
""" + code("""
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
""", cls="sm") + """
<p class="kicker">If the count surprises you, <b>the filter is wrong &mdash; not the data.</b> Some engines also let you see exactly which rows a write touched: <span class="mono">RETURNING</span> (PostgreSQL), <span class="mono">OUTPUT</span> (SQL Server).</p>
"""))

# ---------------------------------------------------------------- 05 blast radius
S.append(('std', """
<div class="eyebrow">04 &middot; BLAST RADIUS</div>
<h2>A missing <span class="mono big">WHERE</span><br>updates everything</h2>
""" + code("""
-- The most expensive typo in SQL:
UPDATE customers SET tier = 'gold';  -- every customer. all of them.
DELETE FROM orders;                  -- the whole table.

-- Constrain by key, by partition, by date, by batch:
UPDATE customers SET tier = 'gold'
WHERE customer_id IN (101, 102, 103);

DELETE FROM events
WHERE event_date >= '2026-01-01' AND event_date < '2026-02-01';
""", cls="sm") + """
<div class="rules tight">
  <div><b>Confirm the environment first</b> &mdash; <span class="mono">SELECT CURRENT_DATABASE(), CURRENT_USER;</span> costs nothing.</div>
  <div><b>Filter on the partition key</b> on large or columnar warehouses &mdash; it caps cost and damage at once.</div>
  <div><b>Delete in batches</b> instead of one giant statement; long writes hold locks and stall production.</div>
  <div><b>Engine note:</b> <span class="mono">LIMIT</span> on <span class="mono">UPDATE</span>/<span class="mono">DELETE</span> works in MySQL, but <b>not</b> in PostgreSQL or most warehouses &mdash; bound the predicate instead.</div>
</div>
<p class="kicker">Ask of every write: <b>&ldquo;If this matched ten times more rows than I expect, what breaks?&rdquo;</b></p>
"""))

# ---------------------------------------------------------------- 06 transactions
S.append(('std', """
<div class="eyebrow">05 &middot; TRANSACTIONS</div>
<h2>Give yourself<br>an undo button</h2>
""" + code("""
BEGIN;                             -- open the transaction

UPDATE orders SET status = 'expired'
WHERE status = 'pending' AND created_at < '2026-01-01';

-- VALIDATE inside the transaction, before you commit:
SELECT status, COUNT(*) FROM orders GROUP BY status;

COMMIT;    -- numbers look right? make it permanent
ROLLBACK;  -- numbers look wrong? undo everything since BEGIN
""", cls="sm") + """
<div class="rules tight">
  <div><b>Verify your engine's behaviour.</b> Autocommit is on by default in many clients, and some tools commit each statement as it runs.</div>
  <div><b>DDL is the exception.</b> MySQL and Oracle commit <span class="mono">CREATE</span>/<span class="mono">ALTER</span>/<span class="mono">DROP</span> implicitly &mdash; there's nothing left to roll back.</div>
  <div><b>Don't leave it open.</b> An uncommitted transaction holds locks and can block everyone else.</div>
</div>
<p class="kicker">A transaction is not a substitute for a backup. <b>It protects the next five minutes, not the next five days.</b></p>
"""))

# ---------------------------------------------------------------- 07 sensitive data
S.append(('std', """
<div class="eyebrow">06 &middot; SENSITIVE DATA</div>
<h2>The query ran fine.<br>That's not the risk.</h2>
<p class="lead">A <span class="mono">SELECT</span> can't corrupt a table &mdash; but it can move regulated data somewhere it was never approved to go.</p>
""" + code("""
-- RISKY: pulls every column, including ones you never asked for
SELECT * FROM customers;  -- email, dob, national_id, card_last4...

-- SAFER: name the columns, mask what you don't need in full
SELECT customer_id,
       LEFT(email, 2) || '***' AS email_hint,
       signup_date
FROM customers
WHERE signup_date >= '2026-01-01';
""", cls="sm") + """
<div class="rules tight">
  <div><b>Least privilege</b> &mdash; analysts read from views, not base tables. Write access is granted, never assumed.</div>
  <div><b>Never paste real PII, secrets or credentials into an AI prompt.</b> Share the schema, not the rows.</div>
  <div><b>Exports are where data leaks</b> &mdash; a CSV in a downloads folder has left every control you have.</div>
</div>
<p class="kicker"><span class="mono">SELECT *</span> in a shared notebook or on a screen share is a <b>disclosure decision</b>, not a shortcut.</p>
"""))

# ---------------------------------------------------------------- 08 parameterize
S.append(('std', """
<div class="eyebrow">07 &middot; APPLICATION CODE</div>
<h2>Never build SQL by<br>gluing strings together</h2>
<p class="lead">When AI generates <b>application</b> code, string-concatenated SQL is the classic injection hole: user input becomes executable syntax.</p>
""" + code("""
# UNSAFE - the input becomes part of the statement
q = "SELECT * FROM users WHERE email = '" + user_input + "'"
#   user_input = "x' OR '1'='1"          -> returns every user
#   user_input = "x'; DROP TABLE users;--" -> ends very badly

# SAFE - the value is sent separately from the SQL text
cur.execute(
    "SELECT id, email FROM users WHERE email = %s",
    (user_input,)
)
""", cls="sm", plain=True) + """
<div class="rules tight">
  <div>Placeholders differ by driver (<span class="mono">%s</span>, <span class="mono">?</span>, <span class="mono">:name</span>) &mdash; the principle doesn't: <b>data is data, not syntax.</b></div>
  <div>Table and column names can't be parameterized &mdash; validate them against an <b>allow-list</b>, never against user input.</div>
</div>
<p class="kicker">Ad-hoc analysis and shipped code are different risk classes. <b>Anything that accepts outside input must be parameterized</b> &mdash; no escaping by hand.</p>
"""))

# ---------------------------------------------------------------- 09 checklist
S.append(('std', """
<div class="eyebrow">08 &middot; BEFORE PRODUCTION</div>
<h2>The 8-point<br>pre-flight check</h2>
<p class="lead">Run this before any statement touches a production system &mdash; whoever, or whatever, wrote it.</p>
<ul class="checks two">
  <li><b>Environment</b> &mdash; confirmed dev, staging or prod. Say it out loud.</li>
  <li><b>Backup</b> &mdash; a recent snapshot, and a restore path you've tested.</li>
  <li><b>Peer review</b> &mdash; a second human has read the statement.</li>
  <li><b>Expected rows</b> &mdash; you predicted the count before running it.</li>
  <li><b>Query cost</b> &mdash; bytes scanned, locks, runtime, impact on others.</li>
  <li><b>Permissions</b> &mdash; least privilege; not connected as a superuser.</li>
  <li><b>Logging</b> &mdash; who ran what, when, against which objects.</li>
  <li><b>Rollback plan</b> &mdash; written down before the statement executes.</li>
</ul>
<p class="kicker">If you can't answer <b>all eight</b>, the query isn't ready &mdash; no matter how good it looks.</p>
"""))

# ---------------------------------------------------------------- 10 CTA
S.append(('std', """
<div class="eyebrow">THE TAKEAWAY</div>
<h2>AI can write<br>the statement.</h2>
<p class="lead big"><b>You own the consequence.</b></p>
<div class="rules">
  <div>A model has no idea which connection is open, who is on call, or what that table means to the business.</div>
  <div>Permissions, business impact, security and production safety are <b>human accountabilities</b>. They don't transfer.</div>
  <div>Safe SQL isn't a syntax skill. It's a <b>habit</b> &mdash; read, preview, constrain, wrap, verify.</div>
</div>
<div class="cta">
  <div class="cta-line">What's the most dangerous SQL command you've seen run in production?<br>Share it in the comments &mdash; someone is about to run it today.</div>
  <div class="cta-by"><b>Sagar Rathkanthiwar</b> &middot; Data &amp; AI Professional &middot; follow for more field guides</div>
</div>
<div class="srcs"><b>Note on dialects:</b> examples use generic SQL unless labelled otherwise. Transaction and DDL behaviour, <span class="mono">LIMIT</span> on writes, masking functions and driver placeholders vary across PostgreSQL, MySQL, SQL Server, Oracle, Snowflake and BigQuery &mdash; verify against your engine's documentation before running anything destructive.</div>
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
  padding:76px 74px 124px; background:var(--paper);
  page-break-after:always; display:flex; flex-direction:column;
}
.slide:last-child{ page-break-after:auto; }

.foot{ position:absolute; left:0; right:0; bottom:0; height:74px; background:var(--ink);
  display:flex; align-items:center; justify-content:space-between; padding:0 74px; }
.foot span{ color:#fff; font-size:21px; letter-spacing:.045em; font-weight:600; }
.foot .r{ color:#8ea2c9; font-weight:500; letter-spacing:.12em; }
.accentbar{ position:absolute; top:0; left:0; width:100%; height:10px; background:var(--accent); }

.eyebrow{ font-size:22px; font-weight:700; letter-spacing:.2em; color:var(--accent); margin-bottom:22px; }
.eyebrow.light{ color:#9db4f7; }
h2{ font-size:60px; line-height:1.1; letter-spacing:-.02em; color:var(--ink); font-weight:800; margin-bottom:28px; }
.lead{ font-size:29px; line-height:1.45; color:var(--body); margin-bottom:26px; }
.lead.big{ font-size:40px; line-height:1.3; }
.lead b{ color:var(--ink); }
.kicker{ margin-top:auto; font-size:26px; line-height:1.5; color:var(--body);
  border-left:8px solid var(--accent); background:var(--soft); padding:24px 28px; border-radius:0 14px 14px 0; }
.kicker b{ color:var(--ink); }
.mono{ font-family:Consolas,"Cascadia Mono",monospace; font-size:.9em; background:#eef1f7; color:#1b2a4a;
  padding:2px 8px; border-radius:6px; }
h2 .mono.big{ font-size:.8em; background:#eef1f7; padding:4px 14px; border-radius:10px; }

.code{ font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:22px; line-height:1.58;
  background:#0d1526; color:#dbe4f5; padding:30px 32px; border-radius:16px; white-space:pre;
  margin-bottom:26px; overflow:hidden; }
.code.sm{ font-size:20px; line-height:1.55; padding:26px 28px; }
.code.xs{ font-size:18.5px; line-height:1.55; padding:24px 26px; }
.code .k{ color:#7fb0ff; font-weight:600; }
.code .f{ color:#f2b45c; }
.code .s{ color:#7fd6a5; }
.code .c{ color:#8091b4; font-style:italic; }

.cover{ background:var(--ink); color:#fff; padding:88px 74px 124px; }
.cover .accentbar{ background:linear-gradient(90deg,#2f5bea,#22b3a4); }
.cover-title{ font-size:94px; line-height:1.04; font-weight:800; letter-spacing:-.035em; color:#fff; }
.cover-title .hl{ color:#7fb0ff; }
.cover-sub{ margin-top:34px; font-size:34px; line-height:1.35; color:#b9c6e0; font-weight:400; }
.chips{ margin-top:40px; display:flex; flex-wrap:wrap; gap:13px; max-width:900px; }
.chips span{ border:2px solid #33456d; color:#9db4f7; border-radius:999px; padding:9px 20px;
  font-size:22px; font-weight:600; }
.cover-foot{ margin-top:auto; }
.cover-foot .rule{ height:3px; background:#2a3a5e; margin-bottom:30px; }
.cover-by{ font-size:31px; font-weight:700; color:#fff; }
.cover-by span{ display:block; font-size:24px; font-weight:500; color:#8ea2c9; margin-top:6px; }
.cover-meta{ margin-top:22px; font-size:23px; color:#7fb0ff; font-weight:600; letter-spacing:.03em; }

.rules{ display:flex; flex-direction:column; gap:20px; margin-bottom:26px; }
.rules.tight{ gap:16px; }
.rules div{ font-size:26px; line-height:1.45; padding-left:34px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:11px; width:16px; height:16px;
  border-radius:5px; background:var(--accent); }
.rules div b{ color:var(--ink); }

.framework{ display:flex; gap:16px; margin-bottom:26px; }
.fw{ flex:1; background:var(--soft); border-radius:16px; padding:22px 24px; border-top:8px solid var(--rose); }
.fw.amber{ border-top-color:var(--amber); }
.fw.teal{ border-top-color:var(--teal); }
.fw b{ display:block; font-size:30px; font-weight:800; color:var(--ink); letter-spacing:.04em; margin-bottom:10px; }
.fw i{ display:block; font-style:normal; font-size:22px; line-height:1.4; color:var(--body); }

.cmdgrid{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:26px; }
.cmd{ background:var(--soft); border-radius:14px; padding:20px; border-left:8px solid var(--teal); }
.cmd.warn{ border-left-color:var(--amber); }
.cmd.danger{ border-left-color:var(--rose); background:#fdf2f5; }
.cmd b{ display:block; font-family:Consolas,"Cascadia Mono",monospace; font-size:28px; color:var(--ink);
  font-weight:800; margin-bottom:9px; letter-spacing:-.01em; }
.cmd span{ display:block; font-size:20px; line-height:1.35; color:var(--body); }

.checks{ list-style:none; counter-reset:c; margin-bottom:28px; }
.checks.two{ display:grid; grid-template-columns:1fr 1fr; gap:40px 26px; }
.checks li{ counter-increment:c; position:relative; padding-left:70px;
  font-size:27px; line-height:1.4; }
.checks.two li:before{ width:50px; height:50px; font-size:26px; }
.checks li:before{ content:counter(c); position:absolute; left:0; top:-2px; width:46px; height:46px;
  border-radius:14px; background:var(--accent); color:#fff; font-weight:800; font-size:24px;
  display:flex; align-items:center; justify-content:center; }
.checks li b{ color:var(--ink); }

.cta{ background:var(--ink); border-radius:18px; padding:32px 34px; margin-top:auto; }
.cta-line{ font-size:29px; line-height:1.38; color:#fff; font-weight:700; }
.cta-by{ margin-top:14px; font-size:23px; color:#9db4f7; }
.cta-by b{ color:#fff; }
.srcs{ margin-top:20px; font-size:17px; line-height:1.5; color:var(--muted); }
.srcs b{ color:var(--body); }
"""

BODY = []
for i, (kind, content) in enumerate(S, start=1):
    cls = "slide" + (" cover" if kind == "cover" else "")
    if kind == 'cover':
        foot = ('<div class="foot"><span>The SQL Safety Cheat Sheet</span>'
                '<span class="r">01 / %02d &nbsp;&middot;&nbsp; SWIPE &rarr;</span></div>' % len(S))
    else:
        foot = ('<div class="foot"><span>Sagar Rathkanthiwar &nbsp;|&nbsp; The SQL Safety Cheat Sheet</span>'
                '<span class="r">%02d / %02d</span></div>' % (i, len(S)))
    BODY.append('<section class="%s"><div class="accentbar"></div>%s%s</section>' % (cls, content, foot))

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>Before You Run AI-Generated SQL: The SQL Safety Cheat Sheet</title><style>%s</style></head><body>%s</body></html>""" % (
    CSS, "\n".join(BODY))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "sql_safety_cheat_sheet_carousel_2026-09-10.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
