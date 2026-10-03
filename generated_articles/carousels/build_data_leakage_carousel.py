# -*- coding: utf-8 -*-
"""Builds the 'Data Leakage: The Silent Way Your Model Cheats' carousel (1080x1350, 10 slides)."""
import html, re, io, os

KEYWORDS = r"""def|return|if|elif|else|for|while|in|not|and|or|is|None|True|False|import|from|as|try|except|finally|raise|with|assert|class|lambda|pass|continue|break|yield"""
FUNCS = r"""print|len|sum|round|float|int|str|list|dict|set|tuple|sorted|fit|transform|fit_transform|predict|score|Pipeline|StandardScaler|SimpleImputer|OneHotEncoder|LogisticRegression|train_test_split|cross_val_score|TimeSeriesSplit|GroupKFold|sort_values|read_csv|split|drop"""


def highlight(src):
    out = []
    for line in src.split("\n"):
        m = re.search(r"#.*$", line)
        comment = ""
        if m:
            comment = line[m.start():]
            line = line[:m.start()]
        s = html.escape(line)
        # \x01 \x02 \x03 stand in for span tags so later passes cannot match a
        # keyword inside markup an earlier pass already wrote.
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


def code(src, cls=""):
    return '<pre class="code %s">%s</pre>' % (cls, highlight(src.strip("\n")))


S = []

# ------------------------------------------------------------ 01 cover
S.append(('cover', """
<div class="eyebrow light">MACHINE LEARNING &middot; DATA LEAKAGE CHEAT SHEET</div>
<h1 class="cover-title">Your model<br>is not brilliant.<br><span class="hl">It may be<br>cheating.</span></h1>
<p class="cover-sub">A practical data leakage cheat sheet<br>for the AI era.</p>
<div class="chips">
  <span>What leakage is</span><span>Target leakage</span><span>Time leakage</span>
  <span>Train/test contamination</span><span>Choosing a split</span>
  <span>Red flags</span><span>Pipelines in scikit-learn</span><span>A review checklist</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">10 slides &middot; save for later &rarr;</div>
</div>
"""))

# ------------------------------------------------------------ 02 what is leakage
S.append(('std', """
<div class="eyebrow">01 &middot; THE DEFINITION</div>
<h2>Information from<br>the wrong side<br>of the line</h2>
<p class="lead"><b>Data leakage is when a model trains on &mdash; or is scored with &mdash; information it would not actually have at prediction time.</b> The score looks great because the exam contained the answers.</p>
<div class="tl">
  <div class="tl-bar"><span class="past">DATA YOU REALLY HAVE</span><span class="now">PREDICT<br>HERE</span><span class="future">THE FUTURE &mdash; UNKNOWN</span></div>
  <div class="tl-leak">&larr; leakage is any value that crosses this line backwards</div>
</div>
<div class="rules tight">
  <div><b>Ask one question of every column:</b> at the exact moment I need a prediction, does this value exist yet?</div>
  <div><b>If the answer is &ldquo;no&rdquo; or &ldquo;only afterwards,&rdquo;</b> it is leakage &mdash; no matter how predictive it looks.</div>
</div>
<div class="ex">
  <span class="tag">ONE EXAMPLE &mdash; PREDICTING WHO WILL CANCEL NEXT MONTH</span>
  <div class="exrow ok2"><b>tickets_opened_last_30d</b><span>already true today &mdash; safe to use</span></div>
  <div class="exrow no2"><b>cancellation_survey_score</b><span>only filled in <i>after</i> they cancel &mdash; leakage</span></div>
</div>
<p class="kicker">Leakage is not a flaw in the algorithm. It is a <b>mistake in how the data and the evaluation were set up</b> &mdash; which is exactly the part no model can check for you.</p>
"""))

# ------------------------------------------------------------ 03 why dangerous
S.append(('std', """
<div class="eyebrow">02 &middot; WHY IT IS DANGEROUS</div>
<h2>It fails <i>after</i><br>you ship it</h2>
<p class="lead">Leakage never announces itself. It shows up as a number so good that nobody questions it &mdash; until the model meets real data.</p>
<div class="chart">
  <div class="bars">
    <div class="bcol"><div class="bar b1" style="height:417px"><b>0.97</b></div><span>Validation<br>score</span></div>
    <div class="bcol"><div class="bar b2" style="height:400px"><b>0.93</b></div><span>Hold-out<br>(same leak)</span></div>
    <div class="bcol"><div class="bar b3" style="height:262px"><b>0.61</b></div><span>Production<br>week 1</span></div>
    <div class="bcol"><div class="bar b4" style="height:224px"><b>0.52</b></div><span>Production<br>week 4</span></div>
  </div>
  <div class="cap">Illustrative pattern, not measured data &mdash; the <b>shape</b> is the point</div>
</div>
<p class="kicker">Notice the trap: <b>the hold-out set agreed.</b> If the leak is in your data, every split you carve out of that data carries it too &mdash; so the second opinion was never independent. <b>Production is the first honest test.</b></p>
"""))

