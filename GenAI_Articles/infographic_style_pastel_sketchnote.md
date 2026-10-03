# Infographic Style — Pastel Sketchnote

Default visual style for every LinkedIn infographic image prompt. It is fully self-contained:
no reference image needs to be attached.

**How the agent uses this file:** every image prompt = **STYLE BLOCK (copied verbatim)** +
**CONTENT BLOCK (written fresh for the post)**. Never edit, shorten, or paraphrase the style block.

---

## 1. STYLE BLOCK (copy verbatim into every image prompt)

```
Create a portrait educational infographic, 4:5 vertical (1080x1350px), optimized for
mobile LinkedIn. Style: a hand-drawn pastel sketchnote on a white page — like a
teacher's neat whiteboard summary made print-quality.

1. PAGE: The whole page is plain warm off-white paper (#FAFAF7). There is NO colored
   header banner and NO dark areas anywhere. Airy and calm, with generous white space
   between sections.

2. TITLE: Top center, huge bold hand-lettered dark-navy text. Behind the title ONLY,
   one soft pale-blue brush-stroke smear. Three tiny doodle dashes beside the title.
   A centered subtitle in smaller handwriting below it, with no underline.

3. LETTERING: Every word looks hand-lettered with a fine marker: neat, even, rounded
   print handwriting with a straight baseline, like a teacher's clean print. Dark navy
   ink (#1F2340). Not a computer font, not cursive, not bouncy or comic-style.

4. SECTIONS: Sections sit directly on the white page; they are NOT filled boxes.
   Sections are separated only by thin light-gray lines (a thin vertical gray line
   between side-by-side sections). Each section heading starts with a circled number
   (1, 2, 3...) with a thick dark outline and a light pastel fill, followed by the
   heading in bold dark-navy handwriting. Section headings have NO highlight,
   NO pill, and NO background.

5. EMPHASIS: Bold words are simply bold dark-navy lettering, or colored blue or
   coral-red. They have NO highlighter swipe and NO background behind them.

6. CARDS: Inside a section, content may sit in a small rounded card with a VERY faint
   tint (barely-there blue, pink, or yellow). Cards have NO outline or border.
   Most of the page stays white.

7. DIAGRAMS: Simple thin-line drawings with soft pastel fills, dashed guide lines and
   small labels, like a textbook sketch.

8. CALLOUT: At most one pale-yellow note card with a hand-drawn curved black arrow
   pointing at a diagram.

9. ICONS: Small flat icons in muted warm colors with soft shading, simple, used
   sparingly (max 4 on the page).

10. COLOR: Very soft, washed-out pastels only — blue, coral-pink, mint, lavender,
    butter yellow, beige. Blue = correct/good, coral-red = problem/wrong.

11. DOODLES: Small doodle dashes appear ONLY beside the title and beside the
    key-takeaway cards, nowhere else.

12. FOOTER: A thin soft beige band across the bottom. Centered horizontally in it,
    on one line, bold dark-navy handwriting: "Repost & Follow me for more" then a wide
    gap, then "Sagar Rathkanthiwar". Nothing else in the footer — no icons, no avatar.

Render every quoted string exactly as written, correctly spelled. No extra sections,
no extra text, no logos of other companies, no photorealism, no 3D, no gradients.
```

---

## 2. CONTENT BLOCK (agent writes this per post)

Template:

```
CONTENT
Title: "{{short title, max 6 words}}"
Subtitle: "{{one-sentence hook from the post}}"

① ({{color}} number circle) "{{Heading}}" — {{left half | right half | full width}}.
   {{module + exact quoted text}}
② ...
⑥ ({{color}} number circle) "Key takeaway" — {{position}}.
   Two stacked faint cards with small doodle dashes on each side:
   Faint-blue card: "{{rule}} → **{{action}}**"
   Faint-pink card: "{{rule}} → **{{action}}**"

Render every quoted string exactly as written. No extra sections, no extra text.
```

### Section modules (pick 4–6; last is always Key takeaway)

