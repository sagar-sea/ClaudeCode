# -*- coding: utf-8 -*-
"""Builds the 'Python Cheat Sheet for the AI Era' LinkedIn carousel HTML (1080x1350 slides).

Palette sampled from the reference carousel PDF: cream paper #F2ECE1, terracotta
accent #E76F51, near-black ink #231F20, dark code panel #1B1F23.
"""
import html, re, io, os

KEYWORDS = (r"False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|"
            r"except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|"
            r"return|try|while|with|yield")
BUILTINS = (r"print|len|range|open|dict|list|set|tuple|str|int|float|bool|max|min|sum|sorted|"
            r"enumerate|zip|isinstance|type|eval|exec|super|abs|round|any|all|map|filter")

TOKEN = re.compile(
    r"(?P<comment>\#.*$)"
    r"|(?P<string>[fFrRbBuU]{0,2}(?:\"\"\".*?\"\"\"|'''.*?'''|\"[^\"\n]*\"|'[^'\n]*'))"
    r"|(?P<decorator>^\s*@[\w.]+)"
    r"|(?P<kw>\b(?:" + KEYWORDS + r")\b)"
    r"|(?P<bi>\b(?:" + BUILTINS + r")\b)"
    r"|(?P<num>\b\d+(?:\.\d+)?\b)"
)

CLS = {"comment": "c", "string": "s", "decorator": "d", "kw": "k", "bi": "b", "num": "n"}


def highlight(code_src: str) -> str:
    out = []
    for line in code_src.split("\n"):
        pos, buf = 0, []
        for m in TOKEN.finditer(line):
            buf.append(html.escape(line[pos:m.start()]))
            kind = m.lastgroup
            buf.append('<span class="%s">%s</span>' % (CLS[kind], html.escape(m.group())))
            pos = m.end()
        buf.append(html.escape(line[pos:]))
        out.append("".join(buf))
    return "\n".join(out)


def code(src: str, cls: str = "", plain: bool = False) -> str:
    body = html.escape(src.strip("\n")) if plain else highlight(src.strip("\n"))
    return '<pre class="code %s">%s</pre>' % (cls, body)


# ---------------------------------------------------------------- slides
S = []

S.append(('cover', """
<div class="eyebrow">PYTHON &middot; PRACTICAL FIELD GUIDE</div>
<h1 class="cover-title">Python<br>Cheat Sheet<br><span class="hl">for the AI&nbsp;Era</span></h1>
<p class="cover-sub">AI writes the first draft.<br>You still own what ships.</p>
<div class="chips">
  <span>Requirements</span><span>Reading code</span><span>Logic</span><span>Errors</span>
  <span>Tests</span><span>Secrets</span><span>Dependencies</span><span>Maintainability</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">12 slides &middot; save for later &rarr;</div>
</div>
"""))

S.append(('std', """
<div class="eyebrow">THE HOOK</div>
<h2>It runs. That doesn't<br>make it right.</h2>
<div class="stats">
  <div class="stat"><b>90% use it &middot; 30% barely trust it</b><span>DORA surveyed ~5,000 practitioners: over 80% report AI made them more productive, yet 30% report little or no trust in the code it returns.</span></div>
  <div class="stat"><b>45% of samples had a security flaw</b><span>Veracode tested 100+ models. Python failed 38&ndash;45% of security tasks &mdash; and security stayed flat even as the models got better at correctness.</span></div>
  <div class="stat"><b>1 in 5 suggested packages didn't exist</b><span>Across 576,000 generated samples, 19.7% of imported packages were hallucinated &mdash; and 43% of those fake names reappear on repeat prompts.</span></div>
</div>
<p class="kicker">The scarce skill moved from <b>writing</b> Python to <b>judging</b> Python. Everything after this slide is the judging part.</p>
"""))

S.append(('std', """
<div class="eyebrow">THE FRAME</div>
<h2>Split the work into three lanes</h2>
<div class="lanes">
  <div class="lane one"><div class="lane-tag">ASK AI</div>
    <p>First drafts, boilerplate, docstrings, test scaffolding, alternate approaches, and plain-English walkthroughs of code you inherited.</p></div>
  <div class="lane two"><div class="lane-tag">VERIFY YOURSELF</div>
    <p>Requirements, data shapes and types, business rules, error paths, the security surface, and whether the output actually reconciles.</p></div>
  <div class="lane three"><div class="lane-tag">CATCH BEFORE SHIPPING</div>
    <p>Bare <span class="mono">except</span>, hard-coded keys, <span class="mono">eval</span>, invented or unpinned packages, O(n&sup2;) loops, mutable defaults, and code with no tests.</p></div>
</div>
<p class="kicker">AI is fast at Python. You are accountable for the business rule, the blast radius, and the person who maintains this next.</p>
"""))

