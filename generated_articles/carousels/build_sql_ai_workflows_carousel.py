# -*- coding: utf-8 -*-
"""Builds the 'SQL's New Job in the AI Era' LinkedIn carousel HTML (1080x1350, 10 slides)."""
import html, re, io, os

KEYWORDS = r"""SELECT|FROM|WHERE|GROUP\s+BY|ORDER\s+BY|HAVING|LEFT\s+JOIN|JOIN|ON|AND|OR|NOT|IN|IS\s+NOT\s+NULL|IS\s+NULL|NULL|AS|CASE|WHEN|THEN|ELSE|END|INSERT\s+INTO|INTO|CREATE\s+VIEW|DESC|ASC"""
FUNCS = r"""COUNT|SUM|AVG|MAX|MIN|CAST|CURRENT_DATE|DATE"""


def highlight(code_src):
    out = []
    for line in code_src.split("\n"):
        m = re.search(r"--.*$", line)
        comment = ""
        if m:
            comment = line[m.start():]
            line = line[:m.start()]
        s = html.escape(line, quote=False)
        s = re.sub(r"('[^']*')", r'<span class="s">\1</span>', s)
        s = re.sub(r"\b(" + FUNCS + r")\b(?![^<]*</span>)", r'<span class="f">\1</span>', s)
        s = re.sub(r"\b(" + KEYWORDS + r")\b(?![^<]*</span>)", r'<span class="k">\1</span>', s)
        s = re.sub(r"(?<![\w.#])(\d+\.\d+|\d+)(?![\w<])(?![^<]*</span>)", r'<span class="n">\1</span>', s)
        if comment:
            s += '<span class="c">' + html.escape(comment, quote=False) + "</span>"
        out.append(s)
    return "\n".join(out)


def code(src, cls="", label=""):
    lab = '<div class="codelabel">%s</div>' % label if label else ""
    return '<div class="codewrap">%s<pre class="code %s">%s</pre></div>' % (lab, cls, highlight(src.strip("\n")))


def T(kind):
    names = {"sql": "SQL", "llm": "LLM", "vec": "VECTOR / SEARCH", "app": "APP CODE", "hum": "HUMAN"}
    return '<span class="tag %s">%s</span>' % (kind, names[kind])


S = []

# ---------------------------------------------------------------- 01 cover
S.append(('cover', """
<div class="eyebrow light">SQL &times; AI &middot; FIELD GUIDE</div>
<h1 class="cover-title">SQL&rsquo;s New Job<br>in the <span class="hl">AI Era</span></h1>
<p class="cover-sub">How the language behind dashboards is<br>powering reliable AI workflows.</p>

<div class="coverflow">
  <div class="cf-node"><b>Warehouse</b><i>orders &middot; tickets &middot; usage &middot; CRM</i></div>
  <div class="cf-arrow">&rarr;</div>
  <div class="cf-node sql"><b>SQL</b><i>context &middot; metrics &middot; governance</i></div>
  <div class="cf-arrow">&rarr;</div>
  <div class="cf-node ai"><b>AI product</b><i>assistant &middot; agent &middot; copilot</i></div>
  <div class="cf-back">&larr; logs, feedback &amp; outcomes flow back into SQL &larr;</div>
</div>

<div class="chips">
  <span>Trusted context</span><span>Data profiles</span><span>Observability</span><span>Quality evals</span>
  <span>Experiments</span><span>Human review</span><span>Governance</span><span>Semantic layer</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">10 slides &middot; save for later &rarr;</div>
</div>
"""))

# ---------------------------------------------------------------- 02 trusted context
S.append(('std', """
<div class="eyebrow">01 &middot; TRUSTED CONTEXT</div>
<h2>Decide what the model sees &mdash; before it sees it</h2>
<p class="lead">A support assistant drafting a reply for one customer doesn&rsquo;t need the warehouse. It needs <b>their</b> recent orders and open tickets &mdash; and nothing that belongs to anyone else.</p>
<div class="pipe">
  <div class="step">""" + T("sql") + """<div><b>Scope</b><span>This customer only, last 90 days, rows the requesting agent is allowed to see.</span></div></div>
  <div class="step">""" + T("sql") + """<div><b>Clean &amp; shape</b><span>Dedupe orders, drop test accounts, pick 12 useful columns instead of 80.</span></div></div>
  <div class="step">""" + T("vec") + """<div><b>Retrieve policy text</b><span>Find the refund-policy passages that match the question by meaning.</span></div></div>
  <div class="step">""" + T("app") + """<div><b>Assemble the prompt</b><span>Template + SQL context + retrieved passages, within a token budget.</span></div></div>
  <div class="step">""" + T("llm") + """<div><b>Draft the reply</b><span>Language, tone, summarisation.</span></div></div>
  <div class="step">""" + T("hum") + """<div><b>Approve &amp; send</b><span>The agent owns what the customer receives.</span></div></div>
</div>
<div class="split">
  <div class="yes"><h4>SQL is the right tool for</h4><p>Exact filters, joins across systems, freshness checks, permission scoping, reproducible inputs you can audit later.</p></div>
  <div class="no"><h4>SQL is not the tool for</h4><p>Ranking free text by meaning, writing the reply, or deciding whether a reply is appropriate to send.</p></div>
</div>
<p class="kicker">The cheapest hallucination fix is <b>better input</b>. Every wrong row in the context is a fact the model will confidently repeat.</p>
"""))

