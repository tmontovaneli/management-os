#!/usr/bin/env python3
"""
Collect activity metrics for each direct report over a period, and write them to
team_performance/metrics/<from>_<to>.md.

GitHub numbers come from the GitHub CLI (`gh`), which must be signed in. Jira numbers are
collected by the team-metrics skill through the Jira connection and passed in as a JSON file:
    {"João Silva": {"created": 4, "closed": 7, "in_progress": 2}, ...}

Usage (from the workspace root):
    python3 skills/team-metrics/collect_metrics.py --from 2026-09-01 --to 2026-09-30
    python3 skills/team-metrics/collect_metrics.py --from 2026-10-12 --to 2026-10-23 --label "Sprint 42" \
        --jira-counts /tmp/jira.json
    python3 skills/team-metrics/collect_metrics.py ... --no-github     # Jira only
    python3 skills/team-metrics/collect_metrics.py ... --print         # show it, don't write it

Standard library only, Python 3.8+.
"""

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SEARCH_PAUSE = 2.2  # seconds between search calls: GitHub allows 30 searches a minute
ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$")
COLUMNS = [
    ("jira", "created", "Tickets created"),
    ("jira", "closed", "Tickets closed"),
    ("jira", "in_progress", "Tickets in progress"),
    ("github", "commits", "Commits"),
    ("github", "prs_created", "PRs created"),
    ("github", "prs_merged", "PRs merged"),
    ("github", "prs_reviewed", "PRs reviewed"),
    ("github", "pr_comments", "PR comments"),
]


# --------------------------------------------------------------------------- #
# Workspace
# --------------------------------------------------------------------------- #

def default_root():
    here = Path(__file__).resolve().parent
    for candidate in (Path.cwd(), here.parent.parent):
        if (candidate / ".management_os.json").is_file():
            return candidate
    return Path.cwd()


def read_people(root):
    """[{name, github}] from direct_reports/*/notes.md."""
    people = []
    folder = root / "direct_reports"
    if not folder.is_dir():
        return people
    for person in sorted(p for p in folder.iterdir() if p.is_dir() and p.name != "template"):
        notes = person / "notes.md"
        if not notes.is_file():
            continue
        name, github = None, ""
        for line in notes.read_text(encoding="utf-8").splitlines():
            if name is None and line.startswith("# "):
                name = line[2:].strip()
            match = ROW.match(line)
            if match and match.group(1).lower() == "github":
                github = match.group(2).strip().lstrip("@").strip("`")
        people.append({"name": name or person.name.replace("_", " ").title(), "github": github})
    return people


def read_config(root):
    path = root / ".management_os.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


# --------------------------------------------------------------------------- #
# GitHub
# --------------------------------------------------------------------------- #

class GitHub:
    def __init__(self, scope):
        self.scope = scope
        self.last_search = 0.0

    def api(self, path, params=None):
        args = ["gh", "api", "-X", "GET", path]
        for key, value in (params or {}).items():
            args += ["-f", "{}={}".format(key, value)]
        for attempt in range(3):
            result = subprocess.run(args, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout or "null")
            error = (result.stderr or result.stdout).strip()
            if "rate limit" in error.lower() and attempt < 2:
                print("  GitHub rate limit reached, waiting 60 seconds…", file=sys.stderr)
                time.sleep(60)
                continue
            raise SystemExit("gh api {} failed: {}".format(path, error))

    def search(self, query, per_page=100, max_pages=10, kind="issues"):
        """Yield search results (GitHub returns at most 1,000). kind is "issues" (PRs) or "commits"."""
        for page in range(1, max_pages + 1):
            wait = SEARCH_PAUSE - (time.time() - self.last_search)
            if wait > 0:
                time.sleep(wait)
            self.last_search = time.time()
            data = self.api("search/" + kind, {"q": "{} {}".format(query, self.scope),
                                              "per_page": per_page, "page": page})
            if per_page == 1:
                yield data.get("total_count", 0)
                return
            items = data.get("items", [])
            yield from items
            if len(items) < per_page:
                return

    def count(self, query, kind="issues"):
        return next(self.search(query, per_page=1, kind=kind))

    def pages(self, path):
        page = 1
        while True:
            items = self.api(path, {"per_page": 100, "page": page}) or []
            yield from items
            if len(items) < 100:
                return
            page += 1