# ------------------------------------------------------------ 04 target leakage
S.append(('std', """
<div class="eyebrow">03 &middot; TARGET LEAKAGE</div>
<h2>The feature that<br>quietly <i>is</i><br>the answer</h2>
<p class="lead">Some columns are created <b>because</b> of the outcome, or at the same moment as it. Include them and the model simply reads the label back.</p>
<div class="ba">
  <div class="b"><span class="tag">THE TASK</span><i>Predict whether a <b>loan application will be approved</b> &mdash; at the moment it is submitted.</i></div>
  <div class="arrow">&rarr;</div>
  <div class="a"><span class="tag">COLUMNS IN THE TRAINING TABLE</span>
    <div class="cols">
      <div class="bad"><b>interest_rate_offered</b><span>only set once approved</span></div>
      <div class="bad"><b>funds_disbursed_on</b><span>happens after the decision</span></div>
      <div class="bad"><b>assigned_loan_officer</b><span>only assigned to approvals</span></div>
      <div class="bad"><b>rejection_reason_code</b><span>literally the label</span></div>
      <div class="ok"><b>credit_score &middot; income &middot; debt_ratio</b><span>known at submission &mdash; keep</span></div>
    </div>
    <div class="colnote">Four of these five columns do not exist yet at the moment you need the prediction.</div>
  </div>
</div>
<p class="kicker"><b>The indirect leaks are the dangerous ones.</b> Nobody ships <span class="mono">rejection_reason_code</span>. But a blank <span class="mono">assigned_loan_officer</span> means &ldquo;rejected&rdquo; just as reliably &mdash; and looks like an innocent feature in the schema.</p>
"""))

# ------------------------------------------------------------ 05 time leakage
S.append(('std', """
<div class="eyebrow">04 &middot; TIME LEAKAGE</div>
<h2>Letting the future<br>teach the past</h2>
<p class="lead">If your data has a timeline &mdash; churn, fraud, demand, prices, clicks &mdash; a <b>random</b> split scatters future rows into training. The model learns from events that had not happened yet.</p>
<div class="split2">
  <div class="sp bad2">
    <span class="tag">RANDOM SPLIT &mdash; WRONG HERE</span>
    <div class="dots">
      <i class="tr"></i><i class="te"></i><i class="tr"></i><i class="tr"></i><i class="te"></i><i class="tr"></i><i class="te"></i><i class="tr"></i><i class="tr"></i><i class="te"></i><i class="tr"></i><i class="te"></i>
    </div>
    <div class="axis">JAN &rarr; DEC</div>
    <p>Test rows sit <b>before</b> training rows. To score January, the model has already read December.</p>
  </div>
  <div class="sp good2">
    <span class="tag">TIME-BASED SPLIT &mdash; CORRECT</span>
    <div class="dots">
      <i class="tr"></i><i class="tr"></i><i class="tr"></i><i class="tr"></i><i class="tr"></i><i class="tr"></i><i class="tr"></i><i class="tr"></i><i class="te"></i><i class="te"></i><i class="te"></i><i class="te"></i>
    </div>
    <div class="axis">JAN &rarr; DEC</div>
    <p>Train on the past, test on the future &mdash; <b>the same order production will face.</b></p>
  </div>
</div>
<div class="legend"><span class="sw tr"></span> training rows <span class="sw te2"></span> test rows &nbsp;&middot;&nbsp; each block is one month</div>
""" + code('''
# WRONG for time-ordered data - shuffling scrambles the calendar
train_test_split(X, y, test_size=0.2, shuffle=True)

# RIGHT - expanding windows that always score a LATER slice
for train_idx, test_idx in TimeSeriesSplit(n_splits=5).split(X):
    ...          # every fold trains on the past, tests on the next period
''', cls="xs") + """
<p class="kicker">This applies <b>inside</b> a feature too. A &ldquo;customer lifetime value&rdquo; or &ldquo;total complaints&rdquo; column computed over the whole dataset already contains the months you are trying to predict.</p>
"""))

