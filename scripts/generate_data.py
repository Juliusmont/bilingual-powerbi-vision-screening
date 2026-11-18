"""
Synthetic data generator - Bilingual Power BI demo (school vision screening, Togo).

All records are SYNTHETIC. Distributions are loosely calibrated on an aggregate profile
of a real school screening survey (no individual record is reused). School names are
fictitious and built from real locality names (prefecture capitals).

Output: star-schema CSV files (UTF-8) in ../data/
Usage:  python generate_data.py            (seed 2026, ~25-30k students over 3 campaigns)
"""
import csv, os, random
from datetime import date, timedelta

SEED = 2026
random.seed(SEED)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Geography: 5 regions, 39 prefectures, communes named "<PREFECTURE> N"
#    Source: Loi n° 2017-008 du 29/06/2017 portant création de communes
#    (116 communes listed here; the law amended in 2019 brings the total to 117:
#    adjust N_COMMUNES below if you know which prefecture gained a commune).
#    Chef-lieu = prefecture capital (verify the ones marked '?').
# ---------------------------------------------------------------------------
GEO = [
    # Region, Prefecture, N_communes, Chef-lieu
    ("Savanes", "Cinkassé", 2, "Cinkassé"), ("Savanes", "Tône", 4, "Dapaong"),
    ("Savanes", "Kpendjal", 2, "Mandouri"), ("Savanes", "Kpendjal-Ouest", 2, "Naki-Est"),
    ("Savanes", "Oti", 2, "Sansanné-Mango"), ("Savanes", "Oti-Sud", 2, "Gando"),
    ("Savanes", "Tandjouaré", 2, "Tandjouaré"),
    ("Kara", "Kozah", 4, "Kara"), ("Kara", "Bassar", 4, "Bassar"),
    ("Kara", "Dankpen", 3, "Guérin-Kouka"), ("Kara", "Kéran", 3, "Kandé"),
    ("Kara", "Binah", 2, "Pagouda"), ("Kara", "Doufelgou", 2, "Niamtougou"),
    ("Kara", "Assoli", 3, "Bafilo"),
    ("Centrale", "Tchaoudjo", 4, "Sokodé"), ("Centrale", "Sotouboua", 3, "Sotouboua"),
    ("Centrale", "Mô", 2, "Djarkpanga"), ("Centrale", "Tchamba", 3, "Tchamba"),
    ("Centrale", "Blitta", 3, "Blitta"),
    ("Plateaux", "Ogou", 4, "Atakpamé"), ("Plateaux", "Anié", 2, "Anié"),
    ("Plateaux", "Est-Mono", 3, "Elavagnon"), ("Plateaux", "Moyen-Mono", 2, "Tohoun"),
    ("Plateaux", "Haho", 4, "Notsé"), ("Plateaux", "Wawa", 3, "Badou"),
    ("Plateaux", "Amou", 3, "Amlamé"), ("Plateaux", "Akébou", 2, "Kougnohou"),
    ("Plateaux", "Kloto", 3, "Kpalimé"), ("Plateaux", "Kpélé", 2, "Kpélé-Adéta"),
    ("Plateaux", "Danyi", 2, "Danyi-Apéyémé"), ("Plateaux", "Agou", 2, "Agou-Gadzépé"),
    ("Maritime", "Golfe", 7, "Lomé"), ("Maritime", "Agoè-Nyivé", 6, "Agoè-Nyivé"),
    ("Maritime", "Zio", 4, "Tsévié"), ("Maritime", "Avé", 2, "Kévé"),
    ("Maritime", "Lacs", 4, "Aného"), ("Maritime", "Vo", 4, "Vogan"),
    ("Maritime", "Yoto", 3, "Tabligbo"), ("Maritime", "Bas-Mono", 2, "Afagnagan"),
]
REGIONS = ["Savanes", "Kara", "Centrale", "Plateaux", "Maritime"]
REGION_CODE = {"Savanes": "SAV", "Kara": "KAR", "Centrale": "CEN", "Plateaux": "PLA", "Maritime": "MAR"}
# Illustrative regional effects (synthetic): urban Maritime = more screens & myopia
REGION_MYOPIA_SHIFT = {"Savanes": -0.04, "Kara": -0.02, "Centrale": 0.0, "Plateaux": 0.0, "Maritime": 0.06}
REGION_SCREEN = {"Savanes": 0.45, "Kara": 0.55, "Centrale": 0.58, "Plateaux": 0.65, "Maritime": 0.82}

