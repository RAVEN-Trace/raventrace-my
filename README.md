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

## Share System v1

Material story cards now receive a compact share toolbar when the page loads.

- **Kongsi** uses the device-native share sheet when available, so readers can send to WhatsApp, Telegram, Facebook, Threads, X, Messages and other installed apps.
- **WhatsApp** opens a pre-filled message directly.
- **Salin** copies the Raven summary, evidence/status label when available, original source link when available, and a deep link back to the exact card or evidence item.
- Shared deep links use stable page anchors generated from the article context. Opening one re-focuses the relevant card; closed investment records are opened automatically.
- The share text is generated at click time so later evidence/status updates are reflected instead of reusing stale wording.

### Current social-preview limitation

Anchor links such as `/news/#...` and `/investigations/.../#...` still inherit the **page-level** Open Graph preview used by WhatsApp/Facebook/X crawlers. JavaScript cannot reliably provide a unique crawler preview for each anchor.

For story-specific title, image and preview text, material stories should eventually receive their own static URL with dedicated `og:title`, `og:description` and `og:image`. That is the intended Share System v2 path; v1 prioritises accurate summary + source + deep link without pretending anchor metadata is story-specific.

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

The RCI Tabung Haji investigation is at **CASEFILE v16**, with the rendered evidence layer reconciled through **6 September 2026 · early morning MYT**. Current updates include the 6 September Jamil Khir remand checkpoint, 5 September public-transparency reporting, governance reform progress, disputed Al-Rawda impairment metrics, a stricter correction ledger, and Share System v1 across news and investigation cards.

The site records several reconciliation corrections, including **211 pages rather than 252** for the public RCI report, **30 July rather than 31 July** for announcement of the MACC special task force, and separation of expected/proposed charges from charges actually read in court.

> A lie wins by speed. Truth wins by audit.