# ------------------------------------------------------------ 06 contamination
S.append(('std', """
<div class="eyebrow">05 &middot; TRAIN / TEST CONTAMINATION</div>
<h2>Fit on train only.<br>Every time.</h2>
<p class="lead">Scaling, imputing, encoding, feature selection &mdash; each one <b>learns statistics from the data you hand it.</b> Fit on everything and the test set has already shaped the model.</p>
""" + code('''
# WRONG - the scaler saw the test rows' mean and standard deviation
X_scaled = StandardScaler().fit_transform(X)            # all rows
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)

# RIGHT - a Pipeline refits every step inside each fold
# sklearn: Pipeline, SimpleImputer, StandardScaler,
#          LogisticRegression, train_test_split, cross_val_score
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),       # median from TRAIN only
    ("scale",  StandardScaler()),                       # mean/std from TRAIN only
    ("model",  LogisticRegression(max_iter=1000)),
])

scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")
pipe.fit(X_train, y_train)                              # test set still untouched
''', cls="sm") + """
<p class="kicker">A <b><span class="mono">Pipeline</span> is not a style preference &mdash; it is the leak guard.</b> It makes &ldquo;fit on train only&rdquo; true automatically inside every cross-validation fold, which is exactly where it is easiest to get wrong by hand.</p>
"""))

# ------------------------------------------------------------ 07 the right split
S.append(('std', """
<div class="eyebrow">06 &middot; CHOOSING THE SPLIT</div>
<h2>The split <i>is</i><br>the experiment</h2>
<p class="lead">Your split should imitate the moment of deployment. Pick it from the structure of the data &mdash; not from habit.</p>
<div class="sgrid">
  <div class="sc">
    <b>Random split</b>
    <span class="when">WHEN rows are independent and order does not matter &mdash; one image, one patient, one document per row.</span>
    <em>train_test_split(X, y, stratify=y)</em>
  </div>
  <div class="sc t">
    <b>Time-based split</b>
    <span class="when">WHEN anything about the data is a timeline &mdash; churn, fraud, demand, prices, sessions.</span>
    <em>TimeSeriesSplit(n_splits=5)</em>
  </div>
  <div class="sc r">
    <b>Group-based split</b>
    <span class="when">WHEN one entity produces many rows &mdash; a customer, a patient, a device, a store. Keep it wholly on one side.</span>
    <em>GroupKFold(n_splits=5).split(X, y, groups=customer_id)</em>
  </div>
</div>
""" + code('''
# Time-aware: sort first, then split forward - never shuffle
df = df.sort_values("event_date")
cutoff = "2026-07-01"                  # train on the past, test on the future
train = df[df["event_date"] <  cutoff]
test  = df[df["event_date"] >= cutoff]
''', cls="xs") + """
<p class="kicker">Real data often has <b>two</b> of these structures at once &mdash; repeat customers <i>and</i> a timeline. The right choice always depends on your data and how the model is actually deployed.</p>
"""))

# ------------------------------------------------------------ 08 red flags
S.append(('std', """
<div class="eyebrow">07 &middot; RED FLAGS</div>
<h2>Five signs not to<br>celebrate yet</h2>
<p class="lead">Leakage rarely arrives as an error message. It arrives as a result that is <b>a little too good.</b> These are the tells.</p>
<div class="fm">
  <div class="fmc"><b>1. Suspiciously high score</b><span>0.99 AUC on a messy human problem is a bug report, not a result. Compare it against a trivial baseline.</span></div>
  <div class="fmc"><b>2. One feature dominates</b><span>Drop your top feature. If the score collapses, go read that column's definition very carefully.</span></div>
  <div class="fmc"><b>3. Post-outcome columns</b><span>Anything named <span class="mono">_final</span>, <span class="mono">_closed</span>, <span class="mono">_resolved</span>, <span class="mono">_total</span> &mdash; or carrying a timestamp after the decision point.</span></div>
  <div class="fmc"><b>4. The same entity on both sides</b><span>One customer with 40 rows split across train and test means the model memorised them, not the pattern.</span></div>
  <div class="fmc wide"><b>5. Production performance falls off a cliff</b><span>A model that scores well offline and poorly in week one is the classic signature. Before you retrain or swap algorithms, re-audit the features, the timeline and the split &mdash; that is usually where the answer is hiding.</span></div>
</div>
<p class="kicker">The fastest sanity check there is: <b>can you tell a colleague a plausible story for <i>why</i> each top feature predicts the outcome?</b> If the only story is &ldquo;because it already knows,&rdquo; you have found your leak.</p>
"""))

