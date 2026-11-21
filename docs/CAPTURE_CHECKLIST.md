# Screenshots and demo video - checklist

## Before capturing
- [ ] Definition of done in `DESIGN_GUIDEBOOK.md` section 10 is met.
- [ ] Power BI Desktop: *View > Fit to page*, panes collapsed (Filters, Visualizations, Data), zoom 100 %.
- [ ] Windows display scaling 100 %, screen 1920 x 1080 or larger.
- [ ] Slicers on **2026 campaign, all regions** unless stated otherwise.
- [ ] No personal e-mail, tenant name or file path visible (title bar, Service header).

## Screenshots (PNG, saved in `screenshots/`)

| # | File name | Content |
|---|---|---|
| 1 | `01-overview-fr.png` | Overview page, French |
| 2 | `02-overview-en.png` | Overview page, English (same filters) |
| 3 | `03-clinical-analysis-fr.png` | Clinical analysis, French |
| 4 | `04-clinical-analysis-en.png` | Clinical analysis, English |
| 5 | `05-quality-security-en.png` | Quality & security page |
| 6 | `06-kpi-tooltip-fr.png` | Hover on the Need card, definition tooltip visible |
| 7 | `07-rls-view-as-plateaux.png` | *Modeling > View as > Region - Plateaux*, banner visible |
| 8 | `08-model-view.png` | Model view, all tables visible, laid out by star schema |
| 9 | `09-service-language-fr.png` | (optional) Power BI Service with `?language=fr`, translated field list |
| 10 | `10-claude-code-session.png` | (optional) Claude Code + Desktop side by side, for the "how it was built" section |

Use *Win + Shift + S* (window capture) for the report canvas only, or *File > Export > PDF* for a full-report PDF (`screenshots/report-fr.pdf`).

## Demo video (60-90 s, no voice needed, captions on screen)

| Time | Shot |
|---|---|
| 0-10 s | Overview in **French**, slow hover over the KPI cards |
| 10-20 s | Click **EN**: titles, axes, numbers (`87,2 %` > `87.2%`) and narrative switch |
| 20-35 s | Select a region: narrative, KPIs and ranking update |
| 35-50 s | Clinical analysis page, hover the screen-time chart |
| 50-65 s | Quality & security page: DQ status, then *View as Region - Plateaux* |
| 65-80 s | (optional) Claude Code prompt building a visual, Desktop reloading |

Record with *Win + Alt + R* (Xbox Game Bar) or Clipchamp, 1080p, 30 fps.
Then, for the README (GitHub plays a GIF inline, an MP4 only as a link or uploaded attachment):

```powershell
# compressed MP4 (< 10 MB) for screenshots/demo.mp4
ffmpeg -i raw.mp4 -vf "scale=1600:-2" -c:v libx264 -preset veryfast -crf 28 -an screenshots/demo.mp4
# light GIF preview for the README
ffmpeg -i screenshots/demo.mp4 -vf "fps=10,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" screenshots/demo.gif
```

## Publishing the Power BI file
- Commit the **`.pbip` project** (text, diffable): this is the source.
- Attach the **`.pbix`** (*File > Save as > .pbix*) to a **GitHub Release `v1.0`** rather than committing the binary.
