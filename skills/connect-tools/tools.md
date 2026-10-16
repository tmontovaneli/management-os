# How to connect each tool

Last checked against the official docs: **2026-10-16**. These commands change. If one
fails, open the official link for that tool, follow what it says now, and update this file.

General rules:
- Prefer OAuth (browser sign-in) over API tokens. Never write a token into the workspace:
  it's a git repository.
- Add MCP servers with `--scope local` while in the workspace folder. Local scope keeps
  the config in `~/.claude.json`, outside the repository, and only for this workspace.
- After adding an MCP server, its tools only appear in a **new** Claude Code session.
  OAuth sign-in happens inside Claude Code with `/mcp`.
- Many companies require an admin to approve these connections. If sign-in is blocked,
  that's usually why: the user needs to ask their admin. Don't look for workarounds.

## Jira (Atlassian Cloud)

- **Method:** Atlassian Rovo MCP server (official, OAuth).
- **Command** (the user runs it in a terminal from the workspace folder, or with `!` inside Claude Code):
  `claude mcp add --transport http --scope local atlassian https://mcp.atlassian.com/v2/mcp`
- **Then:** start a new Claude Code session, run `/mcp`, choose `atlassian`, and sign in.
- **Admin:** an Atlassian site admin may need to complete the first consent.
- **Detect:** `claude mcp list` shows `atlassian … ✔ Connected`, and Jira tools are available
  (names contain `atlassian` and `jira`, e.g. issue search with JQL).
- **Official docs:** https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
- **Jira Server / Data Center:** not covered by the Rovo server. Say so and stop. A
  community server could work, but that's the user's call to make with their admin.

## Slack

- **Method:** Slack MCP server (official, OAuth).
- **Option A, inside Claude Code:** `/plugin install slack@claude-plugins-official`, then follow the sign-in prompt.
- **Option B, in a terminal:** `claude mcp add --transport http --scope local slack https://mcp.slack.com/mcp`,
  then start a new session, run `/mcp`, choose `slack`, and sign in.
- **Admin:** the workspace admin must allow the MCP integration.
- **Detect:** `claude mcp list` shows `slack … ✔ Connected`, and Slack search/read tools are available.
- **Official docs:** https://docs.slack.dev/ai/slack-mcp-server/connect-to-harnesses

## Gmail and Google Calendar (Google Workspace)

- **Method:** Claude connectors. They're set up once on claude.ai and appear in Claude Code
  when it's signed in with the same claude.ai account (as `claude.ai Gmail` and `claude.ai Google Calendar`).
- **Steps:** on claude.ai, open Settings → Connectors, connect Gmail and Google Calendar,
  and sign in with the **work** Google account. Then start a new Claude Code session.
- **Admin:** on Team and Enterprise plans an owner must enable the connectors first.
  The Google Workspace admin may also need to allow Claude.
- **Detect:** `claude mcp list` shows entries starting with `claude.ai` for Gmail and
  Google Calendar, and their tools are available.
- **Official docs:** https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
- **Note:** if Claude Code is signed in with an API key instead of a claude.ai account,
  connectors don't appear. The user would need a Google MCP server instead. Explain this and
  let them decide.

## GitHub

- **Method:** GitHub CLI `gh` (recommended: simple, read commands are predictable).
  - Install: `brew install gh` on macOS; other systems: https://cli.github.com
  - Sign in: `gh auth login` (choose GitHub.com, HTTPS, and sign in with a browser). If the org uses SSO,
    approve the org during sign-in.
  - **Detect:** `gh auth status` shows the account as logged in.
- **Alternative:** the GitHub MCP server:
  `claude mcp add --transport http --scope local github https://api.githubcopilot.com/mcp/`,
  then `/mcp` to sign in. Use it if the user can't install `gh`.
- **Official docs:** https://cli.github.com/manual/gh_auth_login and https://github.com/github/github-mcp-server

## Not supported yet

Microsoft 365 (Outlook mail and calendar), GitLab, Bitbucket, Linear, Teams. The config
format allows them (`provider`), but morning-pulse has no instructions for them yet.
Tell the user, and suggest they add a section here and in morning-pulse if they want one.
