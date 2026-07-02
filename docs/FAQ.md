# FAQ

**What is a `/goal`?** A short contract that states the outcome, how it's
verified, what must not break, and when to stop — so an agent can run
autonomously until the outcome is verifiably true. Rashinban drafts, lints, and
activates it.

**Does a 100/100 lint score mean my goal is good?** No. It means the contract is
*well-formed* (names an outcome, evidence, Done, and fits the length cap). Whether
it's the *right* goal is your judgment. The lint is a guardrail, not an oracle.

**Is the lint a hard pass/fail?** Only the **length cap** is hard (4,000 chars;
Codex counts codepoints, Claude Code counts UTF-16 units). Element checks are
heuristic guidance because a `/goal` is free prose, not a form.

**Does it work with agents other than Claude?** Yes — Codex, Claude Code, Grok,
OpenAI, Gemini, Cursor. `rashinban activate` detects the runtime and prints the
right guidance. See [../skills/rashinban/adapters/ROUTING.md](../skills/rashinban/adapters/ROUTING.md).

**Why does Codex sometimes need me to send the `/goal` line myself?**
`spawn_agent` and `create_thread` are gated to explicit user requests. If the
goal must launch them, an auto-set goal would run only in the main thread — so
Rashinban returns the `/goal` line for *you* to send, which is what authorizes
those tools.

**Does it change my plans-store?** Only via `bridge`, and only by appending to a
separate inbox file (`rashinban-inbox.jsonl`). The SoT `index.json` is never
edited directly.

**Dependencies?** None. Pure Python standard library. If `python3` runs, it runs.

**How is this related to gotalab's goal-setter?** Rashinban is a harness-engineered
**derivative** of [goal-setter-skill](https://github.com/gotalab/goal-setter-skill)
(MIT). The contract spec is gotalab's; Rashinban adds the lint, CLI, bridge,
references, and tests. Attribution is preserved in `LICENSE` and `NOTICE.md`. It
is not affiliated with or endorsed by gotalab.