| Module | Use for | Describe as |
|---|---|---|
| Concept card | Defining something | 3 dot bullets, optionally a small icon per row |
| Side-by-side | Before/after, myth/fact, A vs B, AI vs you | Faint-pink card with red ✗ bullets + faint-blue card with blue ✓ bullets |
| Diagram + note | How something works | Simple thin-line sketch + yellow note card with curved arrow |
| Steps / flow | Processes | 3–5 small rounded boxes joined by hand-drawn arrows |
| Example | Real-world scenario | One-line scenario + 1–2 faint cards, one small icon each |
| Code snippet | Technical topics | Faint card with a monospace snippet, max 5 lines, keywords in blue |
| Quick table | Comparing options | Thin gray gridlines, tinted header cells, 3–5 rows, max 3 columns |
| Key takeaway | Always last | 2 stacked faint cards, one-line rules, doodle dashes |

### Content rules
- 5–6 sections total; rotate number-circle colors: blue, mint, pink, lavender, yellow, blue.
- Max ~12 words per bullet; max 3 bullets per card.
- At least one visual module (diagram, flow, or table).
- Put color on the **number circle** and in "faint-blue/faint-pink card" wording only —
  never write "(blue section)", which makes models fill the whole section.
- Give every section a layout hint: left half / right half / full width / bottom-left / bottom-right.
- Every piece of text that should appear goes in quotes.
- Content must be technically correct — double-check diagrams, SQL/code, and table facts.

---

## 3. Worked example — "Why JOINs Still Matter"

```
CONTENT
Title: "Why JOINs Still Matter"
Subtitle: "AI can write SQL for you. But only you can tell if the join is right."

① (blue number circle) "What a JOIN does" — left half.
   Three rows, each with a small icon on the left:
   • table-grid icons "+" : "Combines rows from **two or more tables**"
   • key icon: "Matches them using a **shared key** (e.g. customer_id)"
   • document icon: "Turns scattered data into **one useful answer**"

② (mint number circle) "The 4 joins you need" — right half.
   Four small thin-line two-circle Venn sketches in a row, each with a small pastel
   label above: INNER (only the overlap shaded blue), LEFT (left circle + overlap
   shaded blue), RIGHT (right circle + overlap shaded lavender), FULL (both circles
   shaded pink). Below, a yellow note card with a curved arrow pointing to LEFT:
   "**LEFT JOIN** is the one you'll use most. Unmatched rows show up as **NULL**."

③ (pink number circle) "Why AI doesn't replace this skill" — full width, two faint cards.
   Left faint-pink card, heading "AI-written query", red ✗ bullets:
   • "Picks the wrong join type silently"
   • "Duplicates rows on one-to-many keys"
   • "Runs fine, returns **wrong numbers**"
   Right faint-blue card, heading "You, knowing joins", blue ✓ bullets:
   • "Spot the wrong join in seconds"
   • "Check row counts before trusting results"
   • "Explain **why** the number is right"

④ (lavender number circle) "Real-world scenario" — full width.
   One line: "Find customers who have never placed an order."
   Small shopping-cart icon on the left, then a faint card with a monospace snippet
   (SQL keywords in blue):
     SELECT c.name
     FROM customers c
     LEFT JOIN orders o ON c.id = o.customer_id
     WHERE o.id IS NULL;
   On the right, a small faint-pink card: "**INNER JOIN** here would return zero rows."

⑤ (yellow number circle) "When to use which" — bottom-left.
   Table with thin gray gridlines and pale-yellow tinted header cells:
   Join | Returns | Typical use
   INNER | Matches only | Orders with customer details
   LEFT | All left + matches | Customers with or without orders
   FULL | Everything | Reconciling two data sources
   SELF | Table joined to itself | Employee → manager

⑥ (blue number circle) "Key takeaway" — bottom-right.
   Two stacked faint cards with small doodle dashes on each side:
   Faint-blue card with a small robot icon: "AI writes the join → **you verify it.**"
   Faint-pink card with a small key icon: "Know your keys → **trust your numbers.**"

Render every quoted string exactly as written. No extra sections, no extra text.
```

---

## 4. Fix-up edit prompt (if a generated image drifts)

```
Keep everything else identical, only change: remove any dark header and put the title
on the white page with a pale-blue brush-stroke behind it; remove highlight pills behind
section headings and bold words; remove filled backgrounds and outlines from sections
and cards; separate sections with thin gray lines; make handwriting neat and even;
keep doodle dashes only beside the title and takeaway cards; footer = beige band with
one centered line of bold text: "Repost & Follow me for more" + wide gap +
"Sagar Rathkanthiwar", no icons or avatar.
```
