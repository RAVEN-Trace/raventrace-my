# RAVEN-Trace Production Integrity Lock

**Status:** LOCKED · PASS

**Re-locked:** 13 September 2026 · Public Language V2.3 + full rendered QA

**Verified legal-state cutoff:** 11 September 2026 · 23:37 MYT

**Verified public-content review:** 12 September 2026 · 20:44 MYT

**Verified narrative/source delta cutoff:** 13 September 2026 · 01:00 MYT

**Narrative Forensics baseline commit:** `e093235165dd49c7dbefd5e0781dd1fd15786a07`

**Public Language V2.3 content commit:** `3378c5f0512a2c1d7113267fe56faf40220eda00`

**Final V2.3 live-integrity gate:** run `34747581652` · PASS

**Full rendered visual/accessibility QA:** run `34747392724` · PASS

**Latest Pages deployment checked with V2.3:** run `34747581301` · PASS

## Current evidence boundary

- No verified 12 September development changes the court-read charge count: four individuals remain verified as having charges read in court, while MACC's separate count of five remains unresolved.
- The former-minister prosecution announcement remains a **14 September checkpoint** until charges are actually read in court.
- Parliament's official PAC schedule lists **Prosiding 5(a) berhubung Lembaga Tabung Haji** for **15 September 2026 at 10:00 AM**. A scheduled proceeding is not a PAC finding.
- The post-remand outcome for the two AMLA-track individuals remains **BELUM DIKETAHUI** in the reliable public sources reviewed.
- The viral claim that more than RM18.6 million in TH accounts belonging to Abdul Azeez's family was forfeited remains **BELUM SELESAI**. His lawyer has denied the claim, but that denial is not independent proof of the source of the funds.
- The RM193.5 million figure in Abdul Azeez's current charge is treated as the **value of TH's investment in Putrajaya Perdana**, not as an amount the charge alleges was paid, taken, or deposited into Abdul Azeez's or his family's accounts.
- Abdul Azeez has pleaded not guilty. The charge remains unproven unless and until decided by the court.
- The supplied political/social-media research memo remains **Gred C · bahan penyelidikan** overall. Individual political statements may be Grade B when independently corroborated.
- Platform-wide “sentiment” claims remain non-representative without a clear sample and auditable measurement method.

## Public Language V2.3 lock

The public layer is now deliberately different from the analyst layer.

**Backstage Raven** may use technical evidence concepts, legal distinctions, source grading and narrative-analysis terminology.

**Frontstage Raven** must explain the same state in ordinary Malaysian language without weakening the evidence boundary.

Locked public pattern:

1. **Cerita yang dibawa** — what people are being asked to believe.
2. **Apa yang boleh disahkan?** — what the record actually supports.
3. **Apa trick cerita ni?** — how language, number choice, omission or emotion can distort perception.
4. **Apa yang cerita tak sebut?** — context needed before drawing a conclusion.
5. **Raven kata macam mana?** — the narrowest explanation current evidence can support.
6. **Apa bukti yang boleh ubah keputusan Raven?** — what new evidence would materially change the assessment.

Locked communication rule:

> **Cakap macam manusia. Tunjuk bukti macam penyiasat.**

The reader should understand the distinction between a claim and evidence without first learning forensic, legal or data-analysis jargon.

## Narrative mechanism mapping

Internal analytical labels remain available when useful for research and QA. The primary public labels are now translated.

- **SELECTION EFFECT** → **DIA TUNJUK YANG INI JE**
- **CATEGORY COLLAPSE** → **EH, BENDA NI TAK SAMA**
- **EMOTIONAL PRIMING** → **DIA BAGI KITA RASA DULU**
- **MOTIVE INFLATION** → **KITA NAMPAK TINDAKAN. NIAT? BELUM TENTU**
- **REPETITION RISK** → **ULANG BANYAK KALI TAK JADIKAN IA BETUL**
- **REPRESENTATIVENESS ERROR** → **VIRAL TAK BERMAKSUD SUARA SEMUA ORANG**
- **NUMBER LAUNDERING** is explained publicly as numbers/categories being mixed rather than presented as an unexplained analyst label.

