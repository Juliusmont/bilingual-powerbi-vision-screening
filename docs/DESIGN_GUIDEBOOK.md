# Report design guidebook - Bilingual Vision Screening (FR/EN)

This document fixes the rules **before** anything is built. Anyone (human or Claude Code)
building or changing a page follows it; nothing in it is left to guess.
If a rule here conflicts with a request, the rule wins until this file is updated.

---

## 1. Purpose and audience

| | |
|---|---|
| **Primary reader** | Regional / national school-health managers (FR first), donors and partners (EN) |
| **Question the report answers** | How many students did we reach, how many need glasses, where, and are we on target? |
| **Decision it supports** | Where to send optometrists and glasses in the next campaign |
| **Tone** | Public-health, factual, calm. Not a sales dashboard: no alarm colours for ordinary values |

The screened population is **not** a national prevalence (students seen during campaigns,
symptomatic students over-represented). Every page that shows a rate carries the
`Lbl Note Population` footnote. Never write "prevalence" in a title.

## 2. Canvas, grid and layout

- **Page size**: custom 16:9, **1440 x 810 px**. Tooltip page: 320 x 200 px.
- **Sidebar**: x 0, width **220**, full height, colour `#0B1F3A`.
- **Content area**: x **244** to **1416** (width 1172), top margin 20, bottom margin 20.
- **Gutter**: 16 px between visuals, everywhere. Snap all positions to multiples of 4.
- **Vertical rhythm** (all report pages):

| Band | y | height |
|---|---:|---:|
| Header (page title + campaign pill + slicers) | 20 | 48 |
| Narrative banner | 80 | 72 |
| Section label 01 | 164 | 20 |
| KPI row | 188 | 120 |
| Section label 02 / 03 | 324 | 20 |
| Main visuals | 348 | 420 |
| Footnote line | 776 | 16 |

- **KPI row**: 5 cards of **220 x 120**, x = 244, 482, 720, 958, 1196 (18 px gap: 5 x 220 + 4 x 18 = 1172).

## 3. Colour

Validated with the dataviz palette checker (colour-vision-deficiency separation >= 8, normal-vision >= 15).

| Role | Light | Dark |
|---|---|---|
| Page background | `#F4F6FA` | `#0B1220` |
| Card / visual background | `#FFFFFF` | `#141C2E` |
| Sidebar | `#0B1F3A` | `#060B16` |
| Primary ink (values, titles) | `#0B1F3A` | `#EEF2F8` |
| Secondary ink (labels) | `#4A5873` | `#B6C0D2` |
| Muted ink (footnotes, axes) | `#8A94A6` | `#7D889C` |
| Grid lines / borders | `#E6EAF0` | `#26304A` |

**Categorical (fixed order, never cycled)**, light / dark:

| Slot | Use | Light | Dark |
|---|---|---|---|
| 1 | Default single series, Astigmatism | `#2A78D6` | `#3987E5` |
| 2 | Myopia, Previous year | `#C2410C` | `#D95926` |
| 3 | Hyperopia | `#1BAF7A` | `#199E70` |
| 4 | Emmetropia | `#6250D6` | `#9085E9` |

Diagnosis groups always keep these colours, on every page and in both languages (colour follows the entity).
Slot 3 is below 3:1 contrast on white: any visual using it **must** show data labels.

**Sequential** (visual acuity categories, heat tables): single blue ramp `#CDE2FB` > `#86B6EF` > `#3987E5` > `#1C5CAB` > `#104281`.

**Status (reserved, only with an icon or text)**: good `#0CA30C`, warning `#FAB219`, critical `#D03B3B`.
Used only for: target achievement (>= 95 % / 85-95 % / < 85 %), YoY arrow, data-quality status.

Theme files: [`powerbi/themes/vision-screening-light.json`](../powerbi/themes/vision-screening-light.json) (default) and `...-dark.json`.

## 4. Typography

