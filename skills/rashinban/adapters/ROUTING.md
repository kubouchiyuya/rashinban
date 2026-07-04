# Cross-runtime activation (Rashinban)

A `/goal` is **portable plain text**: a self-contained contract (outcome,
evidence, constraints, stop condition) that any capable agent can execute.
Rashinban writes and lints it, detects the host, and tells you exactly how to
activate it there. It never implements a scheduler — it rides each runtime's
native mechanism, and falls back to "send the `/goal` line" everywhere else.

`bin/rashinban activate <file>` prints the right guidance for the detected host.

## Runtime matrix

| Runtime | Native goal tool | How to activate | Worker/parallel tools |
|---|---|---|---|
| **Codex** (CLI / cloud) | `create_goal` / `get_goal` | set via the native tool **only if** the goal does not need worker tools; check `get_goal` first and reuse a matching active goal | `spawn_agent` / `create_thread` |
| **Codex** needing `spawn_agent`/`create_thread` | — | **emit the `/goal …` line for the USER to send** — sending it is what authorizes those tools; an auto-set goal runs fully in the main thread | user-gated |
| **Claude Code** | `/goal` line | send the `/goal` line; decomposition can be realized as a dynamic workflow (read-only stages → subagents) | dynamic workflow / subagents |
| **Grok** · **Grok Build** (xAI) | — | send the `/goal` line as the task; keep run/stop + evidence rules inside the contract | n/a |
| **Gemini CLI** | — | send the `/goal` line | n/a |
| **Google Antigravity** | agent manager | paste the `/goal` as the task brief for the agent(s); the contract's Done/evidence drives the run | agent manager |
| **Cursor** · **Windsurf** · **Aider** | — | paste the `/goal` as the task; keep the contract self-contained | n/a |
| **GLM** (Zhipu) · **DeepSeek** CLIs | — | send the `/goal` line | n/a |
| **Hermes** (agent router) | ingress queue | enqueue the `/goal` as the objective; the router dispatches to a worker that runs it to Done | router |
| **OpenClaw** (agent runtime) | run objective | set the `/goal` as the run objective; keep the block/stop rules as the runtime's halt condition | runtime workers |
| **Anything else** that follows instructions | — | give it the `/goal` line verbatim — that is the whole contract | n/a |

## Two rules that make it portable

1. **The contract is the interface.** Because the `/goal` states outcome +
   evidence + constraints + stop condition in plain prose, a runtime does not
   need a special "goal" feature to honor it — it needs only to follow
   instructions and check evidence. That is why the same `/goal` works on a
   native-goal runtime and on a bare chat CLI.
2. **Native tools are an optimization, not a requirement.** Where a runtime has
   a real goal/parallel mechanism (Codex, Claude Code, Hermes, OpenClaw), use
   it. Everywhere else, the `/goal` line executed directly gives the same
   outcome, just without the runtime's built-in orchestration.

## The Codex linchpin (only where it applies)

`spawn_agent` and `create_thread` are gated to explicit user requests. A
tool-set goal describes the work, but the **user-sent** `/goal` line is what
authorizes those tools — even when a subagent is only used for final
verification. Never auto-set such a goal; never claim it was set unless it was.
This applies to Codex; other runtimes use their own worker mechanism or run the
contract serially.

## AKATSUKI bridge

Inside an AKATSUKI project, `rashinban bridge <file> --title "…"` drops the goal
into `.claude/state/plans-store/rashinban-inbox.jsonl` (non-destructive) for
`goal-seek` / Hermes to ingest. The plans-store SoT (`index.json`) is never
edited directly.
