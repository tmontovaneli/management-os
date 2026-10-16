#!/usr/bin/env python3
"""
Create a weekly journal from manager-cadence.html.

Writes my_performance/weeks/YYYY-Www.md with:
  - the weekly cadence tasks, one per direct report where the task is per report
  - monthly and quarterly tasks not yet ticked off in an earlier week of the same month/quarter
  - unfinished items you added yourself last week (carried over)
  - one section per working day with the daily tasks, and a Friday review
  - sprint goal check-ins, final checks and the next sprint planning on their days, from the
    sprint files in team_performance/sprints/ (see the sprint-goals skill)

It also creates the month's journal (my_performance/journal-YYYY-MM.md) from the
template when it doesn't exist yet, and reports the month's intentions and whether
this is the first or last week of the month.

Usage (from the workspace root):
    python3 skills/plan-week/plan_week.py                  # this week Mon–Thu, next week Fri–Sun
    python3 skills/plan-week/plan_week.py --week next
    python3 skills/plan-week/plan_week.py --week current --whole-week
    python3 skills/plan-week/plan_week.py --week 2026-W43 --days-off 2026-10-21
    python3 skills/plan-week/plan_week.py --print          # show it, don't write it

Standard library only, Python 3.8+.
"""

import argparse
import datetime as dt
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

WORKDAYS = 5
PER_REPORT = re.compile(r"direct reports|per report|each report", re.I)
CHECKBOX = re.compile(r"^- \[( |x|X)\] (.+?)\s*$")
SPRINT_FIELD = re.compile(r"^- \*\*(Dates|Mid-sprint check-in|Final check):\*\*\s*(.*?)\s*$")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
SPRINT_TASKS = ("Sprint goals check-in", "Sprint goals final check", "Record sprint goals", "Send the sprint report")


# --------------------------------------------------------------------------- #
# Inputs
# --------------------------------------------------------------------------- #

class CadenceParser(HTMLParser):
    """Collects {frequency: [{"title", "desc"}]} from the cadence page's cards."""

    def __init__(self):
        super().__init__()
        self.items = {}
        self.freq = None
        self.field = None
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get("class") or "").split()
        if "section-label" in classes:
            self.field, self.buf = "label", ""
        elif self.freq and "card-title" in classes:
            self.field, self.buf = "title", ""
        elif self.freq and "card-desc" in classes:
            self.field, self.buf = "desc", ""

    def handle_data(self, data):
        if self.field:
            self.buf += data

    def handle_endtag(self, tag):
        if not self.field or tag not in ("span", "div"):
            return
        text = " ".join(self.buf.split())
        if self.field == "label":
            self.freq = text.lower()
            self.items.setdefault(self.freq, [])
        elif self.field == "title":
            self.items[self.freq].append({"title": text, "desc": ""})
        elif self.field == "desc" and self.items[self.freq]:
            self.items[self.freq][-1]["desc"] = text
        self.field = None


def read_cadence(root):
    path = root / "manager-cadence.html"
    if not path.is_file():
        raise SystemExit("Can't find {}. Run this from your Management OS workspace.".format(path))
    parser = CadenceParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.items.get("daily") and not parser.items.get("weekly"):
        raise SystemExit("No Daily or Weekly tasks found in manager-cadence.html.")
    return parser.items


def read_direct_reports(root):
    names = []
    folder = root / "direct_reports"
    if not folder.is_dir():
        return names
    for person in sorted(p for p in folder.iterdir() if p.is_dir() and p.name != "template"):
        notes = person / "notes.md"
        name = None
        if notes.is_file():
            for line in notes.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    name = line[2:].strip()
                    break
        names.append(name or person.name.replace("_", " ").title())
    return names


def expand(items, reports):
    """Cadence cards -> (key, description) tasks, one per report where the card is per report."""
    tasks = []
    for item in items:
        if reports and PER_REPORT.search(item["title"] + " " + item["desc"]):
            tasks += [("{} · {}".format(item["title"], name), "") for name in reports]
        else:
            tasks.append((item["title"], item["desc"]))
    return tasks


