# Management OS

A personal operating system for engineering managers: a folder of plain markdown
notes and HTML reports, organised around a **cadence** of daily, weekly, monthly and
quarterly routines, plus Claude Code skills that do the repetitive parts for you.

**[See what it looks like →](https://tmontovaneli.github.io/management-os/)**

- **One rhythm:** `manager-cadence.html` lists what to do and when, tagged by area:
  People, Delivery, Stakeholder and Strategy.
- **One place to write it down:** notes per direct report, stakeholder and initiative,
  weekly and monthly journals, sprint goals and sprint health.
- **Skills that keep it going:** plan your week from the cadence, get a morning briefing
  from Jira, Slack, email, calendar and GitHub, and produce branded reports.
- **A coach, when you want one:** the AI challenges your inputs and connects them with what it
  already knows, so you go the extra mile. On a tired day, switch to Assist mode.

Everything is local files in a git repository you own. No server, no database.

## Quick start

Requirements: **Python 3.8+**. Git and [Claude Code](https://claude.com/claude-code)
are optional, but you need Claude Code to use the skills.

```bash
git clone https://github.com/tmontovaneli/management-os.git
cd management-os
python3 setup_management_os.py
```

Clone the whole repository rather than downloading only the script: the skills in
`skills/` are copied into every workspace setup creates.

Setup asks about:
- you, your manager and your team
- your direct reports, key stakeholders and current initiatives
- your tech stack, company values and sprint length (these personalise the cadence)
- which tools your team uses: Jira, Slack, Gmail + Google Calendar, GitHub
- whether you're new in the role (then it offers to plan your first 90 days)
- how much the AI should challenge you: always, only in rituals, or never (Assist mode)
- where to create the workspace, and whether to make it a git repository

Then it creates your workspace, registers the tools it can, and offers to continue in
Claude Code: either to finish connecting your tools or to set up your report design.

### Options

| Option | What it does |
|---|---|
| `--dry-run` | Lists the files it would create, without creating anything |
| `--config answers.json` | Skips the questions and uses a JSON file (same shape as the `.management_os.json` setup writes) |
| `--target <folder>` | Where to create the workspace |
| `--no-git` | Doesn't create a git repository |

## What you get

```
your_workspace/
  manager-cadence.html        your rhythm: daily, weekly, monthly, quarterly
  direct_reports/
    <name>/notes.md           1:1 log, goals, career conversations, feedback, recognition
    <name>/reports/           reports you've filled in for this person
    template/
  team_performance/
    sprints.md                sprint health log
    sprints/<sprint>.md       one per sprint: goals and owners, mid-sprint check-in, final check
    sprints/<sprint>-report.html   the sprint report you sent to stakeholders
    metrics/<from>_<to>.md    activity per direct report for a period, from Jira and GitHub
  initiatives/
    <project>.md              goal, milestones, risks, decision log
    template/
  stakeholders/
    <name>.md                 what they care about, how to work with them, history
    template/
  my_performance/
    weeks/YYYY-Www.md         weekly journal: focus, tasks, daily win/risk, Friday review
    journal-YYYY-MM.md        monthly intentions and month retro
    first-90-days/plan.md     your 90-day plan, if you're new in the role
    manager-1on1-notes.md     your 1:1s with your manager
    template/
  reports/
    my_report_design.html     your report design: colours, fonts, logo, footer
    templates/                team update (weekly), sprint report, monthly and quarterly individual reports
    assets/
  skills/                     the skills below (.claude/skills points here)
  CLAUDE.md                   how the AI works in your workspace, including coaching
  .management_os.json         your setup answers and tool settings (no secrets)
```

Reports are self-contained HTML files: open one in a browser, click any text to edit
it, then print to PDF.

## Skills

Open your workspace in Claude Code and ask in your own words, or call a skill directly
with `/<name>`.

| Skill | Say something like | What it does |
|---|---|---|
| `plan-week` | "plan my week" | Builds the week's journal from your cadence: daily tasks for each working day, weekly tasks (one 1:1 per report), monthly and quarterly items not done yet, and unfinished items carried over from last week. It also sets up the month's intentions in the first week of a month and reminds you about the retro in the last week. |
| `first-90-days` | "plan my first 90 days" | For a new role: builds a 30/60/90-day plan from your situation, prepares listening-tour conversations and records what you learn, and runs checkpoint reviews at days 30, 60 and 90. Based on the ideas in *The First 90 Days* by Michael D. Watkins. |
| `sprint-goals` | "record sprint goals", "sprint check-in", "sprint report" | After sprint planning: records each goal and its owners. Halfway: a check-in that catches goals off track, already achieved, or needing realignment. At the end: the final check. Then it builds the sprint report for stakeholders: what the team achieved, and what it focuses on next sprint. Check-in and final check days show up in your week file. |
| `team-metrics` | "team metrics for last sprint", "Mia's numbers this quarter" | Collects each direct report's activity for a period: tickets created, closed and in progress from Jira; commits and PRs created, merged, reviewed and commented on from GitHub. Saves one table per period, compares each person with their own earlier periods, and asks for the context the numbers miss. No rankings. |
| `morning-pulse` | "morning pulse" | Read-only daily briefing, blockers first: today's calendar, Jira board, PRs by your reports, Slack and email that need you, and today's journal. |
| `coach` | "assist mode", "coach me on this" | Sets how much the AI challenges you (see below). |
| `connect-tools` | "connect my tools" | Connects Jira, Slack, Gmail, Google Calendar and GitHub one at a time, lets you pick the board, channels and repos, matches your reports to their accounts, and tests each connection. |
| `report-templates` | "set up my report design", "create a report template for …" | Applies your design (five presets, or your own colours, fonts and logo) to every report template, and creates new templates from a catalogue of common manager reports. |

### Coach mode and Assist mode

By default the AI **coaches** you. After you've given your input, it raises up to three
challenges, each tied to something in your workspace. For example: a focus item that serves none
of your month's intentions, a direct report you haven't had a 1:1 with in three weeks, a sprint goal with no
"done when", or a report that lists work but not why it matters. Reply "skip" or "good enough" and it moves on.

That's demanding, so you choose how often it happens:

| Level | Coaching happens in |
|---|---|
| `always` *(default)* | everything, including the morning pulse and 1:1 notes |
| `rituals` | weekly planning, retros, sprint goals, reviews and reports, first-90-days checkpoints |
| `off` | nowhere: **Assist mode**, with defaults, few questions and no challenges |

- **For today:** say "assist mode", or "coach me on this" for one task.
- **For a week:** plan-week asks your energy. "Low" turns coaching off for that week, and "high" turns it on everywhere.
- **From now on:** say "set coaching to rituals" (it's `coaching` in `.management_os.json`).

### A typical week

- **Friday:** "plan my week" → next week's journal, with a suggested focus.
- **Every morning:** "morning pulse" → what needs you, then tick tasks off in the week file.
- **Every evening:** one win and one risk in today's section (3 minutes).
- **End of the week:** Friday review in the week file, then fill in the team update report.
- **Each sprint:** "record sprint goals" after planning, "sprint check-in" halfway, "final check" at the
  end, then "sprint report" once the next sprint's goals are set.

## Connecting your tools

The morning pulse reads from your work tools. Setup records which ones you use and
registers what it can; `connect-tools` does the rest with you inside Claude Code.

| Tool | Connected through |
|---|---|
| Jira (Atlassian Cloud) | Atlassian's official MCP server |
| Slack | Slack's official MCP server |
| Gmail and Google Calendar | Claude connectors (claude.ai → Settings → Connectors) |
| GitHub | The GitHub CLI (`gh`) |

- Sign-ins use your browser (OAuth). **No tokens or passwords are stored in the workspace.**
- Jira and Slack often need an admin to approve the connection the first time.
- The exact commands, with links to the official docs, are in
  [`skills/connect-tools/tools.md`](skills/connect-tools/tools.md).
- Not supported yet: Microsoft 365 (Outlook), GitLab, Bitbucket, Linear, Teams.

## Privacy

Your workspace holds notes about real people. Keep it in a **private** repository, and
only connect tools your company allows you to connect. The skills only read from your
tools: they never send messages, post comments or change tickets.

## This repository

```
setup_management_os.py   the setup script (Python standard library only)
skills/                  skills copied into every new workspace
manager-cadence.html     example of the cadence setup generates, with generic answers (open it to preview)
```

### Adding or changing a skill

Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter, and add a
row to [`skills/README.md`](skills/README.md). Every workspace created afterwards gets it.
Existing workspaces keep their own copy: copy the updated skill folder into
`<workspace>/skills/` to update one.

### Changing the generated files

The notes, cadence and report templates are generated by `setup_management_os.py`.
Edit the matching `md_*` or `html_*` function, then check the result with:

```bash
python3 setup_management_os.py --dry-run
python3 setup_management_os.py --config answers.json --target /tmp/test_workspace --no-git
```
