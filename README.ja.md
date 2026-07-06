<div align="center">

# 🧭 羅針盤 / Rashinban

**自律エージェントのゴールの羅針盤 — ラフな依頼を、検証可能で lint 済みの `/goal` に。**

長い自走を決めるのは、ただ一つ *「完了」が定義されていたか*。

[![CI](https://github.com/kubouchiyuya/rashinban/actions/workflows/ci.yml/badge.svg)](https://github.com/kubouchiyuya/rashinban/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![deps](https://img.shields.io/badge/deps-zero%20(python%20stdlib)-black.svg)](#-クイックスタート)
[![Agents](https://img.shields.io/badge/Codex%20%7C%20Claude%20%7C%20Grok%20%7C%20OpenAI%20%7C%20Gemini-black.svg)](skills/rashinban/adapters/ROUTING.md)

[English](README.md) · [中文](README.zh.md) · [ガイド](docs/GUIDE.ja.md) · [仕組み](docs/HOW-IT-WORKS.md)

**Rashinban が検証可能なゴール作りに役立ったら、⭐ を。他のエージェント開発者が見つけやすくなります。**

</div>

---

AI に「アプリを良くして」と言って自走させると迷走します — 違う所を磨く、早すぎる
段階で止まる、実際は動かないデモで勝利宣言する。**羅針盤はそれを止める工程。**
ラフな依頼を `/goal`（短い契約）に変換します: 成果・検証方法・壊してはならない境界・
停止条件を明記 — エージェントが**検証可能な結果が真になるまで自走**し、正直に報告する。

```bash
python3 skills/rashinban/bin/rashinban activate my-goal.txt
#   起草を lint → /goal 行 + ランタイム別の正しい案内を出力
```

## ✨ 主な機能

- **文字数だけでなくゴールを lint。** `goal_lint.py` が契約要素（目的/証拠/Done/検証/
  制約/停止）を確認、「better/works」等の曖昧さや"タスク列挙=Done"を指摘、0-100 で採点。
- **全ランタイムで動く。** `rashinban activate` が Codex / Claude Code / Grok /
  Grok Build / Gemini / Antigravity / Cursor / GLM / DeepSeek / Hermes /
  OpenClaw を検出。他の任意のエージェントも移植可能な `/goal` をそのまま実行。
- **goal-seek へ橋渡し。** AKATSUKI 内で `rashinban bridge` が `plans-store` へ
  非破壊投入（SoT は直接触らない）。
- **実ランタイムの長さ上限を強制。** 4,000字（Codex=codepoint / Claude=UTF-16）。両方報告。
- **依存ゼロ。** Python 標準ライブラリのみ。

## 🚀 クイックスタート

```bash
# Claude Code プラグインとして
claude plugin marketplace add kubouchiyuya/rashinban
claude plugin install rashinban

# または直接スクリプトを使う
python3 skills/rashinban/scripts/goal_lint.py my-goal.txt     # 起草した /goal を採点
python3 skills/rashinban/bin/rashinban activate my-goal.txt   # lint + /goal 行を出力
sh tests/smoke.sh                                            # オフライン6アサーション
```

弱い起草は低スコアで、欠けを名指しします:

```text
rashinban goal-lint — score 22/100
  MISSING core: Objective; Evidence / verification surface; Done (pass/fail condition)
  warning: vague success term ("better/works") with no concrete check named
```

> **Tip:** 高スコア＝契約が*整形されている*であって、*良いゴール*ではない。判断は人。

## 🧭 仕組み

契約仕様（`SKILL.md`）＋ハーネス（`goal_lint.py`・
`bin/rashinban`・`goal_seek_bridge.py`・`references/`・`tests/`）の二層。ゴールを
**書いて検査する**もので、スケジューラは作らない — 各ランタイムの native 機構に乗る。
詳細 → [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md)

### Codex の要
`spawn_agent`/`create_thread` は明示的なユーザー要求に限定。必要なら羅針盤は
`/goal` 行を**あなたが送る**形で返す — それがツールを認可する。セットされたと偽らない。

## 🧪 テスト / CI

| コマンド | 目的 |
|---|---|
| `sh tests/smoke.sh` | 6 アサーション（良は通過・弱は指摘・超過は失敗・CLI が /goal 行を出力） |
| GitHub Actions (`ci.yml`) | push ごとに lint+smoke 実行 — 上のバッジが証拠 |

## 🤝 コントリビュート

[CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) ·
[SECURITY.md](SECURITY.md) · [ドキュメント](docs/GUIDE.ja.md)

## 📜 ライセンス・クレジット

MIT — [LICENSE](LICENSE) / [NOTICE.md](NOTICE.md) 参照。