def read_sprints(root):
    """Sprints from team_performance/sprints/*.md that have valid dates, oldest first."""
    folder = root / "team_performance" / "sprints"
    sprints = []
    if not folder.is_dir():
        return sprints
    for path in folder.glob("*.md"):
        name, fields = None, {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if name is None and line.startswith("# "):
                name = line[2:].strip()
            match = SPRINT_FIELD.match(line)
            if match:
                fields[match.group(1)] = [dt.date.fromisoformat(d) for d in ISO_DATE.findall(match.group(2))
                                          if valid_date(d)]
        dates = fields.get("Dates", [])
        if len(dates) != 2:
            continue
        sprints.append({
            "name": name or path.stem, "file": path.name, "start": dates[0], "end": dates[1],
            "check_in": (fields.get("Mid-sprint check-in") or [None])[0],
            "final": (fields.get("Final check") or [None])[0],
        })
    return sorted(sprints, key=lambda sprint: sprint["start"])


def valid_date(text):
    try:
        dt.date.fromisoformat(text)
    except ValueError:
        return False
    return True


def next_working_day(day):
    day += dt.timedelta(days=1)
    while day.weekday() >= WORKDAYS:
        day += dt.timedelta(days=1)
    return day


def sprint_tasks(sprints):
    """{date: [task]} for check-ins, final checks, and planning of a sprint not recorded yet."""
    tasks = {}
    starts = {sprint["start"] for sprint in sprints}
    for sprint in sprints:
        if sprint["check_in"]:
            tasks.setdefault(sprint["check_in"], []).append("Sprint goals check-in · " + sprint["name"])
        if sprint["final"]:
            tasks.setdefault(sprint["final"], []).append("Sprint goals final check · " + sprint["name"])
        planning = next_working_day(sprint["end"])
        if planning not in starts:
            tasks.setdefault(planning, []).extend([
                "Record sprint goals · after sprint planning",
                "Send the sprint report · " + sprint["name"],
            ])
    return tasks


def is_sprint_task(key):
    return key.startswith(SPRINT_TASKS)


# --------------------------------------------------------------------------- #
# Weeks
# --------------------------------------------------------------------------- #

def resolve_week(spec, today):
    """Return (monday, label) for 'current', 'next', 'auto' or 'YYYY-Www'."""
    this_monday = today - dt.timedelta(days=today.weekday())
    if spec == "auto":
        spec = "current" if today.weekday() < 4 else "next"
    if spec == "current":
        return this_monday, "current"
    if spec == "next":
        return this_monday + dt.timedelta(days=7), "next"
    match = re.match(r"^(\d{4})-W(\d{1,2})$", spec)
    if not match:
        raise SystemExit("--week must be current, next, auto or YYYY-Www (e.g. 2026-W43).")
    year, week = int(match.group(1)), int(match.group(2))
    try:
        monday = dt.date.fromisocalendar(year, week, 1)
    except ValueError:
        raise SystemExit("{} isn't a valid ISO week.".format(spec))
    label = "current" if monday == this_monday else ("next" if monday == this_monday + dt.timedelta(days=7) else "other")
    return monday, label


def week_id(monday):
    year, week, _ = monday.isocalendar()
    return "{}-W{:02d}".format(year, week)


def anchor(monday):
    """The Thursday decides which month and quarter a week belongs to (ISO convention)."""
    return monday + dt.timedelta(days=3)


def month_key(monday):
    d = anchor(monday)
    return (d.year, d.month)


def quarter_key(monday):
    d = anchor(monday)
    return (d.year, (d.month - 1) // 3 + 1)


def parse_week_file(path):
    match = re.match(r"^(\d{4}-W\d{2})\.md$", path.name)
    if not match:
        return None
    try:
        monday, _ = resolve_week(match.group(1), dt.date.today())
    except SystemExit:
        return None
    return monday


def checkboxes(path):
    """Yield (done, key, full_text) for every checkbox line. The key is the text before ' — '."""
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CHECKBOX.match(line)
        if match:
            text = match.group(2)
            yield match.group(1).lower() == "x", text.split(" — ")[0].strip(), text


# --------------------------------------------------------------------------- #
# Monthly journal
# --------------------------------------------------------------------------- #

MONTH_FALLBACK = """# Journal — Month YYYY

## Intentions for the month
-

## Weeks
<!-- Daily tasks, wins/risks and Friday reviews live in my_performance/weeks/YYYY-Www.md. -->

## Month retro
- What process is slowing the team down?
- What debt is accumulating?
- One thing to fix next month:
"""


def month_journal_path(root, monday):
    year, month = month_key(monday)
    return root / "my_performance" / "journal-{}-{:02d}.md".format(year, month)


def month_journal_content(root, monday):
    template = root / "my_performance" / "template" / "journal-yyyy-mm.md"
    text = template.read_text(encoding="utf-8") if template.is_file() else MONTH_FALLBACK
    return text.replace("Month YYYY", anchor(monday).strftime("%B %Y"), 1)


def month_intentions(path):
    """Non-empty bullets under '## Intentions for the month'."""
    if not path.is_file():
        return []
    found, inside = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip().lower() == "## intentions for the month"
            continue
        item = re.sub(r"^\s*(?:[-*]|\d+\.)\s*", "", line).strip()
        if inside and item and not item.startswith("<!--") and re.match(r"^\s*(?:[-*]|\d+\.)", line):
            found.append(item)
    return found


def month_position(monday):
    """'first', 'last', 'only' or '' depending on where the week sits in its month."""
    week = dt.timedelta(days=7)
    first = month_key(monday - week) != month_key(monday)
    last = month_key(monday + week) != month_key(monday)
    return "only" if first and last else "first" if first else "last" if last else ""


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def date_range(first, last):
    if first.year != last.year:
        return "{} {} {} – {} {} {}".format(first.day, first.strftime("%B"), first.year,
                                            last.day, last.strftime("%B"), last.year)
    if first.month != last.month:
        return "{} {} – {} {} {}".format(first.day, first.strftime("%B"), last.day, last.strftime("%B"), last.year)
    return "{}–{} {} {}".format(first.day, last.day, last.strftime("%B"), last.year)


def task_lines(tasks):
    return ["- [ ] {}{}".format(key, " — " + desc if desc else "") for key, desc in tasks]


def short_day(day):
    return "{} {} {}".format(day.strftime("%a"), day.day, day.strftime("%b"))


def sprint_line(sprint):
    parts = ["Sprint: [{}](../../team_performance/sprints/{})".format(sprint["name"], sprint["file"]),
             date_range(sprint["start"], sprint["end"])]
    if sprint["check_in"]:
        parts.append("check-in " + short_day(sprint["check_in"]))
    if sprint["final"]:
        parts.append("final check " + short_day(sprint["final"]))
    return " · ".join(parts)


def render(monday, days, days_off, cadence, reports, carried, prev_id, month_open, quarter_open, month_file,
           sprints=(), day_tasks=None):
    friday = monday + dt.timedelta(days=WORKDAYS - 1)
    year, week, _ = monday.isocalendar()
    month_name = anchor(monday).strftime("%B")
    q = quarter_key(monday)[1]

    month_label = anchor(monday).strftime("%B %Y")
    out = ["# Week {} · {}".format(week, date_range(monday, friday)), "",
           "Month: [{}](../{})".format(month_label, month_file)]
    out += [sprint_line(sprint) for sprint in sprints] + [""]
    out += ["## Focus", "<!-- The three outcomes that would make this week a success. "
            "Each should serve one of the month's intentions. -->", "1.", "2.", "3.", ""]

    if carried:
        out += ["## Carried over from {}".format(prev_id)] + ["- [ ] " + text for text in carried] + [""]

    weekly = expand(cadence.get("weekly", []), reports)
    if weekly:
        out += ["## This week"] + task_lines(weekly) + [""]
    if month_open:
        out += ["## This month ({})".format(month_name),
                "<!-- Monthly cadence items not yet ticked off in an earlier week of {}. -->".format(month_name)]
        out += task_lines(month_open) + [""]
    if quarter_open:
        out += ["## This quarter (Q{})".format(q),
                "<!-- Quarterly cadence items not yet ticked off in an earlier week of Q{}. -->".format(q)]
        out += task_lines(quarter_open) + [""]

    daily = expand(cadence.get("daily", []), reports)
    for day in days:
        heading = "## {} {} {}".format(day.strftime("%A"), day.day, day.strftime("%B"))
        if day in days_off:
            out += [heading + " · day off", ""]
            continue
        out += [heading] + ["- [ ] " + key for key, _ in daily]
        out += ["- [ ] " + task for task in (day_tasks or {}).get(day, [])]
        out += ["", "**Win:** ", "**Risk:** ", "**Notes:** ", ""]

    out += ["## Friday review",
            "<!-- 30 min. What did you intend vs. what happened? Adjust next week's plan. -->",
            "- Intended:", "- Happened:", "- Next week:", ""]
    if month_position(monday) in ("last", "only"):
        out[-1:] = ["", "Last week of {}: write the month retro in [{}](../{}).".format(
            month_name, month_file, month_file), ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def default_root():
    here = Path(__file__).resolve().parent
    for candidate in (Path.cwd(), here.parent.parent):
        if (candidate / "manager-cadence.html").is_file():
            return candidate
    return Path.cwd()


def main():
    parser = argparse.ArgumentParser(description="Create a weekly journal from manager-cadence.html.")
    parser.add_argument("--week", default="auto",
                        help="current, next, auto (default: this week Mon–Thu, next week Fri–Sun) or YYYY-Www")
    parser.add_argument("--whole-week", action="store_true",
                        help="for the current week, include days that have already passed")
    parser.add_argument("--days-off", nargs="*", default=[], metavar="YYYY-MM-DD",
                        help="working days you're off; they're marked but get no tasks")
    parser.add_argument("--root", type=Path, help="workspace root (default: auto-detected)")
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="print the journal instead of writing it")
    args = parser.parse_args()

    root = (args.root or default_root()).resolve()
    today = dt.date.today()
    monday, label = resolve_week(args.week, today)
    friday = monday + dt.timedelta(days=WORKDAYS - 1)

    try:
        days_off = {dt.date.fromisoformat(d) for d in args.days_off}
    except ValueError as exc:
        raise SystemExit("--days-off: {}".format(exc))

    days = [monday + dt.timedelta(days=i) for i in range(WORKDAYS)]
    if label == "current" and not args.whole_week and today <= friday:
        days = [d for d in days if d >= today]

    cadence = read_cadence(root)
    reports = read_direct_reports(root)
    cadence_keys = {key for freq in cadence.values() for key, _ in expand(freq, reports)}

    weeks_dir = root / "my_performance" / "weeks"
    target = weeks_dir / "{}.md".format(week_id(monday))
    if target.exists() and not args.print_only:
        raise SystemExit("{} already exists. Nothing was changed.".format(target.relative_to(root)))

    earlier = []
    if weeks_dir.is_dir():
        for path in weeks_dir.glob("*.md"):
            other = parse_week_file(path)
            if other and other < monday:
                earlier.append((other, path))
    earlier.sort()

    done_month, done_quarter = set(), set()
    for other, path in earlier:
        for done, key, _ in checkboxes(path):
            if done and month_key(other) == month_key(monday):
                done_month.add(key)
            if done and quarter_key(other) == quarter_key(monday):
                done_quarter.add(key)

    month_open = [t for t in expand(cadence.get("monthly", []), reports) if t[0] not in done_month]
    quarter_open = [t for t in expand(cadence.get("quarterly", []), reports) if t[0] not in done_quarter]

    carried, prev_id = [], None
    if earlier:
        prev_monday, prev_path = earlier[-1]
        prev_id = week_id(prev_monday)
        carried = [text for done, key, text in checkboxes(prev_path)
                   if not done and key not in cadence_keys and not is_sprint_task(key)]

    all_sprints = read_sprints(root)
    sprints = [sp for sp in all_sprints if sp["start"] <= friday and sp["end"] >= monday]
    day_tasks = sprint_tasks(all_sprints)

    month_file = month_journal_path(root, monday)
    content = render(monday, days, days_off, cadence, reports, carried, prev_id, month_open, quarter_open,
                     month_file.name, sprints, day_tasks)

    if args.print_only:
        print(content)
        return

    weeks_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    month_status = "exists"
    if not month_file.exists():
        month_file.write_text(month_journal_content(root, monday), encoding="utf-8")
        month_status = "created"
    working = [d for d in days if d not in days_off]
    print("Created {}".format(target.relative_to(root)))
    print("Week: {} ({}), {}".format(week_id(monday), label, date_range(monday, friday)))
    print("Days: {}{}".format(", ".join("{} {}".format(d.strftime("%a"), d.day) for d in working) or "none",
                              " · off: " + ", ".join(sorted(d.isoformat() for d in days_off)) if days_off else ""))
    print("Weekly tasks: {} · this month: {} · this quarter: {} · carried over: {}{}".format(
        len(expand(cadence.get("weekly", []), reports)), len(month_open), len(quarter_open), len(carried),
        " (from {})".format(prev_id) if prev_id else ""))
    print("Direct reports: {}".format(", ".join(reports) or "none"))
    sprint_days = ["{} ({}{})".format(task, short_day(day), ", day off" if day in days_off else "")
                   for day, day_list in sorted(day_tasks.items()) if monday <= day <= friday for task in day_list]
    print("Sprint: {}".format("; ".join(sp["name"] for sp in sprints) or "none recorded for this week"))
    print("Sprint tasks: {}".format("; ".join(sprint_days) or "none"))
    intentions = month_intentions(month_file)
    position = month_position(monday)
    print("Monthly journal: {} ({})".format(month_file.relative_to(root), month_status))
    print("Month intentions: {}".format("; ".join(intentions) if intentions else "none yet"))
    print("Week in month: {}".format({"first": "first week of ", "last": "last week of ",
                                       "only": "first and last week of "}.get(position, "middle of ")
                                      + anchor(monday).strftime("%B")))


if __name__ == "__main__":
    main()
