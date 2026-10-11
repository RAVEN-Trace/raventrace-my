# RAVEN-Trace — Visitor Analytics Quality & Reader Journey Contract

**Snapshot:** 11 October 2026, ~21:15 MYT.  
**Provider:** Lytical, site ID `3070`, domain `raven-trace.github.io`.  
**Scope:** website visits to `/raventrace-my/`, **not** GitHub repository views.  
**Evidence levels:** OBSERVED = provider/API or code; INFERENCE = plausible explanation; UNKNOWN = requires provider-side validation.

## Observed baseline

| Metric | 11 Sep–11 Oct 2026 | 4–11 Oct 2026 |
| --- | ---: | ---: |
| Visitors (reported) | 243 | 17 |
| Sessions | 277 | 17 |
| Pageviews | 645 | 10 |
| Bounce rate (reported) | 53.4% | 58.8% |
| Average session duration (reported) | 8m 56s | 3s |

**Baseline warning:** Tracking started on 7 September. The comparative 30-day period predates instrumentation for most days. Do not present the reported visitor increase (+247.1%) as validated organic growth.

### Observed high-interest pages, 30 days

- Homepage: 219 pageviews; 133 landing sessions.
- RCI Tabung Haji CASEFILE: 126 pageviews.
- Narrative Forensics: 86 pageviews.
- Investigation Desk: 41 pageviews.
- Newsroom: 31 pageviews.
- CASEFILE Source Room: 5 pageviews.

**Interpretation:** People access explanations and narrative content more frequently than the Source Room; this is **not** proof of a specific conversion/drop-off rate without a deduplicated session-level funnel.

## Data-quality ledger

| Severity | Evidence | Risk and action |
| --- | --- | --- |
| HIGH | Country summary reports 277 visitors as `US`, while city records include Kuala Lumpur, Kuching and Petaling Jaya also labelled `US`. | Do not use country breakdown for geographic targeting. Verify provider geolocation and country dimension upstream. |
| HIGH | Last 7 days: 17 sessions vs 10 pageviews; four page-metric entries include entries greater than recorded pageviews. | Unexplained grain/collection issue; validate event ingestion, window boundaries, bot sessions and definitions with Lytical. No automatic retrospective adjustment. |
| HIGH | Source summary: Direct 251, chatgpt.com 22, threads 4 (sum 277), despite 243 overall visitors. Referrer report records 96 from `l.threads.com`. | Source breakdown likely session-based or classified differently. Do not combine these as distinct visitors or infer precise channel share. |
| MEDIUM | Recent `get_events(click)` export returned 432 clicks, including 209 without href, while summary reported 429 earlier. | Event counts may reflect different fetch times and non-link interactions. Restrict reader journey to meaningful `a[href]` targets and reconcile counts using identical snapshot boundaries. |
| MEDIUM | Existing `?raven_internal=1` prevents `RavenAnalytics` custom dispatch but **does not stop** a separate Lytical tracker already loaded from `lytcdn.com`. | Do not call internal/test sessions excluded from Lytical. Exclusion requires provider-supported controls or tested tracker-load suppression across all public pages. |
| MEDIUM | `RavenAnalytics` sends custom events to optional listeners/sinks (CustomEvent, Plausible, Umami, gtag), but does not prove `Lytical` ingests them. | Lytical automatically collects pageviews and clicks. Treat Raven custom stage events as experimental until ingestion is verified. |

## Reader journey measurement

**Primary path:** Homepage → current CASEFILE → narrative / Source Room → external original source. Users may legitimately visit branches in a different order.

| Stage | Event/evidence | Notes |
| --- | --- | --- |
| Entry | Lytical landing page and session | Normalize page paths, ignore URL parameters for canonical page grouping. |
| Discovery | Lytical auto-click target href / human text on Homepage | Three labelled CTAs: `understand`, `narrative`, `evidence`. |
| Understanding | CASEFILE landing/section entry | Hash navigation does not prove the section was read. |
| Narrative | Narrative Forensics pageview | Interpret as interest, not agreement with an article. |
| Evidence | Source Room landing + outbound official-source click | Never treat an outbound link click as proof the external document was read. |
| Return | Provider returning visitors / deduplicated sessions | UNKNOWN until Lytical definition and report support verified. |

**Denominator discipline:** Conversion requires a coherent visitor/session identity and window. Click counts divided by unique people are **not** a validated funnel conversion rate.

## Changes proposed in this branch

1. Homepage: correct status strip to **7 individuals charged**, with **five investigations explicitly dated to 19 Sep**; preserve the September snapshot elsewhere.
2. Homepage: direct the primary CTA to the current 11 Oct CASEFILE; label the 19 Sep visual as archived.
3. Mark key orientation CTAs with anonymous `data-raven-journey` stages.
4. Dispatch optional `raven_journey_click` events with a stage, current path and destination path, without visitor identifiers, search queries or full URLs.
5. Strip search parameters and external source URLs from custom analytics URL properties.
6. Bump the local analytics loader cache version.

### Tracking caveat

These changes improve **Raven's own analytics contract** and make the reader path easier to interpret. They **do not** retroactively repair Lytical location/attribution or prove custom `raven_journey_click` events arrive in Lytical.

## Share links and campaign convention

Use canonical content URLs, with explicit UTM on externally published posts:

```text
utm_source=threads
utm_medium=social
utm_campaign=raven_publication
utm_content=<stable_editorial_slug>
```

Example:
```text
https://raven-trace.github.io/raventrace-my/investigations/rci-tabung-haji/narratives/?utm_source=threads&utm_medium=social&utm_campaign=raven_publication&utm_content=narrative_oct2026
```

Repeat for Facebook with `utm_source=facebook`. Do not add identifiers for individual readers, private conversation tokens or personal data to UTM fields. Existing Raven Share System already supports campaign tagging; verify incoming attribution in Lytical before claiming a campaign result.

## Validation gates before publishing conversion claims

- Confirm the 35-page site's Lytical tracker loads exactly once per page.
- Reproduce a test link click in an isolated session and find its matching Lytical click target.
- Reconcile Lytical pageviews, entries and sessions on the **same** UTC window.
- Request provider-side explanation for `US` country mismatch and Direct vs Threads attribution.
- Verify (not assume) test/bot exclusion method for native Lytical.
- Confirm no personal information, URL query strings or reader IDs appear in Raven custom event payloads.
- Recompute the 7-day and 30-day baseline after fixes; keep pre-fix numbers archived.

**Do not silently backfill, relabel or erase historical event data.**
