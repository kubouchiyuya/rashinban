<div align="center">

# 🧭 羅針盤 / Rashinban

**自主代理目标的指南针 —— 把一个模糊的请求，变成经过 lint 检验、可验证的 `/goal`。**

因为决定一次长时间代理运行成败的，只有一件事：*"完成"到底有没有被定义过*。

[![CI](https://github.com/kubouchiyuya/rashinban/actions/workflows/ci.yml/badge.svg)](https://github.com/kubouchiyuya/rashinban/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![deps](https://img.shields.io/badge/deps-zero%20(python%20stdlib)-black.svg)](#-快速开始)
[![Agents](https://img.shields.io/badge/Codex%20%7C%20Claude%20%7C%20Grok%20%7C%20OpenAI%20%7C%20Gemini-black.svg)](skills/rashinban/adapters/ROUTING.md)

[English](README.md) · [日本語](README.ja.md) · [Guide](docs/GUIDE.md) · [How it works](docs/HOW-IT-WORKS.md)

**如果 Rashinban 帮你写出了一个可验证的目标，点个 ⭐ 能帮助其他 agent 开发者发现它。**

</div>

---

如果你只告诉 AI "把这个应用做得更好"然后让它自己运行，它会迷失方向 —— 打磨错了
地方、停得太早，或是在一个根本跑不起来的演示上宣布胜利。**Rashinban 就是用来
阻止这一切的那一步。** 它把一个模糊的请求转化为 `/goal`：一份简短的契约，写明
最终结果是什么、如何验证、什么东西不能被破坏、以及何时应该停止 —— 让代理
**持续运行，直到一个可验证的结果成立为止**，然后如实汇报。

```bash
python3 skills/rashinban/bin/rashinban activate my-goal.txt
#   对草稿做 lint，然后输出 /goal 语句 + 与运行时相符的指引
```

## ✨ 核心能力

- **对目标做 lint，而不只是数字符数。** `goal_lint.py` 会检查契约的各个*要素*
  （目标 / 证据 / Done / 验证 / 约束 / 停止条件），标记出"更好/能用"之类的模糊
  表述以及"把任务清单当 Done"的问题，并给出 0-100 的评分。
- **适配所有运行时。** `rashinban activate` 能识别 Codex、Claude Code、
  Grok / Grok Build、Gemini、Google Antigravity、Cursor、GLM、DeepSeek、Hermes、
  以及 OpenClaw —— 其他任何有能力的代理也可以直接运行这份可移植的 `/goal`。
- **桥接到 goal-seek。** 在 AKATSUKI 内部，`rashinban bridge` 会把目标以
  非破坏性的方式投递进 `plans-store`（SoT 本身永远不会被直接修改）。
- **强制真实的长度上限。** 4,000 字符，并按每个运行时实际的计数方式计算
  （Codex 按 codepoint、Claude Code 按 UTF-16），两种结果都会显示。
- **零依赖。** 纯 Python 标准库。

## 🚀 快速开始

```bash
# 作为 Claude Code 插件
claude plugin marketplace add kubouchiyuya/rashinban
claude plugin install rashinban

# 或者直接克隆并使用脚本
python3 skills/rashinban/scripts/goal_lint.py my-goal.txt     # 对起草的 /goal 打分
python3 skills/rashinban/bin/rashinban activate my-goal.txt   # lint + 输出 /goal 语句
sh tests/smoke.sh                                             # 6 条离线断言
```

一份薄弱的草稿会得到低分，并被明确指出缺了什么：

```text
rashinban goal-lint — score 22/100
  elements: -objective, -evidence, -done, +validation, -constraints, -block
  MISSING core: Objective; Evidence / verification surface; Done (pass/fail condition)
  warning: vague success term ("better/works") with no concrete check named
```

> **提示：** 高分只说明这份契约*结构完整*，并不代表这个目标本身*足够好*。
> 判断权仍然在你手里。

## 🧭 工作原理

Rashinban 由两部分组成：**契约规范**（`skills/rashinban/SKILL.md`）与**harness**
（`goal_lint.py`、`bin/rashinban`、`goal_seek_bridge.py`、`references/`、
`tests/`）。它负责*编写和检查*目标，本身*不*调度任何东西 —— 而是搭乘每个
运行时自带的原生 goal 机制运行。深入了解 →
[docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md)。

### Codex 的关键点
`spawn_agent`/`create_thread` 仅在明确的用户请求下才会被授权。如果某个目标
需要用到它们，Rashinban 会把 `/goal` 语句返回给**你**去发送 —— 正是这一步
授权了这些工具。它绝不会在目标尚未真正设置时，就声称已经设置完成。

## 🧪 测试 / CI

| 命令 | 用途 |
|---|---|
| `sh tests/smoke.sh` | 6 条离线断言：优质目标通过、薄弱目标被标记、超出上限则失败、CLI 能输出 `/goal` 语句 |
| GitHub Actions (`ci.yml`) | 每次 push 都会运行 lint + smoke —— 上方的徽章就是证明 |

## 🤝 贡献

[CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) ·
[SECURITY.md](SECURITY.md) · [文档](docs/GUIDE.md)

## 📜 许可证与署名

MIT —— 详见 [LICENSE](LICENSE) 与 [NOTICE.md](NOTICE.md)。
