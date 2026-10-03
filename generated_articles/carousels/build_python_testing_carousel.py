# -*- coding: utf-8 -*-
"""Builds the 'Python Testing & Debugging Cheat Sheet for AI-Generated Code' carousel (1080x1350, 10 slides)."""
import html, re, io, os

KEYWORDS = r"""def|return|if|elif|else|for|while|in|not|and|or|is|None|True|False|import|from|as|try|except|finally|raise|with|assert|class|lambda|pass|continue|break|yield|global"""
FUNCS = r"""print|len|sum|round|float|int|str|list|dict|set|tuple|open|range|isinstance|type|sorted|enumerate|zip|abs|max|min|any|all|repr|logging|pytest|breakpoint|summarize|clean_phone"""


def highlight(src):
    out = []
    for line in src.split("\n"):
        m = re.search(r"#.*$", line)
        comment = ""
        if m:
            comment = line[m.start():]
            line = line[:m.start()]
        s = html.escape(line)
        # \x01 \x02 \x03 are sentinels standing in for the span tags. They carry no
        # word characters, so a later pass can't match a keyword inside a span an
        # earlier pass already wrote (which would shred the markup).
        s = re.sub(r"(&quot;[^&]*?&quot;|&#x27;[^&]*?&#x27;)", "\x01s\x02\\1\x03", s)
        s = re.sub(r"\b(" + FUNCS + r")\b(?=\s*[\(\.])", "\x01f\x02\\1\x03", s)
        s = re.sub(r"\b(" + KEYWORDS + r")\b", "\x01k\x02\\1\x03", s)
        s = (s.replace("\x01", '<span class="')
              .replace("\x02", '">')
              .replace("\x03", "</span>"))
        if comment:
            s += '<span class="c">' + html.escape(comment) + "</span>"
        out.append(s)
    return "\n".join(out)


def code(src, cls="", plain=False):
    body = html.escape(src.strip("\n")) if plain else highlight(src.strip("\n"))
    return '<pre class="code %s">%s</pre>' % (cls, body)


S = []

# ------------------------------------------------------------ 01 cover
S.append(('cover', """
<div class="eyebrow light">PYTHON &middot; TESTING &amp; DEBUGGING CHEAT SHEET</div>
<h1 class="cover-title">AI wrote<br>the Python.<br><span class="hl">How do you<br>know it works?</span></h1>
<p class="cover-sub">A testing and debugging cheat sheet<br>for AI-generated code.</p>
<div class="chips">
  <span>Behaviour first</span><span>The test matrix</span><span>assert</span>
  <span>pytest</span><span>Debug with evidence</span><span>AI failure modes</span>
  <span>Minimal repro</span><span>A review prompt</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">10 slides &middot; save for later &rarr;</div>
</div>
"""))

# ------------------------------------------------------------ 02 behaviour first
S.append(('std', """
<div class="eyebrow">01 &middot; START WITH BEHAVIOUR</div>
<h2>Write the answer<br>before the code</h2>
<p class="lead">A vague requirement gets vague code. Turn the sentence into <b>concrete inputs and the exact output you expect</b> &mdash; then hand that to the AI.</p>
<div class="ba">
  <div class="b"><span class="tag">VAGUE ASK</span><i>&ldquo;Write a function to clean up the phone numbers in my spreadsheet column.&rdquo;</i></div>
  <div class="arrow">&rarr;</div>
  <div class="a"><span class="tag">BEHAVIOUR SPEC</span>
""" + code('''
# clean_phone(raw) -> str or None
"(425) 555-0132"   ->  "4255550132"
"425-555-0132"     ->  "4255550132"
"+1 425 555 0132"  ->  "4255550132"   # drop country code
"" (empty string)  ->  None           # blank is not an error
"n/a"              ->  None           # junk is not an error
"5550132"          ->  None           # too short: reject
''', cls="xs") + """
  </div>
</div>
<p class="kicker">Those six lines are your <b>spec and your first test suite at the same time</b>. Notice how writing them forced three decisions the original sentence never made: country codes, blank values, and what &ldquo;too short&rdquo; means.</p>
"""))