| Element | Font | Size | Colour |
|---|---|---:|---|
| Page title | Segoe UI Semibold | 20 | primary ink |
| Section label ("01 Coverage") | Segoe UI Semibold, uppercase, letter-spaced | 9 | muted ink |
| Visual title | Segoe UI Semibold | 12 | primary ink |
| KPI value | Segoe UI Semibold | 28 | primary ink |
| KPI caption / axis / labels | Segoe UI | 9-10 | secondary ink |
| Footnote | Segoe UI Italic | 9 | muted ink |

Minimum size 9 pt anywhere, 11 pt for body text on the About page.

## 5. How a KPI is displayed

Every KPI card has exactly four lines, top to bottom:

1. **Label** (`Lbl …` measure), 10 pt, secondary ink, with a small icon on the left.
2. **Value**, 28 pt, locale-aware (`87,2 %` in FR, `87.2%` in EN).
3. **Comparison** pill: `KPI … Caption` measure (▲/▼ + vs previous campaign). Status colour only if the comparison has a direction that is good or bad.
4. **Context** line, 9 pt muted: target, denominator or definition hint.

Each card has a **KPI definition tooltip** (tooltip page, `Def …` measures) so the reader can check the formula.
Use the new card visual (`cardVisual`) or a card + text boxes; never a gauge.

| Card | Value | Comparison | Context |
|---|---|---|---|
| Students screened | `Students Screened` | `KPI Screened YoY Caption` (colour `Color YoY`) | `KPI Target Caption` |
| Target achievement | `Target Achievement %` | status pill (`Color Target Achievement`) | `KPI Target Caption` |
| Need for correction | `Correction Need Rate (Safe)` | `KPI Need Subtitle` (neutral, no status colour) | `Def Need Rate` (tooltip) |
| Uncorrected need | `Uncorrected Need Rate` | none | `KPI Uncorrected Caption` |
| Visual impairment | `Impairment Rate` | none | `KPI Impairment Caption` |

## 6. Pages and navigation

| # | Page (FR / EN via `Lbl Nav …`) | Content |
|---|---|---|
| 1 | Présentation / About | What the report is, definitions, how to switch language, population caveat, author |
| 2 | Vue direction / Overview | Narrative banner, 5 KPI cards, need by region, prefecture ranking, trend by campaign |
| 3 | Analyse clinique / Clinical analysis | Diagnosis breakdown, visual acuity, symptoms, diagnosis by screen time |
| 4 | Qualité & sécurité / Quality & security | `DQ Status`, DQ checks table, RLS roles, small-cell rule, model diagram |
| T | Tooltip - KPI info (hidden) | `Def …` measure for the hovered card |

**Sidebar (identical on every page, grouped and copied, not rebuilt):**
- Top: title "Vision Screening" + "Togo · 2024-2026" (muted), y 24.
- Navigation: 4 page-navigator buttons, 188 x 36, y 112 / 156 / 200 / 244. Selected state: white background, primary ink text; default: transparent, `#B6C0D2` text. Button text from `Lbl Nav …` (fx).
- Bottom: **language slicer** (DimLanguage[LanguageCode], tile style, single select, "FR | EN"), y 700, **synced on all pages**. Below it: `Lbl Note Synthetic`, 9 pt muted.

**Header (pages 2-4):** page title (`Lbl Title …`) + campaign pill (`Header Campaign Pill`, rounded, `#2A78D6` fill, white text) on the left;
Region and Campaign dropdown slicers on the right (labels via field parameters), synced across pages 2-4.

### Page 2 - Overview, main band (y 348, h 420)

| Visual | Position (x, y, w, h) | Spec |
|---|---|---|
| Need by region | 244, 348, 572, 420 | Horizontal bar, `Param Region` on axis, `Correction Need Rate (Safe)`, sorted by `RegionSortOrder`, colour `Color Region Bar`, data labels on, no gridlines. Alt text `Alt Text Region Chart` |
| Trend by campaign | 832, 348, 584, 196 | Clustered column, `Param Campaign` on axis, `Students Screened`, + `Target Students` as a line (line and clustered column chart, *secondary y-axis turned off* so both share one axis) |
| Prefecture ranking | 832, 560, 584, 208 | Table: Prefecture, Screened, Need rate (data bar slot 1), Rank, Target achievement (icon + colour). Top 10 by rank, no scrollbar in screenshots |

