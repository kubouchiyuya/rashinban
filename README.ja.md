<div align="center">

# 羅針盤 / Rashinban

### 自律エージェントのゴールの羅針盤 — ラフな依頼を、検証可能で lint 済みの `/goal` に変える。

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![Based on goal-setter](https://img.shields.io/badge/based%20on-goal--setter%20by%20gotalab-black.svg)](https://github.com/gotalab/goal-setter-skill)
[![Every agent](https://img.shields.io/badge/Codex%20%7C%20Claude%20%7C%20Grok%20%7C%20OpenAI%20%7C%20Gemini-black.svg)](skills/rashinban/adapters/ROUTING.md)

English: [README.md](README.md)

</div>

> **帰属.** Rashinban は [goal-setter-skill](https://github.com/gotalab/goal-setter-skill)
> （作者 **gotalab**・MIT）の**ハーネス強化派生版**です。優れたゴール契約仕様は
> gotalab のもので、Rashinban はその周りに決定論的ハーネスを足しています。
> [NOTICE.md](NOTICE.md) 参照。

---

## これは何

**メタスキル**。タスク自体は実装しない — ラフな依頼を、成果・Done の検証方法・
壊してはならない境界・停止条件を明記した**コンパクトな `/goal`** に変換し、AI
エージェント（Codex / Claude Code / Grok / OpenAI / Gemini…）が**検証可能な結果が
真になるまで自走**できるようにする。

上流の goal-setter は本質的に「1枚の優れたプロンプト」。**Rashinban はそこに
ハーネスを被せます:**

| 追加 | はたらき |
|---|---|
| `scripts/goal_lint.py` | 品質ゲート — 契約要素（目的/証拠/Done/検証/制約/停止）の充足を確認、「better/works」等の曖昧表現や"タスク列挙=Done"を指摘、0-100 でスコア化、実ランタイム 4,000字上限（Codex=コードポイント / Claude Code=UTF-16）を強制 |
| `bin/rashinban` | ホスト検出 CLI — `lint` / `host` / `activate`（`/goal` 行＋ランタイム別の正しい案内を出力）/ `bridge` / `selfcheck` |
| `scripts/goal_seek_bridge.py` | ゴールを AKATSUKI `plans-store`（`rashinban-inbox.jsonl`・非破壊）へドロップし goal-seek へ橋渡し |
| `references/` | `templates.md`（即用 `/goal` 雛形）・`validation-playbooks.md`（領域別の"検証済"の定義）・`adapters/ROUTING.md`（クロスランタイム活性化） |
| `tests/smoke.sh` | オフライン検証: 良いゴールは通過・弱いゴールは指摘・超過は失敗 |

## クイックスタート

```bash
python3 skills/rashinban/scripts/goal_lint.py my-goal.md      # 起草した /goal を lint
python3 skills/rashinban/bin/rashinban activate my-goal.md    # lint + /goal 行を出力
python3 skills/rashinban/bin/rashinban selfcheck
sh tests/smoke.sh
```

lint は欠けている要素・弱い表現を挙げてスコア化します。高スコア＝"良いゴール"では
なく、契約が**整形されている**という意味です。

## 活性化（スケジューラは作らない・ランタイムに乗る）

| ランタイム | 活性化 |
|---|---|
| **Codex**（worker 不要） | native goal tool でセット可 |
| **Codex**（`spawn_agent`/`create_thread` が要る） | **あなたが** `/goal` 行を送る — それがツールを認可する |
| **Claude Code** | `/goal` 行を送る・動的ワークフローで fan-out 可 |
| **Grok / OpenAI / Gemini / Cursor** | `/goal` 行を送る・run/stop 規律は契約に保持 |

詳細: [skills/rashinban/adapters/ROUTING.md](skills/rashinban/adapters/ROUTING.md)

## ドキュメント

| Doc | 内容 |
|---|---|
| [docs/GUIDE.ja.md](docs/GUIDE.ja.md) | 平易なガイド（非エンジニア/AIユーザー向け） |
| [docs/QUICKSTART.md](docs/QUICKSTART.md) | install・lint・activate・bridge |
| [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md) | 契約・lint・CLI・ランタイム別活性化・正直な限界 |
| [docs/FAQ.md](docs/FAQ.md) | よくある質問 |
| [skills/rashinban/references/](skills/rashinban/references/) | templates・validation playbooks・routing |
| English | [README.md](README.md) · [docs/GUIDE.md](docs/GUIDE.md) |

## ライセンス・クレジット

MIT — [LICENSE](LICENSE)（Copyright gotalab）。Rashinban は独立した派生であり
gotalab とは**非提携**。正規版は[上流リポジトリ](https://github.com/gotalab/goal-setter-skill)を参照。
