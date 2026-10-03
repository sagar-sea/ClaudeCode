# -*- coding: utf-8 -*-
"""Builds the 'Time Series Forecasting Cheat Sheet' carousel (1080x1350, 10 slides)."""
import html, re, io, os, math

KEYWORDS = r"""def|return|if|elif|else|for|while|in|not|and|or|is|None|True|False|import|from|as|try|except|finally|raise|with|assert|class|lambda|pass|continue|break|yield"""
FUNCS = r"""print|len|sum|abs|round|float|int|str|list|dict|range|mean|shift|iloc|loc|head|tail|sort_values|read_csv|asfreq|resample|append|dropna|seasonal_naive|backtest|rolling"""


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


# ---------------------------------------------------------------- svg helpers
def poly(points, w, h, x0, x1, y0, y1, stroke, width=3, dash=None, fill=None):
    """Map (x,y) data points into an svg polyline inside the given box."""
    n = len(points)
    xs = [x0 + (x1 - x0) * i / float(n - 1) for i in range(n)]
    lo, hi = min(points), max(points)
    rng = (hi - lo) or 1.0
    ys = [y1 - (y1 - y0) * (v - lo) / rng for v in points]
    pts = " ".join("%.1f,%.1f" % (a, b) for a, b in zip(xs, ys))
    out = ""
    if fill:
        out += '<polygon points="%s %.1f,%.1f %.1f,%.1f" fill="%s"/>' % (
            pts, x1, y1, x0, y1, fill)
    out += ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round" stroke-linecap="round"%s/>' % (
                pts, stroke, width, ' stroke-dasharray="%s"' % dash if dash else ""))
    return out


def end_y(points, y0, y1):
    """The y coordinate poly() will place the LAST point at."""
    lo, hi = min(points), max(points)
    return y1 - (y1 - y0) * (points[-1] - lo) / ((hi - lo) or 1.0)


def series(n, trend=0.0, amp=0.0, period=12, noise_seed=1, noise=0.0, base=50.0):
    """Deterministic pseudo-random series so the build is reproducible."""
    out = []
    s = noise_seed
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        r = (s / 2147483648.0) - 0.5
        out.append(base + trend * i + amp * math.sin(2 * math.pi * i / period) + noise * r)
    return out


S = []

# ------------------------------------------------------------ 01 cover
S.append(('cover', """
<div class="eyebrow light">DATA SCIENCE &middot; TIME SERIES FORECASTING CHEAT SHEET</div>
<h1 class="cover-title">Your forecast<br>has a number.<br><span class="hl">Does it have<br>a decision?</span></h1>
<p class="cover-sub">A time-series forecasting cheat sheet<br>for the AI era.</p>
<div class="chips">
  <span>Start with the decision</span><span>Choosing a horizon</span><span>Baselines first</span>
  <span>Trend &amp; seasonality</span><span>Business calendars</span><span>External drivers</span>
  <span>Prediction intervals</span><span>Backtests &amp; monitoring</span>
</div>
<div class="cover-foot">
  <div class="rule"></div>
  <div class="cover-by">Sagar Rathkanthiwar<span>Data &amp; AI Professional</span></div>
  <div class="cover-meta">10 slides &middot; save for later &rarr;</div>
</div>
"""))

# ------------------------------------------------------------ 02 start with the decision
S.append(('std', """
<div class="eyebrow">01 &middot; START WITH THE DECISION</div>
<h2>A forecast with<br>no decision is<br>just a chart</h2>
<p class="lead"><b>Nobody needs a number. They need to choose something.</b> Before you model anything, name the decision the forecast is supposed to improve &mdash; and who makes it.</p>
<div class="dgrid">
  <div class="dc"><span class="q">HOW MUCH INVENTORY DO WE ORDER?</span><b>Weekly units per SKU, per warehouse</b><span class="w">Decided every Monday &middot; owner: supply planning</span></div>
  <div class="dc t"><span class="q">HOW MANY STAFF DO WE SCHEDULE?</span><b>Hourly arrivals per store</b><span class="w">Decided 2 weeks ahead &middot; owner: ops manager</span></div>
  <div class="dc r"><span class="q">DO WE ADJUST THE BUDGET?</span><b>Quarterly revenue by region</b><span class="w">Decided at quarter close &middot; owner: finance</span></div>
</div>
<div class="ex">
  <span class="tag">THE FOUR QUESTIONS THAT DEFINE THE MODEL</span>
  <div class="qrow"><b>What is decided?</b><span>order quantity, headcount, budget, capacity</span></div>
  <div class="qrow"><b>How often?</b><span>sets your forecast frequency &mdash; hourly, daily, weekly</span></div>
  <div class="qrow"><b>How far ahead?</b><span>sets your horizon &mdash; and the lead time you must cover</span></div>
  <div class="qrow"><b>What does being wrong cost?</b><span>over-forecast vs under-forecast are rarely equal</span></div>
</div>
<p class="kicker">That last one reshapes everything. <b>A stockout may cost five times what excess inventory costs</b> &mdash; so the &ldquo;best&rdquo; forecast is not the most accurate one, it is the one that minimises the cost of being wrong.</p>
"""))

