# Validation playbooks (Rashinban)

The `/goal` must name the *most relevant* validation, not every possible check.
Per-domain, what "verified" concretely means. Extracted and expanded from the
/goal contract spec.

| Domain | Concrete validation the /goal should require |
|---|---|
| **Bugs** | Reproduce first. Done = the failing case passes with no related regression. |
| **Performance** | Metric + threshold + method + runs (e.g. `p95 < 250 ms over 3 runs`). |
| **Tests / CI** | The exact command and its pass condition. Checks must not pass by deleting/weakening tests. |
| **Working systems / UI** | Test the user goal, not component existence. Real browser / end-to-end run through the core path; inspect the resulting runtime/API/storage state. Each named item checked separately: pass / fail / not-checked / blocked. |
| **Migration / batch** | Counts verified by query or grep, with the coverage bound stated. |
| **Research** | Central question + competing hypotheses + what weakens each + a stop rule. At least one pass tries to disprove the lead. "Unconfirmed" ≠ "no". |
| **Quality** | An observable bar: lint/types/tests green, N reviewed examples, readable/low-branching diffs — not "cleaner". |

## Distinct outcome classes
Where outcomes have classes (success / failure / timeout), require evidence that
each relevant class actually fired. A check that could not have failed proves
nothing.

## Review tiers (match to risk)
- **Low risk + strong automated checks** → rerun those checks; no subagent.
- **Medium risk / incomplete evidence / broad change** → one read-only subagent.
- **High risk** (correctness, safety, security, billing, privacy, UX, research,
  evidence-quality) → adversarial read-only review that hunts counterexamples,
  unsupported claims, missing checks, and overclaims.

Findings touching correctness / safety / Done block until fixed; the rest are the
executor's call (fix, or keep with the reason recorded).

## The anti-substitution rule
Evidence from a mock, demo, fixture, fake service, or nearby example is
*supporting* evidence only. It cannot complete a named requirement unless the
user accepted the substitution.
