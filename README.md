# RAVEN-Trace Malaysia

Independent evidence-led journalism for Malaysia.

This repository contains the mobile-first editorial site for **RAVEN-Trace™ by SharulR X(ai) Projects**.

## Mission

Investigate deeply, separate fact from claim and political narrative, then explain the strongest defensible account to ordinary readers in clear Malaysian Malay.

Public-facing output should be understandable to teenagers, older readers and people without specialist legal, financial or technical knowledge.

## Site structure

- `/` — lead investigation and newsroom front page
- `/news/` — latest verified development desk
- `/investigations/rci-tabung-haji/` — auditable CASEFILE
- `/methodology/` — evidence labels, source grading, human-clarity rules and source-link standard
- `/tips/` — source-safety guidance and channel status
- `/corrections/` — public correction ledger
- `/about/` — mission, identity and editorial principles

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

## Local preview

Run a static server from the directory that contains this repository:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/raventrace-my/`.

## GitHub Pages

Deploy from the `main` branch and repository root (`/`). The project-site path is `/raventrace-my/`.

## Status

Public evidence room revised 6 September 2026.

The RCI Tabung Haji investigation is at **CASEFILE v16**, with data reconciled through **5 September 2026 MYT**. The public pages now use evidence-bounded wording, simpler public language, direct source links for newsroom updates, disputed-record handling and a public correction ledger.

> A lie wins by speed. Truth wins by audit.
