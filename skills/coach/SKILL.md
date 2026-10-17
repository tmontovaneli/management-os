---
name: coach
description: Switches between Coach mode (the AI challenges the user's inputs and connects them with the workspace's context, so they go the extra mile) and Assist mode (low cognitive load, for tired days). Use when the user says "coach mode", "assist mode", "no coaching", "I'm tired", "go easy on me", "challenge me", "coach me on this", or asks how much the AI challenges them. Also use when the user asks for a review of a plan, note or report they've written.
---

# Coach

Controls how much the AI in this workspace challenges the user. The coaching behaviour itself, its
levels and limits, are in [coaching.md](coaching.md): read it first. All paths are relative to the
workspace root.

## Change the level

Work out from the user's words how long the change should last, and confirm it in one line:

| The user says something like | Do this |
|---|---|
| "assist mode", "I'm tired", "go easy on me", "no coaching" | Assist mode **for this conversation**. Then ask once: "Just today, this week, or from now on?" |
| "coach me on this", "challenge me", "be tough" | Coaching on **for this conversation** (or this task), whatever the setting |
| "assist mode this week", "coaching back on this week" | Write or update `Coaching this week: off` (or `always` / `rituals`) at the top of this week's file in `my_performance/weeks/`, right after the "Month:" and "Sprint:" lines. Remove the line to go back to the setting |
| "from now on", "always", "only for rituals", "turn coaching off" | Change `coaching` in `.management_os.json` to `always`, `rituals` or `off`. Keep the rest of the file as it is |

If the user is unsure, explain the three levels from coaching.md in three lines and recommend:
`always` when they have energy, `rituals` for busy weeks, `off` for tired days or leave.

## Show the level

When the user asks how coaching is set, answer in one or two lines: the level in effect now and
where it comes from (this conversation, this week's file, or the setting).

## "Coach me on this"

When the user asks for coaching on something specific (a plan, a note, a report, an email draft):

1. Read what it is, and find the related context in the workspace: the person's notes, the initiative,
   the sprint file, the month's intentions, the last week files.
2. Give at most three challenges, following "How to coach" in coaching.md, then the one extra-mile move
   you'd make first.
3. Offer to make the changes the user picks. Change nothing they didn't pick.
