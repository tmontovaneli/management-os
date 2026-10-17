---
name: first-90-days
description: Plans and guides a leader's first 90 days in a new role, using the ideas of The First 90 Days (Michael D. Watkins). Creates my_performance/first-90-days/plan.md, prepares listening-tour conversations and records what was learned, and runs checkpoint reviews at days 30, 60 and 90. Use when the user is starting (or about to start) a new management role, a promotion or a new team, asks for a 30-60-90 day plan for themselves, wants to prepare a first meeting with someone, or asks how their first months are going.
---

# First 90 days

Helps the user through their own transition into a new leadership role. The goal is to reach
the point where they add more value than they consume as early as possible, without the usual
transition traps. All paths are relative to the workspace root.

Read [framework.md](framework.md) before anything else: it summarises the book's ideas in our
own words. Don't quote or reproduce the book. If the user hasn't read it, recommend it once.

This skill is for the user's own transition. To plan a **new hire's** onboarding, use the
onboarding plan in the report-templates catalogue instead.

## Where things go

The plan is the hub; the details live where they already belong in the workspace:

| What | Where |
|---|---|
| The plan, phases, diagnosis, early wins, checkpoint reviews | `my_performance/first-90-days/plan.md` (from [plan-template.md](plan-template.md)) |
| The five conversations with the boss, in detail | `my_performance/manager-1on1-notes.md`, one dated entry each, titled e.g. "First 90 days · Expectations" |
| Listening-tour answers from a direct report | that person's `direct_reports/<name>/notes.md`, under "## First 90 days" |
| Team assessment of a direct report | the same section of their notes |
| Listening-tour answers and stance of a stakeholder | `stakeholders/<name>.md`, under "## First 90 days" (create the file from the template if needed) |

## Workflow 1: start the plan

1. If `my_performance/first-90-days/plan.md` exists, don't overwrite it: go to workflow 3
   (checkpoint) or ask what the user wants to update.
2. Ask in one batch (use a multiple-choice question tool if you have one):
   - **Day 1:** the start date (past or future). Read `role_start_date` from `.management_os.json` if it's there.
   - **Transition type:** new company, internal promotion, new team in the same company, or other.
   - **Situation:** offer the five STARS situations with one line each from framework.md, plus
     "a mix" and "not sure yet". If "a mix", ask which parts of the role are in which situation.
     If "not sure yet", record it as a hypothesis to confirm in the first 30 days.
   - **What the boss already said** about expectations, if anything.
3. Compute days 30, 60 and 90 with a command (calendar days: day N = day 1 + N − 1); don't
   work out dates in your head. Show them.
4. Create `my_performance/first-90-days/plan.md` from plan-template.md:
   - fill in the dates, role, transition type, boss (from `.management_os.json`)
   - fill the Situation table with what the user said, marked as a hypothesis until agreed with the boss
   - fill the listening tour with every direct report (from `direct_reports/*/notes.md`) and stakeholder
     (from `stakeholders/*.md`), plus the boss and peers the user names
   - adapt the phase goals to the situation: in a **turnaround** or **start-up**, move the first decisions
     and the first early win earlier; in a **realignment** or **sustaining success**, keep more of the
     first 30 days for learning and building the case for change
   - for a **promotion inside the same team**, add a "Preparing myself" note about changing the
     relationship with former peers
5. Suggest 2–3 learning-plan questions per area (technical, cultural, political), based on what's
   already in the workspace (initiatives, sprints, stakeholders). Write them after the user agrees.
6. Offer to prepare the first conversation with the boss (Situation and Expectations).
7. Close with what happens next: plan-week will show "Day N of 90" and pull one focus item from the
   current phase each week; ask for "first 90 days checkpoint" around days 30, 60 and 90.

## Workflow 2: listening-tour conversation

**Before** ("prepare my first 1:1 with Mia", "meeting with Priya tomorrow"):
- Read what the workspace knows about the person (notes or stakeholder file, initiatives they're on).
- Give the five diagnostic questions from framework.md, plus 2–3 tailored questions that test the
  current hypotheses in the plan. For a direct report, add: what they need from their manager, and
  how they like to work and get feedback.
- Remind the user the first meetings are for listening, not announcing changes.

**After** (the user shares notes or a summary):
- Write the answers under "## First 90 days" in the person's file, with the date. Keep the user's
  words; summarise, don't embellish.
- Tick them off in the plan's listening tour table.
- For a stakeholder, suggest a stance (supporter, persuadable, opponent) with the reason, and record
  it only when the user agrees.
- After every 3–4 conversations, update "Themes and hypotheses" in the plan: what keeps coming up,
  where people disagree, and what to test next. Say which conversations each theme came from.

## Workflow 3: checkpoint review (around days 30, 60 and 90, or any time)

1. Work out today's day number. Read the plan, the week files since day 1
   (`my_performance/weeks/`), `manager-1on1-notes.md`, and the "First 90 days" sections in people's files.
2. Review against the current phase: what's done, what's late, what's missing. Be specific and
   use evidence from the files.
3. Check for the common traps in framework.md, for example: no expectations conversation with the boss
   yet, listening tour skipped for peers, too many priorities, early wins that don't matter to the boss,
   learning only on the technical side. Name at most three, with what to do about each.
4. **Day 60:** make sure each direct report has an assessment against the criteria in framework.md,
   based on evidence. Draft from their notes when the user asks; the user decides. Never share or
   summarise assessments outside the person's notes and the plan's one-line summary.
5. **Day 90:** draft a review: what was learned, the agreed situation, early wins delivered, team and
   alignment changes, and the plan for the rest of the year. Offer to turn it into a report for the
   boss with the report-templates skill.
6. Append the review under "## Checkpoint reviews" in the plan (dated, 5–10 lines), after the user agrees.
7. Suggest the agenda for the next conversation with the boss.

## Coach mode

Follow [coaching.md](../coach/coaching.md) for the level in effect and how to challenge (at most
three challenges, after the work, each grounded in a file). In this skill, look for:
- **Diagnosis:** a situation (STARS) still marked as a hypothesis after day 30, or never agreed with the boss.
- **Listening tour:** key people not met by the end of the Learn phase; themes heard from several people that
  aren't in the plan yet.
- **Early wins:** wins that matter to the user but not to the boss or the team; no early win planned by day 60.
- **Traps:** the common transition traps in framework.md, linked to what the plan and notes show.

## Rules

- **Diagnose before prescribing.** Until the situation is agreed with the boss, present ideas as
  hypotheses, not conclusions.
- **People assessments are private.** They stay in the person's notes, are based on evidence, and
  are revisited. Don't infer them from personal traits or from what others gossip about.
- **The user decides.** Draft, suggest and challenge, but write into files only what the user accepted.
- **Use the user's situation, not generic advice.** Refer to their actual people, initiatives and notes.