# ------------------------------------------------------------ 03 horizon
S.append(('std', """
<div class="eyebrow">02 &middot; THE FORECAST HORIZON</div>
<h2>How far ahead<br>changes <i>everything</i></h2>
<p class="lead">Horizon is not a parameter you tune at the end. It decides your data, your model, and how much confidence you are entitled to.</p>
<div class="hz">
  <div class="hzbar">
    <span class="h1">NEXT DAY</span><span class="h2">NEXT WEEK</span><span class="h3">NEXT QUARTER</span><span class="h4">NEXT YEAR</span>
  </div>
  <div class="hzcone">""" + """
    <svg viewBox="0 0 932 200" width="932" height="200" preserveAspectRatio="none">
      <polygon points="0,98 932,6 932,194 0,102" fill="#dde5fb"/>
      <polygon points="0,98 932,44 932,156 0,102" fill="#b9cbf7"/>
      <line x1="0" y1="100" x2="932" y2="100" stroke="#2f5bea" stroke-width="4"/>
      <text x="470" y="92" font-family="Segoe UI" font-size="19" font-weight="700" fill="#28468f">POINT FORECAST</text>
      <text x="700" y="34" font-family="Segoe UI" font-size="19" font-weight="700" fill="#5f7fc4">PLAUSIBLE RANGE</text>
    </svg>""" + """</div>
  <div class="hzlab">uncertainty widens with every step you forecast ahead &rarr;</div>
</div>
<div class="hgrid">
  <div class="hc"><b>Next day</b><span>Recent momentum, hour-of-day patterns. Tight intervals. Drives dispatch, staffing, on-call.</span></div>
  <div class="hc t"><b>Next week</b><span>Weekly seasonality and the promo calendar dominate. Drives ordering and rostering.</span></div>
  <div class="hc r"><b>Next quarter</b><span>Trend, holidays, pricing. Intervals matter more than the point. Drives budgets and capacity.</span></div>
  <div class="hc a"><b>Next year</b><span>Scenarios, not predictions. Range planning &mdash; low, base, high. Drives hiring and contracts.</span></div>
</div>
<p class="kicker"><b>Match the horizon to the lead time of the decision.</b> If it takes six weeks to receive stock, a one-week forecast is accurate and useless &mdash; you needed the six-week number, intervals and all.</p>
"""))

# ------------------------------------------------------------ 04 baseline + python
S.append(('std', """
<div class="eyebrow">03 &middot; BUILD A BASELINE FIRST</div>
<h2>Beat the boring<br>model, or don't<br>ship the clever one</h2>
<p class="lead">A baseline is a forecast so simple it needs no training. <b>If the clever model cannot beat it, it has earned nothing.</b></p>
<div class="brow">
  <div class="bc"><b>Naive</b><span>tomorrow = today</span><em>forecast(t+1) = y(t)</em></div>
  <div class="bc t"><b>Seasonal naive</b><span>same day last week / same month last year</span><em>forecast(t+1) = y(t+1&minus;s)</em></div>
  <div class="bc r"><b>Moving average</b><span>mean of the last k periods</span><em>forecast(t+1) = mean(last k values)</em></div>
</div>
""" + code('''
# Seasonal naive: the forecast for a day is the same weekday one
# season ago.  season = 7 daily, 12 monthly, 24 hourly.
SEASON = 7

def seasonal_naive(history, horizon, season=SEASON):
    return [history[-season + (i % season)] for i in range(horizon)]

def backtest(y, horizon=7, season=SEASON):
    errors, start = [], 4 * season     # keep history before scoring
    for t in range(start, len(y) - horizon + 1, horizon):
        forecast = seasonal_naive(y[:t], horizon, season)  # past only
        actual   = y[t:t + horizon]                        # never seen
        errors += [abs(f - a) for f, a in zip(forecast, actual)]
    return sum(errors) / len(errors)   # MAE, in units of the series

print("baseline MAE:", round(backtest(daily_units), 1))
''', cls="xs") + """
<p class="kicker">Report your model <b>against</b> this number, not on its own: &ldquo;MAE 42 vs a seasonal-naive 61 &mdash; a 31% improvement.&rdquo; <b>Model choice depends on your data and decision</b> &mdash; but the baseline comes first, every time.</p>
"""))

