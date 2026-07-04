# Contributing to 羅針盤 / Rashinban

Thanks for helping aim agents at verifiable goals. Rashinban is small on purpose
— pure Python stdlib, no build step.

## Ground rules

- **Keep it a meta-skill.** Rashinban writes and checks `/goal` contracts; it does
  not implement tasks or schedule runs — it rides each runtime's native goal
  mechanism (like upstream goal-setter). PRs that add a scheduler are out of scope.
- **The lint is guidance, length is the gate.** A `/goal` is prose, so element
  checks are heuristic. Only the 4,000-char cap is a hard failure.
- **Be honest.** A high lint score means *well-formed*, not *good*. Docs say so.
- **Preserve attribution.** Keep `LICENSE` and `NOTICE.md` intact.

## Dev loop

```bash
git clone https://github.com/kubouchiyuya/rashinban
cd rashinban
python3 skills/rashinban/bin/rashinban selfcheck
sh tests/smoke.sh        # must stay green
```

## Improving the lint

1. Adjust element/vagueness heuristics in `skills/rashinban/scripts/goal_lint.py`.
2. Add or update a fixture under `tests/fixtures/` (a good goal and a weak goal).
3. Keep `sh tests/smoke.sh` green; add an assertion if you add a behavior.

## Pull requests

- Keep changes scoped; every changed line should trace to the PR's purpose.
- CI (`ci.yml`) runs lint + smoke — green before review.
- Explain *why*, not just *what*.