# ---------------------------------------------------------------- 03 profiles
S.append(('std', """
<div class="eyebrow">02 &middot; AI-READY DATA PROFILES</div>
<h2>Compress each customer into one row a model can read</h2>
""" + code("""
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
""", cls="sm", label="SNIPPET 1 &middot; COMPACT CUSTOMER CONTEXT") + """
<div class="twocol">
  <div class="card">
    <div class="cardlabel">WHAT THE ASSISTANT RECEIVES</div>
<pre class="json">{ "plan_tier":      "Pro",
  "account_status": "active",
  "lifetime_value": 4820,
  "last_order_at":  "2026-09-18",
  "events_30d":     212,
  "open_tickets":   1 }</pre>
  </div>
  <div class="card soft">
    <ul class="mini">
      <li><b>~60 tokens</b> instead of hundreds of raw order and event rows.</li>
      <li><b>SQL does the arithmetic.</b> LLMs are unreliable at summing rows; they&rsquo;re good at explaining a number.</li>
      <li><b>Materialise &amp; refresh</b> on a schedule; add a <span class="mono">refreshed_at</span> stamp.</li>
    </ul>
  </div>
</div>
<p class="kicker">Compute the facts in SQL. <b>Let the model explain them &mdash; not invent them.</b></p>
"""))

# ---------------------------------------------------------------- 04 observability
S.append(('std', """
<div class="eyebrow">03 &middot; PROMPT &amp; MODEL OBSERVABILITY</div>
<h2>Log every AI call. Query it like any fact table.</h2>
<div class="hflow">
  <div class="hn">""" + T("app") + """<b>Your app</b><i>calls the model</i></div>
  <div class="ha">&rarr;</div>
  <div class="hn">""" + T("llm") + """<b>Model API</b><i>returns tokens</i></div>
  <div class="ha">&rarr;</div>
  <div class="hn hl">""" + T("sql") + """<b>ai_request_log</b><i>one row per call</i></div>
</div>
<div class="schema"><span>request_id</span><span>feature</span><span>prompt_version</span><span>model_version</span><span>input_tokens</span><span>output_tokens</span><span>latency_ms</span><span>cost_usd</span><span>status</span><span>feedback</span></div>
""" + code("""
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
""", cls="xs", label="SNIPPET 2 &middot; DAILY COST / QUALITY MONITOR") + """
<div class="qs"><b>Questions this answers:</b><span>Which prompt version doubled cost?</span><span>Did the new model slow responses?</span><span>Where are errors spiking?</span></div>
<p class="kicker">Averages hide pain: add <b>p95 latency</b> with your warehouse&rsquo;s percentile function. And logged prompts can contain PII &mdash; <b>redact and set retention</b> like any customer data.</p>
"""))

