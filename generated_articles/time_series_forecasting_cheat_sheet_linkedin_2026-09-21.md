# Time Series Forecasting Cheat Sheet: Before You Trust the Forecast

**Format:** LinkedIn Carousel (10 slides, 1080 × 1350 portrait)
**Date:** 2026-09-21
**Audience:** Aspiring data scientists, analysts, data professionals, ML practitioners, product leaders, AI-assisted developers
**Assets:**
- PDF — `carousels/time_series_forecasting_carousel_2026-09-21.pdf`
- HTML source — `carousels/time_series_forecasting_carousel_2026-09-21.html`
- Build script — `carousels/build_forecasting_carousel.py`

---

## Slide-by-slide copy

### Slide 1 — Cover

**Eyebrow:** DATA SCIENCE · TIME SERIES FORECASTING CHEAT SHEET

**Title:** Your forecast has a number. **Does it have a decision?**

**Subtitle:** A time-series forecasting cheat sheet for the AI era.

**Topic chips:** Start with the decision · Choosing a horizon · Baselines first · Trend & seasonality · Business calendars · External drivers · Prediction intervals · Backtests & monitoring

**Byline:** Sagar Rathkanthiwar — Data & AI Professional
**Footer:** 10 slides · save for later →

---

### Slide 2 — 01 · Start with the decision

**Headline:** A forecast with no decision is just a chart

**Lead:** **Nobody needs a number. They need to choose something.** Before you model anything, name the decision the forecast is supposed to improve — and who makes it.

**Three worked decisions:**

| Decision | What you forecast | Cadence & owner |
|---|---|---|
| How much inventory do we order? | Weekly units per SKU, per warehouse | Decided every Monday · supply planning |
| How many staff do we schedule? | Hourly arrivals per store | Decided 2 weeks ahead · ops manager |
| Do we adjust the budget? | Quarterly revenue by region | Decided at quarter close · finance |

**The four questions that define the model:**
1. **What is decided?** — order quantity, headcount, budget, capacity
2. **How often?** — sets your forecast frequency: hourly, daily, weekly
3. **How far ahead?** — sets your horizon, and the lead time you must cover
4. **What does being wrong cost?** — over-forecast vs under-forecast are rarely equal

**Kicker:** That last one reshapes everything. **A stockout may cost five times what excess inventory costs** — so the "best" forecast is not the most accurate one, it is the one that minimises the cost of being wrong.

---

### Slide 3 — 02 · The forecast horizon

**Headline:** How far ahead changes *everything*

**Lead:** Horizon is not a parameter you tune at the end. It decides your data, your model, and how much confidence you are entitled to.

**Visual:** A widening uncertainty cone running from NEXT DAY → NEXT WEEK → NEXT QUARTER → NEXT YEAR, with the point forecast as a flat line through the middle and the plausible range fanning out around it.

| Horizon | What drives it | What it decides |
|---|---|---|
| **Next day** | Recent momentum, hour-of-day patterns. Tight intervals. | Dispatch, staffing, on-call |
| **Next week** | Weekly seasonality and the promo calendar dominate. | Ordering and rostering |
| **Next quarter** | Trend, holidays, pricing. Intervals matter more than the point. | Budgets and capacity |
| **Next year** | Scenarios, not predictions. Range planning — low, base, high. | Hiring and contracts |

**Kicker:** **Match the horizon to the lead time of the decision.** If it takes six weeks to receive stock, a one-week forecast is accurate and useless — you needed the six-week number, intervals and all.

---

### Slide 4 — 03 · Build a baseline first

**Headline:** Beat the boring model, or don't ship the clever one

**Lead:** A baseline is a forecast so simple it needs no training. **If the clever model cannot beat it, it has earned nothing.**

| Baseline | Rule | Formula |
|---|---|---|
| **Naive** | tomorrow = today | `forecast(t+1) = y(t)` |
| **Seasonal naive** | same day last week / same month last year | `forecast(t+1) = y(t+1−s)` |
| **Moving average** | mean of the last k periods | `forecast(t+1) = mean(last k values)` |

**Python — seasonal naive + rolling (walk-forward) evaluation:**

```python
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
```

**Kicker:** Report your model **against** this number, not on its own: "MAE 42 vs a seasonal-naive 61 — a 31% improvement." **Model choice depends on your data and decision** — but the baseline comes first, every time.

---

### Slide 5 — 04 · Find the signal

**Headline:** Four things are happening in every series

**Lead:** What you see is a sum. Learning to separate the parts tells you which model — and which mistakes — to expect.

**Visual:** A monthly-active-users line chart labelled *= trend + seasonality + cycle + noise*, with four sparkline panels beneath it.

- **Trend** — The long slope. Growth, decay, a step change after a launch.
- **Seasonality** — **Fixed** period. Hour of day, day of week, month of year.
- **Cycle** — **Variable** length. Economic or product cycles — no fixed calendar.
- **Noise** — Irreducible. If you fit this, you have overfit.

**Kicker:** **Seasonality repeats on a calendar; a cycle does not.** Confusing the two is the classic error — it makes a model extrapolate a boom as if it were a quarterly pattern.

---

### Slide 6 — 05 · Respect the calendar

**Headline:** The business calendar beats the algorithm

**Lead:** Most large forecast misses are not modelling failures. They are **a date the model did not know was special.**

**Visual:** A one-month calendar with weekends, paydays (15th, 30th), a promo run (18–20) and a holiday (25–26) colour-coded, plus a legend.
*Caption: One month, four overlapping calendars. A model given only **the date** sees none of them.*

