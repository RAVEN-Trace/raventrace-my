# RAVEN-Trace Malaysia

Independent evidence-led journalism for Malaysia.

This repository contains the mobile-first editorial site for **RAVEN-Trace™ by SharulR X(ai) Projects**.

## Mission

Investigate deeply, separate fact from claim and political narrative, then explain the strongest defensible account to ordinary readers in clear Malaysian Malay.

Public-facing output should be understandable to teenagers, older readers and people without specialist legal, financial or technical knowledge.

## Site structure

- `/` — lead investigation and newsroom front page
- `/news/` — latest verified development desk
- `/news/YYYY/MM/DD/<story>/` — dedicated static story pages for material updates and social sharing
- `/investigations/` — Investigation Desk / index of active CASEFILEs
- `/investigations/rci-tabung-haji/` — auditable CASEFILE for the current lead investigation
- `/methodology/` — evidence labels, source grading, human-clarity rules and source-link standard
- `/tips/` — source-safety guidance and channel status
- `/corrections/` — public correction ledger
- `/about/` — mission, editorial identity, publisher disclosure and principles

## Publication architecture

RAVEN-Trace follows a **story first → evidence one click away → full CASEFILE for audit** model.

- **Homepage / Newsroom** — what changed and why it matters.
- **Dedicated story** — one development explained in public-readable language with status, limits and source links.
- **Investigation Desk** — index of active long-form investigations.
- **CASEFILE** — timeline, people/status ledger, financial records, disputed points, unknowns and evidence controls.
- **Source Room** — direct route back to material public sources.

The public site should not force a casual reader to understand the full forensic framework before they can understand a story.

## Editorial method

Every published item distinguishes facts supported by the available record, attributed claims, inferences, speculation, unknowns and disputed points. Sources are graded A–X by their value for the specific claim being tested, and confidence is stated when material.

Reporter rhythm: **Lead → Context → Evidence → Gap → Impact → Next**.

Public explanation: **Apa berlaku → apa buktinya → apa yang belum tahu → kenapa penting → apa seterusnya**.

## Source-link standard

- Every news item should include at least one source link when a public source is available.
- Investigation findings, timelines, named-person status and material claims should link to a direct source or the CASEFILE Source Room.
- Material numbers/data should link to their source and explain what the metric means.
- If no public source is available, say so. Do not invent a source link.
- Source protection, privacy and safety override public-link requirements for confidential material.

## Share System v2.1

Material story cards receive a compact share toolbar.

- **Kongsi** uses the device-native share sheet when available.
- **WhatsApp** opens a pre-filled evidence-bounded summary.
- **Salin** copies headline, summary, status, original source when available, and the Raven URL.
- **Artikel** appears when that update has a dedicated static story page.
- **Sumber** opens the original reporting/source rather than a social-share service.
- Dedicated story pages now also expose direct **WhatsApp / Salin ringkasan / Sumber asal** controls below the main share action.
- Story pages use dedicated canonical URLs plus `og:title`, `og:description`, `og:image`, `og:type=article`, Twitter card metadata and article timestamps where relevant.
- The share map routes matching Homepage and Newsroom cards to the dedicated story URL; other evidence items keep stable deep anchors.

Initial dedicated story pages cover the 6 September Jamil Khir remand checkpoint, 5 September transparency vox-pop, Madinah–Rashid disputed record, THP Bina RM72,000 court case, and governance-reform progress.

## Evidence-reconciliation rule

Research dossiers and user-supplied compilations are treated as working indexes, not automatically as publication-grade proof. Material claims are reconciled against primary records, official statements, court reporting or independent corroboration before publication. Where reliable records conflict, RAVEN-Trace keeps the point **DISPUTED** or **UNKNOWN** rather than forcing a single answer.

## Local preview

Run a static server from the directory that contains this repository:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/raventrace-my/`.

## GitHub Pages

Deploy from the `main` branch and repository root (`/`). The project-site path is `/raventrace-my/`.

## Status

Public evidence room revised **6 September 2026**.

The RCI Tabung Haji investigation is at **CASEFILE v16**, with the rendered evidence layer reconciled through **6 September 2026 MYT**. Current work includes the 6 September Jamil Khir remand checkpoint, 5 September public-transparency reporting, governance reform progress, disputed Al-Rawda impairment metrics, the public correction ledger, dedicated article-level social metadata, the Investigation Desk, and the publication-architecture pass.

The site records reconciliation corrections including **211 pages rather than 252** for the public RCI report, **30 July rather than 31 July** for announcement of the MACC special task force, and separation of expected/proposed charges from charges actually read in court.

> A lie wins by speed. Truth wins by audit.