# ---------------------------------------------------------------- 05 quality eval
S.append(('std', """
<div class="eyebrow">04 &middot; QUALITY EVALUATION AT SCALE</div>
<h2>Turn scattered feedback into a quality scorecard</h2>
<p class="lead">Join four signals on <span class="mono">request_id</span>: user thumbs, human review labels, ticket outcomes, and confirmed hallucination tags. Then slice by intent.</p>
<div class="sources">
  <div>""" + T("app") + """<b>User thumbs</b></div>
  <div>""" + T("hum") + """<b>Review labels</b></div>
  <div>""" + T("app") + """<b>Ticket outcomes</b></div>
  <div>""" + T("hum") + """<b>Halluc. tags</b></div>
  <div class="ha">&rarr;</div>
  <div class="hl">""" + T("sql") + """<b>Scorecard</b></div>
</div>
<table class="tbl">
  <tr><th>Support intent</th><th>Convos</th><th>Thumbs-up</th><th>Reviewed</th><th>Halluc. tag</th><th>Resolved, no escalation</th></tr>
  <tr><td>Order status</td><td>4,210</td><td>88%</td><td>312</td><td>0.6%</td><td>81%</td></tr>
  <tr><td>Product how-to</td><td>6,870</td><td>83%</td><td>402</td><td>1.2%</td><td>74%</td></tr>
  <tr><td>Account access</td><td>980</td><td>70%</td><td>188</td><td>2.1%</td><td>55%</td></tr>
  <tr class="bad"><td>Billing dispute</td><td>1,145</td><td>61%</td><td>290</td><td>3.8%</td><td>42%</td></tr>
</table>
<div class="note">Illustrative numbers. The overall average (~80% thumbs-up) looks healthy &mdash; the billing segment is where the assistant is failing.</div>
<div class="split">
  <div class="yes"><h4>SQL does</h4><p>Aggregates, trends by version, segment slices, and <b>stratified samples</b> so reviewers see hard cases, not just easy ones.</p></div>
  <div class="no"><h4>SQL can&rsquo;t</h4><p>Judge whether an answer was actually correct. That takes human reviewers &mdash; or an LLM judge <b>calibrated against</b> them.</p></div>
</div>
<p class="kicker">Thumbs are biased: few users vote, unhappy ones vote more. SQL won&rsquo;t tell you an answer was wrong &mdash; <b>it tells you where to look, and whether it&rsquo;s improving.</b></p>
"""))

# ---------------------------------------------------------------- 06 experiments
S.append(('std', """
<div class="eyebrow">05 &middot; EXPERIMENT ANALYSIS</div>
<h2>Ship prompt v2 like a product change &mdash; not a vibe check</h2>
<div class="ab">
  <div class="abn">Users randomly<br>assigned</div>
  <div class="ha">&rarr;</div>
  <div class="abcol">
    <div class="abv a"><b>A</b> Model X &middot; prompt v1</div>
    <div class="abv b"><b>B</b> Model Y &middot; prompt v2</div>
  </div>
  <div class="ha">&rarr;</div>
  <div class="abn sql">assignments +<br>outcome events<br>&rarr; SQL scorecard</div>
</div>
<table class="tbl">
  <tr><th>Sales-assistant metric</th><th>A &middot; v1</th><th>B &middot; v2</th><th>Change</th></tr>
  <tr><td>Adoption (reps who used it)</td><td>34%</td><td>37%</td><td class="up">+3 pts</td></tr>
  <tr><td>Task completion</td><td>71%</td><td>76%</td><td class="up">+5 pts</td></tr>
  <tr><td>Satisfaction (1&ndash;5)</td><td>4.1</td><td>4.2</td><td class="up">+0.1</td></tr>
  <tr><td>Escalated to a human</td><td>18%</td><td>14%</td><td class="up">&minus;4 pts</td></tr>
  <tr><td>Cost per completed task</td><td>$0.042</td><td>$0.061</td><td class="down">+45%</td></tr>
</table>
<div class="note">Illustrative numbers.</div>
<div class="rules">
  <div><b>Analyse by assigned variant</b>, not by who happened to use the feature.</div>
  <div><b>Check the split</b> &mdash; a 50/50 test that lands at 56/44 means broken assignment.</div>
  <div><b>SQL builds the inputs;</b> the significance test belongs in a stats library or notebook.</div>
  <div><b>Segment the result</b> &mdash; new vs tenured reps, small vs large deals. An average win can hide a segment loss.</div>
  <div><b>+5 pts completion for +45% cost</b> is a business trade-off. Humans decide it.</div>
</div>
<p class="kicker">The winner isn&rsquo;t the variant that <i>feels</i> smarter. It&rsquo;s the one that <b>clears your quality bar at a cost you&rsquo;ll accept at scale.</b></p>
"""))

# ---------------------------------------------------------------- 07 HITL
S.append(('std', """
<div class="eyebrow">06 &middot; HUMAN-IN-THE-LOOP</div>
<h2>Use SQL to decide which drafts a person must see</h2>
""" + code("""
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
""", cls="sm", label="SNIPPET 3 &middot; ROUTE FOR HUMAN REVIEW") + """
<div class="hflow small">
  <div class="hn">""" + T("llm") + """<b>AI draft</b></div>
  <div class="ha">&rarr;</div>
  <div class="hn hl">""" + T("sql") + """<b>Routing rules</b></div>
  <div class="ha">&rarr;</div>
  <div class="hn">""" + T("hum") + """<b>Review queue</b></div>
  <div class="ha">&rarr;</div>
  <div class="hn">""" + T("sql") + """<b>Decisions logged</b></div>
</div>
<div class="rules tight">
  <div><b>&ldquo;Confidence&rdquo; is whatever your app produces</b> &mdash; a classifier score or a model self-rating. It is a signal, not a guarantee.</div>
  <div><b>Calibrate thresholds with SQL:</b> how often did reviewers actually change a <span class="mono">low_confidence</span> draft?</div>
  <div><b>Real-time routing often lives in app code.</b> SQL is where you design, backtest and audit the rules.</div>
</div>
"""))