# ------------------------------------------------------------ 03 test matrix
S.append(('std', """
<div class="eyebrow">02 &middot; THE MINIMUM TEST MATRIX</div>
<h2>Six cases, every<br>single function</h2>
<p class="lead">Don't guess at what to test. Walk this list &mdash; it takes two minutes and catches most of what AI gets wrong.</p>
<div class="mgrid">
  <div class="m"><b>1. Happy path</b><span>The normal case it was written for.</span><em>clean_phone("425-555-0132")</em></div>
  <div class="m"><b>2. Empty input</b><span>Empty string, empty list, empty file, zero rows.</span><em>clean_phone("") &middot; summarize([])</em></div>
  <div class="m"><b>3. Wrong type</b><span>A number where text is expected, or None.</span><em>clean_phone(None) &middot; clean_phone(4255550132)</em></div>
  <div class="m"><b>4. Boundary value</b><span>The edge of the valid range, and one step past it.</span><em>9 digits &middot; 10 digits &middot; 11 digits</em></div>
  <div class="m"><b>5. Missing data</b><span>NaN, None, blank cells, absent dictionary keys.</span><em>row.get("phone") is None</em></div>
  <div class="m"><b>6. Large / realistic</b><span>Real volume and real mess &mdash; not three tidy rows.</span><em>50,000 rows from yesterday's export</em></div>
</div>
<p class="kicker">AI code is usually excellent at case 1 and <b>silently improvised for cases 2&ndash;6.</b> That is exactly where your time is worth the most.</p>
"""))

# ------------------------------------------------------------ 04 assert
S.append(('std', """
<div class="eyebrow">03 &middot; WRITE AN ASSERTION</div>
<h2>&ldquo;It ran&rdquo; is not<br>&ldquo;it is correct&rdquo;</h2>
<p class="lead">A script that finishes without an error has proved one thing: <b>nothing crashed</b>. An assertion is how you check the answer.</p>
""" + code('''
def clean_phone(raw):
    digits = "".join(c for c in str(raw) if c.isdigit())
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits if len(digits) == 10 else None

# An assertion states a fact. If the fact is false, Python stops.
assert clean_phone("(425) 555-0132") == "4255550132"
assert clean_phone("+1 425 555 0132") == "4255550132"
assert clean_phone("") is None
assert clean_phone("5550132") is None       # boundary: too short

# Put the actual value in the message - future-you will thank you
got = clean_phone("425.555.0132")
assert got == "4255550132", f"expected 4255550132, got {got!r}"
''', cls="sm") + """
<p class="kicker"><b>Run the file and nothing prints?</b> That silence is the result &mdash; every stated fact held. Note <span class="mono">{got!r}</span>: <span class="mono">repr</span> shows the quotes and stray whitespace that plain printing hides. <span class="mono">assert</span> is stripped out when Python runs with <span class="mono">-O</span>, so keep it for tests, never for validating production input.</p>
"""))

# ------------------------------------------------------------ 05 pytest
S.append(('std', """
<div class="eyebrow">04 &middot; MAKE IT REPEATABLE</div>
<h2>Graduate to <span class="mono big">pytest</span></h2>
<p class="lead">Loose asserts get lost. Move them into a file named <span class="mono">test_*.py</span> and every check re-runs on demand, forever.</p>
""" + code('''
# test_phones.py           run it with:   pytest -q
import pytest
from phones import clean_phone

def test_strips_formatting_characters():
    raw = "(425) 555-0132"           # Arrange - set up the input
    result = clean_phone(raw)        # Act     - call the one thing
    assert result == "4255550132"    # Assert  - check the result

@pytest.mark.parametrize("raw, expected", [
    ("425-555-0132",    "4255550132"),   # happy path
    ("+1 425 555 0132", "4255550132"),   # country code
    ("",                None),           # empty input
    ("5550132",         None),           # boundary: too short
])
def test_clean_phone_cases(raw, expected):
    assert clean_phone(raw) == expected
''', cls="sm") + """
<div class="rules tight">
  <div><b>Arrange &rarr; Act &rarr; Assert.</b> One input, one call, one claim. Two behaviours to check means two tests, not two asserts.</div>
  <div><b>Name the test after the behaviour</b>, not the function. <span class="mono">test_strips_formatting_characters</span> tells you what broke without opening the file.</div>
  <div><b><span class="mono">parametrize</span> turns your matrix into rows.</b> Add an edge case in one line; each row passes or fails on its own.</div>
</div>
"""))