def in_period(timestamp, start, end):
    if not timestamp:
        return False
    day = dt.date.fromisoformat(timestamp[:10])  # GitHub timestamps are UTC
    return start <= day <= end


def github_counts(gh, login, start, end):
    period = "{}..{}".format(start.isoformat(), end.isoformat())
    counts = {
        # Commit search only covers each repo's default branch.
        "commits": gh.count("author:{} author-date:{}".format(login, period), kind="commits"),
        "prs_created": gh.count("is:pr author:{} created:{}".format(login, period)),
        "prs_merged": gh.count("is:pr is:merged author:{} merged:{}".format(login, period)),
    }
    # Search can't filter reviews or comments by date, so find PRs by others that the
    # person reviewed or commented on and that changed since the start, then check each one.
    since = "updated:>={}".format(start.isoformat())
    candidates = {}
    for qualifier in ("reviewed-by", "commenter"):
        for item in gh.search("is:pr {}:{} -author:{} {}".format(qualifier, login, login, since)):
            repo = item["repository_url"].split("/repos/", 1)[1]
            candidates[(repo, item["number"])] = True

    reviewed = comments = 0
    for repo, number in candidates:
        reviews = [r for r in gh.pages("repos/{}/pulls/{}/reviews".format(repo, number))
                   if (r.get("user") or {}).get("login", "").lower() == login.lower()
                   and r.get("state") != "PENDING" and in_period(r.get("submitted_at"), start, end)]
        if reviews:
            reviewed += 1
        for path in ("repos/{}/pulls/{}/comments".format(repo, number),
                     "repos/{}/issues/{}/comments".format(repo, number)):
            comments += sum(1 for c in gh.pages(path)
                            if (c.get("user") or {}).get("login", "").lower() == login.lower()
                            and in_period(c.get("created_at"), start, end))
    counts["prs_reviewed"] = reviewed
    counts["pr_comments"] = comments
    return counts


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #

def date_range(first, last):
    if first.year != last.year:
        return "{} {} {} – {} {} {}".format(first.day, first.strftime("%B"), first.year,
                                            last.day, last.strftime("%B"), last.year)
    if first.month != last.month:
        return "{} {} – {} {} {}".format(first.day, first.strftime("%B"), last.day, last.strftime("%B"), last.year)
    return "{}–{} {} {}".format(first.day, last.day, last.strftime("%B"), last.year)


def render(start, end, label, sources, rows, missing, jira_project):
    title = "# Team metrics · {}".format(label or date_range(start, end))
    out = [title, "",
           "- **Period:** {} → {}{}".format(start.isoformat(), end.isoformat(),
                                             " ({})".format(date_range(start, end)) if label else ""),
           "- **Collected:** {}".format(dt.date.today().isoformat()),
           "- **Sources:** {}".format(" · ".join(sources) or "none"), ""]
    out += ["| Person | " + " | ".join(header for _, _, header in COLUMNS) + " |",
            "|---|" + "---:|" * len(COLUMNS)]
    totals = {key: None for _, key, _ in COLUMNS}
    for name, values in rows:
        cells = []
        for _, key, _ in COLUMNS:
            value = values.get(key)
            cells.append("—" if value is None else str(value))
            if value is not None:
                totals[key] = (totals[key] or 0) + value
        out.append("| {} | {} |".format(name, " | ".join(cells)))
    out.append("| **Team** | {} |".format(" | ".join(
        "—" if totals[key] is None else "**{}**".format(totals[key]) for _, key, _ in COLUMNS)))
    out += ["", "— means not collected."]
    if missing:
        out += ["Not collected: " + "; ".join(missing) + "."]
    project = jira_project or "the team's project"
    out += ["",
            "## Context",
            "<!-- What the numbers don't show: leave, on-call, onboarding, incidents, design work,",
            "     mentoring, pairing. Write it before you share or discuss these numbers. -->",
            "-",
            "",
            "## How these are counted",
            "- **Tickets created:** Jira issues in {} they reported, created in the period.".format(project),
            "- **Tickets closed:** issues assigned to them that reached Done in the period.",
            "- **Tickets in progress:** issues assigned to them and in progress at the end of the period.",
            "- **Commits:** commits they authored in the period on each repo's default branch (GitHub only "
            "searches default branches). With squash merges, one merged PR is one commit.",
            "- **PRs created / merged:** pull requests they opened / that were merged in the period.",
            "- **PRs reviewed:** pull requests by others where they submitted a review in the period.",
            "- **PR comments:** comments they wrote on others' pull requests in the period (conversation and "
            "inline review comments).",
            "- Dates are UTC. These are activity signals, not a measure of performance: compare a person with "
            "their own earlier periods, not with each other.",
            ""]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def parse_date(text, flag):
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        raise SystemExit("{} must be a date like 2026-09-01.".format(flag))