# ------------------------------------------------------------ 05 signal
S.append(('std', """
<div class="eyebrow">04 &middot; FIND THE SIGNAL</div>
<h2>Four things are<br>happening in<br>every series</h2>
<p class="lead">What you see is a sum. Learning to separate the parts tells you which model &mdash; and which mistakes &mdash; to expect.</p>
<div class="bigchart">
  <span class="tag">WHAT YOU ACTUALLY OBSERVE &mdash; MONTHLY ACTIVE USERS</span>
  <svg viewBox="0 0 900 262" width="900" height="262">
    <line x1="0" y1="257" x2="900" y2="257" stroke="#e4e8ef" stroke-width="3"/>
    """ + poly(series(48, trend=0.9, amp=9, period=12, noise=5.5, noise_seed=7),
               900, 262, 6, 894, 16, 247, "#2f5bea", 4,
               fill="rgba(47,91,234,0.10)") + """
  </svg>
  <div class="cap">= trend + seasonality + cycle + noise</div>
</div>
<div class="sig4">
  <div class="sg"><span class="h">TREND</span>
    <svg viewBox="0 0 200 74" width="200" height="74">""" +
    poly(series(40, trend=1.0, base=10), 200, 74, 4, 196, 10, 66, "#2f5bea", 4) + """</svg>
    <p>The long slope. Growth, decay, a step change after a launch.</p></div>
  <div class="sg"><span class="h">SEASONALITY</span>
    <svg viewBox="0 0 200 74" width="200" height="74">""" +
    poly([math.sin(2 * math.pi * i / 10.0) for i in range(41)], 200, 74, 4, 196, 10, 66, "#0e8177", 4) + """</svg>
    <p><b>Fixed</b> period. Hour of day, day of week, month of year.</p></div>
  <div class="sg"><span class="h">CYCLE</span>
    <svg viewBox="0 0 200 74" width="200" height="74">""" +
    poly([math.sin(2 * math.pi * i / 27.0) for i in range(41)], 200, 74, 4, 196, 10, 66, "#c07806", 4) + """</svg>
    <p><b>Variable</b> length. Economic or product cycles &mdash; no fixed calendar.</p></div>
  <div class="sg"><span class="h">NOISE</span>
    <svg viewBox="0 0 200 74" width="200" height="74">""" +
    poly(series(41, noise=10, noise_seed=23, base=0), 200, 74, 4, 196, 10, 66, "#c8305c", 3) + """</svg>
    <p>Irreducible. If you fit this, you have overfit.</p></div>
</div>
<p class="kicker"><b>Seasonality repeats on a calendar; a cycle does not.</b> Confusing the two is the classic error &mdash; it makes a model extrapolate a boom as if it were a quarterly pattern.</p>
"""))

