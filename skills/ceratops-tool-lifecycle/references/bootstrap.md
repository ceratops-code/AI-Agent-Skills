# Bootstrap Action

## Goal

Install the first manager using the same engine as its CLI and MCP interfaces.

## Workflow

1. Require first-install authorization and an active AI-Agent-Skills source
   checkout. From that checkout run `python scripts/bootstrap-tool-manager.py`.
   This provisions the pinned runtime and dependencies under the fixed tool
   root, packages the first release, and stages and validates its installation.
2. Inspect the manager with
   `C:\AI-Agents-Tools\bin\ceratops-tool-manager.cmd versions`.
3. When registration is requested, register only this stdio service in the
   intended coding agent's Codex configuration. Use the fixed runtime Python
   with `-I -B`, the installed `bin/ceratops-tool-manager.py` launcher, and
   `--mcp`; set the tool allowlist to `install`, `update`, and `versions`.
   Verify the restricted Forms agent cannot inherit this service before
   enabling any shared registration. Do not restart the desktop app.
4. Verify tools through a real local MCP connection. Report whether the active
   Codex task has reconnected and exposes them; a CLI test alone is
   insufficient.

## Completion Gate

The first installation passed readiness. Any requested registration is scoped
and verified, or is reported blocked with the installed CLI still available.

## Output Contract

Report installed version, callable MCP availability, and required reconnection.
