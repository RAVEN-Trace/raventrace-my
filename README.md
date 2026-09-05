# RAVEN-Trace Malaysia

Independent evidence-led journalism for Malaysia.

This repository contains the mobile-first editorial site for **RAVEN-Trace™ by SharulR X(ai) Projects**.

## Site structure

- `/` — lead investigation and newsroom front page
- `/news/` — reverse-chronology development desk
- `/investigations/rci-tabung-haji/` — auditable casefile
- `/methodology/` — claim taxonomy and source grading
- `/tips/` — source-safety guidance and channel status
- `/corrections/` — public correction ledger
- `/about/` — identity and editorial compact

## Editorial method

Every published item separates verified facts, attributed claims, inferences, speculation, unknowns, and disputed points. Sources are graded A–X and confidence is stated when material.

## Local preview

Run a static server from the directory that contains this repository:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/raventrace-my/`.

## GitHub Pages

Deploy from the `main` branch and repository root (`/`). The project-site path is `/raventrace-my/`.

## Status

V3 public evidence room: 5 September 2026.

The RCI Tabung Haji investigation now contains the full v14 dataset, revised to the RAVEN CASEFILE structure. The primary newsroom and investigation views use evidence-led typography and data components instead of illustrative hero artwork.

> Lie wins by speed. Truth wins by audit.