# ------------------------------------------------------------ 06 calendar
S.append(('std', """
<div class="eyebrow">05 &middot; RESPECT THE CALENDAR</div>
<h2>The business<br>calendar beats<br>the algorithm</h2>
<p class="lead">Most large forecast misses are not modelling failures. They are <b>a date the model did not know was special.</b></p>
<div class="calwrap">
  <div class="calcol">
  <div class="cal">
    <span class="cd dim">M</span><span class="cd dim">T</span><span class="cd dim">W</span><span class="cd dim">T</span><span class="cd dim">F</span><span class="cd dim">S</span><span class="cd dim">S</span>
    <span class="cd">1</span><span class="cd">2</span><span class="cd">3</span><span class="cd">4</span><span class="cd">5</span><span class="cd we">6</span><span class="cd we">7</span>
    <span class="cd">8</span><span class="cd">9</span><span class="cd">10</span><span class="cd">11</span><span class="cd">12</span><span class="cd we">13</span><span class="cd we">14</span>
    <span class="cd pay">15</span><span class="cd">16</span><span class="cd">17</span><span class="cd promo">18</span><span class="cd promo">19</span><span class="cd we promo">20</span><span class="cd we">21</span>
    <span class="cd">22</span><span class="cd">23</span><span class="cd">24</span><span class="cd hol">25</span><span class="cd hol">26</span><span class="cd we">27</span><span class="cd we">28</span>
    <span class="cd">29</span><span class="cd pay">30</span><span class="cd">31</span>
    </div>
    <div class="clg">
      <div><i class="we"></i>Weekend</div>
      <div><i class="pay"></i>Payday</div>
      <div><i class="promo"></i>Promotion</div>
      <div><i class="hol"></i>Holiday</div>
    </div>
    <p class="calnote">One month, four overlapping calendars. A model given only <b>the date</b> sees none of them.</p>
  </div>
  <div class="callist">
    <div class="cl we2"><b>Weekends &amp; weekdays</b><span>Different demand shape entirely &mdash; and a month with five Saturdays is not like one with four.</span></div>
    <div class="cl pay2"><b>Payday effects</b><span>The 1st, the 15th, month end. Retail and payments spike on a schedule the model cannot infer.</span></div>
    <div class="cl promo2"><b>Promotions &amp; launches</b><span>A self-inflicted spike. Without a promo flag, the model learns it as random noise.</span></div>
    <div class="cl hol2"><b>Holidays &amp; school terms</b><span>Moving dates &mdash; Easter, Diwali, Ramadan &mdash; plus the days <i>around</i> them.</span></div>
  </div>
</div>
<p class="kicker">Ask the people who live with the series: <b>&ldquo;what happened on the weird days?&rdquo;</b> That conversation adds more accuracy than switching algorithms &mdash; and it is knowledge no model can read out of the numbers.</p>
"""))

# ------------------------------------------------------------ 07 external drivers
S.append(('std', """
<div class="eyebrow">06 &middot; EXTERNAL DRIVERS</div>
<h2>A driver is only<br>valid if you'll<br><i>have</i> it in time</h2>
<p class="lead">Price, marketing spend, weather, rates &mdash; covariates can help a lot. But there is one test every one of them must pass first.</p>
<div class="testbox">
  <span class="tnum">THE ONLY TEST THAT MATTERS</span>
  <p>At the moment I produce the forecast, <b>will I already know this value for every future period I am forecasting?</b></p>
</div>
<div class="dcols">
  <div class="dcol ok3">
    <span class="tag">PASSES &mdash; KNOWN IN ADVANCE</span>
    <div class="dr"><b>Planned price &amp; promo calendar</b><span>you set it yourself</span></div>
    <div class="dr"><b>Committed marketing spend</b><span>budget already signed off</span></div>
    <div class="dr"><b>Holidays, paydays, school terms</b><span>known for years ahead</span></div>
    <div class="dr"><b>Store openings, contracted volume</b><span>on the plan</span></div>
  </div>
  <div class="dcol no3">
    <span class="tag">FAILS &mdash; UNKNOWN AT FORECAST TIME</span>
    <div class="dr"><b>Actual weather next month</b><span>needs its own forecast &mdash; with its own error</span></div>
    <div class="dr"><b>Competitor pricing</b><span>you learn it afterwards</span></div>
    <div class="dr"><b>Same-period web traffic</b><span>arrives at the same time as the target</span></div>
    <div class="dr"><b>Economic indicators, unlagged</b><span>published weeks late &mdash; lag them or drop them</span></div>
  </div>
</div>
<p class="kicker">A failing driver is not always fatal &mdash; <b>lag it</b> (last month's indicator, yesterday's weather) or feed it a forecast and accept the compounded uncertainty. What you cannot do is train on the actual value and pretend you will have it.</p>
"""))

# ------------------------------------------------------------ 08 intervals
ACTUALS = series(30, trend=1.1, amp=7, period=7, noise=5, noise_seed=11)
_y = end_y(ACTUALS, 150, 304)                # where the actuals line stops
_yf = _y - 26                                # median drifts gently upward
FAN = (
    # widest band first, then the inner band, both symmetric about the median
    '<polygon points="520,%.1f 906,%.1f 906,%.1f" fill="#dde5fb"/>'
    '<polygon points="520,%.1f 906,%.1f 906,%.1f" fill="#b9cbf7"/>'
    '<line x1="520" y1="%.1f" x2="906" y2="%.1f" stroke="#2f5bea" '
    'stroke-width="4" stroke-dasharray="10 7"/>'
    '<circle cx="520" cy="%.1f" r="7" fill="#0d1526"/>'
) % (_y, _yf - 86, _yf + 86,
     _y, _yf - 45, _yf + 45,
     _y, _yf, _y)

