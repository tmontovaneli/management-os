---
name: plan-week
description: Creates the weekly journal (my_performance/weeks/YYYY-Www.md) from manager-cadence.html, with daily tasks per working day, weekly tasks, open monthly and quarterly items, and unfinished items carried over from last week. Also keeps the monthly journal going (intentions at the start of the month, retro at the end). Use when the user wants to plan their week or next week, set up or start this week's journal, set monthly intentions, or asks what's on their plate this week.
---

# Plan week

Builds the user's journal for one week from their operating cadence. A script does
the mechanical work; your job is to pick the right week, collect days off, run the
script, and help the user set the week's focus. All paths are relative to the
workspace root.

## What the script produces

`python3 skills/plan-week/plan_week.py` writes `my_performance/weeks/YYYY-Www.md` (ISO week)
containing:

| Section | Comes from |
|---|---|
| Focus | Left blank for the user (you'll suggest items, see step 5) |
| Carried over from last week | Unticked items the user added themselves in the previous week's file |
| This week | Weekly cards in `manager-cadence.html` |
| This month / This quarter | Monthly and quarterly cards not yet ticked (`- [x]`) in an earlier week of the same month or quarter |
| One section per working day | Daily cards, plus Win / Risk / Notes lines |
| Friday review | Intended / Happened / Next week |
| Sprint line and sprint tasks | Sprint files in `team_performance/sprints/` (the sprint-goals skill): a "Sprint:" line under the month link, and the mid-sprint check-in, final check, and the next sprint's planning (record goals, send the sprint report) in their days |

The week file links to the month's journal, and in the last week of a month its
Friday review reminds the user to write the month retro.

**Monthly journal.** The script also creates `my_performance/journal-YYYY-MM.md` from
`my_performance/template/journal-yyyy-mm.md` if it doesn't exist yet. The monthly journal holds
only what is bigger than a week: **Intentions for the month** (one to three, set at the start)
and the **Month retro** (written at the end). Each week's Focus should serve the intentions.
The script's summary ends with three lines you use below:

```
Monthly journal: my_performance/journal-2026-11.md (created | exists)
Month intentions: <intentions separated by ;> | none yet
Week in month: first week of November | middle of November | last week of November
```

Before those, two sprint lines: `Sprint:` (the sprints that overlap the week, or "none recorded")
and `Sprint tasks:` (each sprint task and its day). Sprint tasks aren't carried over: the next
week gets them again only if they're still due.

Cards whose title or description says "direct reports", "per report" or "each report"
become one task per direct report (names from `direct_reports/*/notes.md`).
A week belongs to the month and quarter its Thursday falls in.

Options: `--week current|next|YYYY-Www`, `--whole-week` (current week: include days
already passed), `--days-off YYYY-MM-DD ...`, `--print` (preview without writing).
The script never overwrites an existing week file.

## Workflow

1. **Pick the week.** Check today's date. If the user said which week, use it.
   Otherwise suggest the current week from Monday to Thursday and next week from Friday to Sunday,
   and confirm with the user in one line. If `my_performance/weeks/<that week>.md` already exists, say so
   and go to "Week already exists" below.
2. **For the current week only:** by default the journal starts today. Ask whether
   to include the earlier days too (`--whole-week`) if it's past Monday.
3. **Days off:** ask once whether they're off on any working day that week (holidays,
   leave). Accept answers like "Wednesday" and turn them into dates.
   Combine steps 1–3 into a single question batch. Use a multiple-choice question tool if you have one.
4. **Run the script** with the chosen options from the workspace root, and show the
   summary it prints.
5. **Month intentions, if there are none yet** ("Month intentions: none yet"; usually
   when the monthly journal was just created or this is the first week of the month).
   Suggest one to three intentions for the month, based on:
   - the previous month's retro, especially "One thing to fix next month:"
   - open quarterly items, weighted by how much of the quarter is left
   - open initiatives in `initiatives/*.md` with targets this month
   Write them under "Intentions for the month" only after the user agrees or edits them.
   If the user would rather skip this, move on and don't ask again this week.
6. **Set the focus.** Suggest up to three Focus outcomes that serve the month's
   intentions. Base them on the previous week's Friday review ("Next week:" and
   "Happened:") and the carried-over items. Write them into the Focus section only after
   the user agrees or edits them.
   **During the first 90 days** (`my_performance/first-90-days/plan.md` exists and the week
   falls within day 1–90): work out the day numbers the week covers, add a line under the
   "Month:" link such as `First 90 days: days 23–27 · Learn`, and make at least one Focus
   item come from an unticked goal of the current phase. If a checkpoint (day 30, 60 or 90)
   falls in the week, say so and suggest booking time for it.
7. **Last week of the month** ("Week in month: last week of …"): remind the user that
   the month retro is due this week. Offer to draft it at the end of the week from that
   month's week files: wins, risks, Friday reviews, and what got done versus the intentions.
   The user writes the final version; you only draft.
8. **Point out what needs attention**, briefly:
   - Sprint tasks from the summary. If one falls on a day off, suggest moving it. If
     `sprint_length_weeks` isn't 0 in `.management_os.json` and no sprint is recorded for the week,
     suggest `/sprint-goals` after the next sprint planning.
   - Monthly items still open in the last week of the month, and quarterly items still
     open in the last month of the quarter.
   - Carried-over items that have been carried more than once (check the earlier files).
   - If the week has days off, which weekly tasks may need to move (e.g. 1:1s).
9. Tell the user where the files are. Mention that ticking a monthly or quarterly item
   (`- [x]`) removes it from later weeks of that month or quarter.

## Drafting the month retro

If the user asks for it (or accepts the offer in step 7): read every week file whose
month is that month (the "Month:" link at the top), plus the monthly journal's
intentions. Draft answers under "Month retro" for each prompt, ending with one
suggestion for "One thing to fix next month:". Quote the user's own words from their
wins, risks and reviews where you can. Show the draft before writing it.

## Week already exists

Don't recreate or overwrite it. Offer to:
- add tasks that are missing (compare with `--print` output for the same week and
  insert only the missing lines, keeping everything the user wrote), or
- add or remove a day off (rename the day heading to `· day off` and remove its tasks, or the reverse).

## When the cadence changes

The script reads `manager-cadence.html` every time, so edits to the cadence apply
to the next week created. It relies on the page's structure: a `.section-label`
per frequency (Daily, Weekly, Monthly, Quarterly) followed by cards with
`.card-title` and `.card-desc`. If the user adds a card, keep that structure.
