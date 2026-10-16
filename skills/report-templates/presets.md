# Presets

Starting points to offer the user, so they pick instead of typing everything.
Every preset can be adjusted afterwards (e.g. "Corporate, but with our brand blue").

## Design presets

Each preset sets the font links, `--font-body`, `--font-heading` and the colour tokens below.
Leave the category tokens (`--people-*`, `--delivery-*`, `--stakeholder-*`, `--strategy-*`)
as they are: they're tuned to work on all five presets.

Every text colour below meets WCAG AA (4.5:1) against `--bg`, `--surface` and
`--surface-2` in its mode. If the user changes a value, check the ratios again.

| Preset | Feel | Fonts | Good for |
|---|---|---|---|
| **Classic** (default) | Warm neutral, quiet blue accent | System fonts | Everyday reports, no setup |
| **Corporate** | Cool greys, navy accent | Inter | Reports for leadership and stakeholders |
| **Editorial** | Ivory paper, serif headings, deep red | Source Serif 4 + Source Sans 3 | Performance reviews, long-form writing |
| **Minimal** | Pure white, black type, teal accent | IBM Plex Sans | Technical and engineering audiences |
| **Friendly** | Soft lavender, violet accent, rounded type | DM Sans | Team-facing updates, recognition |

Two more options are always available:
- **From my logo:** take the dominant brand colour from the logo as `--accent`, then build
  the rest on the closest preset (usually Classic or Corporate). Adjust the accent until it
  passes 4.5:1 in both modes; use a lighter tint of it in dark mode.
- **Custom:** the user gives their own colours and fonts.

### Classic
Fonts: none (system).
`--font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;`
`--font-heading: var(--font-body);`

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#185fa5` | `#b5d4f4` |
| `--bg` | `#f5f4f0` | `#1a1a18` |
| `--surface` | `#ffffff` | `#252523` |
| `--surface-2` | `#f0ede8` | `#2e2e2b` |
| `--text-primary` | `#1a1a18` | `#f0ede8` |
| `--text-secondary` | `#5a5a56` | `#a0a09a` |
| `--text-muted` | `#6b6b65` | `#96968f` |
| `--border` | `rgba(0,0,0,0.08)` | `rgba(255,255,255,0.07)` |
| `--border-strong` | `rgba(0,0,0,0.13)` | `rgba(255,255,255,0.12)` |

### Corporate
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```
`--font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;`
`--font-heading: var(--font-body);`

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#1e3a8a` | `#93b4f5` |
| `--bg` | `#f4f6f9` | `#0b1220` |
| `--surface` | `#ffffff` | `#131c2e` |
| `--surface-2` | `#eaeef3` | `#1b263b` |
| `--text-primary` | `#0f1b2d` | `#e8edf5` |
| `--text-secondary` | `#4a5568` | `#a3b1c6` |
| `--text-muted` | `#5f6b7d` | `#8a99b0` |
| `--border` | `rgba(15,27,45,0.08)` | `rgba(232,237,245,0.08)` |
| `--border-strong` | `rgba(15,27,45,0.14)` | `rgba(232,237,245,0.14)` |

### Editorial
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap" rel="stylesheet">
```
`--font-body: "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;`
`--font-heading: "Source Serif 4", Georgia, "Times New Roman", serif;`

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#9b2c2c` | `#f0a3a3` |
| `--bg` | `#faf7f2` | `#1c1815` |
| `--surface` | `#fffdf9` | `#26211d` |
| `--surface-2` | `#f2ece2` | `#302a25` |
| `--text-primary` | `#221c17` | `#f3ece3` |
| `--text-secondary` | `#5c5148` | `#b8ab9c` |
| `--text-muted` | `#6f6359` | `#9e9183` |
| `--border` | `rgba(34,28,23,0.09)` | `rgba(243,236,227,0.08)` |
| `--border-strong` | `rgba(34,28,23,0.15)` | `rgba(243,236,227,0.14)` |

