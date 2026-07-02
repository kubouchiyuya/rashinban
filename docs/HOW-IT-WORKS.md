# How Rashinban works

Rashinban has two halves: **the contract spec** (what a good `/goal` contains —
gotalab's goal-setter, preserved in `skills/rashinban/SKILL.md`) and **the
harness** (tooling that checks and activates it — added by Rashinban).

## The contract a `/goal` should carry

Written as plain prose, no labeled fields. Rashinban's `SKILL.md` is the full
spec; the essentials:

| Element | What it pins |
|---|---|
| **Objective** | one verifiable end state ("X does Y, verified by Z" — never "improve X") |
| **Evidence / verification** | where Done is checked: command output, screenshot, benchmark, artifact, sourced comparison |
| **Core flow / pass-fail** | for real systems: the smallest complete path from input through real layers to output — not a mock |
| **Read first** | 1-2 anchor files, then "discover as needed" |
| **Constraints / boundaries** | the scope rule + the 1-3 things this task could actually break |
| **Validation** | the real command/check, concrete by domain |
| **Done** | pass/fail, evidence-bounded, with a review tier matched to risk |
| **Block** | when to stop instead of thrashing |
| **Final report** | outcome first, plain words, written for someone who watched none of the run |

## The harness

### 1. `goal_lint.py` — the quality gate

Beyond the upstream length check, it inspects the *elements* above (heuristically
— a `/goal` is prose, so this is guidance, not a hard structural pass), flags
weak phrasing, and scores 0-100.

- **Core elements** (objective, evidence, Done) missing → strong penalty + named.
- **Vague success terms** ("better", "works", "nice") with no concrete check → warning.
- **Task-list-as-Done** ("build X, add Y, …") with no Done/evidence → warning.
- **Length** → the only *hard* failure. Both runtimes cap at 4,000, but count
  differently: Codex counts Unicode codepoints, Claude Code counts UTF-16 code
  units (emoji/rare CJK = 2). Lint reports both and fails on the stricter one.

> A high score means the contract is *well-formed*, not that the goal is *good*.
> Judgment still yours.

### 2. `bin/rashinban` — host-aware activation

`activate` lints, then emits the `/goal …` line plus guidance for the detected
runtime. It never claims to have "set" a goal — setting is the runtime's job.

### 3. `goal_seek_bridge.py` — AKATSUKI integration

Drops the goal into `plans-store/rashinban-inbox.jsonl`. It **never edits the
SoT `index.json`** (that's owned by goal-seek/supervisor) — the inbox is a safe,
reversible hand-off.

## Activation, per runtime (no scheduler — it rides the runtime)

| Runtime | Activation |
|---|---|
| **Codex**, no worker tools | native goal tool may set it |
| **Codex**, needs `spawn_agent`/`create_thread` | **you** send the `/goal` line — sending it is what authorizes those tools |
| **Claude Code** | send the `/goal` line; decomposition can become a dynamic workflow |
| **Grok / OpenAI / Gemini / Cursor** | send the `/goal` line; keep run/stop rules in the contract |

**The Codex linchpin:** `spawn_agent`/`create_thread` are gated to explicit user
requests. An auto-set goal runs fully in the main thread; only a *user-sent*
`/goal` line authorizes those tools — even when a subagent is only for final
verification.

## Honest limits

- **The lint is heuristic.** A `/goal` is prose with no fixed schema, so element
  detection is signal-based guidance. Length is the only hard gate.
- **A good score is not a good goal.** It means well-formed, not correct.
- **Rashinban writes and checks goals; it does not run your task or schedule
  anything** — it rides each runtime's native mechanism, exactly like upstream
  goal-setter.