# ---------------------------------------------------------------- 08 governance
S.append(('std', """
<div class="eyebrow">07 &middot; DATA GOVERNANCE &amp; ACCESS</div>
<h2>An AI tool should never get every column</h2>
<div class="twocol wide">
  <table class="tbl cols">
    <tr><th>customers column</th><th>AI assistant gets</th></tr>
    <tr><td class="m">customer_id</td><td><span class="pill ok">Yes</span></td></tr>
    <tr><td class="m">plan_tier</td><td><span class="pill ok">Yes</span></td></tr>
    <tr><td class="m">region</td><td><span class="pill filt">Row filter</span></td></tr>
    <tr><td class="m">email</td><td><span class="pill mask">Masked</span> j***@acme.com</td></tr>
    <tr><td class="m">phone</td><td><span class="pill no">Excluded</span></td></tr>
    <tr><td class="m">date_of_birth</td><td><span class="pill no">Excluded</span></td></tr>
    <tr><td class="m">internal_notes</td><td><span class="pill no">Excluded</span></td></tr>
  </table>
  <div class="controls">
    <div><b>Least-privilege views</b><span>Grant the AI service account a purpose-built view, never base tables.</span></div>
    <div><b>Row-level security</b><span>The assistant inherits the <i>end user&rsquo;s</i> access &mdash; an EMEA agent sees EMEA customers.</span></div>
    <div><b>Masking</b><span>Mask or tokenise PII at the column; don&rsquo;t hope the model ignores it.</span></div>
    <div><b>Auditability</b><span>Log which identity queried what, when &mdash; and join it to the AI request log.</span></div>
  </div>
</div>
<div class="impl"><b>Same idea, different syntax:</b> PostgreSQL row-level security &middot; SQL Server RLS &amp; dynamic data masking &middot; Snowflake row access &amp; masking policies &middot; BigQuery authorized views &amp; policy tags.</div>
<div class="warnbox"><b>A prompt that says &ldquo;don&rsquo;t reveal emails&rdquo; is not access control.</b> Instructions can be ignored or bypassed by prompt injection. Permissions enforced in the database can&rsquo;t be talked out of.</div>
<p class="kicker">Rule of thumb: <b>if a column would be a problem in a screenshot, it&rsquo;s a problem in a prompt.</b></p>
"""))

# ---------------------------------------------------------------- 09 semantic layer
S.append(('std', """
<div class="eyebrow">08 &middot; THE SEMANTIC LAYER MATTERS</div>
<h2>One definition of &ldquo;active&rdquo; &mdash; before AI answers anything</h2>
<p class="lead">&ldquo;How many active customers do we have?&rdquo; Three teams, three honest answers:</p>
<table class="tbl">
  <tr><th>Team</th><th>&ldquo;Active customer&rdquo; means</th><th>Answer</th></tr>
  <tr><td>Marketing</td><td>Logged in during the last 30 days</td><td>18,400</td></tr>
  <tr><td>Finance</td><td>Paid an invoice in the last 90 days</td><td>11,250</td></tr>
  <tr><td>Product</td><td>&ge; 3 key actions in the last 28 days</td><td>7,900</td></tr>
</table>
<div class="note">Illustrative numbers. The same trap hides in every business noun:</div>
<div class="defs">
  <div><b>&ldquo;Resolved ticket&rdquo;</b><span>Closed by an agent? Or closed <i>and</i> not reopened within 7 days?</span></div>
  <div><b>&ldquo;Qualified lead&rdquo;</b><span>Filled in a form? Or matches the ideal-customer profile <i>and</i> accepted by sales?</span></div>
</div>
<div class="hflow">
  <div class="hn">""" + T("llm") + """<b>Maps the question</b><i>to a named metric</i></div>
  <div class="ha">&rarr;</div>
  <div class="hn hl">""" + T("sql") + """<b>Governed metric</b><i>one definition, owner, version</i></div>
  <div class="ha">&rarr;</div>
  <div class="hn">""" + T("app") + """<b>Answer + definition</b><i>cited back to the user</i></div>
</div>
<div class="rules tight">
  <div><b>Metric owners (humans)</b> agree the definition; the semantic layer or governed views encode it once.</div>
  <div><b>The LLM translates language to metric names</b> &mdash; it should not re-derive the business logic on every question.</div>
</div>
<p class="kicker">AI doesn&rsquo;t resolve ambiguity in your metrics. <b>It automates it &mdash; at the speed of chat.</b></p>
"""))

