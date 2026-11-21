# Building the report with Claude Code + Power BI Desktop

How this report was built: Claude Code drives Power BI Desktop through Microsoft's
**powerbi-authoring** plugin (Skills for Fabric), guided by a design guidebook written first.
The guidebook is the lever: the agent has nothing left to guess.

> Everything below runs on **Windows**, on the machine where Power BI Desktop is installed.
> The Report Authoring CLI is in public preview: commands may change between 0.x versions.

## 0. Prerequisites (once)

| Tool | Why | Check |
|---|---|---|
| Power BI Desktop (recent) | the report itself | *Options > Preview features*: enable **Power BI Project (.pbip) save option** and **PBIR format** |
| Node.js 20+ | runs the CLIs | `node -v` |
| Git | undo history, commits | `git --version` |
| Claude desktop app, **Code** tab (paid plan) | the agent | |
| Azure CLI (optional) | publish to the Service | `az version` |

```powershell
winget install OpenJS.NodeJS.LTS
winget install Git.Git
winget install --exact --id Microsoft.AzureCLI   # optional, for publishing
```

## 1. Prepare the project (once)

1. Clone the repo to a **local folder outside OneDrive**, e.g. `C:\dev\bilingual-powerbi-vision-screening`.
2. Open the existing `.pbix`. In Power Query, create a text parameter **`DataFolder`** = `C:\dev\bilingual-powerbi-vision-screening\data\` and make every CSV source use it (`File.Contents(DataFolder & "FactScreening.csv")`). No absolute path left in any query.
3. *Refresh*: the new `FactEyeExam.csv` (prescribing rule v1.1) and `Labels.csv` (new labels) are loaded.
4. *File > Save as > Power BI project (.pbip)* into `powerbi\` as **`VisionScreening.pbip`**. Keep Desktop open.
5. In Claude (Code tab), open the repo folder.

## 2. Install the Power BI tooling in Claude Code (once)

Prompt 1:
```
Add the plugin marketplace microsoft/skills-for-fabric, then install the plugin powerbi-authoring@fabric-collection.
```
Prompt 2:
```
Install this npm package globally: @microsoft/powerbi-report-authoring-cli@latest
```
Restart Claude, then check with `/skills` that `semantic-model-authoring` and `powerbi-report-authoring` are listed.

## 3. Build, one prompt per step

Run them in order. **Review the screenshot and commit after each step** (`git commit -am "…"`), so any bad step can be undone.

**Step A - Audit the model (read only)**
```
Read CLAUDE.md, docs/DESIGN_GUIDEBOOK.md and docs/expected-kpis.md.
Connect to the open Power BI Desktop model with the Power BI Modeling MCP.
List tables, relationships (direction, cardinality), measures, field parameters, RLS roles and the fr-FR culture.
Compare with dax/measures.dax. Report what is missing or different. Do not change anything.
```

**Step B - Report-layer measures + verification**
```
Add every measure from dax/measures-report.dax to the _Measures table, with the display folders from the comments.
Then run DAX queries to check Students Screened, Correction Need Rate, Uncorrected Need Rate, Impairment Rate
and Target Achievement % by DimDate[Year], and the DQ measures, against docs/expected-kpis.md.
Show me a comparison table. Stop if anything differs by more than 0.1 point.
```

**Step C - Theme, canvas, sidebar, header (Overview page)**
```
Apply powerbi/themes/vision-screening-light.json. Set every report page to 1440 x 810.
On the Overview page build the sidebar and the header exactly as in sections 2, 6 and 7 of the guidebook
(page navigator buttons bound to Lbl Nav measures, FR | EN language slicer synced on all pages, campaign pill).
Validate, reload Desktop, screenshot, and check positions against the guidebook before stopping.
```

**Step D - Narrative banner and KPI cards**
```
Build the narrative banner (Lbl Narrative Title + Narrative Headline) and the 5 KPI cards from section 5 of the guidebook,
including the comparison pills with their colour measures and the KPI definition tooltip page.
Screenshot in FR and in EN. Check the values against docs/expected-kpis.md.
```

**Step E - Overview main visuals**
```
Build the three main visuals of page 2 (section 6, "Page 2 - Overview"): need by region, trend by campaign, prefecture ranking.
Titles from Lbl measures, axis from field parameters, alt text, tab order. Screenshot FR and EN, then list any hard-coded text.
```

**Step F - Clinical analysis page**, **Step G - Quality & security page**, **Step H - About page**: same prompt pattern, pointing to the matching guidebook table.

**Step I - Final review**
```
Go through every page in FR then EN. For each screenshot, check the guidebook section 8 "What we do NOT want" and
section 10 "Definition of done". Fix what fails, then give me a checklist with pass / fail per item.
```

## 4. Captures, video, publish

- Captures and demo video: follow [`CAPTURE_CHECKLIST.md`](CAPTURE_CHECKLIST.md).
- Optional publish:
```
Log me in to Azure with the Azure CLI, then publish powerbi/VisionScreening.pbip to my workspace "<name>".
Open the report with ?language=fr and ?language=en and confirm the metadata translations appear.
```

## Limits worth knowing

- The agent edits files; **Power BI Desktop stays the source of truth**. Always look at the rendered page, not only at the agent's summary.
- "First time right" is not the goal: the guidebook reduces iterations, it does not remove review. Budget one review per page.
- Tools are in preview and renamed often: if a command fails, ask Claude to check the plugin's current skill documentation rather than retrying blindly.
