---
name: report-templates
description: Owns the look of this Management OS's HTML reports. Use when the user wants to set up or change their report design (colours, fonts, logo, footer line), create a new HTML report template, or re-apply the design to existing templates. The design lives in reports/my_report_design.html and templates live in reports/templates/.
---

# Report templates

Every HTML report in this workspace shares one design, defined in
`reports/my_report_design.html`. This skill keeps that file and the templates in
`reports/templates/` in step. All paths are relative to the workspace root.

## The design contract

`reports/my_report_design.html` is the source of truth. It has four marked
regions, and every template carries a copy of the same four:

| Region | Where | Holds |
|---|---|---|
| Fonts | `<!-- brand:fonts:start -->` … `<!-- brand:fonts:end -->` in `<head>` | Google Fonts `<link>` tags, or nothing for system fonts |
| Tokens | `<style id="design-tokens">` … `</style>` | CSS custom properties: colours (light and dark), `--font-body`, `--font-heading`, `--accent` |
| Logo | `<!-- brand:logo:start -->` … `<!-- brand:logo:end -->` inside `.brand-logo` | One `<img>` with a `data:` URI, or nothing |
| Footer | `<!-- brand:footer:start -->` … `<!-- brand:footer:end -->` | The footer line, e.g. "Confidential · Acme" |

Rules:
- Everything outside the regions is layout and content. Layout CSS uses only
  `var(--…)` tokens: never hard-code a colour or font outside the tokens block.
- Reports must stay self-contained, so they still work after being copied
  anywhere or printed to PDF. Embed the logo as a `data:` URI and keep the
  original file in `reports/assets/`. The only allowed external resource is Google Fonts.
- Keep the existing token names; templates depend on them. You may add tokens.
- Keep the shape of the tokens block: light values in `:root`, dark values in
  `@media screen and (prefers-color-scheme: dark)` (screen only, so reports always
  print light), and the `@media print` block that forces white backgrounds.
- Keep the markers exactly as written. Put nothing inside `.brand-logo` except
  the logo region, with no whitespace around it: an empty slot is hidden with `:empty`.

## Workflow 1: set up or change the design

1. Read `reports/my_report_design.html` and summarise the current design in two or three lines.
2. Offer choices, so the user picks rather than types. Read [presets.md](presets.md),
   then ask in one short batch:
   - **Look:** the five design presets as a numbered list, each with its one-line feel
     and what it's good for, plus "From my logo" and "Custom". Mark the current one.
     If the user is unsure, recommend Classic or Corporate, depending on who reads their reports.
   - **Logo:** a path to an SVG or PNG file (SVG preferred), or "no logo".
   - **Footer line:** the suggestions from presets.md, with `<Company>` and `<Team>`
     filled in from `.management_os.json`.
   Use a multiple-choice question tool if you have one. Don't ask about category
   colours unless the user brings them up.
3. Apply the changes:
   - **Colours and fonts from a preset:** copy its values from presets.md exactly.
     The values are already checked, so no adjustment is needed.
   - **Any other colour change** (from a logo, custom, or tweaking a preset): update the light
     tokens and the dark-mode block. All text, including badges and labels, must meet
     WCAG AA (4.5:1) against `--bg`, `--surface` and `--surface-2`. Calculate the ratios
     with a script; don't estimate them. In dark mode, don't invert the colours: use dark
     backgrounds and lighter tints of the same hues.
   - **Fonts:** put the Google Fonts `<link>` (with `display=swap`) in the fonts
     region, and set `--font-body` and `--font-heading` with a system fallback stack.
   - **Logo:** copy the file to `reports/assets/logo.<ext>`, then embed it in the
     logo region as `<img src="data:image/svg+xml;base64,…" alt="<Company> logo">`
     (use `image/png` for PNG). Produce the base64 with a shell command such as
     `base64 < file | tr -d '\n'`, and write it into the file with a script. Never
     type base64 out. If the file is over ~200 KB, say so and suggest a smaller or SVG version.
   - **Footer:** replace the text inside the footer region.
4. Ask the user to open `reports/my_report_design.html` in a browser and check it
   in light and dark mode.
5. Offer workflow 3 to apply the design to the existing templates.

## Workflow 2: create a new report template

1. If the user hasn't said which report they want, offer the template catalogue from
   [presets.md](presets.md) as a numbered list, leaving out templates that already exist in
   `reports/templates/`. Once they pick one, show its suggested sections and ask what to
   add, remove or rename. For a report that isn't in the catalogue, ask what it's for,
   who reads it and how often, then suggest sections. Base the suggestions on the matching
   item in `manager-cadence.html` and on the notes the content will come from.
2. Start from the closest file in `reports/templates/` so the structure, CSS and
   print behaviour match. Copy the four brand regions from
   `reports/my_report_design.html`, not from the other template.
3. Conventions:
   - File name in kebab-case: `reports/templates/<name>.html`.
   - The title, subtitle and every section panel are `contenteditable="true"`, with
     placeholder text that says what goes there.
   - Sections reuse the existing `.section`, `.panel` and `table` patterns.
   - Keep the `.hint` line and the `@media print` rules.
   - It must work at phone width, with no horizontal scrolling.
4. Add a card for it to the Templates list in `reports/my_report_design.html`,
   between `<!-- templates:start -->` and `<!-- templates:end -->`.
5. Tell the user where the file is and how to use it: copy it next to what it is
   about (e.g. `direct_reports/<name>/reports/`), open it in a browser, edit, then print to PDF.

## Workflow 3: apply the design to existing templates

1. For every `.html` file in `reports/templates/`, replace each of the four brand
   regions with the current version from `reports/my_report_design.html`. Change nothing else.
   Do it with a small Python script that edits the files in place, not by retyping them.
2. If a template is missing a region, add it where `my_report_design.html` has it,
   and tell the user.
3. Filled-in reports elsewhere (e.g. `direct_reports/*/reports/`) are records of
   what was sent. Leave them alone unless the user explicitly asks.
4. List the files you changed.