S.append(('std', """
<div class="eyebrow">07 &middot; RANGES, NOT FALSE PRECISION</div>
<h2>&ldquo;1,000 units&rdquo;<br>hides the number<br>you needed</h2>
<p class="lead">A point forecast is the middle of a distribution presented as a fact. <b>The width is the decision-relevant part.</b></p>
<div class="fan">
  <svg viewBox="0 0 920 336" width="920" height="336">
    <line x1="0" y1="328" x2="920" y2="328" stroke="#e4e8ef" stroke-width="3"/>
    <line x1="520" y1="12" x2="520" y2="328" stroke="#94a3bb" stroke-width="3" stroke-dasharray="8 8"/>
    """ + FAN + """
    """ + poly(ACTUALS, 920, 336, 8, 520, 150, 304, "#0d1526", 4) + """
    <text x="130" y="320" font-family="Segoe UI" font-size="21" font-weight="700" fill="#64748b">ACTUALS</text>
    <text x="600" y="320" font-family="Segoe UI" font-size="21" font-weight="700" fill="#2f5bea">FORECAST + 80% INTERVAL</text>
  </svg>
</div>
<div class="numrow">
  <div class="nb"><span>POINT FORECAST</span><b>1,000</b><i>units next week</i></div>
  <div class="nb mid"><span>80% INTERVAL</span><b>850 &ndash; 1,180</b><i>the planning range</i></div>
  <div class="nb hi"><span>WHAT YOU ORDER</span><b>1,180</b><i>if a stockout costs more than excess</i></div>
</div>
<p class="kicker">Read it out loud: <b>&ldquo;we expect about 1,000, and in 8 weeks out of 10 it lands between 850 and 1,180.&rdquo;</b> That sentence is what lets someone size a safety buffer. &ldquo;1,000&rdquo; alone quietly invites a plan with no slack in it.</p>
"""))

# ------------------------------------------------------------ 09 evaluate & monitor
S.append(('std', """
<div class="eyebrow">08 &middot; EVALUATE AND MONITOR</div>
<h2>Backtest forward.<br>Then keep<br>watching.</h2>
<p class="lead">One train/test split tests one lucky week. <b>A rolling backtest re-forecasts at many origins</b> &mdash; the way production actually runs.</p>
<div class="roll">
  <div class="rr"><span class="rl">ORIGIN 1</span><i class="tr" style="flex:6"></i><i class="fc" style="flex:2"></i><i class="un" style="flex:8"></i></div>
  <div class="rr"><span class="rl">ORIGIN 2</span><i class="tr" style="flex:8"></i><i class="fc" style="flex:2"></i><i class="un" style="flex:6"></i></div>
  <div class="rr"><span class="rl">ORIGIN 3</span><i class="tr" style="flex:10"></i><i class="fc" style="flex:2"></i><i class="un" style="flex:4"></i></div>
  <div class="rr"><span class="rl">ORIGIN 4</span><i class="tr" style="flex:12"></i><i class="fc" style="flex:2"></i><i class="un" style="flex:2"></i></div>
  <div class="legend"><span class="sw tr"></span> train on the past <span class="sw fc"></span> forecast &amp; score <span class="sw un"></span> not yet available &nbsp;&middot;&nbsp; average the errors across all origins</div>
</div>
<div class="mgrid">
  <div class="mc"><b>MAE</b><span>Average miss <i>in units</i>. &ldquo;We are off by 42 units a day.&rdquo; Easy to explain, easy to cost.</span></div>
  <div class="mc t"><b>MAPE</b><span>Average miss <i>in percent</i>. Comparable across products &mdash; but breaks near zero and punishes under-forecasts less.</span></div>
  <div class="mc r"><b>vs BASELINE</b><span>The only number that says whether the model was worth building. Always report it.</span></div>
</div>
<div class="mon">
  <span class="tag">AFTER DEPLOYMENT &mdash; THE PART EVERYONE SKIPS</span>
  <p>Chart <b>actual vs forecast</b> every cycle &middot; watch for <b>bias</b> (missing the same direction repeatedly &mdash; a pattern you have not modelled) &middot; alert when error drifts past a threshold &middot; <b>retrain when the world changes</b>, not on a calendar reflex.</p>
</div>
"""))