# ------------------------------------------------------------ 09 AI review checklist
S.append(('std', """
<div class="eyebrow">08 &middot; THE AI-ASSISTED ML REVIEW</div>
<h2>AI can build the<br>pipeline. You own<br>the validity.</h2>
<p class="lead">A model will happily generate a clean, well-structured, <b>completely invalid</b> pipeline &mdash; because leakage lives in facts about your business that were never in the code.</p>
<ol class="checks">
  <li><b>Would this feature exist at prediction time?</b> Column by column. Not &ldquo;is it in the table&rdquo; &mdash; <i>is it populated yet</i>.</li>
  <li><b>Was preprocessing fit on training data only?</b> Every scaler, imputer, encoder and feature selector, inside every fold.</li>
  <li><b>Does the split reflect real deployment?</b> If production predicts forward in time, the evaluation must too.</li>
  <li><b>Could the same customer or entity land on both sides?</b> Check duplicates and repeated IDs before you trust any score.</li>
  <li><b>What is the exact prediction timestamp?</b> Write it down. Every question above is answered relative to that one moment.</li>
</ol>
<div class="prompt">
  <div class="ph">A PROMPT WORTH REUSING</div>
  <p>Review this ML pipeline for <b>data leakage</b>. For each feature, state whether it would be available at prediction time. Flag any preprocessing fit outside the training fold, and say whether the split matches this deployment. <b>List the risks before suggesting any fix.</b></p>
</div>
"""))