### Minimal
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```
`--font-body: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;`
`--font-heading: var(--font-body);`

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#0f766e` | `#5eead4` |
| `--bg` | `#ffffff` | `#0d0d0d` |
| `--surface` | `#ffffff` | `#161616` |
| `--surface-2` | `#f5f5f5` | `#1f1f1f` |
| `--text-primary` | `#111111` | `#f2f2f2` |
| `--text-secondary` | `#4d4d4d` | `#b3b3b3` |
| `--text-muted` | `#666666` | `#949494` |
| `--border` | `rgba(0,0,0,0.12)` | `rgba(255,255,255,0.10)` |
| `--border-strong` | `rgba(0,0,0,0.20)` | `rgba(255,255,255,0.18)` |

Minimal's surface matches its background in light mode, so the borders are stronger to keep panels visible.

### Friendly
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
```
`--font-body: "DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;`
`--font-heading: var(--font-body);`

| Token | Light | Dark |
|---|---|---|
| `--accent` | `#6d28d9` | `#c4b5fd` |
| `--bg` | `#f7f5fb` | `#17131f` |
| `--surface` | `#ffffff` | `#211b2c` |
| `--surface-2` | `#efeaf7` | `#2a2338` |
| `--text-primary` | `#1f1a2e` | `#f1edf8` |
| `--text-secondary` | `#544c66` | `#b7aecb` |
| `--text-muted` | `#665d79` | `#9d93b1` |
| `--border` | `rgba(31,26,46,0.08)` | `rgba(241,237,248,0.08)` |
| `--border-strong` | `rgba(31,26,46,0.14)` | `rgba(241,237,248,0.14)` |

## Footer line suggestions
- `Internal · <Company>` (default)
- `Confidential · <Company> · Do not forward`
- `<Team> · <Company>`
- `Prepared by <Name> · <Team>`

## Report template catalogue

Offer these when the user asks for a new template without a clear idea, or asks what's
possible. Skip the ones that already exist in `reports/templates/`.

| Template | Who reads it | When | Sections | Draws from |
|---|---|---|---|---|
| Team update *(weekly, ships with setup)* | Your manager, stakeholders | Weekly | Personal note · This week · Watch items · Manager impact · Delivery · Team | `my_performance/weeks/` (wins, risks, Friday review), `team_performance/sprints.md`, the current sprint in `team_performance/sprints/`, `initiatives/*.md`, `direct_reports/*/notes.md` |
| Monthly individual report *(ships with setup)* | The report, you | Monthly | Highlights · Progress on goals · Feedback · Wellbeing · Next focus | `direct_reports/<name>/notes.md` |
| Quarterly review *(ships with setup)* | The report, HR | Quarterly | Summary · Goals · Strengths · Growth areas · Values · Next quarter | `direct_reports/<name>/notes.md` (feedback log, goals) |
| 1:1 summary | The report | After a 1:1 | Topics · Decisions · Actions (owner, date) · For next time | `direct_reports/<name>/notes.md` (1:1 log) |
| Sprint report *(ships with setup, filled in by the sprint-goals skill)* | Stakeholders, your manager | Each sprint | Summary · Numbers · Achieved · Not achieved or changed · Next sprint · Risks and asks | `team_performance/sprints/*.md` (goals, check-in, final check) |
| Initiative status | Stakeholders | Fortnightly or monthly | Status (on track / at risk / off track) · Progress vs milestones · Risks · Decisions needed · Next steps | `initiatives/<name>.md` |
| Quarterly team report | Your manager, leadership | Quarterly | Headline · Goal/OKR results · Delivery trends · Team health · People changes · Next quarter | `team_performance/`, `initiatives/`, `my_performance/` |
| Stakeholder pre-brief | Your manager or a stakeholder | Before a key meeting | Context · Outcome I want · Options · My recommendation · What I need from you | `stakeholders/<name>.md`, `my_performance/manager-1on1-notes.md` |
| Onboarding plan (30-60-90) | New joiner | First week | Welcome · People to meet · 30 / 60 / 90-day goals · First tasks · Check-in dates | `direct_reports/<name>/notes.md` |
| Promotion case | Calibration panel | Promotion cycle | Summary · Scope and impact · Evidence by competency · Peer feedback · Readiness and risks | `direct_reports/<name>/notes.md` (goals, feedback, recognition) |
| Incident summary | Team, stakeholders | After an incident | Impact · Timeline · Root cause · What went well · Actions (owner, date) | — |
| Tech strategy one-pager | Team, leadership | Quarterly | Context · Problem · Options considered · Recommendation · Risks · Ask | Quarterly tech strategy review in `manager-cadence.html` |
