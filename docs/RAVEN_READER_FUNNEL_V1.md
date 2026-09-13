# RAVEN READER FUNNEL V1

## Purpose

Strengthen the reader journey already visible in production analytics without turning Raven into a click-optimised site.

**Social/Threads intent → Narrative → Verdict → Evidence → CASEFILE / primary source**

The objective is not more pageviews. The objective is to move a reader closer to evidence with less friction.

## 1. Narrative deep links

Every current Narrative Forensics card receives a stable static HTML anchor. The slug is created once from the current claim title and then preserved on later builds.

Example shape:

`/investigations/rci-tabung-haji/narratives/#naratif-aset-th-dijual-kepada-bukan-islam-china`

Each card exposes one quiet `Salin link naratif` control. Do not restore per-card social-button walls.

## 2. Contextual Evidence Bridge

After every Raven verdict, show only two high-value next steps:

1. **Buka sumber asal ↗** — the best matching source already present in Raven's Source Room.
2. **Faham keseluruhan kes** — return to the RCI CASEFILE briefing.

The bridge also states which source Raven selected and its source grade. The bridge must never imply that one source alone proves the whole case.

## 3. Raven Read Metrics

Raven uses reader-quality metrics rather than optimising raw bounce rate.

Primary interpretation tiers:

- `read_30s` — quick/engaged read
- `read_60s` — meaningful read
- `deep_read_180s` — deep read
- `scroll_50`
- `scroll_75`
- `scroll_100`
- `narrative_deeplink_land`
- `narrative_deeplink_copy`
- `primary_source_click`
- `case_continuation`
- `narrative_entry`
- `evidence_entry`

Lytical already exposes session duration, scroll, click text and target href. Raven therefore does **not** introduce a second remote analytics backend in V1. Instead, the site standardises semantic event hooks and consistent CTA labels so Lytical analysis can calculate:

**External arrivals → ≥30s → ≥60s → deep read → evidence/source click → CASEFILE continuation**

A `raven:metric` CustomEvent is also emitted in-page for future adapters without rewriting the interaction layer.

## Editorial rule

Never force page changes merely to reduce bounce rate. A reader spending eight minutes on one Narrative page is a successful read even if analytics technically classifies the session as a bounce.

## Acquisition rule

Use intent-matched social landing URLs:

- general RCI / Raven introduction → Homepage or CASEFILE
- specific viral claim → exact Narrative deep link
- financial number → Money
- person / legal status → People
- proof / document question → Source Room
- current development → Newsroom / Updates

## Guardrails

- Existing public URLs remain unchanged.
- Narrative is still one click away globally.
- Evidence copy and legal state are not rewritten by funnel code.
- No new third-party tracking service.
- No card-wall or CTA proliferation.
- Deep links must survive page reloads and mobile rendering.
