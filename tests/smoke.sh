#!/bin/sh
# Rashinban smoke test — offline, deterministic. Proves goal_lint distinguishes
# a well-formed /goal from a weak one and enforces the length cap.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LINT="$ROOT/skills/rashinban/scripts/goal_lint.py"
FIX="$ROOT/tests/fixtures"
pass=0; fail=0
ok(){ pass=$((pass+1)); echo "  ok   - $1"; }
no(){ fail=$((fail+1)); echo "  FAIL - $1"; }

echo "[1] good goal → no missing core, exit 0"
OUT="$(python3 "$LINT" "$FIX/good_goal.txt" --json 2>/dev/null)"; rc=$?
MC="$(printf '%s' "$OUT" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["missing_core"]))')"
[ "$rc" = "0" ] && ok "exit 0" || no "exit $rc"
[ "$MC" = "0" ] && ok "no missing core" || no "missing_core=$MC"

echo "[2] weak goal → missing core + warnings"
OUT2="$(python3 "$LINT" "$FIX/weak_goal.txt" --json 2>/dev/null)"
MC2="$(printf '%s' "$OUT2" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["missing_core"]))')"
W2="$(printf '%s' "$OUT2" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["warnings"]))')"
[ "$MC2" -ge 1 ] && ok "flags missing core ($MC2)" || no "missed weak goal"
[ "$W2" -ge 1 ] && ok "raises warnings ($W2)" || no "no warnings on weak goal"

echo "[3] oversize goal → over cap, exit 1"
python3 -c "print('x'*4001)" > /tmp/rashinban-big.txt
python3 "$LINT" /tmp/rashinban-big.txt >/dev/null 2>&1; rc3=$?
[ "$rc3" = "1" ] && ok "exit 1 on over-cap" || no "exit $rc3 on over-cap"

echo "[4] CLI activate emits /goal line for a good goal"
python3 "$ROOT/skills/rashinban/bin/rashinban" activate "$FIX/good_goal.txt" 2>/dev/null | grep -q '^/goal ' \
  && ok "activate emits /goal line" || no "no /goal line"

echo ""
echo "RESULT: pass=$pass fail=$fail"
[ "$fail" = "0" ]