# ------------------------------------------------------------ 06 debug with evidence
S.append(('std', """
<div class="eyebrow">05 &middot; DEBUG WITH EVIDENCE</div>
<h2>Read the error before<br>you change the code</h2>
<p class="lead">The traceback holds the answer. Read the <b>bottom line first</b> (what went wrong), then scan up to <b>the last line that is your file</b> (where it went wrong).</p>
""" + code('''
Traceback (most recent call last):
  File "run.py", line 12, in <module>           # 3. your entry point
    report = summarize(rows)
  File "clean.py", line 27, in summarize        # 2. YOUR code: start here
    total = sum(r["amount"] for r in rows)
TypeError: unsupported operand type(s) for +: 'int' and 'str'
#  1. read this first - an amount arrived as text, not a number''', cls="tb plain") + """
<div class="tools">
  <div class="t"><b>print()</b><span>Fastest first move. Print the value <i>and</i> its type: <span class="mono">print(repr(x), type(x))</span> &mdash; one line before the failure, one after.</span></div>
  <div class="t"><b>logging</b><span>For code that runs unattended. A timestamped trail you can switch off with one config line &mdash; not prints you must remember to delete.</span></div>
  <div class="t"><b>breakpoint()</b><span>Drop it one line above the failure and inspect every variable live. <span class="mono">n</span> next &middot; <span class="mono">c</span> continue &middot; <span class="mono">q</span> quit. Or <span class="mono">pytest --pdb</span> lands you exactly where a test failed.</span></div>
</div>
<p class="kicker">Then change <b>one thing at a time</b> and re-run. Two edits at once and you no longer know which one fixed it &mdash; or which one broke something else.</p>
"""))

# ------------------------------------------------------------ 07 failure modes
S.append(('std', """
<div class="eyebrow">06 &middot; COMMON AI FAILURE MODES</div>
<h2>What to look for<br>on the first read</h2>
<div class="fm">
  <div class="fmc"><b>Invented input shape</b><span>It assumed a column name, a date format, a dictionary key, a delimiter. It had to guess &mdash; it never saw your data.</span><em>row["amount"] -&gt; KeyError on the real file</em></div>
  <div class="fmc"><b>Silent fallback values</b><span>A missing value quietly becomes <span class="mono">0</span> or an empty string. Nothing errors; your total is just wrong.</span><em>float(row.get("amount", 0))</em></div>
  <div class="fmc"><b>Over-broad except</b><span><span class="mono">except Exception: pass</span> swallows typos, network failures and real bugs identically.</span><em>catch the specific error instead</em></div>
  <div class="fmc"><b>Off-by-one logic</b><span>Ranges and slices that drop the last item, or a <span class="mono">&gt;</span> that should be <span class="mono">&gt;=</span>. Test the boundary, always.</span><em>range(1, len(x)) skips index 0</em></div>
  <div class="fmc"><b>Happy path only</b><span>No handling for empty input, a missing file, or a duplicate row &mdash; because the example it learned from had none.</span><em>works on 3 rows, dies on 30,000</em></div>
  <div class="fmc"><b>Confidently stale</b><span>A deprecated argument or a library version that has moved on. It reads perfectly and no longer exists.</span><em>check the docs, not the confidence</em></div>
</div>
<p class="kicker">None of these throw an obvious error on line one. <b>Four of the six produce a wrong answer with a clean exit code</b> &mdash; which is precisely why &ldquo;it ran&rdquo; cannot be your finish line.</p>
"""))

# ------------------------------------------------------------ 08 minimal repro
S.append(('std', """
<div class="eyebrow">07 &middot; MAKE BUGS SMALLER</div>
<h2>Shrink it before<br>you ask for help</h2>
<p class="lead">Pasting 300 lines and &ldquo;it doesn't work&rdquo; gets you a guess. <b>Isolate the failing function with hard-coded input</b> and you often find the bug yourself &mdash; before you even hit send.</p>
""" + code('''
# repro.py - everything needed to reproduce, nothing else
from clean import summarize

rows = [                            # smallest input that still fails
    {"id": 1, "amount": "12.50"},   # <- text, not a number
    {"id": 2, "amount": 8},
]
print(summarize(rows))

# expected: 20.5
# actual:   TypeError: unsupported operand type(s) for +: 'int' and 'str'
''', cls="sm") + """
<ol class="checks">
  <li><b>Cut the input down</b> until one more deletion makes the bug disappear. Two rows beat two thousand.</li>
  <li><b>Remove the surroundings</b> &mdash; the dashboard, the API call, the database. Can it fail in one file?</li>
  <li><b>Write down expected vs. actual.</b> If you cannot state what you expected, that is the real bug.</li>
</ol>
<p class="kicker">A minimal reproducible example is the <b>highest-leverage debugging move there is</b> &mdash; and it doubles as your next regression test.</p>
"""))