S.append(('std', """
<div class="eyebrow">01 &middot; REQUIREMENTS</div>
<h2>A vague prompt is<br>a vague spec</h2>
<div class="badline bad"><b>Weak prompt</b>&nbsp; "Write a Python script to clean my sales data."</div>
""" + code("""
Input:   sales.csv, ~2M rows
         order_id (str), order_ts (ISO 8601, may be blank),
         amount (str, may contain "$" and ","), region (str)
Output:  DataFrame, one row per order_id, amount as float
Rules:   drop blank order_ts; uppercase region;
         duplicate order_id -> keep the latest order_ts
Limits:  pandas 2.x, runs in under 60s, no network calls

Then list your assumptions and the edge cases you skipped.
""", plain=True) + """
<p class="kicker"><b>Catch:</b> code with no stated assumptions still has assumptions &mdash; you just inherit them silently. Make "list what you assumed" the last line of every prompt.</p>
"""))

S.append(('std', """
<div class="eyebrow">02 &middot; READING CODE</div>
<h2>Know what each<br>line hands back</h2>
<p class="lead">Most AI bugs are <b>shape and type</b> bugs. The model guessed what your data looks like; it has never seen it.</p>
""" + code("""
row = {"id": 7, "tags": ["a", "b"], "amount": None}

row["email"]              # KeyError -> crash in production
row.get("email", "")      # safe default
row["tags"][0]            # IndexError if the list is empty

# Nested access AI assumes is always populated
row["user"]["email"]                # can KeyError at either level
(row.get("user") or {}).get("email")

# Every one of these is falsy:  0  0.0  ""  []  {}  None
if row["amount"]:                 # silently skips a real 0.0
if row["amount"] is not None:     # what you actually meant
""") + """
<p class="kicker"><b>Ask AI:</b> "Walk through this line by line and tell me the type of every name." Then confirm it against real data with <span class="mono">type()</span>, <span class="mono">len()</span> and <span class="mono">df.dtypes</span>.</p>
"""))

S.append(('std', """
<div class="eyebrow">03 &middot; LOOPS &amp; COMPREHENSIONS</div>
<h2>Shorter isn't the goal.<br>Clear and cheap is.</h2>
""" + code("""
# Common first draft
result = []
for r in rows:
    if r["region"] == "US":
        result.append(r["amount"] * 1.08)

# Same thing - fine while it stays this simple
result = [r["amount"] * 1.08 for r in rows if r["region"] == "US"]

# Hidden O(n^2): a list scan inside a loop over n rows
flagged = [r for r in rows if r["id"] in blocked_list]   # slow
flagged = [r for r in rows if r["id"] in blocked_set]    # O(1) lookups
""") + """
<div class="rules tight">
  <div><b>Nested or triple-conditional comprehensions</b> are worse than the loop. Write the loop.</div>
  <div><b>Row-by-row loops over a DataFrame</b> (<span class="mono">iterrows</span>) are the slow default AI reaches for &mdash; vectorise or <span class="mono">groupby</span> instead.</div>
</div>
"""))

S.append(('std', """
<div class="eyebrow">04 &middot; ERRORS, FILES &amp; LOGGING</div>
<h2>Handle the failure<br>you can name</h2>
""" + code("""
# First draft: hides the reason, and never closes the file
try:
    data = json.loads(open("config.json").read())
except:                       # also swallows Ctrl+C and your own typos
    data = {}

# What to ship
from pathlib import Path
log = logging.getLogger(__name__)
try:
    data = json.loads(Path("config.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    log.warning("config.json missing; falling back to defaults")
    data = {}
except json.JSONDecodeError as e:
    raise ValueError(f"config.json is malformed: {e}") from e
""") + """
<p class="kicker"><b>Three questions per <span class="mono">try</span>:</b> which exceptions can this actually raise, which do I want to recover from, and does the handle close if it blows up? Always pass <span class="mono">encoding</span>. And <span class="mono">print()</span> is not logging.</p>
"""))