SUFFIX = ["Centre", "Est", "Ouest", "Nord", "Sud", "Gare", "Marché", "Plateau"]
CAMPAIGNS = {2024: 0.55, 2025: 0.75, 2026: 1.00}   # share of communes screened per campaign

# ---------------------------------------------------------------------------
# 2. Bilingual code tables (FR / EN)
# ---------------------------------------------------------------------------
DIAG = [  # key, detail FR, detail EN, group key, weight (calibrated on aggregate profile)
    (1, "Astigmatisme mixte", "Mixed astigmatism", "AST", 340),
    (2, "Astigmatisme myopique composé", "Compound myopic astigmatism", "AST", 182),
    (3, "Astigmatisme myopique simple direct", "Simple myopic astigmatism (with-the-rule)", "AST", 24),
    (4, "Astigmatisme myopique simple indirect", "Simple myopic astigmatism (against-the-rule)", "AST", 21),
    (5, "Astigmatisme myopique simple oblique", "Simple myopic astigmatism (oblique)", "AST", 15),
    (6, "Astigmatisme hypermétropique composé", "Compound hyperopic astigmatism", "AST", 5),
    (7, "Astigmatisme hypermétropique simple", "Simple hyperopic astigmatism", "AST", 2),
    (8, "Myopie physiologique", "Physiological myopia", "MYO", 8),
    (9, "Myopie faible", "Low myopia", "MYO", 10),
    (10, "Myopie moyenne", "Moderate myopia", "MYO", 16),
    (11, "Myopie forte", "High myopia", "MYO", 1),
    (12, "Hypermétropie physiologique", "Physiological hyperopia", "HYP", 40),
    (13, "Hypermétropie faible", "Low hyperopia", "HYP", 25),
    (14, "Hypermétropie moyenne", "Moderate hyperopia", "HYP", 1),
    (15, "Emmétropie", "Emmetropia", "EMM", 5),
]
DIAG_GROUP = {"AST": ("Astigmatisme", "Astigmatism", 1), "MYO": ("Myopie", "Myopia", 2),
              "HYP": ("Hypermétropie", "Hyperopia", 3), "EMM": ("Emmétropie", "Emmetropia", 4)}
SEX = [(1, "Féminin", "Female"), (2, "Masculin", "Male")]
AGEBAND = [(1, "10 à 14 ans", "10 to 14 years"), (2, "15 à 24 ans", "15 to 24 years")]
CYCLE = [(1, "Collège", "Lower secondary"), (2, "Lycée", "Upper secondary")]
SCHOOLTYPE = [(1, "Public", "Public"), (2, "Confessionnel", "Faith-based"), (3, "Privé", "Private")]
SCREEN = [(0, "Aucune exposition", "No exposure"), (1, "2 h ou moins", "2 hours or less"),
          (2, "Plus de 2 h à 4 h", "More than 2 to 4 hours"), (3, "Plus de 4 h", "More than 4 hours")]
VACAT = [(1, "Absence de déficience", "No impairment"), (2, "Légère ]0,5-0,3]", "Mild ]0.5-0.3]"),
         (3, "Modérée ]0,3-0,1]", "Moderate ]0.3-0.1]"), (4, "Sévère ]0,1-0,05]", "Severe ]0.1-0.05]"),
         (5, "Cécité <0,05", "Blindness <0.05")]
