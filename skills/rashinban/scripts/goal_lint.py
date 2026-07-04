#!/usr/bin/env python3
"""Rashinban goal-lint — quality gate for a compact /goal contract.

Beyond a raw length check, this lints the
*contract elements* a good /goal should carry and flags vague or task-list-as-Done
phrasing. Heuristic by design: a /goal is plain prose with no labeled fields, so
this gives guidance and a score, not a hard pass/fail on structure. The ONLY hard
failure is the runtime length cap.

Usage:
  goal_lint.py <file>              # lint a /goal file
  cat goal.md | goal_lint.py -     # stdin
  goal_lint.py <file> --json       # machine-readable
  goal_lint.py <file> --strict     # exit nonzero on any missing core element
  goal_lint.py <file> --min-score 70   # CI gate: exit nonzero if score < 70

Exit: 0 ok · 1 length over cap (hard) · 2 usage · 3 missing core (--strict) · 4 below --min-score

Length rules verified against Codex (Unicode codepoints) and Claude Code
(UTF-16 code units), cap 4000.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HARD_CAP = 4000


def extract_objective(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text.strip())
    text = text.strip()
    if text.lower().startswith("/goal"):
        text = text[len("/goal"):].lstrip()
    return text.strip()


def length_report(obj: str) -> dict:
    codepoints = len(obj)
    utf16 = sum(2 if ord(c) > 0xFFFF else 1 for c in obj)
    return {
        "codepoints": codepoints,          # Codex counts these
        "utf16_units": utf16,              # Claude Code counts these
        "cap": HARD_CAP,
        "over_cap": utf16 > HARD_CAP or codepoints > HARD_CAP,
    }


# --- contract element heuristics -------------------------------------------
# Each element: (key, human label, is_core, list of signal patterns)
ELEMENTS = [
    ("objective", "Objective (one verifiable end state)", True, [
        r"\b(must|should|will)\b", r"\bso that\b", r"\bresult(s|ing)?\b",
        r"\boutcome\b", r"final state", r"→", r"->",
    ]),
    ("evidence", "Evidence / verification surface", True, [
        r"\bverif", r"\bevidence\b", r"\bprove[ns]?\b", r"\bcheck(ed|s|ing)?\b",
        r"\btest(s|ed|ing)?\b", r"\bscreenshot", r"\bbenchmark", r"\bmeasure",
        r"\boutput\b", r"\bp\d{2}\b", r"\bcommand", r"\bartifact",
    ]),
    ("done", "Done (pass/fail condition)", True, [
        r"\bDone\b", r"\bpass(es|ed|ing)?\b", r"\bfail(s|ed|ing)?\b",
        r"\bcomplete[ds]?\b", r"\bwhen\b.*\b(true|passes|works)\b", r"\bacceptance",
    ]),
    ("validation", "Validation (real commands/checks)", False, [
        r"\b(npm|pytest|pnpm|yarn|cargo|go|make|python3?|bash|sh)\b",
        r"\brun\b", r"`[^`]+`", r"\bp95\b", r"\bthreshold", r"\bregress",
    ]),
    ("constraints", "Constraints / boundaries", False, [
        r"\bnever\b", r"\bonly\b", r"\bmust not\b", r"\bdo not\b",
        r"\bwithout\b", r"\bscope\b", r"\bboundary|boundaries\b", r"\bcompat",
    ]),
    ("block", "Block / stop condition", False, [
        r"\bstop\b", r"\bblock(ed|s)?\b", r"\bif .*(fail|cannot|blocked)",
        r"\bapproval\b", r"\bask\b", r"\b~?3 (distinct )?approaches\b",
    ]),
]

# vague words that signal a weak, unverifiable goal when not near a concrete check
VAGUE = re.compile(r"\b(better|good|nice|improve[ds]?|works?|clean(er)?|robust|"
                   r"high[- ]quality|optimal|properly)\b", re.IGNORECASE)
CONCRETE_NEARBY = re.compile(r"[`0-9]|\bp95\b|\btest|\bverif|\bcommand|\bscreenshot|\bcount", re.IGNORECASE)
# task-list-as-Done: several imperative build verbs joined
TASKLIST = re.compile(r"\b(build|add|create|implement|write|make)\b[^.]*,[^.]*\b(build|add|create|implement|write|make|and)\b", re.IGNORECASE)


def element_report(obj: str) -> dict:
    found, missing_core, warnings = {}, [], []
    for key, label, is_core, pats in ELEMENTS:
        hit = any(re.search(p, obj, re.IGNORECASE) for p in pats)
        found[key] = hit
        if is_core and not hit:
            missing_core.append(label)

    # vagueness: a vague word with no concrete check anywhere is a smell
    if VAGUE.search(obj) and not CONCRETE_NEARBY.search(obj):
        warnings.append('vague success term (e.g. "better/works") with no concrete check named')
    if TASKLIST.search(obj) and not re.search(r"\bDone\b|\bverif|\bevidence\b", obj, re.IGNORECASE):
        warnings.append("reads like a task list (build X, add Y) without defining Done/evidence")
    if len(obj) < 60:
        warnings.append("very short — may be under-specified for an autonomous run")

    return {"found": found, "missing_core": missing_core, "warnings": warnings}


def score(length: dict, elems: dict) -> int:
    s = 100
    if length["over_cap"]:
        s -= 40
    s -= 20 * len(elems["missing_core"])          # core elements matter most
    soft_missing = sum(1 for k, v in elems["found"].items() if not v) - len(elems["missing_core"])
    s -= 5 * max(0, soft_missing)
    s -= 8 * len(elems["warnings"])
    return max(0, min(100, s))


def lint(obj: str) -> dict:
    length = length_report(obj)
    elems = element_report(obj)
    return {
        "length": length,
        "elements": elems["found"],
        "missing_core": elems["missing_core"],
        "warnings": elems["warnings"],
        "score": score(length, elems),
        "chars": len(obj),
    }


def render(rep: dict) -> str:
    L = rep["length"]
    lines = [
        f"rashinban goal-lint — score {rep['score']}/100",
        f"  length: {L['codepoints']} codepoints / {L['utf16_units']} UTF-16 units "
        f"(cap {L['cap']}) {'OVER CAP' if L['over_cap'] else 'ok'}",
        "  elements: " + ", ".join(
            (("+" if v else "-") + k) for k, v in rep["elements"].items()),
    ]
    if rep["missing_core"]:
        lines.append("  MISSING core: " + "; ".join(rep["missing_core"]))
    for w in rep["warnings"]:
        lines.append(f"  warning: {w}")
    if not rep["missing_core"] and not rep["warnings"] and not L["over_cap"]:
        lines.append("  looks well-formed — activate it (a good score is not a good Goal by itself)")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="goal_lint")
    ap.add_argument("path", help="file path, or - for stdin")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 3 if a core element is missing")
    ap.add_argument("--min-score", type=int, default=None,
                    help="exit 4 if the score is below N (use in CI to gate goal quality)")
    a = ap.parse_args(argv)
    raw = sys.stdin.read() if a.path == "-" else Path(a.path).read_text("utf-8")
    obj = extract_objective(raw)
    rep = lint(obj)
    print(json.dumps(rep, indent=2, ensure_ascii=False) if a.json else render(rep))
    if rep["length"]["over_cap"]:
        return 1
    if a.strict and rep["missing_core"]:
        return 3
    if a.min_score is not None and rep["score"] < a.min_score:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