S.append(('std', """
<div class="eyebrow">05 &middot; TESTS &amp; EDGE CASES</div>
<h2>You supply the cases.<br>AI writes the harness.</h2>
""" + code("""
@pytest.mark.parametrize("gross,refund,expected", [
    (100.0,   0.0, 100.0),
    (100.0, 100.0,   0.0),    # fully refunded
    (  0.0,   0.0,   0.0),    # empty order
    (100.0, 150.0,   0.0),    # refund > order -> clamp at 0
])
def test_net_amount(gross, refund, expected):
    assert net_amount(gross, refund) == pytest.approx(expected)

def test_missing_amount_is_rejected():
    with pytest.raises(ValueError):
        net_amount(None, 0.0)
""") + """
<div class="rules tight">
  <div><b>The standing checklist:</b> empty, one, many &middot; zero and negative &middot; <span class="mono">None</span> &middot; duplicates &middot; non-ASCII names &middot; timezone and month boundaries &middot; input too big for memory.</div>
  <div><b>Why you pick them:</b> a model optimises for tests that pass, not for the case that takes production down.</div>
</div>
"""))

S.append(('std', """
<div class="eyebrow">06 &middot; SECRETS &amp; UNSAFE CALLS</div>
<h2>Three patterns to<br>reject on sight</h2>
""" + code("""
# 1. eval on anything a user can influence = code execution
rule = eval(user_input)                  # never
rule = ast.literal_eval(user_input)      # data only, no code

# 2. A hard-coded key is in git history forever
client = OpenAI(api_key="sk-proj-9f3a...")   # never
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 3. shell=True turns a filename into a command
subprocess.run(f"convert {path}", shell=True)  # never
subprocess.run(["convert", path])        # list args, no shell
""") + """
<p class="kicker">Also review on sight: <span class="mono">pickle.load</span>, <span class="mono">yaml.load</span> without <span class="mono">SafeLoader</span>, <span class="mono">verify=False</span>, and f-strings built into SQL. <b>29 million</b> hard-coded secrets hit public GitHub in 2025, and AI-assisted commits leaked at roughly <b>double</b> the baseline rate. If one shipped: rotate it, don't just delete the line.</p>
"""))

S.append(('std', """
<div class="eyebrow">07 &middot; ENVIRONMENTS &amp; DEPENDENCIES</div>
<h2>Pin it, and check<br>the package is real</h2>
""" + code("""
python -m venv .venv
.venv\\Scripts\\activate          # Windows   (source .venv/bin/activate)
pip install -r requirements.txt
pip freeze > requirements.lock   # exact versions, reproducible run

# requirements.txt
pandas==2.2.3                    # pinned: same build next month
pandas>=2                        # unpinned: a silent upgrade away
""", plain=True) + """
<div class="rules tight">
  <div><b>Verify every unfamiliar import</b> before installing: does it exist on PyPI, does the repo match, when was the last release, is the spelling exactly right?</div>
  <div><b>Never <span class="mono">pip install</span> a name you first saw in a chat window.</b> Attackers now register hallucinated package names on purpose &mdash; the same fakes recur, so they are worth squatting.</div>
  <div><b>One environment per project, never global installs</b> &mdash; and commit the lock file, so "works on my machine" stops being a defence.</div>
</div>
"""))

S.append(('std', """
<div class="eyebrow">08 &middot; MAINTAINABILITY</div>
<h2>Write it for the<br>person reviewing it</h2>
""" + code("""
def net_amount(gross: Decimal, refund: Decimal) -> Decimal:
    '''Revenue after refunds. Never returns a negative.'''
    if gross is None:
        raise ValueError("gross is required")
    return max(Decimal("0"), gross - refund)

# Mutable default: one list shared by every call, forever
def add(item, bucket=[]):        # wrong
def add(item, bucket=None):      # right
    bucket = [] if bucket is None else bucket

0.1 + 0.2 == 0.3                 # False - never use float for money
""") + """
<p class="kicker"><b>Why it matters:</b> across 211M changed lines, copy-pasted code rose from 8.3% to 12.3% while refactoring signals fell by more than half. Type hints, docstrings, small functions and a <span class="mono">ruff</span> + <span class="mono">mypy</span> pass are how volume stays reviewable.</p>
"""))