These labels describe a possible **effect on interpretation**. They are not findings that a named actor intentionally manipulated the public.

## Political-neutrality lock

Raven applies the same evidence test to every political camp.

- A political statement proves that the statement was made; it does not automatically prove the substance of the statement.
- Political timing or political benefit does not by itself prove enforcement motive.
- A tactical difference between parties does not by itself prove coalition fracture.
- A few viral posts do not equal national or platform-wide sentiment.
- Narrative effect and deceptive intent must remain separate unless independent evidence establishes intent.

Public doctrine:

> **Betulkan cerita, bukan balas slogan dengan slogan.**

## V2.3 sitewide language state

The deep-clean now covers the main reader-facing surfaces, including:

- homepage;
- Newsroom;
- RCI CASEFILE;
- case updates;
- Narrative Audit hub;
- political/social-media narrative page;
- About;
- Methodology.

Examples of analyst/ops residue removed from primary public copy include:

- `freshness sweep` → **semakan terbaru**;
- `DISPUTED RECORD` → **REKOD TAK SEPADAN**;
- `Peta aktor` → **Siapa bawa cerita apa?**;
- `dokumen primer` → **dokumen asal** where technical precision is not required;
- `metodologi sampel` → **sampel dan cara memilihnya**;
- `sintesis politik` → **ringkasan politik**;
- `RAVEN-Trace Protocol` → **Cara Raven bekerja**;
- `Independence & AI-assisted disclosure` → **Kebebasan editorial + penggunaan AI**;
- `Apa perlu ditahan?` → **Apa yang belum boleh disahkan?**.

Names, dates, amounts, evidence grades, legal states, source URLs, narrative IDs and public routes were not intentionally altered by the tone pass.

## QA evidence

### Public Language V2.3 rollout

Workflow run `34743340950` passed all rollout stages:

- Narrative JS syntax validation;
- Public Language V2.1 deep-clean;
- Public Language V2.2 sitewide cleanup;
- Public Language V2.3 micro-clean;
- editorial invariants;
- content commit.

### Live legal/editorial gate

Final run `34747581652` passed:

- V2.3 production payload readiness;
- legal/factual boundary checks;
- public-language residue checks;
- factual runtime-asset inertness.

### Full rendered QA

Run `34747392724` rendered the production site at:

- **390 × 844** mobile;
- **1440 × 900** desktop.

Result:

- **32 public pages**;
- **64 rendered page/view checks**;
- **0 failures**;
- **0 text contrast failures**;
- **0 undersized audited controls**;
- **0 horizontal-overflow failures**;
- **0 unnamed controls**;
- **0 duplicate IDs**;
- **0 missing internal anchors**;
- **0 fake share links**.

Rendered evidence artifact: `raven-unified-v7-visual-qa` from run `34747392724`.

## Remaining design observation

Passing automated QA does not mean the information architecture is finished.

The current site is technically stable and visually coherent, but several long-form pages remain intentionally dense. The next redesign phase should focus on **progressive disclosure, reader orientation, page rhythm and mobile comprehension**, rather than adding more visual decoration.

The guiding product test remains:

> A reader arriving from social media should understand the issue quickly, distinguish claim from evidence without specialist knowledge, and know where to go next if they want proof.

## Lock boundary

This lock certifies technical/editorial production integrity for the verified public state above. It does **not** freeze future facts, court developments, investigations, PAC proceedings, political statements, social-media claims or corrections.

Reopen the lock whenever a change can alter:

- factual/legal-state HTML;
- current-state HTML;
- narrative/political framing;
- public Narrative Audit language;
- investigation/source-room content;
- factual runtime JavaScript;
- evidence labels or legal-boundary language;
- source links or current-state timestamps;
- public social-preview assets that materially represent the case state;
- major UX/navigation behaviour that can change how evidence is interpreted.

After such a change, the relevant live gate and production-integrity verification must pass again before the status is considered locked.

---

RAVEN-Trace™ by SharulR X(ai) Projects

**Bukti dahulu. Kesimpulan kemudian.**