# ---------------------------------------------------------------- 10 CTA
S.append(('std', """
<div class="eyebrow">THE TAKEAWAY</div>
<h2 class="quote">AI makes answers faster. <span>SQL makes the inputs, measurements, and decisions trustworthy.</span></h2>
<div class="rolemap">
  <div>""" + T("sql") + """<p><b>Select, measure, govern.</b> Trusted context, cost and quality metrics, access rules, one metric definition.</p></div>
  <div>""" + T("vec") + """<p><b>Find relevant unstructured text</b> &mdash; policies, docs, past tickets &mdash; by meaning.</p></div>
  <div>""" + T("llm") + """<p><b>Understand and generate language.</b> Summarise, draft, classify, translate intent.</p></div>
  <div>""" + T("app") + """<p><b>Orchestrate and enforce in real time.</b> Prompts, retries, routing, guardrails.</p></div>
  <div>""" + T("hum") + """<p><b>Define, judge, decide.</b> Metric definitions, quality calls, trade-offs, accountability.</p></div>
</div>
<div class="cta">
  <div class="cta-line">Where could SQL make your AI workflow more reliable?</div>
  <div class="cta-sub">Share your most valuable SQL-for-AI use case in the comments &mdash; and save this for your next AI project review.</div>
  <div class="cta-by"><b>Sagar Rathkanthiwar</b> &middot; Data &amp; AI Professional &middot; follow for more field guides</div>
</div>
<div class="srcs"><b>Implementation note:</b> table names are generic and examples use broadly portable SQL. Date arithmetic, percentile functions, row-level security, masking policies and semantic-layer tooling differ across PostgreSQL, SQL Server, Snowflake, BigQuery, Databricks and others &mdash; details vary by warehouse and product architecture.</div>
"""))

