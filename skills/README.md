# Skills

Agent skills for this workspace. Each folder has a `SKILL.md` that tells an AI
assistant how to do one job here.

`.claude/skills` points to this folder, so Claude Code picks the skills up when you run
it in the workspace. Ask in your own words (e.g. "update my report design") or call
one directly with `/<skill-name>`.

| Skill | What it does |
|---|---|
| [`connect-tools`](connect-tools/SKILL.md) | Connects Jira, Slack, Gmail, Google Calendar and GitHub, and saves which board, channels and repos to use, plus each report's accounts. |
| [`first-90-days`](first-90-days/SKILL.md) | Plans your own first 90 days in a new role (based on *The First 90 Days* by Michael D. Watkins): diagnosis, boss conversations, listening tour, early wins, checkpoints at days 30/60/90. |
| [`morning-pulse`](morning-pulse/SKILL.md) | Daily briefing: blockers first, then calendar, Jira, PRs, Slack, email and today's journal. Read-only. |
| [`plan-week`](plan-week/SKILL.md) | Creates this week's or next week's journal from your cadence (daily and weekly tasks, open monthly/quarterly items, carry-overs), and keeps the monthly journal going: intentions at the start, retro at the end. |
| [`sprint-goals`](sprint-goals/SKILL.md) | Records the goals and owners from sprint planning, runs the mid-sprint check-in and the final check, and builds the sprint report for stakeholders: what the team achieved and what it focuses on next. |
| [`team-metrics`](team-metrics/SKILL.md) | Collects each direct report's activity for a sprint, month or quarter: tickets created, closed and in progress (Jira), and commits and PRs created, merged, reviewed and commented on (GitHub). |
| [`report-templates`](report-templates/SKILL.md) | Owns the look of this Management OS's HTML reports. |

To add a skill, create `skills/<name>/SKILL.md` with `name` and `description` frontmatter,
and add a row to the table above.

- **In the Management OS repository**, every new workspace gets the skill. `setup_management_os.py`
  copies this whole folder.
- **In your own workspace**, only you get it. Existing workspaces don't pick up later changes
  to the repository; copy updated skill folders across by hand.
