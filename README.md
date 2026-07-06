<div align="center">

# 🧭 羅針盤 / Rashinban

**A compass for autonomous agent goals — turn a rough request into a linted, verifiable `/goal`.**

Because the one thing that decides a long agent run is whether *"done"* was ever
defined.

[![CI](https://github.com/kubouchiyuya/rashinban/actions/workflows/ci.yml/badge.svg)](https://github.com/kubouchiyuya/rashinban/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![deps](https://img.shields.io/badge/deps-zero%20(python%20stdlib)-black.svg)](#-quick-start)
[![Agents](https://img.shields.io/badge/Codex%20%7C%20Claude%20%7C%20Grok%20%7C%20OpenAI%20%7C%20Gemini-black.svg)](skills/rashinban/adapters/ROUTING.md)

[日本語](README.ja.md) · [中文](README.zh.md) · [Guide](docs/GUIDE.md) · [How it works](docs/HOW-IT-WORKS.md)

**If Rashinban helped you ship a verifiable goal, a ⭐ helps other agent builders find it.**

</div>

---

Tell an AI to *"make the app better"* and let it run, and it wanders — it polishes
the wrong thing, stops too early, or declares victory on a demo that doesn't work.
**Rashinban is the step that stops that.** It turns a rough request into a `/goal`:
a short contract stating the outcome, how it's verified, what must not break, and
when to stop — so an agent runs **until a verifiable result is true**, then reports
honestly.

```bash
python3 skills/rashinban/bin/rashinban activate my-goal.txt
#   lints the draft, then prints the /goal line + runtime-correct guidance
```

## ✨ Key capabilities

- **Lints a goal, doesn't just count characters.** `goal_lint.py` checks the
  contract *elements* (objective / evidence / Done / validation / constraints /
  stop), flags vague "better/works" and task-list-as-Done, and scores 0-100.
- **Runs on every runtime.** `rashinban activate` detects Codex, Claude Code,
  Grok / Grok Build, Gemini, Google Antigravity, Cursor, GLM, DeepSeek, Hermes,
  and OpenClaw — and any other capable agent runs the portable `/goal` directly.
- **Bridges into goal-seek.** Inside AKATSUKI, `rashinban bridge` files the goal
  into `plans-store` — non-destructively (the SoT is never edited directly).
- **Enforces the real length cap.** 4,000 chars, counted the way each runtime
  actually counts (Codex codepoints, Claude Code UTF-16). Both are reported.
- **Zero dependencies.** Pure Python stdlib.

## 🚀 Quick start

```bash
# as a Claude Code plugin
claude plugin marketplace add kubouchiyuya/rashinban
claude plugin install rashinban

# or clone and use the scripts directly
python3 skills/rashinban/scripts/goal_lint.py my-goal.txt     # grade a drafted /goal
python3 skills/rashinban/bin/rashinban activate my-goal.txt   # lint + emit the /goal line
sh tests/smoke.sh                                             # 6 offline assertions
```

A weak draft scores low and names what's missing:

```text
rashinban goal-lint — score 22/100
  elements: -objective, -evidence, -done, +validation, -constraints, -block
  MISSING core: Objective; Evidence / verification surface; Done (pass/fail condition)
  warning: vague success term ("better/works") with no concrete check named
```

> **Tip:** a high score means the contract is *well-formed*, not that the goal is
> *good*. Judgment still yours.

## 🧭 How it works

Rashinban has two halves: the **contract spec** (`skills/rashinban/SKILL.md`) and the **harness** (`goal_lint.py`,
`bin/rashinban`, `goal_seek_bridge.py`, `references/`, `tests/`). It writes and
checks goals; it does *not* schedule anything — it rides each runtime's native
goal mechanism. Deep dive → [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md).

### The Codex linchpin
`spawn_agent`/`create_thread` are gated to explicit user requests. If a goal
needs them, Rashinban returns the `/goal` line for **you** to send — sending it
is what authorizes those tools. It never claims a goal was set unless it was.

## 🧪 Testing / CI

| Command | Purpose |
|---|---|
| `sh tests/smoke.sh` | 6 offline assertions: good goal passes, weak goal is flagged, over-cap fails, CLI emits the `/goal` line |
| GitHub Actions (`ci.yml`) | runs lint + smoke on every push — the badge above is the proof |

## 🤝 Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) ·
[SECURITY.md](SECURITY.md) · [Docs](docs/GUIDE.md)

## 📜 License & credit

MIT — see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