### Page 3 - Clinical analysis

| Visual | Position | Spec |
|---|---|---|
| Diagnosis breakdown | 244, 80, 572, 336 | Bar, `Param Diagnosis Group`, `Diagnosis Share`, slots 1-4 per group, labels on |
| Visual acuity per eye | 832, 80, 584, 336 | Column, VA category (ordinal, sequential ramp), `Eyes Examined` share |
| Reported symptoms | 244, 432, 572, 336 | Bar sorted desc, `Param Symptom`, `Symptom Rate`, single colour slot 1 |
| Diagnosis by screen time | 832, 432, 584, 336 | 100 % stacked column, `Param Screen Time` axis, diagnosis group legend (slots 1-4). Subtitle: "Association, not causation" / "Association, pas causalité" |

Page 3 has no narrative banner and no KPI row: the four visuals fill the band from y 80 to y 768 (2 x 2 grid).

### Page 4 - Quality & security

| Visual | Position | Spec |
|---|---|---|
| DQ status card | 244, 80, 572, 72 | `DQ Status`, colour `Color DQ Status`, icon ✓ / ⚠ |
| DQ checks table | 244, 168, 572, 300 | One row per `DQ …` measure: check name, issues, injected rule |
| Security panel | 832, 80, 584, 388 | Text: static roles, dynamic role, `USERPRINCIPALNAME()`, Entra ID groups note, small-cell rule |
| Model diagram | 244, 484, 1172, 284 | Image of the model view (exported PNG) |

## 7. Bilingual rules

- **No hard-coded text** on any visual: titles, buttons, captions and footnotes all come from `Lbl …` / caption measures (Format > Title > fx > Field value).
- Axis and legend text comes from **field parameters** linked to `DimLanguage`, never from a `_FR` / `_EN` column directly.
- Numbers use `[Selected Locale]` in every `FORMAT`.
- Each page is checked in both languages before a screenshot is taken. A French label must fit: plan for **+20 % text length** vs English.

## 8. What we do NOT want

- No pie, donut, gauge, 3D, treemap or map visual (Togo shape files add noise for 5 regions).
- No secondary (dual) y-axis.
- No default Power BI titles ("Sum of …", "Count of …"), no visual header icons in screenshots.
- No drop shadows, no gradients, no background images behind data.
- No rate computed on fewer than 10 students (always use the `(Safe)` measure on detailed visuals).
- No colour carrying meaning alone; no status colour on a neutral value (the need rate is not "bad", it is a need).
- No more than 5 KPI cards and 4 main visuals per page.
- No truncated labels, no scrollbars, no "(Blank)" category visible.
- No word "prevalence", no claim of causality between screen time and myopia.
- No real student data, names or schools: the data stays 100 % synthetic.

## 9. Accessibility checklist

- Alt text on every visual (bilingual measure where the visual carries data).
- Tab order set on every page (sidebar, header, banner, KPIs, visuals).
- Data labels on all bar / column charts.
- Contrast >= 4.5:1 for text, >= 3:1 for marks (slot 3 relies on labels, see section 3).

## 10. Definition of done (before screenshots)

1. Values match [`docs/expected-kpis.md`](expected-kpis.md) for 2026 and all campaigns.
2. Every page reviewed in FR and EN, no hard-coded text left.
3. RLS tested with *View as*: `Region - Plateaux` shows only Plateaux.
4. Performance analyzer: no visual > 500 ms.
5. Screenshots taken per the checklist in [`docs/CAPTURE_CHECKLIST.md`](CAPTURE_CHECKLIST.md).

## 11. Dark mode (deferred, deliberate)

Dark mode is **not** in v1. Supporting it inside one report means duplicated hidden pages plus bookmarks
(every change done twice) or colour measures on every property. For a portfolio whose differentiator is
bilingualism, that cost is not justified. The dark theme JSON is provided for a future version or a dark screenshot.