S.append(('close', """
<div class="eyebrow">SHIP CHECKLIST</div>
<h2>Six checks before<br>you merge it</h2>
<ol class="checks">
  <li><b>I can explain every line</b> in my own words.</li>
  <li><b>Types and shapes verified</b> on real data, not assumed.</li>
  <li><b>Errors are specific and logged</b> &mdash; no bare <span class="mono">except</span>, no swallowed failures.</li>
  <li><b>Tests cover</b> empty, zero, <span class="mono">None</span>, duplicate and too-big.</li>
  <li><b>No secrets, no <span class="mono">eval</span>, no <span class="mono">shell=True</span></b> anywhere in the diff.</li>
  <li><b>Dependencies pinned</b> and every package confirmed to exist.</li>
</ol>
<div class="cta">
  <div class="cta-line">Save this &mdash; then run check #1 on the last Python file AI wrote for you.</div>
  <div class="cta-by">Follow <b>Sagar Rathkanthiwar</b> for practical Data &amp; AI</div>
</div>
<div class="srcs"><b>Sources:</b> DORA, State of AI-assisted Software Development 2025 (dora.dev) &middot; Veracode 2025 GenAI Code Security Report (veracode.com) &middot; GitGuardian State of Secrets Sprawl 2026 (gitguardian.com) &middot; Spracklen et al., package hallucination study, USENIX Security 2025 &middot; GitClear AI Code Quality Research 2025 (gitclear.com). Examples are illustrative; verify behaviour against your Python and library versions.</div>
"""))