# ---------------------------------------------------------------- template
CSS = """
:root{
  --ink:#10172a; --body:#374257; --muted:#6b7488; --line:#e3e1da;
  --paper:#fbfaf7; --soft:#f2f0ea;
  --sql:#0b6e69; --llm:#6a48c9; --vec:#2360a5; --app:#4a5568; --hum:#b0580f;
  --accent:#0b6e69; --rose:#b8324f;
}
*{box-sizing:border-box;margin:0;padding:0;}
@page{ size:810pt 1012.5pt; margin:0; }
html,body{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ font-family:"Segoe UI","Inter",Arial,sans-serif; color:var(--body); background:#fff; }
.slide{ position:relative; width:1080px; height:1350px; overflow:hidden;
  padding:74px 72px 118px; background:var(--paper);
  page-break-after:always; display:flex; flex-direction:column; }
.slide:last-child{ page-break-after:auto; }
.slide > *{ flex-shrink:0; }
.accentbar{ position:absolute; top:0; left:0; width:100%; height:10px;
  background:linear-gradient(90deg,var(--sql) 0 40%,var(--vec) 40% 55%,var(--llm) 55% 75%,var(--app) 75% 88%,var(--hum) 88%); }
.foot{ position:absolute; left:0; right:0; bottom:0; height:70px; background:var(--ink);
  display:flex; align-items:center; justify-content:space-between; padding:0 72px; }
.foot span{ color:#fff; font-size:20px; letter-spacing:.04em; font-weight:600; }
.foot .r{ color:#9fb0cc; font-weight:500; letter-spacing:.12em; }

.eyebrow{ font-size:21px; font-weight:700; letter-spacing:.2em; color:var(--sql); margin-bottom:18px; }
.eyebrow.light{ color:#7fd3c8; }
h2{ font-family:Georgia,"Times New Roman",serif; font-size:54px; line-height:1.1; letter-spacing:-.015em;
  color:var(--ink); font-weight:700; margin-bottom:24px; }
.lead{ font-size:26px; line-height:1.45; margin-bottom:22px; }
.lead b{ color:var(--ink); }
.kicker{ margin-top:auto; font-size:24px; line-height:1.45; border-left:8px solid var(--sql);
  background:#e8f1ef; padding:20px 26px; border-radius:0 14px 14px 0; }
.kicker b{ color:var(--ink); }
.mono{ font-family:Consolas,"Cascadia Mono",monospace; font-size:.88em; background:#e9e7e0; color:#1b2a4a;
  padding:1px 7px; border-radius:6px; }
.note{ font-size:18px; color:var(--muted); font-style:italic; margin:-8px 0 20px; }

.tag{ display:inline-block; font-size:14px; font-weight:800; letter-spacing:.1em; color:#fff;
  padding:5px 10px; border-radius:6px; white-space:nowrap; line-height:1.2; }
.tag.sql{ background:var(--sql);} .tag.llm{ background:var(--llm);} .tag.vec{ background:var(--vec);}
.tag.app{ background:var(--app);} .tag.hum{ background:var(--hum);}

.codewrap{ margin-bottom:22px; }
.codelabel{ display:inline-block; background:var(--sql); color:#fff; font-size:15px; font-weight:800;
  letter-spacing:.12em; padding:7px 14px; border-radius:10px 10px 0 0; }
.code{ font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:21px; line-height:1.5;
  background:#111a2e; color:#dde5f3; padding:24px 28px; border-radius:0 14px 14px 14px; white-space:pre; overflow:hidden; }
.code.sm{ font-size:19.5px; }
.code.xs{ font-size:18px; line-height:1.48; padding:20px 24px; }
.code .k{ color:#86b6ff; font-weight:600; } .code .f{ color:#f0b660; } .code .s{ color:#86d9a8; }
.code .n{ color:#f59e9e; } .code .c{ color:#8390ad; font-style:italic; }

/* pipeline */
.pipe{ display:flex; flex-direction:column; gap:0; margin-bottom:22px; border-left:3px dashed #c9c5b9; margin-left:14px; }
.step{ display:flex; align-items:flex-start; gap:18px; padding:9px 0 9px 24px; position:relative; }
.step:before{ content:""; position:absolute; left:-9px; top:21px; width:15px; height:15px; border-radius:50%;
  background:var(--paper); border:3px solid #9a9587; }
.step .tag{ width:190px; min-width:190px; text-align:center; margin-top:3px; }
.step b{ font-size:23px; color:var(--ink); display:block; }
.step > div span{ font-size:20px; line-height:1.35; color:var(--body); }

.split{ display:flex; gap:18px; margin-bottom:22px; }
.split > div{ flex:1; border-radius:14px; padding:18px 22px; }
.split .yes{ background:#e3f0ed; border-top:6px solid var(--sql); }
.split .no{ background:#f1ece6; border-top:6px solid var(--hum); }
.split h4{ font-size:19px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink); margin-bottom:8px; }
.split p{ font-size:20px; line-height:1.4; }
.split b{ color:var(--ink); }

.twocol{ display:flex; gap:18px; margin-bottom:22px; }
.twocol > *{ flex:1; }
.card{ background:#fff; border:2px solid var(--line); border-radius:14px; padding:18px 20px; }
.card.soft{ background:var(--soft); border-color:var(--soft); }
.cardlabel{ font-size:14px; font-weight:800; letter-spacing:.12em; color:var(--sql); margin-bottom:10px; }
.json{ font-family:Consolas,monospace; font-size:18px; line-height:1.5; color:var(--ink); white-space:pre; }
.mini{ list-style:none; display:flex; flex-direction:column; gap:10px; }
.mini li{ font-size:19px; line-height:1.38; padding-left:20px; position:relative; }
.mini li:before{ content:""; position:absolute; left:0; top:9px; width:9px; height:9px; border-radius:2px; background:var(--sql); }
.mini b{ color:var(--ink); }

.hflow{ display:flex; align-items:stretch; gap:10px; margin-bottom:18px; }
.hn{ flex:1; background:#fff; border:2px solid var(--line); border-radius:14px; padding:14px 16px; display:flex;
  flex-direction:column; gap:7px; align-items:flex-start; }
.hn.hl{ border-color:var(--sql); background:#eaf3f1; }
.hn b{ font-size:21px; color:var(--ink); }
.hn i{ font-style:normal; font-size:17px; color:var(--muted); }
.ha{ align-self:center; font-size:30px; color:#9a9587; font-weight:700; }
.hflow.small .hn{ padding:11px 13px; }
.hflow.small .hn b{ font-size:19px; }

.schema{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:18px; }
.schema span{ font-family:Consolas,monospace; font-size:17px; background:#e9e7e0; color:#1b2a4a; padding:5px 11px; border-radius:7px; }

.tbl{ width:100%; border-collapse:separate; border-spacing:0; margin-bottom:18px; background:#fff;
  border:2px solid var(--line); border-radius:14px; overflow:hidden; }
.tbl th{ background:var(--ink); color:#fff; font-size:17px; letter-spacing:.04em; text-align:left; padding:13px 16px; font-weight:700; }
.tbl td{ font-size:21px; padding:12px 16px; border-top:1px solid var(--line); color:var(--ink); }
.tbl tr.bad td{ background:#f9e9ec; color:#7c1d33; font-weight:700; }
.tbl td.up{ color:var(--sql); font-weight:800; } .tbl td.down{ color:var(--rose); font-weight:800; }
.tbl td.m{ font-family:Consolas,monospace; font-size:19px; }
.tbl.cols td{ padding:11px 14px; font-size:18px; }

.pill{ display:inline-block; font-size:15px; font-weight:800; letter-spacing:.05em; padding:4px 10px; border-radius:999px; margin-right:6px; }
.pill.ok{ background:#d7ece8; color:var(--sql);} .pill.no{ background:#f6dde3; color:var(--rose);}
.pill.mask{ background:#f5e6d3; color:var(--hum);} .pill.filt{ background:#dde7f5; color:var(--vec);}
.twocol.wide > .tbl{ flex:1.05; margin-bottom:0; }
.controls{ display:flex; flex-direction:column; gap:12px; }
.controls div{ background:#fff; border-left:6px solid var(--sql); border-radius:0 12px 12px 0; padding:12px 16px; }
.controls b{ display:block; font-size:20px; color:var(--ink); margin-bottom:3px; }
.controls span{ font-size:17.5px; line-height:1.38; }
.warnbox{ background:#f9e9ec; border:2px solid #efc3cd; border-radius:14px; padding:18px 22px; font-size:21px; line-height:1.42; margin-bottom:22px; }
.warnbox b{ color:#7c1d33; }

.ab{ display:flex; align-items:center; gap:10px; margin-bottom:20px; }
.abn{ background:#fff; border:2px solid var(--line); border-radius:14px; padding:14px 16px; font-size:19px; line-height:1.3; color:var(--ink); font-weight:600; text-align:center; flex:1; }
.abn.sql{ border-color:var(--sql); background:#eaf3f1; }
.abcol{ display:flex; flex-direction:column; gap:10px; flex:1.4; }
.abv{ border-radius:12px; padding:12px 16px; font-size:19px; color:var(--ink); background:#fff; border:2px solid var(--line); }
.abv b{ display:inline-block; width:34px; height:34px; border-radius:8px; color:#fff; text-align:center; line-height:34px; margin-right:10px; }
.abv.a b{ background:var(--app);} .abv.b b{ background:var(--llm);}

.rules{ display:flex; flex-direction:column; gap:12px; margin-bottom:22px; }
.rules.tight{ gap:10px; }
.rules div{ font-size:21px; line-height:1.4; padding-left:28px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:10px; width:13px; height:13px; border-radius:4px; background:var(--sql); }
.rules b{ color:var(--ink); }

h2.quote{ font-size:52px; line-height:1.14; margin-bottom:30px; }
h2.quote span{ color:var(--sql); }
.rolemap{ display:flex; flex-direction:column; gap:14px; margin-bottom:26px; }
.rolemap > div{ display:flex; align-items:flex-start; gap:18px; background:#fff; border:2px solid var(--line); border-radius:14px; padding:18px 20px; }
.rolemap .tag{ min-width:160px; text-align:center; margin-top:3px; font-size:15px; }
.rolemap p{ font-size:21.5px; line-height:1.38; } .rolemap b{ color:var(--ink); }
.cta{ background:var(--ink); border-radius:18px; padding:28px 32px; margin-top:auto; }
.cta-line{ font-family:Georgia,serif; font-size:34px; line-height:1.25; color:#fff; font-weight:700; }
.cta-sub{ margin-top:12px; font-size:21px; line-height:1.4; color:#c8d2e4; }
.cta-by{ margin-top:14px; font-size:19px; color:#7fd3c8; } .cta-by b{ color:#fff; }
.srcs{ margin-top:16px; font-size:15.5px; line-height:1.45; color:var(--muted); } .srcs b{ color:var(--body); }

.qs{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:16px; font-size:19px; }
.qs b{ color:var(--ink); margin-right:4px; }
.qs span{ background:#fff; border:2px solid var(--line); border-radius:999px; padding:6px 14px; color:var(--ink); }
.sources{ display:flex; gap:10px; align-items:stretch; margin-bottom:20px; }
.sources > div:not(.ha){ flex:1; background:#fff; border:2px solid var(--line); border-radius:12px; padding:11px 12px;
  display:flex; flex-direction:column; gap:6px; align-items:flex-start; }
.sources > div.hl{ border-color:var(--sql); background:#eaf3f1; }
.sources b{ font-size:18px; color:var(--ink); }
.sources .tag{ font-size:12px; padding:4px 8px; }
.impl{ font-size:18px; line-height:1.45; color:var(--body); background:var(--soft); border-radius:12px; padding:14px 18px; margin:22px 0 18px; }
.impl b{ color:var(--ink); }
.defs{ display:flex; gap:16px; margin-bottom:22px; }
.defs div{ flex:1; background:#fff; border:2px solid var(--line); border-radius:12px; padding:14px 18px; }
.defs b{ display:block; font-size:20px; color:var(--ink); margin-bottom:5px; }
.defs span{ font-size:18px; line-height:1.4; }
/* cover */
.cover{ background:var(--ink); color:#fff; padding:90px 72px 118px; }
.cover-title{ font-family:Georgia,"Times New Roman",serif; font-size:100px; line-height:1.02; font-weight:700; letter-spacing:-.025em; color:#fff; }
.cover-title .hl{ color:#6fd0c3; }
.cover-sub{ margin-top:30px; font-size:34px; line-height:1.35; color:#bcc7dc; }
.coverflow{ margin-top:52px; display:flex; flex-wrap:wrap; align-items:center; gap:12px; }
.cf-node{ flex:1; border:2px solid #34425f; border-radius:16px; padding:18px 18px; background:#172139; }
.cf-node b{ display:block; font-size:27px; color:#fff; margin-bottom:6px; }
.cf-node i{ font-style:normal; font-size:17px; color:#9fb0cc; }
.cf-node.sql{ border-color:#2ba597; background:#0f3b3d; } .cf-node.sql b{ color:#7fe0d2; }
.cf-node.ai{ border-color:#7a5fd6; background:#241c46; } .cf-node.ai b{ color:#c3b3ff; }
.cf-arrow{ font-size:32px; color:#6f7fa0; font-weight:700; }
.cf-back{ width:100%; text-align:center; font-size:18px; color:#8ea0c2; letter-spacing:.03em; margin-top:4px; }
.chips{ margin-top:38px; display:flex; flex-wrap:wrap; gap:12px; }
.chips span{ border:2px solid #34425f; color:#a9c4ee; border-radius:999px; padding:8px 18px; font-size:20px; font-weight:600; }
.cover-foot{ margin-top:auto; }
.cover-foot .rule{ height:3px; background:#2a3654; margin-bottom:26px; }
.cover-by{ font-size:30px; font-weight:700; color:#fff; }
.cover-by span{ display:block; font-size:23px; font-weight:500; color:#9fb0cc; margin-top:6px; }
.cover-meta{ margin-top:18px; font-size:22px; color:#6fd0c3; font-weight:600; letter-spacing:.03em; }
"""

