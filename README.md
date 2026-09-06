# RAVEN-Trace Malaysia

Independent evidence-led journalism for Malaysia.

This repository contains the mobile-first editorial site for **RAVEN-Trace™ by SharulR X(ai) Projects**.

## Mission

Investigate deeply, separate fact from claim and political narrative, then explain the strongest defensible account to ordinary readers in clear Malaysian Malay.

Public-facing output should be understandable to teenagers, older readers and people without specialist legal, financial or technical knowledge.

## Publication architecture

**Story first → evidence one click away → full CASEFILE for audit.**

- `/` — lead investigation and publication front page
- `/news/` — latest verified development desk
- `/news/YYYY/MM/DD/<story>/` — dedicated static story pages for material updates and social sharing
- `/investigations/` — Investigation Desk containing current and future CASEFILEs
- `/investigations/rci-tabung-haji/` — auditable RCI Tabung Haji CASEFILE
- `/methodology/` — evidence labels, source grading, human-clarity rules and source-link standard
- `/tips/` — source-safety guidance and channel status
- `/corrections/` — public correction ledger
- `/about/` — mission, editorial identity and accountability framing

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

## Source Room Navigator

The active CASEFILE Source Room includes a client-side navigator that leaves the underlying evidence ledger intact while making it easier to use on mobile.

- Search by source ID, name, organisation, keyword or URL/domain.
- Filter by **Primer / rasmi**, **Mahkamah**, **Penguatkuasaan**, **Media** or **Analisis**.
- Filter by evidence grade when the row exposes an A–X grade.
- Direct links such as `#s31` automatically reveal the relevant source even when a filter is active.
- Source-type tags are navigation aids only. They do not replace the A–X evidence grade and do not expand what a source can prove.

## Share System v2.1

Material story cards receive a compact share toolbar.

- **Kongsi** uses the device-native share sheet when available.
- **WhatsApp** opens a pre-filled evidence-bounded summary.
- **Salin** copies headline, summary, status, original source when available, and the Raven URL.
- **Artikel** appears when that update has a dedicated static story page.
- **Sumber** opens the original reporting/source rather than a social-share service.
- Story pages use dedicated canonical URLs plus article-level Open Graph metadata and timestamps where relevant.
- Matching Homepage and Newsroom cards route to the dedicated story URL; other evidence items keep stable deep anchors.

Initial dedicated story pages cover the 6 September Jamil Khir remand checkpoint, 5 September transparency vox-pop, Madinah–Rashid disputed record, THP Bina RM72,000 court case, and governance-reform progress.

## Phase 2B social news cards

Material stories now receive a dedicated **1200×630 JPEG RAVEN News Card** for social-link previews rather than reusing one generic investigation artwork.

- Cards live in `assets/og/` and are generated deterministically by `scripts/render_og_cards.py`.
- Each card carries the story date, CASEFILE ID, a short evidence-bounded headline, an explicit status label and RAVEN-Trace publisher branding.
- Status language remains part of the evidence discipline: examples include **UNKNOWN**, **DISPUTED**, **CONTEXT** and **DIDAKWA · BELUM SABIT**.
- Cards are editorial graphics for distribution and identification. They are **not evidence, source photographs or proof of an event**.
- Dedicated story HTML contains static absolute `og:image` and Twitter image metadata, including explicit `1200×630` dimensions, image type and accessible alt text.
- Each material story also exposes one `NewsArticle` JSON-LD block whose image points to the same dedicated card.
- `.github/workflows/render-og-cards.yml` renders, validates and commits the cards plus their static metadata. Verification fails if a card is not 1200×630, exceeds the configured size ceiling or a target story loses its required static social metadata.
- Social platforms may cache previews. RAVEN-Trace does not treat an immediately visible WhatsApp/Facebook/X preview as guaranteed proof that the latest metadata has already been re-fetched by that platform.

The social card and the article's in-page editorial/source imagery are deliberately separate. The social card identifies the story; source imagery and evidence remain governed by the visual evidence policy inside the publication.

## Performance policy

Long lists use progressive rendering hints so off-screen cards and evidence rows do not need to be fully painted immediately. This reduces rendering work without removing content, changing source order or weakening deep-link access.

Source-photo enrichment remains editorial context only and is not evidence. The longer-term performance target is to move source-image metadata resolution from reader-time requests to publication-time metadata wherever practical.

## Evidence-reconciliation rule

Research dossiers and user-supplied compilations are treated as working indexes, not automatically as publication-grade proof. Material claims are reconciled against primary records, official statements, court reporting or independent corroboration before publication. Where reliable records conflict, RAVEN-Trace keeps the point **DISPUTED** or **UNKNOWN** rather than forcing a single answer.

## Local preview

Run a static server from the directory that contains this repository:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/raventrace-my/`.

To regenerate Phase 2B cards locally:

```bash
python -m pip install pillow
python scripts/render_og_cards.py
python scripts/apply_og_metadata.py
```

## GitHub Pages

Deploy from the `main` branch and repository root (`/`). The project-site path is `/raventrace-my/`.

## Status

Public evidence room revised **7 September 2026**.

RAVEN-Trace now operates as a publication rather than a single-case dashboard: Newsroom for developments, dedicated story pages for readers and sharing, an Investigation Desk for CASEFILE discovery, and the CASEFILE/Source Room layer for audit.

The RCI Tabung Haji investigation is now at **CASEFILE v17**, reconciled through **7 September 2026 · early morning MYT**. Current publication infrastructure includes the Jamil Khir remand extension through 8 September, transparency reporting, governance reform progress, UJSB refinancing context, disputed Al-Rawda metrics, the public correction ledger, Share System v2.1, Source Room Navigator and **Phase 2B dedicated social news cards**.

The site records reconciliation corrections including **211 pages rather than 252** for the public RCI report, **30 July rather than 31 July** for announcement of the MACC special task force, and separation of expected/proposed charges from charges actually read in court.

> A lie wins by speed. Truth wins by audit.