SYMPTOM = [  # key, FR, EN, probability given symptoms = yes (aggregate profile)
    (1, "Baisse d'acuité visuelle", "Reduced visual acuity", 0.44), (2, "Douleurs oculaires", "Eye pain", 0.52),
    (3, "Céphalées", "Headaches", 0.27), (4, "Fatigue visuelle", "Eye strain", 0.07),
    (5, "Photophobie", "Photophobia", 0.18), (6, "Larmoiement", "Watery eyes", 0.32),
    (7, "Picotement oculaire", "Eye itching", 0.13), (8, "Déviation oculaire", "Eye deviation", 0.01),
    (9, "Autres signes", "Other symptoms", 0.20)]
HISTORY = [  # key, category FR, category EN, item FR, item EN, probability within category
    (1, "Personnels ophtalmologiques", "Personal ocular", "Traumatisme oculaire", "Eye injury", 0.48),
    (2, "Personnels ophtalmologiques", "Personal ocular", "Glaucome", "Glaucoma", 0.09),
    (3, "Personnels ophtalmologiques", "Personal ocular", "Cataracte", "Cataract", 0.02),
    (4, "Personnels ophtalmologiques", "Personal ocular", "Chirurgie oculaire", "Eye surgery", 0.02),
    (5, "Personnels ophtalmologiques", "Personal ocular", "Strabisme", "Strabismus", 0.02),
    (6, "Personnels généraux", "Personal general", "Drépanocytose", "Sickle cell disease", 0.16),
    (7, "Personnels généraux", "Personal general", "Allergie", "Allergy", 0.08),
    (8, "Personnels généraux", "Personal general", "Albinisme", "Albinism", 0.02),
    (9, "Familiaux", "Family", "Amétropie familiale", "Family refractive error", 0.75),
    (10, "Familiaux", "Family", "Amblyopie familiale", "Family amblyopia", 0.01),
    (11, "Familiaux", "Family", "Glaucome familial", "Family glaucoma", 0.04)]
HIST_CAT_P = {"Personnels ophtalmologiques": 0.08, "Personnels généraux": 0.10, "Familiaux": 0.18}


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name:28s} {len(rows):>7,d} rows")


def q(x):  # round to 0.25 D
    return round(round(x * 4) / 4, 2)


# ---------------------------------------------------------------------------
# 3. Dimensions
# ---------------------------------------------------------------------------
write("DimLanguage.csv", ["LanguageCode", "LanguageName", "Culture", "SortOrder"],
      [("FR", "Français", "fr-FR", 1), ("EN", "English", "en-US", 2)])
REGION_FR = {"Savanes": "Région des Savanes", "Kara": "Région de la Kara", "Centrale": "Région Centrale",
             "Plateaux": "Région des Plateaux", "Maritime": "Région Maritime"}
write("DimRegion.csv", ["RegionKey", "RegionCode", "RegionName_FR", "RegionName_EN", "RegionSortOrder"],
      [(i + 1, REGION_CODE[r], REGION_FR[r], r + " Region", i + 1) for i, r in enumerate(REGIONS)])

pref_rows, commune_rows, school_rows = [], [], []
pk = ck = sk = 0
for region, pref, ncom, chef in GEO:
    pk += 1
    pref_rows.append((pk, REGIONS.index(region) + 1, "Préfecture " + pref, pref + " Prefecture", pref, chef))
    for n in range(1, ncom + 1):
        ck += 1
        commune_rows.append((ck, pk, f"{pref.upper()} {n}"))
        nb_schools = random.choice([2, 3, 3, 4]) + (2 if region == "Maritime" else 0)
        used = random.sample(SUFFIX, k=min(nb_schools, len(SUFFIX)))
        for j, suf in enumerate(used):
            sk += 1
            is_lycee = j == 0 or random.random() < 0.25
            stype = 1 if random.random() < 0.85 else random.choice([2, 3])
            prefix = "Lycée" if is_lycee else "CEG"
            if stype == 3:
                prefix = "Collège privé" if not is_lycee else "Lycée privé"
            elif stype == 2:
                prefix = "Collège confessionnel" if not is_lycee else "Lycée confessionnel"
            label = chef if n == 1 else f"{chef} {n}"
            school_rows.append((sk, ck, f"{prefix} {label} {suf}", f"SCH-{sk:04d}", stype, 1 if is_lycee else 0))