# ------------------------------------------------------------ 10 CTA
S.append(('std', """
<div class="eyebrow">09 &middot; THE TAKEAWAY</div>
<h2>A model that sees<br>the future is not<br><span class="hl2">intelligent.<br>It is invalid.</span></h2>
<div class="rules">
  <div>Leakage is <b>information from the wrong side of the prediction moment</b> &mdash; in a feature, in the timeline, or in the split.</div>
  <div>Wrap every transformation in a <b><span class="mono">Pipeline</span></b> so &ldquo;fit on train only&rdquo; stops depending on memory.</div>
  <div>Choose the split from the <b>structure of the data</b>: random, time-based, or grouped by entity.</div>
  <div>AI can generate the whole pipeline in seconds. <b>Validating the data, the timeline and the evaluation design stays human work.</b></div>
  <div>When a score looks too good, <b>treat it as a bug report</b> &mdash; not a result to announce.</div>
</div>
<div class="cta">
  <div class="cta-line">What data-quality or evaluation issue has surprised you most?<br>Share it below &mdash; someone is about to ship that exact bug.</div>
  <div class="cta-by"><b>Sagar Rathkanthiwar</b> &middot; Data &amp; AI Professional &middot; follow for more field guides</div>
</div>
<div class="srcs"><b>Note:</b> examples target scikit-learn 1.x. The right split and the right feature set always depend on your data and how the model is deployed &mdash; treat this as a review checklist, not a recipe.</div>
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
.foot span{ color:#fff; font-size:20px; letter-spacing:.04em; font-weight:600; }
.foot .r{ color:#8ea2c9; font-weight:500; letter-spacing:.12em; }
.accentbar{ position:absolute; top:0; left:0; width:100%; height:10px; background:var(--accent); }

.eyebrow{ font-size:22px; font-weight:700; letter-spacing:.2em; color:var(--accent); margin-bottom:20px; }
.eyebrow.light{ color:#9db4f7; }
h2{ font-size:60px; line-height:1.1; letter-spacing:-.02em; color:var(--ink); font-weight:800; margin-bottom:26px; }
h2 .hl2{ color:var(--accent); }
h2 i{ font-style:italic; }
.lead{ font-size:29px; line-height:1.45; color:var(--body); margin-bottom:24px; }
.lead b{ color:var(--ink); }
.kicker{ margin-top:auto; font-size:25px; line-height:1.5; color:var(--body);
  border-left:8px solid var(--accent); background:var(--soft); padding:20px 26px; border-radius:0 14px 14px 0; }
.kicker b{ color:var(--ink); }
.mono{ font-family:Consolas,"Cascadia Mono",monospace; font-size:.9em; background:#eef1f7; color:#1b2a4a;
  padding:2px 8px; border-radius:6px; }

.code{ font-family:Consolas,"Cascadia Mono","Courier New",monospace; font-size:22px; line-height:1.55;
  background:#0d1526; color:#dbe4f5; padding:28px 30px; border-radius:16px; white-space:pre;
  margin-bottom:24px; overflow:hidden; }
.code.sm{ font-size:19.5px; line-height:1.5; padding:24px 28px; }
.code.xs{ font-size:18px; line-height:1.5; padding:20px 24px; margin-bottom:22px; }
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
.rules.tight{ gap:15px; margin-bottom:22px; }
.rules div{ font-size:25px; line-height:1.45; padding-left:34px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:10px; width:16px; height:16px;
  border-radius:5px; background:var(--accent); }
.rules div b{ color:var(--ink); }

/* timeline - slide 02 */
.tl{ margin-bottom:26px; }
.tl-bar{ display:flex; height:104px; border-radius:14px; overflow:hidden; }
.tl-bar span{ display:flex; align-items:center; justify-content:center; text-align:center;
  font-size:19px; font-weight:800; letter-spacing:.1em; line-height:1.25; }
.tl-bar .past{ flex:1; background:#e6edfd; color:#28468f; }
.tl-bar .now{ flex:0 0 150px; background:var(--ink); color:#fff; letter-spacing:.06em; }
.tl-bar .future{ flex:1; background:#f4e7ec; color:#9a2c4d; }
.tl-leak{ margin-top:14px; text-align:center; font-size:22px; color:var(--rose); font-weight:700; }

/* example rows - slide 02 */
.ex{ background:var(--soft); border-radius:16px; padding:18px 22px; margin-bottom:22px; }
.exrow{ padding:10px 16px; border-radius:10px; margin-bottom:8px; }
.exrow:last-child{ margin-bottom:0; }
.exrow b{ display:block; font-family:Consolas,"Cascadia Mono",monospace; font-size:22px; }
.exrow span{ display:block; font-size:19px; margin-top:2px; }
.exrow i{ font-style:italic; }
.exrow.ok2{ background:#e3f3f0; } .exrow.ok2 b{ color:#0b6157; } .exrow.ok2 span{ color:#3d7c74; }
.exrow.no2{ background:#fbe8ee; } .exrow.no2 b{ color:#9a2c4d; } .exrow.no2 span{ color:#a4566f; }

/* legend - slide 05 */
.legend{ display:flex; align-items:center; gap:10px; font-size:19px; color:var(--muted);
  font-weight:600; margin-bottom:20px; }
.legend .sw{ display:inline-block; width:26px; height:16px; border-radius:5px; }
.legend .sw.tr{ background:#98a7c4; } .legend .sw.te2{ background:#c8305c; margin-left:14px; }

/* chart - slide 03 */
.chart{ margin-bottom:26px; }
.chart{ margin-top:54px; }
.bars{ display:flex; align-items:flex-end; gap:34px; height:440px;
  border-bottom:4px solid var(--line); padding:0 26px; }
.bcol{ flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%; }
.bar{ width:100%; border-radius:12px 12px 0 0; position:relative; }
.bar b{ position:absolute; top:-46px; left:0; right:0; text-align:center; font-size:30px;
  font-weight:800; color:var(--ink); }
.b1{ background:#2f5bea; } .b2{ background:#5b82f0; }
.b3{ background:#e09a4a; } .b4{ background:#c8305c; }
.bcol span{ margin-top:14px; font-size:20px; line-height:1.25; text-align:center;
  color:var(--body); font-weight:600; }
.cap{ margin-top:16px; text-align:center; font-size:19px; color:var(--muted); }
.cap b{ color:var(--body); }

/* before/after - slide 04 */
.ba{ display:flex; align-items:center; gap:18px; margin-bottom:24px; }
.ba .b{ flex:0 0 266px; background:#fdf2f5; border-radius:16px; padding:22px 24px;
  border-left:8px solid var(--rose); }
.ba .b i{ font-style:normal; display:block; font-size:23px; line-height:1.4; color:var(--body); }
.ba .b i b{ color:var(--ink); }
.ba .a{ flex:1; background:var(--soft); border-radius:16px; padding:20px 22px;
  border-left:8px solid var(--teal); }
.ba .arrow{ font-size:40px; color:#c3ccdd; font-weight:700; }
.tag{ display:block; font-size:17px; font-weight:800; letter-spacing:.13em; color:var(--muted); margin-bottom:12px; }
.cols{ display:flex; flex-direction:column; gap:9px; }
.cols div{ padding:9px 14px; border-radius:10px; }
.cols b{ display:block; font-family:Consolas,"Cascadia Mono",monospace; font-size:21px; }
.cols span{ display:block; font-size:18px; margin-top:2px; }
.cols .bad{ background:#fbe8ee; } .cols .bad b{ color:#9a2c4d; } .cols .bad span{ color:#a4566f; }
.colnote{ margin-top:12px; font-size:18.5px; line-height:1.35; color:var(--muted); }
.cols .ok{ background:#e3f3f0; } .cols .ok b{ color:#0b6157; font-size:19.5px; } .cols .ok span{ color:#3d7c74; }

/* split comparison - slide 05 */
.split2{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px; }
.sp{ border-radius:16px; padding:20px 22px; }
.sp.bad2{ background:#fdf2f5; border-left:8px solid var(--rose); }
.sp.good2{ background:#eef7f5; border-left:8px solid var(--teal); }
.dots{ display:flex; gap:7px; margin-bottom:9px; }
.dots i{ flex:1; height:42px; border-radius:7px; }
.dots .tr{ background:#98a7c4; } .dots .te{ background:#c8305c; }
.good2 .dots .te{ background:#0e8177; }
.axis{ font-size:17px; color:var(--muted); letter-spacing:.08em; font-weight:700; margin-bottom:12px; }
.sp p{ font-size:21px; line-height:1.4; color:var(--body); }
.sp p b{ color:var(--ink); }

/* split types - slide 07 */
.sgrid{ display:flex; flex-direction:column; gap:13px; margin-bottom:22px; }
.sc{ background:var(--soft); border-radius:14px; padding:16px 22px; border-left:7px solid var(--accent); }
.sc.t{ border-left-color:var(--teal); } .sc.r{ border-left-color:var(--amber); }
.sc b{ display:block; font-size:26px; color:var(--ink); font-weight:800; margin-bottom:5px; }
.sc .when{ display:block; font-size:20px; line-height:1.35; color:var(--body); }
.sc em{ display:block; font-style:normal; margin-top:7px; font-family:Consolas,"Cascadia Mono",monospace;
  font-size:17.5px; color:#3d5891; }

/* red flags - slide 08 */
.fm{ display:grid; grid-template-columns:1fr 1fr; gap:19px; margin-bottom:24px; }
.fmc{ background:#fdf2f5; border-radius:14px; padding:19px 21px; border-left:7px solid var(--rose); }
.fmc.wide{ grid-column:1 / -1; }
.fmc b{ display:block; font-size:26px; color:var(--ink); font-weight:800; margin-bottom:7px; }
.fmc > span{ display:block; font-size:20.5px; line-height:1.37; color:var(--body); }
.fmc .mono{ font-size:.85em; background:#f6e0e6; padding:1px 6px; }

.checks{ list-style:none; counter-reset:c; margin-bottom:24px; display:flex;
  flex-direction:column; gap:17px; }
.checks li{ counter-increment:c; position:relative; padding-left:66px; font-size:24px; line-height:1.4; }
.checks li:before{ content:counter(c); position:absolute; left:0; top:-2px; width:44px; height:44px;
  border-radius:13px; background:var(--accent); color:#fff; font-weight:800; font-size:23px;
  display:flex; align-items:center; justify-content:center; }
.checks li b{ color:var(--ink); }

.prompt{ background:#0d1526; border-radius:18px; padding:28px 32px; margin-top:auto;
  border-left:10px solid var(--teal); }
.prompt .ph{ font-size:18px; font-weight:800; letter-spacing:.16em; color:#7fd6a5; margin-bottom:14px; }
.prompt p{ font-size:25px; line-height:1.47; color:#dbe4f5; }
.prompt b{ color:#fff; }

.cta{ background:var(--ink); border-radius:18px; padding:30px 34px; margin-top:auto; }
.cta-line{ font-size:28px; line-height:1.38; color:#fff; font-weight:700; }
.cta-by{ margin-top:14px; font-size:23px; color:#9db4f7; }
.cta-by b{ color:#fff; }
.srcs{ margin-top:18px; font-size:17px; line-height:1.5; color:var(--muted); }
.srcs b{ color:var(--body); }
"""

TITLE = "Data Leakage: The Silent Way Your Model Cheats"
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
<title>Data Leakage: The Silent Way Your Model Cheats</title><style>%s</style></head><body>%s</body></html>""" % (
    CSS, "\n".join(BODY))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "data_leakage_carousel_2026-09-19.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
