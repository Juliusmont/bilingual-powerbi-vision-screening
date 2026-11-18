# Bilingual Power BI Semantic Model - School Vision Screening (FR/EN)

![Power BI](https://img.shields.io/badge/Power%20BI-semantic%20model-F2C811?logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-measures-4B8BBE)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Data](https://img.shields.io/badge/data-100%25%20synthetic-2E7D32)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**Portfolio project.** A single Power BI semantic model and report serving **English and French** users from one common data model, applying Microsoft's multilingual design patterns: field parameters, dynamic language selection and translated metadata. Built on **synthetic data** inspired by a school vision-screening survey in Togo (2026).

> ⚠️ **All data in this repository is synthetic.** No real student record is included. Distributions are loosely calibrated on an aggregate profile; school names are fictitious and built from real locality names.

> 🇫🇷 [Résumé en français](#résumé-en-français) en bas de page.

---

## Table of contents

- [Highlights](#highlights)
- [Screenshots](#screenshots)
- [Multilingual design](#multilingual-design)
- [Data model](#data-model)
- [Key DAX](#key-dax)
- [Security & privacy](#security--privacy)
- [Data integrity checks](#data-integrity-checks)
- [Accessibility](#accessibility)
- [Getting started](#getting-started)
- [Repository structure](#repository-structure)
- [Roadmap](#roadmap)
- [License](#license)

---

## Highlights

- **One model, two languages**: data values, report text and metadata all switch between FR and EN, with no duplicated report or measure.
- **Star schema** with a snowflaked geography, single-direction relationships and bridge tables (no bidirectional filtering).
- **Advanced DAX**: data-driven KPI definition, time intelligence (YoY, YTD), % of target, contextual ranking, locale-aware formatting.
- **Row-level security**: static roles per region plus a dynamic role driven by `USERPRINCIPALNAME()`.
- **Privacy by design**: small-cell suppression on health data about minors.
- **Data-quality layer**: anomalies are deliberately injected by the generator and caught by DAX integrity checks.
- **Reproducible**: a seeded Python generator (standard library only) rebuilds every CSV.

## Screenshots

> 🚧 **Coming soon.** Report screenshots (executive and analysis pages in FR and EN, RLS test, model view) will be added to [`screenshots/`](screenshots/) together with the `.pbix` file.

## Multilingual design

The model separates three translation layers, each handled with the technique Microsoft recommends for it.

| Layer | What it covers | Technique |
|---|---|---|
| **Data values** | Diagnoses, regions, sex, age bands, symptoms, screen time, campaigns | FR/EN columns exposed through **field parameters**. Each parameter gets a 4th `LanguageCode` column linked to `DimLanguage`, so one language slicer drives every axis and legend. |
| **Report text** | Page titles, visual titles, KPI captions, alt text | `Labels` table + `Lbl …` DAX measures (`LOOKUPVALUE`), bound through *conditional formatting > field value*. Numbers follow the locale: `FORMAT(…, "fr-FR")` → `3,2` / `"en-US"` → `3.2`. |
| **Metadata** | Table, column and measure names | **fr-FR culture** added by a Tabular Editor C# script. Shown in the Power BI Service according to the browser language or the `?language=fr` URL parameter. |
| **Default language** | First visit, nothing selected | `[Selected Language]` falls back to `USERCULTURE()`, so a French-speaking viewer gets French automatically. |

> Metadata translations are **not displayed in Power BI Desktop**; they apply in the Power BI Service (field list, default titles, explore, Q&A).

## Data model

Star schema with a snowflaked geography (**Region > Prefecture > Commune > School**) and single-direction one-to-many relationships throughout.

```
DimRegion ─< DimPrefecture ─< DimCommune ─< DimSchool ─< FactScreening ─< FactEyeExam
                  │                            │              │   │            │
              FactTarget                DimSchoolType         │   │   DimDiagnosis / DimVACategory / DimEye
                                                              │   ├─< BridgeSymptom >─ DimSymptom
   DimDate ─< FactScreening, FactTarget                       │   └─< BridgeHistory >─ DimHistory
   DimSex / DimAgeBand / DimCycle / DimScreenTime ────────────┘
   DimLanguage ─< field parameters (LanguageCode)
```

| Table | Grain | Rows |
|---|---|---:|
| `FactScreening` | one row per screened student | 35,253 |
| `FactEyeExam` | one row per eye (visual acuity, cycloplegic refraction, prescription) | 70,506 |
| `FactTarget` | screening target per prefecture and campaign | 111 |
| `BridgeSymptom` | student × reported symptom | 68,730 |
| `BridgeHistory` | student × medical history item | 16,947 |
| `DimRegion` / `DimPrefecture` / `DimCommune` / `DimSchool` | geography (5 / 39 / 116 / 405) | |
| `DimDate` | calendar 2024-2026 with bilingual campaign labels | 1,096 |
| `DimDiagnosis`, `DimVACategory`, `DimEye`, `DimSex`, `DimAgeBand`, `DimCycle`, `DimScreenTime`, `DimSchoolType`, `DimSymptom`, `DimHistory` | bilingual lookup dimensions (`_FR` / `_EN` columns) | |
| `DimLanguage` | FR / EN, culture codes | 2 |
| `Labels` | UI text keyed by `LabelKey` + `LanguageCode` | 38 |
| `SecurityUserRegion` | user e-mail → region mapping for dynamic RLS (hidden) | 7 |

Three annual campaigns (March 2024, 2025, 2026). Geography follows Togo's administrative division (Law no. 2017-008 on communes).

## Key DAX

All measures are in [`dax/measures.dax`](dax/measures.dax), organised in display folders.

| Folder | Measures |
|---|---|
| `0 Language` | `Selected Language` (slicer or `USERCULTURE()` fallback), `Selected Locale`, `Lbl …` label measures |
| `1 Core KPIs` | `Students Screened`, `Correction Need Rate`, `Uncorrected Need Rate`, `Impairment Rate`, `Screen Exposure Rate`, `Diagnosis Share`, `Symptom Rate` |
| `2 Time intelligence & targets` | `Students Screened PY` / `YoY %` / `YTD` (`SAMEPERIODLASTYEAR`, `TOTALYTD`), `Correction Need Rate Change (pts)`, `Target Achievement %` |
| `3 Ranking` | `Prefecture Rank (Need Rate)`: `RANKX` over `ALLSELECTED`, blank on totals with `ISINSCOPE` |
| `4 Formatted captions` | `KPI Need Subtitle`, `KPI Screened Caption`, `Alt Text Region Chart` (bilingual, locale-aware) |
| `5 Privacy` | `Correction Need Rate (Safe)` |
| `6 Data integrity checks` | `DQ …` measures and `DQ Status` |

**Need-for-correction rate**: a student counts when the examiner proposed a non-zero prescription in at least one eye. This data-driven definition avoids the misleading ~99 % "any refractive error" rate that physiological hyperopia and very small cylinders would produce on raw refraction values.

The file also contains the **field parameter** definitions and the **RLS rules** (as commented DAX, to paste into the matching dialogs).

## Security & privacy

- **Row-level security** on `DimRegion`, propagated to facts through the relationships:
  - static roles: `Region - Plateaux` (`[RegionCode] = "PLA"`), `Region - Maritime` (`"MAR"`);
  - `Dynamic by user`: `[RegionCode] IN` the regions mapped to `USERPRINCIPALNAME()` in `SecurityUserRegion`. Test accounts (`directeur.plateaux@demo.org`, `analyste.national@demo.org`, …) are fictitious.
- **Small-cell suppression**: rates computed on fewer than 10 students are hidden, to limit re-identification risk on health data about minors.
- In production, roles would be assigned to **Microsoft Entra ID security groups** rather than to individual users.

## Data integrity checks

The generator deliberately injects realistic errors so that the integrity measures have something to catch:

| Check | Injected issue |
|---|---|
| `DQ Implausible Cylinder` | prescribed cylinder of +8.00 D (typing error), ~0.2 % of eyes |
| `DQ Plus Cylinder Convention` | positive cylinder mixed with the minus convention, ~0.4 % of eyes |
| `DQ Missing Visual Acuity` | blank visual acuity, ~0.4 % of eyes |
| `DQ Students Without Two Eyes` | structural completeness (exactly two eye rows per student) |
| `DQ Symptom Inconsistency` | `HasSymptoms = 0` while symptoms exist in the bridge table |

`DQ Status` summarises the result in the report footer, in the selected language.

## Accessibility

- Dynamic **bilingual alt text** on visuals (`Alt Text …` measures).
- Defined **tab order** on every page.
- **Data labels** on charts: no information is conveyed by colour alone.
- Sufficient contrast and readable font sizes (≥ 11 pt for text).

## Getting started

### Prerequisites

- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (Windows)
- [Tabular Editor 2](https://github.com/TabularEditor/TabularEditor/releases) (free), registered as an external tool
- Python 3.8+ (only to regenerate the data; no third-party package needed)

### 1. (Optional) Regenerate the data

The CSV files are already in [`data/`](data/). To rebuild them:

```bash
python scripts/generate_data.py
```

The generator is seeded (`SEED = 2026`), so the output is identical on every run.

### 2. Build the model in Power BI Desktop

1. Load **each CSV separately** (*Get data > Text/CSV*, UTF-8). Do not use *Folder > Combine*.
2. In Power Query, set keys to whole numbers, `Date` to date, and refraction columns (`SphereCyclo`, `CylinderCyclo`, `SphereRx`, `CylinderRx`) to **decimal number with locale English (United States)** (dot decimal separator).
3. Create the relationships shown in [Data model](#data-model) (one-to-many, single direction) and **mark `DimDate` as a date table**.
4. Sort `DiagnosisGroup_FR/EN` by `GroupSortOrder` and `RegionName_FR/EN` by `RegionSortOrder`; hide technical keys, `Labels` and `SecurityUserRegion`.
5. Create a `_Measures` table and add the measures from [`dax/measures.dax`](dax/measures.dax).
6. Create the field parameters (*Modeling > New parameter > Fields*), add the `LanguageCode` column and relate them to `DimLanguage`.
7. Add the RLS roles (*Modeling > Manage roles*) and test them with *View as*.

### 3. Add the French metadata

*External tools > Tabular Editor > C# Script*, paste [`tabular-editor/add_french_translations.csx`](tabular-editor/add_french_translations.csx), run (F5) and save (Ctrl+S). Check *Model > Translations* for the `fr-FR` culture.

### 4. View the translations

Publish to the Power BI Service and open the report with `?language=fr` or `?language=en`.

## Repository structure

```
.
├── data/                                  star-schema CSV files (UTF-8, synthetic)
├── dax/
│   └── measures.dax                       measures, field parameters, RLS rules
├── powerbi/                               .pbix file (coming soon)
├── screenshots/                           report screenshots (coming soon)
├── scripts/
│   └── generate_data.py                   seeded synthetic data generator
├── tabular-editor/
│   └── add_french_translations.csx        fr-FR metadata translations (C#)
├── LICENSE
└── README.md
```

## Roadmap

- [ ] Add the `.pbix` report
- [ ] Add FR / EN screenshots, RLS test and model view
- [ ] Publish to the Power BI Service and capture `?language=fr` / `?language=en`
- [ ] Object-level security (OLS) on general medical history for selected roles

## License

Code released under the [MIT License](LICENSE). The data is synthetic and free to reuse.

## Author

**Julius Akouété M. ATCHOU** · [github.com/Juliusmont](https://github.com/Juliusmont)

---

### Résumé en français

Projet portfolio : **un seul modèle sémantique Power BI** qui sert des utilisateurs francophones et anglophones. Il combine des paramètres de champs reliés à une table de langues, une sélection dynamique de la langue (par défaut celle du navigateur via `USERCULTURE()`), des titres et formats de nombres bilingues pilotés par DAX, et la traduction des métadonnées (culture fr-FR ajoutée avec Tabular Editor).

Le modèle en étoile (géographie en flocon : Région > Préfecture > Commune > Établissement) est complété par une sécurité au niveau des lignes statique et dynamique par région, des mesures DAX avancées (comparaison annuelle, cumul, atteinte des objectifs, classement), la suppression des petits effectifs et des contrôles d'intégrité des données.

**Toutes les données sont synthétiques.** Elles s'inspirent d'une enquête de dépistage visuel en milieu scolaire au Togo (2026), sans aucune donnée réelle d'élève.