def main():
    parser = argparse.ArgumentParser(description="Collect activity metrics for each direct report.")
    parser.add_argument("--from", dest="start", required=True, metavar="YYYY-MM-DD")
    parser.add_argument("--to", dest="end", required=True, metavar="YYYY-MM-DD")
    parser.add_argument("--label", help='a name for the period, e.g. "Sprint 42" or "September 2026"')
    parser.add_argument("--jira-counts", type=Path, metavar="FILE",
                        help='JSON: {"<name>": {"created": n, "closed": n, "in_progress": n}}')
    parser.add_argument("--no-github", action="store_true", help="skip GitHub")
    parser.add_argument("--root", type=Path, help="workspace root (default: auto-detected)")
    parser.add_argument("--force", action="store_true", help="replace the file if it exists")
    parser.add_argument("--print", dest="print_only", action="store_true", help="print instead of writing")
    args = parser.parse_args()

    start, end = parse_date(args.start, "--from"), parse_date(args.end, "--to")
    if end < start:
        raise SystemExit("--to is before --from.")
    root = (args.root or default_root()).resolve()
    config = read_config(root)
    integrations = config.get("integrations") or {}
    people = read_people(root)
    if not people:
        raise SystemExit("No direct reports found in direct_reports/.")

    target = root / "team_performance" / "metrics" / "{}_{}.md".format(start.isoformat(), end.isoformat())
    if target.exists() and not (args.force or args.print_only):
        raise SystemExit("{} already exists. Use --force to replace it.".format(target.relative_to(root)))

    rows = {p["name"]: {} for p in people}
    missing, sources = [], []

    jira = integrations.get("jira") or {}
    if args.jira_counts:
        counts = json.loads(args.jira_counts.read_text(encoding="utf-8"))
        unknown = sorted(set(counts) - set(rows))
        if unknown:
            raise SystemExit("--jira-counts has names that aren't direct reports: {}".format(", ".join(unknown)))
        for name, values in counts.items():
            rows[name].update({k: values[k] for k in ("created", "closed", "in_progress") if values.get(k) is not None})
        sources.append("Jira project {}".format(jira.get("project") or "?"))
        no_jira = [name for name in rows if name not in counts]
        if no_jira:
            missing.append("Jira for " + ", ".join(no_jira))

    code = integrations.get("code") or {}
    if not args.no_github:
        if not shutil.which("gh"):
            raise SystemExit("The GitHub CLI (gh) isn't installed. Run /connect-tools github, or use --no-github.")
        repos = code.get("repos") or []
        if repos:
            scope = " ".join("repo:" + r for r in repos)
        elif code.get("org"):
            scope = "org:" + code["org"]
        else:
            raise SystemExit("No GitHub org in .management_os.json. Run /connect-tools github, or use --no-github.")
        gh = GitHub(scope)
        sources.append("GitHub " + (", ".join(repos) if repos else "org " + code["org"] + " (all repos)"))
        for person in people:
            if not person["github"]:
                missing.append("GitHub for {} (no username in their notes)".format(person["name"]))
                continue
            print("  GitHub: {} (@{})…".format(person["name"], person["github"]), file=sys.stderr)
            rows[person["name"]].update(github_counts(gh, person["github"], start, end))

    content = render(start, end, args.label, sources, list(rows.items()), missing, jira.get("project"))
    if args.print_only:
        print(content)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print("Wrote {}".format(target.relative_to(root)))
    print("Period: {} → {} · people: {} · sources: {}".format(
        start.isoformat(), end.isoformat(), len(people), " · ".join(sources) or "none"))
    if missing:
        print("Not collected: " + "; ".join(missing))


if __name__ == "__main__":
    main()