write("DimPrefecture.csv", ["PrefectureKey", "RegionKey", "PrefectureName_FR", "PrefectureName_EN", "Prefecture", "ChefLieu"], pref_rows)
write("DimCommune.csv", ["CommuneKey", "PrefectureKey", "CommuneName"], commune_rows)
write("DimSchool.csv", ["SchoolKey", "CommuneKey", "SchoolName", "SchoolCode", "SchoolTypeKey", "HasUpperSecondary"], school_rows)
write("DimSchoolType.csv", ["SchoolTypeKey", "SchoolType_FR", "SchoolType_EN"], SCHOOLTYPE)
write("DimSex.csv", ["SexKey", "Sex_FR", "Sex_EN"], SEX)
write("DimAgeBand.csv", ["AgeBandKey", "AgeBand_FR", "AgeBand_EN"], AGEBAND)
write("DimCycle.csv", ["CycleKey", "Cycle_FR", "Cycle_EN"], CYCLE)
write("DimScreenTime.csv", ["ScreenTimeKey", "ScreenTime_FR", "ScreenTime_EN"], SCREEN)
write("DimVACategory.csv", ["VACategoryKey", "VACategory_FR", "VACategory_EN"], VACAT)
write("DimDiagnosis.csv", ["DiagnosisKey", "Diagnosis_FR", "Diagnosis_EN", "DiagnosisGroup_FR", "DiagnosisGroup_EN", "GroupSortOrder", "IsAmetropia"],
      [(k, fr, en, DIAG_GROUP[g][0], DIAG_GROUP[g][1], DIAG_GROUP[g][2], 0 if g == "EMM" else 1) for k, fr, en, g, _ in DIAG])
write("DimSymptom.csv", ["SymptomKey", "Symptom_FR", "Symptom_EN"], [s[:3] for s in SYMPTOM])
write("DimHistory.csv", ["HistoryKey", "Category_FR", "Category_EN", "History_FR", "History_EN"], [h[:5] for h in HISTORY])
write("DimEye.csv", ["EyeKey", "Eye_FR", "Eye_EN"], [(1, "Œil droit (OD)", "Right eye (OD)"), (2, "Œil gauche (OG)", "Left eye (OS)")])

# Date dimension (2024-01-01 .. 2026-12-31) with bilingual month names
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
drows, d = [], date(2024, 1, 1)
while d <= date(2026, 12, 31):
    drows.append((int(d.strftime("%Y%m%d")), d.isoformat(), d.year, d.month, MONTHS_FR[d.month - 1], MONTHS_EN[d.month - 1], f"Campagne {d.year}", f"{d.year} campaign"))
    d += timedelta(days=1)
write("DimDate.csv", ["DateKey", "Date", "Year", "MonthNumber", "Month_FR", "Month_EN", "Campaign_FR", "Campaign_EN"], drows)

# ---------------------------------------------------------------------------
# 4. Facts
# ---------------------------------------------------------------------------
diag_keys = [x[0] for x in DIAG]
diag_w = [x[4] for x in DIAG]
diag_group = {x[0]: x[3] for x in DIAG}
pref_region = {p[0]: REGIONS[p[1] - 1] for p in pref_rows}
commune_pref = {c[0]: c[1] for c in commune_rows}


def pick_diag(region, year):
    w = list(diag_w)
    shift = REGION_MYOPIA_SHIFT[region] + 0.02 * (year - 2024)   # myopia trend (synthetic)
    for i, k in enumerate(diag_keys):
        if diag_group[k] == "MYO" or k in (2, 3, 4, 5):
            w[i] = w[i] * (1 + 4 * shift)
    return random.choices(diag_keys, weights=w)[0]


