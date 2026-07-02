# 羅針盤 / Rashinban — Guide

> A compass for autonomous agent goals.
> 日本語版: [GUIDE.ja.md](GUIDE.ja.md) · Repo: https://github.com/kubouchiyuya/rashinban
> Based on [goal-setter-skill](https://github.com/gotalab/goal-setter-skill) by gotalab (MIT).

## Read this even if you're not an engineer

When you tell an AI agent *"make the app better"* and let it run on its own, the
single thing that decides success is **whether "done" was ever defined**. If it
wasn't, the agent wanders: it polishes the wrong thing, stops too early, or
declares victory on a demo that doesn't really work.

Rashinban is the step that prevents this. It turns a rough request into a
**`/goal`** — a short contract that says:

- **what result** is expected (not "improve X" but "X does Y"),
- **how you'll know it worked** (a test, a screenshot, a number, a check),
- **what must not break**, and
- **when to stop** instead of thrashing.

Then an agent (Codex, Claude Code, Grok, OpenAI, Gemini…) can run **until that
result is verifiably true** — and you get an honest report at the end.

## What Rashinban adds over "just writing a prompt"

The upstream goal-setter is one excellent prompt. Rashinban wraps it in tooling
so the quality is *checked*, not hoped for:

- **`goal_lint.py`** grades a drafted `/goal` (0-100): does it name an outcome,
  evidence, a Done condition? Does it hide a vague "works nicely" or a task list
  pretending to be Done? Is it within the runtime length cap?
- **`rashinban` CLI** detects your runtime and tells you exactly how to activate
  the goal there.
- **plans-store bridge** files the goal into AKATSUKI's goal-seek queue,
  non-destructively.

## Where to go next

| Doc | For |
|---|---|
| [quickstart](QUICKSTART.md) | run your first lint + activate in 2 minutes |
| [how it works](HOW-IT-WORKS.md) | the contract, the lint, the CLI, activation per runtime, honest limits |
| [FAQ](FAQ.md) | "SAFE score ≠ good goal", runtimes, the Codex linchpin |
| [templates](../skills/rashinban/references/templates.md) | ready `/goal` skeletons |
| [validation playbooks](../skills/rashinban/references/validation-playbooks.md) | what "verified" means per domain |
