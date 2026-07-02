# Quickstart

## Install

```bash
# as a Claude Code plugin
claude plugin marketplace add kubouchiyuya/rashinban
claude plugin install rashinban

# or just clone and use the scripts (zero dependencies — pure Python stdlib)
git clone https://github.com/kubouchiyuya/rashinban
python3 rashinban/skills/rashinban/bin/rashinban selfcheck
```

## 1. Draft a rough goal

Put a first draft in a file — plain prose is fine:

```text
Fix the login timeout so users stay signed in for 24h, verified by a browser
run that logs in, waits, and confirms the session persists; npm test auth must
stay green. Read src/auth/session.ts. Never weaken existing auth tests. Done:
the session persists in the real run and npm test auth passes. Stop and ask if
it would touch token signing or billing.
```

## 2. Lint it

```bash
python3 skills/rashinban/scripts/goal_lint.py my-goal.txt
```

```text
rashinban goal-lint — score 100/100
  length: 462 codepoints / 462 UTF-16 units (cap 4000) ok
  elements: +objective, +evidence, +done, +validation, +constraints, +block
  looks well-formed — activate it (a good score is not a good Goal by itself)
```

A weak draft ("make it better and add features") scores low and tells you what's
missing (objective / evidence / Done) and why.

## 3. Activate it

```bash
python3 skills/rashinban/bin/rashinban activate my-goal.txt
```

This lints, then prints the exact `/goal …` line plus **runtime-correct**
guidance (Codex / Claude Code / Grok / OpenAI / Gemini). Send that line to your
agent.

## 4. (AKATSUKI) file it into goal-seek

```bash
python3 skills/rashinban/bin/rashinban bridge my-goal.txt --title "AKT-NNN login fix"
```

Drops the goal into `.claude/state/plans-store/rashinban-inbox.jsonl`
(non-destructive; the plans-store SoT is never edited directly).

## Verify the tooling

```bash
sh tests/smoke.sh      # 6 offline assertions
```