def refraction(dk):
    g = diag_group[dk]
    sph, cyl = 0.0, 0.0
    if g == "MYO":
        sph = {8: -0.25, 9: random.uniform(-2.0, -0.5), 10: random.uniform(-5.0, -2.25), 11: random.uniform(-9.0, -5.25)}[dk]
    elif g == "HYP":
        sph = {12: random.uniform(0.25, 1.0), 13: random.uniform(1.25, 2.5), 14: random.uniform(2.75, 5.0)}[dk]
    elif g == "AST":
        cyl = -abs(random.gauss(0.9, 0.7)) - 0.25
        sph = {1: random.uniform(0.25, 1.5), 2: random.uniform(-3.0, -0.25), 6: random.uniform(0.5, 2.0), 7: 0.0}.get(dk, 0.0)
    return q(sph), q(max(cyl, -6.0)), random.randint(0, 180) if cyl else 0


def va_from(sph, cyl):
    va = 9 - 1.1 * abs(min(sph, 0)) - 0.4 * max(sph, 0) - 1.5 * abs(cyl) + random.gauss(0, 1.3)
    floor = 0 if sph <= -5 else 1
    return max(floor, min(10, round(va)))


def va_cat(va10):
    v = va10 / 10
    return 1 if v > 0.5 else 2 if v > 0.3 else 3 if v > 0.1 else 4 if v >= 0.05 else 5


screen_rows, eye_rows, sym_rows, hist_rows, target_rows = [], [], [], [], []
stu = 0
for year, coverage in CAMPAIGNS.items():
    start = date(year, 3, 9)
    screened_communes = set(random.sample([c[0] for c in commune_rows], k=round(len(commune_rows) * coverage)))
    per_pref_actual = {}
    for s in school_rows:
        skey, ckey, _, _, stype, has_lycee = s
        if ckey not in screened_communes:
            continue
        region = pref_region[commune_pref[ckey]]
        day = start + timedelta(days=random.randint(0, 20))
        n = max(8, int(random.gauss(38, 12)))
        per_pref_actual[commune_pref[ckey]] = per_pref_actual.get(commune_pref[ckey], 0) + n
        for _ in range(n):
            stu += 1
            cycle = 2 if (has_lycee and random.random() < 0.35) else 1
            age = random.randint(15, 20) if cycle == 2 else random.choices(range(10, 17), weights=[2, 8, 14, 19, 18, 12, 6])[0]
            sex = 1 if random.random() < 0.55 else 2
            p_screen = min(0.95, REGION_SCREEN[region] + 0.04 * (year - 2024))
            screen = 0 if random.random() > p_screen else random.choices([1, 2, 3], weights=[44, 39, 17])[0]
            wears = 1 if random.random() < 0.08 else 0
            years_corr = random.choices(range(1, 8), weights=[14, 15, 11, 4, 5, 3, 1])[0] if wears else None
            impact = 1 if random.random() < 0.90 else 0
            has_sym = 1 if random.random() < 0.91 else 0
            screen_rows.append((stu, int(day.strftime("%Y%m%d")), skey, sex, 1 if age <= 14 else 2, age, cycle, screen, wears, years_corr, impact, has_sym))
            if has_sym:
                for k, _, _, p in SYMPTOM:
                    if random.random() < p:
                        sym_rows.append((stu, k))
            for k, cat_fr, _, _, _, p in HISTORY:
                if random.random() < HIST_CAT_P[cat_fr] * p * 2.2:
                    hist_rows.append((stu, k))
            dk_od = pick_diag(region, year)
            dk_og = dk_od if random.random() < 0.7 else pick_diag(region, year)
            for eye, dk in ((1, dk_od), (2, dk_og)):
                sph, cyl, axis = refraction(dk)
                va = va_from(sph, cyl)
                rx_sph = q(sph * 0.8) if abs(sph) >= 0.5 else 0.0
                rx_cyl = q(cyl * 0.8) if abs(cyl) >= 0.5 else 0.0
                # --- injected data-quality issues (for integrity-check measures) ---
                r = random.random()
                if r < 0.002:
                    rx_cyl = 8.0              # implausible cylinder (typing error)
                elif r < 0.006:
                    rx_cyl = abs(rx_cyl)      # mixed sign convention (plus cylinder)
                va_out = None if random.random() < 0.004 else va
                eye_rows.append((stu, eye, dk, va_out, va_cat(va if va_out is None else va_out), sph, cyl, axis, rx_sph, rx_cyl, axis if rx_cyl else 0))
    for pkey, actual in per_pref_actual.items():
        target_rows.append((pkey, int(f"{year}0301"), round(actual / random.uniform(0.78, 1.08), -1)))