# ------------------------------------------------------------ 09 review prompt
S.append(('std', """
<div class="eyebrow">08 &middot; A REUSABLE REVIEW PROMPT</div>
<h2>Make the AI attack<br>its own code</h2>
<p class="lead">Asking &ldquo;is this correct?&rdquo; gets you reassurance. Asking for <b>assumptions and failing tests</b> gets you evidence.</p>
<div class="prompt">
  <div class="ph">PASTE THIS ABOVE YOUR FUNCTION</div>
  <p>Review this Python function. List the <b>assumptions</b> it makes about its input, the <b>edge cases</b> it does not handle, and the <b>failure modes</b> that would produce a wrong answer without raising an error.</p>
  <p>Then write <b><span class="mono">pytest</span> tests that would expose them</b> &mdash; including empty input, wrong type, boundary values and missing data.</p>
  <p>Do not rewrite the function yet. <b>Show me the failing tests first.</b></p>
</div>
<div class="rules tight push">
  <div><b>&ldquo;Do not rewrite yet&rdquo; is the load-bearing line.</b> It stops the model quietly patching over the bug so you never learn what it was.</div>
  <div><b>Then run the tests yourself.</b> A generated test that has never been executed is a claim, not a check &mdash; and some of them will be wrong.</div>
  <div><b>Keep the ones that fail.</b> Fix the code until they pass, commit them, and that bug can never come back unnoticed.</div>
</div>
"""))

# ------------------------------------------------------------ 10 CTA
S.append(('std', """
<div class="eyebrow">09 &middot; THE TAKEAWAY</div>
<h2>AI can generate code<br>in seconds.<br><span class="hl2">Confidence comes<br>from evidence.</span></h2>
<div class="rules">
  <div>Specify the <b>behaviour</b> before the code &mdash; inputs, outputs, and what counts as invalid.</div>
  <div>Run the <b>six-case matrix</b>: happy path, empty, wrong type, boundary, missing data, realistic volume.</div>
  <div>Turn every bug you fix into a <b>test that stays</b>. That is how regressions stop repeating.</div>
  <div>The model can write the tests. <b>Only you can decide what &ldquo;correct&rdquo; means</b> for your data and your users.</div>
</div>
<div class="cta">
  <div class="cta-line">What test has saved you from a bug recently?<br>Drop it in the comments &mdash; someone is shipping that bug today.</div>
  <div class="cta-by"><b>Sagar Rathkanthiwar</b> &middot; Data &amp; AI Professional &middot; follow for more field guides</div>
</div>
<div class="srcs"><b>Note:</b> examples target Python 3.8+ and <span class="mono">pytest</span> 7+. <span class="mono">assert</span> statements are removed when Python runs with the <span class="mono">-O</span> flag &mdash; use explicit checks and raised exceptions to validate production input, and keep <span class="mono">assert</span> for tests and development-time invariants.</div>
"""))

# ------------------------------------------------------------ template
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
.slide{ position:relative; width:1080px; height:1350px; overflow:hidden;
  padding:70px 74px 118px; background:var(--paper);
  page-break-after:always; display:flex; flex-direction:column; }
.slide:last-child{ page-break-after:auto; }

.foot{ position:absolute; left:0; right:0; bottom:0; height:74px; background:var(--ink);
  display:flex; align-items:center; justify-content:space-between; padding:0 74px; }