- **Weekends & weekdays** — Different demand shape entirely, and a month with five Saturdays is not like one with four.
- **Payday effects** — The 1st, the 15th, month end. Retail and payments spike on a schedule the model cannot infer.
- **Promotions & launches** — A self-inflicted spike. Without a promo flag, the model learns it as random noise.
- **Holidays & school terms** — Moving dates (Easter, Diwali, Ramadan) plus the days *around* them.

**Kicker:** Ask the people who live with the series: **"what happened on the weird days?"** That conversation adds more accuracy than switching algorithms — and it is knowledge no model can read out of the numbers.

---

### Slide 7 — 06 · External drivers

**Headline:** A driver is only valid if you'll *have* it in time

**Lead:** Price, marketing spend, weather, rates — covariates can help a lot. But there is one test every one of them must pass first.

> **THE ONLY TEST THAT MATTERS**
> At the moment I produce the forecast, **will I already know this value for every future period I am forecasting?**

| ✅ Passes — known in advance | ❌ Fails — unknown at forecast time |
|---|---|
| **Planned price & promo calendar** — you set it yourself | **Actual weather next month** — needs its own forecast, with its own error |
| **Committed marketing spend** — budget already signed off | **Competitor pricing** — you learn it afterwards |
| **Holidays, paydays, school terms** — known for years ahead | **Same-period web traffic** — arrives at the same time as the target |
| **Store openings, contracted volume** — on the plan | **Economic indicators, unlagged** — published weeks late |

**Kicker:** A failing driver is not always fatal — **lag it** (last month's indicator, yesterday's weather) or feed it a forecast and accept the compounded uncertainty. What you cannot do is train on the actual value and pretend you will have it.

---

### Slide 8 — 07 · Ranges, not false precision

**Headline:** "1,000 units" hides the number you needed

**Lead:** A point forecast is the middle of a distribution presented as a fact. **The width is the decision-relevant part.**

**Visual:** Actuals running into a dashed forecast line with an 80% interval fanning out around it.

| Point forecast | 80% interval | What you order |
|---|---|---|
| **1,000** units next week | **850 – 1,180** the planning range | **1,180** if a stockout costs more than excess |

**Kicker:** Read it out loud: **"we expect about 1,000, and in 8 weeks out of 10 it lands between 850 and 1,180."** That sentence is what lets someone size a safety buffer. "1,000" alone quietly invites a plan with no slack in it.

---

### Slide 9 — 08 · Evaluate and monitor

**Headline:** Backtest forward. Then keep watching.

**Lead:** One train/test split tests one lucky week. **A rolling backtest re-forecasts at many origins** — the way production actually runs.

**Visual:** Four rolling origins, each training on an expanding past window, forecasting the next block, with the remainder marked *not yet available*. Errors are averaged across all origins.

- **MAE** — Average miss *in units*. "We are off by 42 units a day." Easy to explain, easy to cost.
- **MAPE** — Average miss *in percent*. Comparable across products, but breaks near zero and punishes under-forecasts less.
- **vs BASELINE** — The only number that says whether the model was worth building. Always report it.

**After deployment — the part everyone skips:** Chart **actual vs forecast** every cycle · watch for **bias** (missing the same direction repeatedly — a pattern you have not modelled) · alert when error drifts past a threshold · **retrain when the world changes**, not on a calendar reflex.

---

### Slide 10 — 09 · The takeaway / CTA

**Headline:** The goal is not to predict the future. **It is better decisions under uncertainty.**

- **Name the decision first.** Frequency, horizon and the cost of being wrong all fall out of it.
- **Baseline before model.** Seasonal naive is the bar; report every result against it.
- **Separate trend, seasonality, cycle and noise** — and give the model the business calendar.
- **Only use drivers you will know in advance**, or lag them honestly.
- **Ship the range, not the point.** The interval is what makes a plan robust.
- **Backtest forward, then monitor.** A forecast is a system you operate, not a file you deliver.

**AI can draft the model in seconds.** It cannot tell you what decision this serves, whether a driver will exist at forecast time, or what a stockout costs you. **Defining the decision, validating the assumptions and owning the consequences stays human work.**

**CTA:** What decision would a better forecast improve on your team? Tell me below — that answer is the real model spec.

**Note:** the Python example is a baseline, not a recommendation. Model choice — naive, ETS, ARIMA, gradient boosting, deep learning — always depends on your data, horizon and decision context. Numbers shown are illustrative.

---

## LinkedIn caption

Most forecasts get read as certainty.

A number lands in a slide, someone builds a plan around it, and the range that number came from quietly disappears. Then the week goes differently and everyone blames the model.

AI tools will now write you a forecasting pipeline and a beautiful chart in about thirty seconds. What they can't tell you is the part that actually matters: which decision this forecast is supposed to improve.

Because that's the real test. Not MAPE. Not whether you used ARIMA or gradient boosting. The best forecast is the one that makes a specific decision better — how much stock to order, how many people to schedule, whether to move the budget.

So I put together a 10-slide cheat sheet on the judgment side of forecasting:

→ Start with the decision, not the data
→ Match the horizon to the lead time you actually have
→ Build a baseline first (seasonal naive is a tough opponent)
→ Separate trend, seasonality, cycle and noise
→ Respect the business calendar — paydays, promos, holidays
→ Only use drivers you'll actually know in advance
→ Ship a range, not false precision
→ Backtest forward, then monitor for bias after deployment

There's a short Python example in there too — a seasonal-naive baseline with a rolling backtest you can run against anything before you reach for a bigger model.

AI can draft the model. Defining the decision, validating the assumptions and owning the consequences is still your job.

Save this before your next forecasting project.

What decision would a better forecast improve on your team?

#DataScience #TimeSeries #Forecasting #MachineLearning #Analytics #MLOps #AI
