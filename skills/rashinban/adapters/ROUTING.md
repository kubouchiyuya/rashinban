# Cross-runtime activation (Rashinban)

Rashinban writes goal text; it rides each runtime's native goal/parallel
mechanism (it does not implement a scheduler). `bin/rashinban activate` detects
the host and prints the right guidance. Summary:

| Runtime | How to activate | Worker tools |
|---|---|---|
| **Codex** (no worker tools) | may be set via the native goal tool (`create_goal`; check `get_goal` first) | — |
| **Codex** (needs `spawn_agent`/`create_thread`) | **emit the `/goal …` line for the USER to send** — sending it is what authorizes those tools | user-gated |
| **Claude Code** | send the `/goal …` line; can realize decomposition as a dynamic workflow (read-only stages → subagents) | dynamic workflow |
| **OpenAI** (Codex CLI / API agents) | no separate goal tool assumed — send the `/goal` line; keep run/stop rules in the contract | via Codex |
| **Grok** (xAI) | send the `/goal` line; keep run/stop + evidence rules in the contract | n/a |
| **Gemini CLI** | send the `/goal` line | n/a |
| **Cursor / Aider / others** | paste the `/goal` line as the task; keep the contract self-contained | n/a |

## The Codex linchpin
`spawn_agent` and `create_thread` are gated to explicit user requests. A
tool-set goal can describe the work, but the **user-sent** `/goal …` line is what
authorizes those tools — even when a subagent is only used for final
verification. Never auto-set such a goal; never claim it was set unless it was.

## AKATSUKI bridge
Inside an AKATSUKI project, `rashinban bridge <file> --title "…"` drops the goal
into `.claude/state/plans-store/rashinban-inbox.jsonl` (non-destructive) for
`goal-seek` to ingest. The plans-store SoT (`index.json`) is never edited
directly.

Based on goal-setter-skill by gotalab (MIT).
