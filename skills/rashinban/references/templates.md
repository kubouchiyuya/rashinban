# /goal templates (Rashinban)

Ready-to-adapt `/goal` skeletons, already compressed around the six elements
(outcome · evidence · constraints · boundaries · iteration · stop). Fill the
brackets, delete any clause that would not change the run, then lint:

    python3 scripts/goal_lint.py <file>

These are starting points, not fill-in forms — a Goal is prose in the task's own
terms. Based on goal-setter-skill by gotalab (MIT).

---

## Bug fix
> Fix `[symptom]` so that `[expected behavior]`, verified by a test that
> reproduces the failure first and then passes with no related regressions. Read
> `[anchor file]`. Do not weaken or delete existing tests. Done: the reproducing
> case passes and `[test command]` is green.

## Feature (working system, not a mock)
> `[Feature]` works end-to-end for `[user]`: `[input]` flows through the real
> `[layers]` to `[output/state]`, inspectable via `[running app / API / storage]`.
> Read `[anchor]`. Only the simplest thing that meets this; no dead ends —
> every visible control works, is honestly disabled, or is omitted. Done:
> a real end-to-end run through the core path produces `[expected]`, checked in
> `[browser/API/DB]`.

## Performance
> `[operation]` meets `[metric] [threshold]` (e.g. p95 < 250 ms) measured by
> `[method]` over `[N]` runs, with no correctness regression in `[tests]`. Read
> `[hot path]`. Done: the threshold holds across the runs and the numbers are
> reported.

## Migration / batch
> Migrate `[from] → [to]` across `[scope]`; every item either migrated or
> explicitly listed as skipped with a reason. Verify counts by `[query/grep]`
> and state the coverage bound. Do not lose or silently drop records. Done:
> migrated count + skipped count = total, verified by the query.

## Research / investigation
> Answer `[central question]` to inform `[decision]`. Track competing hypotheses
> and what evidence would weaken each; at least one pass must try to disprove the
> leading answer. Report unconfirmed items as "unconfirmed", not "no". Done: a
> sourced conclusion with the decision it enables and the evidence that would
> overturn it.
