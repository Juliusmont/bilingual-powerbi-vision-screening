// Tabular Editor 2 - C# script: adds the fr-FR culture and French metadata translations.
// Usage: Power BI Desktop > External Tools > Tabular Editor > "C# Script" tab > paste > Run (F5)
// then Ctrl+S to save back to the model. Model default culture stays en-US (object names in English).

var fr = "fr-FR";
if (!Model.Cultures.Contains(fr)) Model.AddTranslation(fr);

var map = new Dictionary<string, string> {
    // Tables
    {"FactScreening", "Dépistages"}, {"FactEyeExam", "Examens oculaires"}, {"FactTarget", "Objectifs"},
    {"DimRegion", "Régions"}, {"DimPrefecture", "Préfectures"}, {"DimCommune", "Communes"},
    {"DimSchool", "Établissements"}, {"DimSchoolType", "Types d'établissement"}, {"DimDate", "Calendrier"},
    {"DimDiagnosis", "Diagnostics"}, {"DimSex", "Sexe"}, {"DimAgeBand", "Tranches d'âge"},
    {"DimCycle", "Cycles"}, {"DimScreenTime", "Temps d'écran"}, {"DimVACategory", "Catégories d'acuité"},
    {"DimSymptom", "Signes fonctionnels"}, {"DimHistory", "Antécédents"}, {"DimEye", "Œil"},
    {"DimLanguage", "Langue"}, {"_Measures", "_Mesures"},
    // Columns
    {"Prefecture", "Préfecture"}, {"ChefLieu", "Chef-lieu"}, {"CommuneName", "Commune"},
    {"SchoolName", "Établissement"}, {"SchoolCode", "Code établissement"}, {"Age", "Âge"},
    {"Year", "Année"}, {"Date", "Date"}, {"LanguageName", "Langue"},
    {"VA_10", "Acuité visuelle (/10)"}, {"SphereCyclo", "Sphère (cycloplégie)"},
    {"CylinderCyclo", "Cylindre (cycloplégie)"}, {"AxisCyclo", "Axe (cycloplégie)"},
    {"SphereRx", "Sphère prescrite"}, {"CylinderRx", "Cylindre prescrit"}, {"AxisRx", "Axe prescrit"},
    {"TargetStudents", "Élèves visés"},
    // Measures
    {"Students Screened", "Élèves dépistés"}, {"Eyes Examined", "Yeux examinés"},
    {"Students Needing Correction", "Élèves nécessitant une correction"},
    {"Correction Need Rate", "Taux de besoin de correction"},
    {"Uncorrected Need", "Besoin non corrigé"}, {"Uncorrected Need Rate", "Taux de besoin non corrigé"},
    {"Students With Impairment", "Élèves avec déficience visuelle"}, {"Impairment Rate", "Taux de déficience visuelle"},
    {"Screen Exposure Rate", "Taux d'exposition aux écrans"}, {"Diagnosis Share", "Part du diagnostic"},
    {"Students With Symptom", "Élèves avec signe fonctionnel"}, {"Symptom Rate", "Taux de signes fonctionnels"},
    {"Students Screened PY", "Élèves dépistés (année précédente)"}, {"Students Screened YoY %", "Variation annuelle des dépistages"},
    {"Students Screened YTD", "Élèves dépistés (cumul annuel)"}, {"Correction Need Rate PY", "Taux de besoin (année précédente)"},
    {"Correction Need Rate Change (pts)", "Variation du taux de besoin (pts)"},
    {"Target Students", "Élèves visés"}, {"Target Achievement %", "Atteinte de l'objectif (%)"},
    {"Prefecture Rank (Need Rate)", "Rang de la préfecture (taux de besoin)"},
    {"Correction Need Rate (Safe)", "Taux de besoin (protégé)"},
    {"DQ Issues Total", "Anomalies de données (total)"}, {"DQ Status", "État de la qualité des données"}
};

int n = 0;
foreach (var t in Model.Tables) {
    if (map.ContainsKey(t.Name)) { t.TranslatedNames[fr] = map[t.Name]; n++; }
    foreach (var c in t.Columns)  if (map.ContainsKey(c.Name)) { c.TranslatedNames[fr] = map[c.Name]; n++; }
    foreach (var m in t.Measures) if (map.ContainsKey(m.Name)) { m.TranslatedNames[fr] = map[m.Name]; n++; }
}
Info("fr-FR translations applied: " + n);