.foot span{ color:#fff; font-size:21px; letter-spacing:.045em; font-weight:600; }
.foot .r{ color:#8ea2c9; font-weight:500; letter-spacing:.12em; }
.accentbar{ position:absolute; top:0; left:0; width:100%; height:10px; background:var(--accent); }

.eyebrow{ font-size:22px; font-weight:700; letter-spacing:.2em; color:var(--accent); margin-bottom:20px; }
.eyebrow.light{ color:#9db4f7; }
h2{ font-size:60px; line-height:1.1; letter-spacing:-.02em; color:var(--ink); font-weight:800; margin-bottom:26px; }
h2 .hl2{ color:var(--accent); }
.lead{ font-size:29px; line-height:1.45; color:var(--body); margin-bottom:24px; }
.lead b{ color:var(--ink); }
.kicker{ margin-top:auto; font-size:25px; line-height:1.5; color:var(--body);
  border-left:8px solid var(--accent); background:var(--soft); padding:20px 26px; border-radius:0 14px 14px 0; }
.kicker b{ color:var(--ink); }
.mono{ font-family:Consolas,"Cascadia Mono",monospace; font-size:.9em; background:#eef1f7; color:#1b2a4a;
  padding:2px 8px; border-radius:6px; }
h2 .mono.big{ font-size:.82em; background:#eef1f7; padding:4px 16px; border-radius:12px; }

.code{ font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:22px; line-height:1.55;
  background:#0d1526; color:#dbe4f5; padding:28px 30px; border-radius:16px; white-space:pre;
  margin-bottom:24px; overflow:hidden; }
.code.sm{ font-size:20px; line-height:1.52; padding:26px 28px; }
.code.xs{ font-size:18px; line-height:1.5; padding:20px 22px; margin-bottom:0; }
.code.tb{ font-size:17px; line-height:1.5; padding:20px 24px; margin-bottom:14px; }
.code.plain{ color:#f0c2cc; }
.code .k{ color:#7fb0ff; font-weight:600; }
.code .f{ color:#f2b45c; }
.code .s{ color:#7fd6a5; }
.code .c{ color:#8091b4; font-style:italic; }

.cover{ background:var(--ink); color:#fff; padding:84px 74px 118px; }
.cover .accentbar{ background:linear-gradient(90deg,#2f5bea,#22b3a4); }
.cover-title{ font-size:92px; line-height:1.04; font-weight:800; letter-spacing:-.035em; color:#fff; }
.cover-title .hl{ color:#7fb0ff; }
.cover-sub{ margin-top:32px; font-size:34px; line-height:1.35; color:#b9c6e0; font-weight:400; }
.chips{ margin-top:38px; display:flex; flex-wrap:wrap; gap:13px; max-width:900px; }
.chips span{ border:2px solid #33456d; color:#9db4f7; border-radius:999px; padding:9px 20px;
  font-size:22px; font-weight:600; }
.cover-foot{ margin-top:auto; }
.cover-foot .rule{ height:3px; background:#2a3a5e; margin-bottom:28px; }
.cover-by{ font-size:31px; font-weight:700; color:#fff; }
.cover-by span{ display:block; font-size:24px; font-weight:500; color:#8ea2c9; margin-top:6px; }
.cover-meta{ margin-top:20px; font-size:23px; color:#7fb0ff; font-weight:600; letter-spacing:.03em; }

.rules{ display:flex; flex-direction:column; gap:20px; margin-bottom:24px; }
.rules.tight{ gap:15px; margin-bottom:0; }
.rules.push{ margin-top:auto; }
.rules div{ font-size:25px; line-height:1.45; padding-left:34px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:10px; width:16px; height:16px;
  border-radius:5px; background:var(--accent); }
.rules div b{ color:var(--ink); }

.ba{ display:flex; align-items:center; gap:18px; margin-bottom:24px; }
.ba .b{ flex:0 0 290px; background:#fdf2f5; border-radius:16px; padding:22px 24px;
  border-left:8px solid var(--rose); }
.ba .b i{ font-style:normal; display:block; font-size:24px; line-height:1.4; color:var(--body); }
.ba .a{ flex:1; background:var(--soft); border-radius:16px; padding:20px 22px;
  border-left:8px solid var(--teal); }
.ba .arrow{ font-size:40px; color:#c3ccdd; font-weight:700; }
.tag{ display:block; font-size:18px; font-weight:800; letter-spacing:.14em; color:var(--muted); margin-bottom:12px; }

.mgrid{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:24px; }
.m{ background:var(--soft); border-radius:14px; padding:19px 21px; border-left:7px solid var(--accent); }
.m b{ display:block; font-size:26px; color:var(--ink); font-weight:800; margin-bottom:7px; }
.m span{ display:block; font-size:20px; line-height:1.35; color:var(--body); }
.m em{ display:block; font-style:normal; margin-top:9px; font-family:Consolas,"Cascadia Mono",monospace;
  font-size:18px; color:#3d5891; }

.fm{ display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-bottom:24px; }
.fmc{ background:#fdf2f5; border-radius:14px; padding:18px 20px; border-left:7px solid var(--rose); }
.fmc b{ display:block; font-size:25px; color:var(--ink); font-weight:800; margin-bottom:7px; }
.fmc span{ display:block; font-size:19.5px; line-height:1.35; color:var(--body); }
.fmc .mono{ font-size:.86em; background:#f6e0e6; padding:1px 6px; }
.fmc em{ display:block; font-style:normal; margin-top:8px; font-family:Consolas,"Cascadia Mono",monospace;
  font-size:17.5px; color:#9a2c4d; }

.tools{ display:flex; flex-direction:column; gap:10px; margin-bottom:22px; }
.t{ background:var(--soft); border-radius:14px; padding:15px 22px; border-left:7px solid var(--teal); }
.t b{ display:inline-block; font-family:Consolas,"Cascadia Mono",monospace; font-size:25px;
  color:var(--ink); font-weight:800; margin-bottom:6px; }
.t span{ display:block; font-size:20px; line-height:1.36; color:var(--body); }
.t .mono{ font-size:.88em; }

.checks{ list-style:none; counter-reset:c; margin-bottom:24px; display:flex;
  flex-direction:column; gap:18px; }
.checks li{ counter-increment:c; position:relative; padding-left:66px; font-size:25px; line-height:1.4; }
.checks li:before{ content:counter(c); position:absolute; left:0; top:-2px; width:44px; height:44px;
  border-radius:13px; background:var(--accent); color:#fff; font-weight:800; font-size:23px;
  display:flex; align-items:center; justify-content:center; }
.checks li b{ color:var(--ink); }

.prompt{ background:#0d1526; border-radius:18px; padding:34px 36px; margin:auto 0 26px;
  border-left:10px solid var(--teal); }
.prompt .ph{ font-size:18px; font-weight:800; letter-spacing:.16em; color:#7fd6a5; margin-bottom:16px; }
.prompt p{ font-size:26px; line-height:1.48; color:#dbe4f5; margin-bottom:15px; }
.prompt p:last-child{ margin-bottom:0; }
.prompt b{ color:#fff; }
.prompt .mono{ background:#22304d; color:#9db4f7; }

.cta{ background:var(--ink); border-radius:18px; padding:30px 34px; margin-top:auto; }
.cta-line{ font-size:29px; line-height:1.38; color:#fff; font-weight:700; }
.cta-by{ margin-top:14px; font-size:23px; color:#9db4f7; }
.cta-by b{ color:#fff; }
.srcs{ margin-top:18px; font-size:17px; line-height:1.5; color:var(--muted); }
.srcs b{ color:var(--body); }
.srcs .mono{ font-size:.94em; padding:1px 5px; }
"""

TITLE = "The Python Testing &amp; Debugging Cheat Sheet"
BODY = []
for i, (kind, content) in enumerate(S, start=1):
    cls = "slide" + (" cover" if kind == "cover" else "")
    if kind == 'cover':
        foot = ('<div class="foot"><span>%s</span>'
                '<span class="r">01 / %02d &nbsp;&middot;&nbsp; SWIPE &rarr;</span></div>' % (TITLE, len(S)))
    else:
        foot = ('<div class="foot"><span>Sagar Rathkanthiwar &nbsp;|&nbsp; %s</span>'
                '<span class="r">%02d / %02d</span></div>' % (TITLE, i, len(S)))
    BODY.append('<section class="%s"><div class="accentbar"></div>%s%s</section>' % (cls, content, foot))

HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>Python Testing &amp; Debugging Cheat Sheet for AI-Generated Code</title><style>%s</style></head><body>%s</body></html>""" % (
    CSS, "\n".join(BODY))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "python_testing_debugging_carousel_2026-09-13.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