write("FactScreening.csv", ["StudentKey", "DateKey", "SchoolKey", "SexKey", "AgeBandKey", "Age", "CycleKey", "ScreenTimeKey",
                            "WearsCorrection", "YearsWithCorrection", "PerceivedSchoolImpact", "HasSymptoms"], screen_rows)
write("FactEyeExam.csv", ["StudentKey", "EyeKey", "DiagnosisKey", "VA_10", "VACategoryKey", "SphereCyclo", "CylinderCyclo", "AxisCyclo",
                          "SphereRx", "CylinderRx", "AxisRx"], eye_rows)
write("BridgeSymptom.csv", ["StudentKey", "SymptomKey"], sym_rows)
write("BridgeHistory.csv", ["StudentKey", "HistoryKey"], hist_rows)
write("FactTarget.csv", ["PrefectureKey", "DateKey", "TargetStudents"], target_rows)

# ---------------------------------------------------------------------------
# 5. Security table for dynamic RLS (replace e-mails with your test accounts)
# ---------------------------------------------------------------------------
write("SecurityUserRegion.csv", ["UserEmail", "RegionCode"],
      [("directeur.plateaux@demo.org", "PLA"), ("director.maritime@demo.org", "MAR"),
       ("analyste.national@demo.org", "SAV"), ("analyste.national@demo.org", "KAR"),
       ("analyste.national@demo.org", "CEN"), ("analyste.national@demo.org", "PLA"),
       ("analyste.national@demo.org", "MAR")])

# ---------------------------------------------------------------------------
# 6. Report labels (UI text) - one row per label and language
# ---------------------------------------------------------------------------
LABELS = [
    ("title_exec", "Dépistage visuel en milieu scolaire - Vue direction", "School Vision Screening - Executive View"),
    ("title_analysis", "Analyse des amétropies", "Refractive Error Analysis"),
    ("kpi_screened", "Élèves dépistés", "Students screened"),
    ("kpi_need", "Besoin de correction", "Need for correction"),
    ("kpi_impairment", "Déficience visuelle", "Visual impairment"),
    ("kpi_target", "Atteinte de l'objectif", "Target achievement"),
    ("kpi_yoy", "Variation annuelle", "Year-over-year change"),
    ("kpi_screen", "Exposition aux écrans", "Screen exposure"),
    ("chart_region", "Besoin de correction par région", "Need for correction by region"),
    ("chart_rank", "Classement des préfectures", "Prefecture ranking"),
    ("chart_trend", "Évolution par campagne", "Trend by campaign"),
    ("chart_diag", "Répartition des diagnostics", "Diagnosis breakdown"),
    ("chart_symptom", "Signes fonctionnels déclarés", "Reported symptoms"),
    ("chart_screen", "Diagnostic selon le temps d'écran", "Diagnosis by screen time"),
    ("slicer_language", "Langue", "Language"),
    ("slicer_region", "Région", "Region"),
    ("slicer_campaign", "Campagne", "Campaign"),
    ("note_synthetic", "Données synthétiques à des fins de démonstration", "Synthetic data for demonstration purposes"),
    ("note_dq", "Contrôles d'intégrité des données", "Data integrity checks"),
]
write("Labels.csv", ["LabelKey", "LanguageCode", "Text"],
      [(k, "FR", fr) for k, fr, _ in LABELS] + [(k, "EN", en) for k, _, en in LABELS])
print("\nDone. Students:", stu)