# ------------------------------------------------------------ 10 CTA
S.append(('std', """
<div class="eyebrow">09 &middot; THE TAKEAWAY</div>
<h2>The goal is not to<br>predict the future.<br><span class="hl2">It is better decisions<br>under uncertainty.</span></h2>
<div class="rules">
  <div><b>Name the decision first.</b> Frequency, horizon and the cost of being wrong all fall out of it.</div>
  <div><b>Baseline before model.</b> Seasonal naive is the bar; report every result against it.</div>
  <div><b>Separate trend, seasonality, cycle and noise</b> &mdash; and give the model the business calendar.</div>
  <div><b>Only use drivers you will know in advance</b>, or lag them honestly.</div>
  <div><b>Ship the range, not the point.</b> The interval is what makes a plan robust.</div>
  <div><b>Backtest forward, then monitor.</b> A forecast is a system you operate, not a file you deliver.</div>
</div>
<div class="airow">
  <b>AI can draft the model in seconds.</b> It cannot tell you what decision this serves, whether a driver will exist at forecast time, or what a stockout costs you. <b>Defining the decision, validating the assumptions and owning the consequences stays human work.</b>
</div>
<div class="cta">
  <div class="cta-line">What decision would a better forecast improve on your team?<br>Tell me below &mdash; that answer is the real model spec.</div>
  <div class="cta-by"><b>Sagar Rathkanthiwar</b> &middot; Data &amp; AI Professional &middot; follow for more field guides</div>
</div>
<div class="srcs"><b>Note:</b> the Python example is a baseline, not a recommendation. Model choice &mdash; naive, ETS, ARIMA, gradient boosting, deep learning &mdash; always depends on your data, horizon and decision context. Numbers shown are illustrative.</div>
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
  margin-bottom:22px; overflow:hidden; }
.code.sm{ font-size:19px; line-height:1.48; padding:24px 28px; }
.code.xs{ font-size:18px; line-height:1.42; padding:20px 26px; margin-bottom:20px; }
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

.rules{ display:flex; flex-direction:column; gap:15px; margin-bottom:22px; }
.rules div{ font-size:24px; line-height:1.42; padding-left:34px; position:relative; }
.rules div:before{ content:""; position:absolute; left:0; top:9px; width:16px; height:16px;
  border-radius:5px; background:var(--accent); }
.rules div b{ color:var(--ink); }
.tag{ display:block; font-size:17px; font-weight:800; letter-spacing:.13em; color:var(--muted); margin-bottom:12px; }

/* ---- slide 02 decisions */
.dgrid{ display:flex; gap:14px; margin-bottom:22px; }
.dc{ flex:1; background:var(--soft); border-radius:14px; padding:16px 18px; border-top:7px solid var(--accent); }
.dc.t{ border-top-color:var(--teal); } .dc.r{ border-top-color:var(--amber); }
.dc .q{ display:block; font-size:16px; font-weight:800; letter-spacing:.09em; color:var(--muted); margin-bottom:9px; line-height:1.3; }
.dc b{ display:block; font-size:23px; line-height:1.28; color:var(--ink); margin-bottom:7px; }
.dc .w{ display:block; font-size:18px; line-height:1.3; color:var(--body); }
.ex{ background:#eef2fb; border-radius:16px; padding:18px 22px; margin-bottom:22px; }
.qrow{ display:flex; align-items:baseline; gap:14px; padding:7px 0; border-bottom:2px solid #dfe6f4; }
.qrow:last-child{ border-bottom:none; }
.qrow b{ flex:0 0 250px; font-size:23px; color:var(--ink); }
.qrow span{ font-size:20px; line-height:1.3; color:var(--body); }

/* ---- slide 03 horizon */
.hz{ margin-bottom:22px; }
.hzbar{ display:flex; gap:6px; margin-bottom:10px; }
.hzbar span{ flex:1; text-align:center; font-size:18px; font-weight:800; letter-spacing:.1em;
  padding:11px 0; border-radius:9px; }
.hzbar .h1{ background:#e6edfd; color:#28468f; }
.hzbar .h2{ background:#dbe5fc; color:#28468f; }
.hzbar .h3{ background:#cdd9fa; color:#22407f; }
.hzbar .h4{ background:#bccdf8; color:#1c3873; }
.hzcone{ line-height:0; }
.hzlab{ margin-top:8px; text-align:right; font-size:19px; color:var(--muted); font-weight:700; }
.hgrid{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:22px; }
.hc{ background:var(--soft); border-radius:14px; padding:15px 20px; border-left:7px solid var(--accent); }
.hc.t{ border-left-color:var(--teal); } .hc.r{ border-left-color:var(--amber); } .hc.a{ border-left-color:var(--rose); }
.hc b{ display:block; font-size:25px; color:var(--ink); font-weight:800; margin-bottom:4px; }
.hc span{ display:block; font-size:19.5px; line-height:1.33; color:var(--body); }

/* ---- slide 04 baselines */
.brow{ display:flex; gap:14px; margin-bottom:18px; }
.bc{ flex:1; background:var(--soft); border-radius:14px; padding:12px 17px; border-left:7px solid var(--accent); }
.bc.t{ border-left-color:var(--teal); } .bc.r{ border-left-color:var(--amber); }
.bc b{ display:block; font-size:24px; color:var(--ink); font-weight:800; }
.bc span{ display:block; font-size:19px; line-height:1.3; color:var(--body); margin-top:3px; }
.bc em{ display:block; font-style:normal; margin-top:8px; font-family:Consolas,"Cascadia Mono",monospace;
  font-size:17.5px; color:#3d5891; }

/* ---- slide 05 signal */
.bigchart{ background:var(--soft); border-radius:16px; padding:16px 20px 12px; margin-bottom:18px; }
.bigchart svg{ display:block; width:100%; height:auto; }
.cap{ margin-top:6px; text-align:center; font-size:19px; color:var(--muted); font-weight:600; }
.sig4{ display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:13px; margin-bottom:20px; }
.sg{ background:#fff; border:2px solid var(--line); border-radius:14px; padding:12px 14px; }
.sg .h{ display:block; font-size:17px; font-weight:800; letter-spacing:.11em; color:var(--ink); margin-bottom:4px; }
.sg svg{ display:block; width:100%; height:auto; }
.sg p{ font-size:17.5px; line-height:1.32; color:var(--body); margin-top:6px; }
.sg p b{ color:var(--ink); }

/* ---- slide 06 calendar */
.calwrap{ display:flex; gap:20px; margin-bottom:22px; }
.calcol{ flex:0 0 330px; }
.cal{ display:grid; grid-template-columns:repeat(7,1fr); gap:6px; align-content:start; }
.clg{ margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:8px 10px; }
.clg div{ display:flex; align-items:center; gap:8px; font-size:18px; font-weight:600; color:var(--body); }
.clg i{ width:18px; height:18px; border-radius:5px; flex:0 0 18px; }
.clg .we{ background:#e6edfd; } .clg .pay{ background:#0e8177; }
.clg .promo{ background:#c07806; } .clg .hol{ background:#c8305c; }
.calnote{ margin-top:16px; font-size:19px; line-height:1.35; color:var(--muted); }
.calnote b{ color:var(--body); }
.cd{ height:42px; display:flex; align-items:center; justify-content:center; border-radius:8px;
  background:#f1f4fa; color:var(--body); font-size:19px; font-weight:700; }
.cd.dim{ background:none; color:var(--muted); font-size:16px; letter-spacing:.06em; height:26px; }
.cd.we{ background:#e6edfd; color:#28468f; }
.cd.pay{ background:#0e8177; color:#fff; }
.cd.promo{ background:#c07806; color:#fff; }
.cd.hol{ background:#c8305c; color:#fff; }
.callist{ flex:1; display:flex; flex-direction:column; gap:11px; }
.cl{ border-radius:13px; padding:13px 17px; background:var(--soft); border-left:7px solid var(--accent); }
.cl.we2{ border-left-color:#28468f; } .cl.pay2{ border-left-color:var(--teal); }
.cl.promo2{ border-left-color:var(--amber); } .cl.hol2{ border-left-color:var(--rose); }
.cl b{ display:block; font-size:24px; color:var(--ink); font-weight:800; margin-bottom:3px; }
.cl span{ display:block; font-size:19.5px; line-height:1.32; color:var(--body); }
.cl i{ font-style:italic; }

/* ---- slide 07 drivers */
.testbox{ background:var(--ink); border-radius:16px; padding:22px 28px; margin-bottom:20px;
  border-left:10px solid var(--teal); }
.testbox .tnum{ display:block; font-size:17px; font-weight:800; letter-spacing:.16em; color:#7fd6a5; margin-bottom:10px; }
.testbox p{ font-size:26px; line-height:1.4; color:#dbe4f5; }
.testbox b{ color:#fff; }
.dcols{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px; }
.dcol{ border-radius:16px; padding:16px 18px; }
.dcol.ok3{ background:#eef7f5; border-top:7px solid var(--teal); }
.dcol.no3{ background:#fdf2f5; border-top:7px solid var(--rose); }
.dr{ padding:8px 0; border-bottom:2px solid rgba(0,0,0,.05); }
.dr:last-child{ border-bottom:none; }
.dr b{ display:block; font-size:21px; color:var(--ink); }
.dr span{ display:block; font-size:18px; line-height:1.28; color:var(--body); margin-top:2px; }

/* ---- slide 08 intervals */
.fan{ background:var(--soft); border-radius:16px; padding:14px 18px; margin-bottom:18px; }
.fan svg{ display:block; width:100%; height:auto; }
.numrow{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; margin-bottom:20px; }
.nb{ background:#fff; border:2px solid var(--line); border-radius:14px; padding:14px 18px; text-align:center; }
.nb.mid{ background:#e6edfd; border-color:#b9cbf7; } .nb.hi{ background:#eef7f5; border-color:#a8d6ce; }
.nb span{ display:block; font-size:16px; font-weight:800; letter-spacing:.11em; color:var(--muted); }
.nb b{ display:block; font-size:38px; color:var(--ink); font-weight:800; margin:5px 0 3px; letter-spacing:-.02em; }
.nb i{ display:block; font-style:normal; font-size:18px; color:var(--body); line-height:1.25; }

/* ---- slide 09 rolling backtest */
.roll{ background:var(--soft); border-radius:16px; padding:18px 20px; margin-bottom:18px; }
.rr{ display:flex; align-items:center; gap:5px; margin-bottom:8px; }
.rl{ flex:0 0 118px; font-size:16px; font-weight:800; letter-spacing:.09em; color:var(--muted); }
.rr i{ height:32px; border-radius:6px; }
.rr .tr{ background:#98a7c4; } .rr .fc{ background:#2f5bea; } .rr .un{ background:#e4e8ef; }
.legend{ display:flex; align-items:center; gap:9px; font-size:18px; color:var(--muted);
  font-weight:600; margin-top:12px; }
.legend .sw{ display:inline-block; width:24px; height:15px; border-radius:5px; }
.legend .sw.tr{ background:#98a7c4; }
.legend .sw.fc{ background:#2f5bea; margin-left:12px; }
.legend .sw.un{ background:#e4e8ef; margin-left:12px; }
.mgrid{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:14px; margin-bottom:18px; }
.mc{ background:#fff; border:2px solid var(--line); border-radius:14px; padding:14px 17px;
  border-top:7px solid var(--accent); }
.mc.t{ border-top-color:var(--teal); } .mc.r{ border-top-color:var(--amber); }
.mc b{ display:block; font-size:25px; color:var(--ink); font-weight:800; margin-bottom:5px; }
.mc span{ display:block; font-size:19px; line-height:1.32; color:var(--body); }
.mc i{ font-style:italic; }
.mon{ margin-top:auto; background:var(--ink); border-radius:16px; padding:20px 26px;
  border-left:10px solid var(--amber); }
.mon .tag{ color:#f2b45c; margin-bottom:10px; }
.mon p{ font-size:23px; line-height:1.48; color:#dbe4f5; }
.mon b{ color:#fff; }

/* ---- slide 10 */
.airow{ background:#eef2fb; border-radius:16px; padding:17px 26px; margin-bottom:16px;
  font-size:23px; line-height:1.4; color:var(--body); border-left:8px solid var(--teal); }
.airow b{ color:var(--ink); }
.cta{ background:var(--ink); border-radius:18px; padding:26px 32px; margin-top:auto; }
.cta-line{ font-size:28px; line-height:1.38; color:#fff; font-weight:700; }
.cta-by{ margin-top:12px; font-size:22px; color:#9db4f7; }
.cta-by b{ color:#fff; }
.srcs{ margin-top:13px; font-size:16.5px; line-height:1.42; color:var(--muted); }
.srcs b{ color:var(--body); }
"""

TITLE = "Time Series Forecasting Cheat Sheet"
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
<title>Time Series Forecasting Cheat Sheet: Before You Trust the Forecast</title>
<style>%s</style></head><body>%s</body></html>""" % (CSS, "\n".join(BODY))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "time_series_forecasting_carousel_2026-09-21.html")
with io.open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", out, len(HTML), "bytes,", len(S), "slides")