# ---------------------------------------------------------------- template
CSS = """
:root{
  --ink:#231F20; --body:#4B443F; --muted:#8A7F76; --line:#DED3C3;
  --accent:#E76F51; --slate:#264653; --teal:#2A9D8F; --amber:#C98A17;
  --paper:#F2ECE1; --soft:#E9E1D3;
}
*{box-sizing:border-box;margin:0;padding:0;}
@page{ size:810pt 1012.5pt; margin:0; }
html,body{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{ font-family:"Segoe UI","Inter",Arial,sans-serif; color:var(--body); background:var(--paper); }
.slide{
  position:relative; width:1080px; height:1350px; overflow:hidden;
  padding:84px 78px 128px; background:var(--paper);
  page-break-after:always; display:flex; flex-direction:column;
}
.slide:last-child{ page-break-after:auto; }

/* footer */
.foot{ position:absolute; left:0; right:0; bottom:0; height:72px; background:var(--ink);
  display:flex; align-items:center; justify-content:space-between; padding:0 78px; }
.foot span{ color:var(--paper); font-size:21px; letter-spacing:.045em; font-weight:600; }
.foot .r{ color:#E76F51; font-weight:700; letter-spacing:.12em; }
.accentbar{ position:absolute; top:0; left:0; width:100%; height:10px; background:var(--accent); }

/* type */
.eyebrow{ font-size:22px; font-weight:800; letter-spacing:.2em; color:var(--accent); margin-bottom:26px; }
h2{ font-size:64px; line-height:1.1; letter-spacing:-.022em; color:var(--ink); font-weight:800; margin-bottom:32px; }
.lead{ font-size:30px; line-height:1.45; color:var(--body); margin-bottom:28px; }
.lead b{ color:var(--ink); }
.kicker{ margin-top:auto; font-size:26px; line-height:1.5; color:var(--body);
  border-left:8px solid var(--accent); background:var(--soft); padding:26px 30px; border-radius:0 14px 14px 0; }
.kicker b{ color:var(--ink); }
.mono{ font-family:Consolas,"Cascadia Mono",monospace; font-size:.9em; background:#E3D9C8; color:#3A2F28;
  padding:2px 8px; border-radius:6px; }

/* code */
.code{ font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:22px; line-height:1.58;
  background:#1B1F23; color:#E4DED4; padding:30px 32px; border-radius:16px; white-space:pre;
  margin-bottom:28px; overflow:hidden; }
.code .k{ color:#F4A261; font-weight:600; }
.code .b{ color:#E9C46A; }
.code .s{ color:#8FCFA8; }
.code .n{ color:#9BC8E8; }
.code .d{ color:#F08A6E; }
.code .c{ color:#93999E; font-style:italic; }

/* cover */
.cover{ background:var(--paper); padding:96px 78px 128px; }
.cover-title{ font-size:112px; line-height:1.02; font-weight:800; letter-spacing:-.035em; color:var(--ink); }
.cover-title .hl{ color:var(--accent); }
.cover-sub{ margin-top:40px; font-size:38px; line-height:1.35; color:#6B615A; font-weight:400; }
.chips{ margin-top:50px; display:flex; flex-wrap:wrap; gap:14px; max-width:840px; }
.chips span{ border:2px solid var(--line); color:#7A6E64; border-radius:999px; padding:10px 22px;
  font-size:23px; font-weight:600; background:rgba(255,255,255,.45); }
.cover-foot{ margin-top:auto; }
.cover-foot .rule{ height:3px; background:var(--line); margin-bottom:34px; }
.cover-by{ font-size:32px; font-weight:700; color:var(--ink); }
.cover-by span{ display:block; font-size:24px; font-weight:500; color:var(--muted); margin-top:6px; }
.cover-meta{ margin-top:26px; font-size:23px; color:var(--accent); font-weight:700; letter-spacing:.03em; }

/* stats */
.stats{ display:flex; flex-direction:column; gap:22px; margin-bottom:32px; }
.stat{ background:var(--soft); border-radius:16px; padding:26px 32px; border-left:8px solid var(--accent); }
.stat b{ display:block; font-size:43px; color:var(--ink); font-weight:800; letter-spacing:-.02em; }
.stat span{ display:block; margin-top:10px; font-size:25px; line-height:1.45; color:var(--body); }
.stat:nth-child(2){ border-color:var(--slate); }
.stat:nth-child(3){ border-color:var(--teal); }

/* lanes */
.lanes{ display:flex; flex-direction:column; gap:24px; margin-bottom:32px; }
.lane{ border:3px solid var(--line); border-radius:18px; padding:28px 32px; background:rgba(255,255,255,.4); }
.lane-tag{ display:inline-block; font-size:21px; font-weight:800; letter-spacing:.16em;
  padding:8px 18px; border-radius:999px; color:#fff; margin-bottom:16px; }
.lane p{ font-size:26px; line-height:1.5; }
.lane.one .lane-tag{ background:var(--slate); }
.lane.two .lane-tag{ background:var(--teal); }
.lane.three .lane-tag{ background:var(--accent); }

/* rule lists */
.rules{ display:flex; flex-direction:column; gap:22px; margin-bottom:28px; }
.rules.tight{ gap:18px; margin-top:auto; margin-bottom:0; }
.rules div{ font-size:26px; line-height:1.45; padding-left:34px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:11px; width:16px; height:16px;
  border-radius:5px; background:var(--accent); }
.rules div b{ color:var(--ink); }

.badline{ font-size:26px; padding:20px 26px; border-radius:12px; margin-bottom:26px; }
.badline.bad{ background:#F7DDD4; color:#8E3520; }
.badline b{ letter-spacing:.06em; }

/* checks */
.checks{ list-style:none; counter-reset:c; margin-bottom:32px; }
.checks li{ counter-increment:c; position:relative; padding-left:74px; margin-bottom:20px;
  font-size:27px; line-height:1.45; }
.checks li:before{ content:counter(c); position:absolute; left:0; top:-2px; width:50px; height:50px;
  border-radius:14px; background:var(--accent); color:#fff; font-weight:800; font-size:26px;
  display:flex; align-items:center; justify-content:center; }
.checks li b{ color:var(--ink); }
.cta{ background:var(--ink); border-radius:18px; padding:32px 34px; margin-top:auto; }
.cta-line{ font-size:30px; line-height:1.35; color:var(--paper); font-weight:700; }
.cta-by{ margin-top:14px; font-size:25px; color:#B6A99C; }
.cta-by b{ color:var(--accent); }
.srcs{ margin-top:20px; font-size:16px; line-height:1.5; color:var(--muted); }
.srcs b{ color:var(--body); }
"""

BODY = []
for i, (kind, content) in enumerate(S, start=1):
    cls = "slide" + (" cover" if kind == "cover" else "")
    if kind == 'cover':
        foot = ('<div class="foot"><span>Python Cheat Sheet for the AI Era</span>'
                '<span class="r">SWIPE &rarr;</span></div>')
    else:
        foot = ('<div class="foot"><span>Sagar Rathkanthiwar &nbsp;|&nbsp; Data &amp; AI Professional</span>'
                '<span class="r">%02d / %02d</span></div>' % (i, len(S)))
    BODY.append('<section class="%s"><div class="accentbar"></div>%s%s</section>' % (cls, content, foot))

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>Python Cheat Sheet for the AI Era</title><style>%s</style></head><body>%s</body></html>""" % (
    CSS, "\n".join(BODY))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "python_cheat_sheet_ai_era_carousel_2026-09-04.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
