<div align="center">

# 羅針盤 / Rashinban

### A compass for autonomous agent goals — turn a rough request into a linted, verifiable `/goal`.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Based on goal-setter](https://img.shields.io/badge/based%20on-goal--setter%20by%20gotalab-black.svg)](https://github.com/gotalab/goal-setter-skill)
[![Every agent](https://img.shields.io/badge/Codex%20%7C%20Claude%20%7C%20Grok%20%7C%20OpenAI%20%7C%20Gemini-black.svg)](skills/rashinban/adapters/ROUTING.md)

日本語版は [README.ja.md](README.ja.md)

</div>

> **Attribution.** Rashinban is a **harness-engineered derivative** of
> [goal-setter-skill](https://github.com/gotalab/goal-setter-skill) by **gotalab**,
> under its original **MIT License**. The goal-contract spec is gotalab's;
> Rashinban adds a deterministic harness around it. See [NOTICE.md](NOTICE.md).

---

## What it is

A **meta-skill**: it does not implement your task — it turns a rough request into
a compact `/goal` that states the outcome, how Done is verified, what must not
break, and when to stop, so an AI agent (Codex, Claude Code, Grok, OpenAI,
Gemini…) can run **until a verifiable outcome is true**.

Upstream goal-setter is essentially one very good prompt. **Rashinban wraps it in
a harness:**

| Added | What it does |
|---|---|
| `scripts/goal_lint.py` | Quality gate — checks the contract *elements* (objective / evidence / Done / validation / constraints / block), flags vague "better/works" and task-list-as-Done, scores 0-100, and enforces the real 4,000-char runtime cap (Codex codepoints + Claude Code UTF-16). |
| `bin/rashinban` | Host-aware CLI — `lint`, `host`, `activate` (emits the `/goal` line + runtime-correct guidance), `bridge`, `selfcheck`. |
| `scripts/goal_seek_bridge.py` | Drops the goal into AKATSUKI `plans-store` (`rashinban-inbox.jsonl`, non-destructive) for goal-seek. |
| `references/` | `templates.md` (ready `/goal` skeletons), `validation-playbooks.md` (per-domain "verified" means), `adapters/ROUTING.md` (cross-runtime activation). |
| `tests/smoke.sh` | Offline assertions: good goal passes, weak goal is flagged, over-cap fails. |

## Quickstart

```bash
python3 skills/rashinban/scripts/goal_lint.py my-goal.md      # lint a drafted /goal
python3 skills/rashinban/bin/rashinban activate my-goal.md    # lint + emit the /goal line
python3 skills/rashinban/bin/rashinban selfcheck
sh tests/smoke.sh
```

Lint output names missing core elements and weak phrasing, and scores the draft.
A good score is not a good Goal by itself — it means the contract is *well-formed*.

## How activation works (it rides the runtime, no scheduler)

| Runtime | Activation |
|---|---|
| **Codex**, no worker tools | native goal tool may set it |
| **Codex**, needs `spawn_agent`/`create_thread` | **you** send the `/goal` line — that is what authorizes those tools |
| **Claude Code** | send the `/goal` line; can fan out as a dynamic workflow |
| **Grok / OpenAI / Gemini / Cursor** | send the `/goal` line; keep run/stop rules in the contract |

Details: [skills/rashinban/adapters/ROUTING.md](skills/rashinban/adapters/ROUTING.md).

## The contract Rashinban writes

Objective (one verifiable end state) · Evidence/verification · Core flow &
pass-fail checks · Read-first anchors · Constraints & boundaries · Validation
(per-domain) · Done (pass/fail, evidence-bounded, risk-matched review) · Run
rules · Block/stop · Final report. Full spec: [skills/rashinban/SKILL.md](skills/rashinban/SKILL.md).

## License & credit

MIT — see [LICENSE](LICENSE) (Copyright gotalab). Rashinban is an independent
derivative and is **not affiliated with or endorsed by** gotalab. For the
canonical goal-setter, use the [upstream repo](https://github.com/gotalab/goal-setter-skill).
