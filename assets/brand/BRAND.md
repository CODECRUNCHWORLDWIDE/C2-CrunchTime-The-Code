# C2 · CrunchTime — The Code — Brand Guide

> **Voice:** modern, technical, startup-engineering — but still recognizably part of the Code Crunch editorial family.
> **Feel:** the inside of a working dev tool. Terminal-adjacent. Confident. Not glossy SaaS.

This guide extends the family brand (see `../../../assets/brand/BRAND-FAMILY.md`) with C2-specific overrides. Everything not listed here inherits from the family guide.

---

## Brand identity

- **Full name:** CrunchTime — The Code
- **Program code:** C2
- **Full title in copy:** *C2 · CrunchTime — The Code*
- **Tagline (short):** Interview prep, done right.
- **Tagline (long):** A free, open-source technical interview preparation course built around the FRAME Method — recognize patterns, explain your thinking, and walk out with the offer.
- **Parent org:** Code Crunch Worldwide ([github.com/CODECRUNCHWORLDWIDE](https://github.com/CODECRUNCHWORLDWIDE))
- **Canonical URL:** `codecrunchglobal.vercel.app/course-c2-crunchtime`
- **Repository:** [github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code](https://github.com/CODECRUNCHWORLDWIDE/C2-CrunchTime-The-Code)
- **License:** GPL-3.0

---

## Where C2 diverges from the C1 family palette

C1 is editorial (parchment, gold, serif). C2 is **technical** — same family, but tuned for code-first surfaces:

| Role | Name | Hex | Use |
|------|------|------|-----|
| Primary | Ink | `#0B1B2C` | Inherited from family. Body text, structural rails. |
| Accent | Crunch Teal | `#2DD4BF` | **C2 override.** The "live cursor" accent — terminals, highlights, the FRAME letter glyphs. |
| Accent deep | Crunch Teal deep | `#0E9484` | Hover states, secondary buttons, eyebrows on parchment. |
| Accent soft | Crunch Teal soft | `#A6F1E5` | Tag chips, subtle highlights, "step active" bars. |
| Code surface | Crunch Slate | `#0F172A` | Background of code blocks, terminal panels. Sits "behind" the Ink. |
| Code text | Crunch Mint | `#5EEAD4` | Code on Slate. Reads as live terminal output. |
| Editorial bg | Parchment | `#F6F1E7` | Inherited. Background where we want warmth (study plans, behavioral material). |
| Rule | Rule | `#C8B89E` | Inherited. |
| Muted | Muted | `#6A6157` | Inherited. |

```css
:root {
  /* inherited from C1 family */
  --ink:        #0B1B2C;
  --parchment:  #F6F1E7;
  --rule:       #C8B89E;
  --muted:      #6A6157;

  /* C2-specific */
  --teal:        #2DD4BF;
  --teal-deep:   #0E9484;
  --teal-soft:   #A6F1E5;
  --crunch-slate: #0F172A;
  --crunch-mint:  #5EEAD4;
}
```

### When to use which surface

- **Parchment + Ink + Teal-deep** — study plans, behavioral material, anything narrative.
- **Slate + Mint + Teal** — code surfaces, the live FRAME walkthrough widget, mock-interview transcripts.
- **Never** put Teal on Parchment for body text — contrast is too low. Teal-deep on Parchment is fine.

---

## Typography

We **keep** the family display + body faces and **add** one technical accent.

| Role | Family | Use |
|------|--------|-----|
| Display | EB Garamond (italic 500) | Section headers, chapter numerals — same as family |
| Body | Lora | Long-form lecture notes, study plans |
| **Mono / UI / code / FRAME letters** | **JetBrains Mono** | **C2 prefers JetBrains Mono for nearly every UI element** — buttons, badges, the U-M-P-I-R-E step chips, terminal output. This is the visual signal: "you are reading something that runs." |
| Optional | Inter | Acceptable substitute for JetBrains Mono in dense UI tables (e.g., the pattern grid). |

> If you have to pick one face that makes C2 feel different from C1, it's **JetBrains Mono used as a UI face**, not just as code. C1 uses mono only in code blocks. C2 uses mono in chrome.

---

## The FRAME glyphs

The six letters U-M-P-I-R-E are the most recognizable C2 visual element. Treat them as a system:

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│ U │  │ M │  │ P │  │ I │  │ R │  │ E │
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
```

Rules:

- **Always** in JetBrains Mono, weight 700, monospace.
- **Always** with the hairline frame around each letter (`--rule` color, 1px).
- **Always** in this order. Never reorder, never abbreviate to "UM" or "UPI."
- **Step active state:** swap the frame color to `--teal-deep` and fill the background with `--teal-soft`. Inactive frames stay on parchment with rule color.
- **Letters retain meaning under translation.** Don't localize the letters. In a Spanish edition, the words below the letters translate (Entender / Coincidir / Planear / …), but the letters stay U-M-P-I-R-E.

This glyph block is C2's equivalent of the C1 gold dot — the visual handshake of the program.

---

## Voice rules (extending family voice)

C2 keeps the family tone (editorial, serious, no emojis in body, no hype) but adds a few C2-specific notes:

- **Speak engineering, not exam prep.** "Solve the problem" not "ace the question." "Whiteboard cleanly" not "crush the interview." The latter sounds like a SaaS sales page.
- **Refer to the method by name.** Always "the FRAME Method," capitalized. Never "the method," "our framework," or other shortenings on first reference.
- **Concrete > motivational.** Don't tell the learner they can do it. Show them what specifically they will be able to do, with metrics: "Solve a medium problem in 30–35 minutes," not "feel confident in interviews."
- **Acknowledge the hard parts.** Interviewing is psychologically grueling. We address that in copy, never minimize it.
- **No "rockstar," "ninja," "10x."** Ever. Anywhere.

---

## Asset list (to produce)

The following per-track assets should exist under `branding/`:

- [x] `BRAND.md` — this file
- [ ] `c2-logo-full.svg` — wordmark with the FRAME glyph row beneath
- [ ] `c2-logo-mark.svg` — just the FRAME glyph row, square crop
- [ ] `c2-favicon.svg` — single "U" tile with Teal frame
- [ ] `c2-og-image.svg` and `.png` (1200×630) — for social sharing
- [ ] `c2-pattern-grid.svg` — the 14-pattern visual map used on the course page

When generating these, follow the typography + color rules above. Logos are GPL-3.0; anyone can use, fork, modify with attribution back.

---

## The 14-pattern visual map

C2 uses a fixed 14-cell grid as the visual organizing principle for the curriculum. Each cell is one pattern, colored by phase. Use this on the course page, on the README, and on the Week 0 onboarding poster.

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Arrays &    │ Sliding     │ Fast/Slow   │ Binary      │
│ Two Pointers│ Window      │ Pointers    │ Search      │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ BFS         │ DFS         │ Backtrack   │ Top-K /     │
│             │             │             │ Heap        │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Intervals   │ Dynamic     │ Dynamic     │ Greedy      │
│             │ Prog 1D     │ Prog 2D     │             │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Bit         │ Design /    │             │             │
│ Manipulation│ System      │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

(14 patterns, 16 cells, 2 reserved for future expansion — not a coincidence. We chose 14 deliberately because it fits a 3.5-day weekly drill cycle.)

Cells are colored by phase:

- **Phase 1 (Weeks 1–4):** Teal soft fill — fundamentals.
- **Phase 2 (Weeks 5–9):** Teal mid fill — core patterns.
- **Phase 3 (Weeks 10–12):** Teal deep fill — advanced & design.
- **Phase 4 (Weeks 13–15):** Slate fill, Mint border — capstone + mocks.

---

## Web / page conventions

For the course page (`course-c2-crunchtime.html`):

- **Above the fold:** the program code "C2", the wordmark, the FRAME glyph row, the short tagline, two CTAs ("Start the 15-week" / "Start the 1-year"). Slate background — terminal-feel. Mint cursor accent.
- **Second section:** the 14-pattern grid.
- **Third section:** sample FRAME walkthrough on a real problem (live, scrollable).
- **Then:** weekly breakdown for both pathways, side-by-side.
- **Then:** what you ship (portfolio outcomes).
- **Finally:** start CTAs + links to GitHub + master catalog.

No marketing testimonials. No "learners hired at" logo wall (gauche; unverifiable). The portfolio is the proof.

---

*This brand guide is GPL-3.0 like the rest of the curriculum. Forks welcome — please rename your fork to avoid trademark confusion with the original.*