TITLE = "SQL&rsquo;s New Job in the AI Era"
BODY = []
for i, (kind, content) in enumerate(S, start=1):
    cls = "slide" + (" cover" if kind == "cover" else "")
    if kind == 'cover':
        foot = ('<div class="foot"><span>%s</span><span class="r">01 / %02d &nbsp;&middot;&nbsp; SWIPE &rarr;</span></div>'
                % (TITLE, len(S)))
    else:
        foot = ('<div class="foot"><span>Sagar Rathkanthiwar &nbsp;|&nbsp; %s</span><span class="r">%02d / %02d</span></div>'
                % (TITLE, i, len(S)))
    BODY.append('<section class="%s"><div class="accentbar"></div>%s%s</section>' % (cls, content, foot))

CHECK = """<script>
window.addEventListener('load',()=>{const r=[];document.querySelectorAll('.slide').forEach((s,i)=>{
const lim=s.getBoundingClientRect().top+1350-70-16;let mx=0;
s.querySelectorAll(':scope > *:not(.foot):not(.accentbar)').forEach(c=>{mx=Math.max(mx,c.getBoundingClientRect().bottom)});
const pre=[...s.querySelectorAll('pre')].some(p=>p.scrollWidth>p.clientWidth+1);
r.push((i+1)+':'+Math.round(lim-mx)+(pre?'(PRE-OVERFLOW)':''));});
const d=document.createElement('div');d.id='fitreport';d.textContent=r.join(' ');document.body.appendChild(d);});
</script>""" if os.environ.get("FITCHECK") else ""

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>SQL's New Job in the AI Era</title><style>%s</style></head><body>%s%s</body></html>""" % (
    CSS, "\n".join(BODY), CHECK)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   ("_fitcheck.html" if CHECK else "sql_ai_workflows_carousel_2026-09-24.html"))
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
