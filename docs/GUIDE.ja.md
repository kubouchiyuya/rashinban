# 羅針盤 / Rashinban — ガイド

> 自律エージェントのゴールの羅針盤。
> English: [GUIDE.md](GUIDE.md) · Repo: https://github.com/kubouchiyuya/rashinban

## 非エンジニアでも分かる話

AI に「アプリを良くして」と言って自走させたとき、成否を決める唯一のものは
**「完了」が定義されていたか**です。定義がないとエージェントは迷走します —
違う所を磨く、早すぎる段階で止まる、実際は動かないデモで勝利宣言する。

羅針盤はそれを防ぐ工程。ラフな依頼を **`/goal`**（短い契約）に変換します:

- **どんな結果**か（"X を良くする"でなく "X が Y する"）
- **どうなれば成功と分かるか**（テスト・スクショ・数値・チェック）
- **壊してはならないもの**
- **いつ止めるか**（迷走せず停止）

その上でエージェント（Codex / Claude Code / Grok / OpenAI / Gemini…）が
**その結果が検証的に真になるまで自走**でき、最後に正直な報告が返ります。

## 「ただのプロンプト」との違い

上流 goal-setter は優れたプロンプト1枚。羅針盤は品質を**期待でなく検査**する
ツールを被せます:

- **`goal_lint.py`** — 起草した `/goal` を 0-100 で採点。成果・証拠・Done を挙げて
  いるか? 「works nicely」等の曖昧さや"タスク列挙=Done"を隠していないか? 長さ上限内か?
- **`rashinban` CLI** — ランタイムを検出し、そこでの正しい活性化方法を教える
- **plans-store ブリッジ** — ゴールを AKATSUKI の goal-seek キューへ非破壊で投入

## 次に読む

| Doc | 目的 |
|---|---|
| [QUICKSTART](QUICKSTART.md) | 2分で最初の lint + activate |
| [HOW-IT-WORKS](HOW-IT-WORKS.md) | 契約・lint・CLI・ランタイム別活性化・正直な限界 |
| [FAQ](FAQ.md) | 「高スコア≠良いゴール」・各ランタイム・Codex の要 |
| [templates](../skills/rashinban/references/templates.md) | 即用 `/goal` 雛形 |
| [validation-playbooks](../skills/rashinban/references/validation-playbooks.md) | 領域別"検証済"の定義 |
