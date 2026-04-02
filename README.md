# awesome-cc-harness

# 从 Claude Code 512K 行源码逆向 Harness Engineering

**目前最全面的 Claude Code 架构逆向工程分析**

[![GitHub stars](https://img.shields.io/github/stars/WanLanglin/-awesome-cc-harness?style=social)](https://github.com/WanLanglin/-awesome-cc-harness/stargazers)
[![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](LICENSE)
[![中文](https://img.shields.io/badge/语言-中文-blue.svg)](docs/zh/)
[![English](https://img.shields.io/badge/Language-English-green.svg)](docs/en/)

> 基于 Claude Code 全部 512,664 行 TypeScript 源码的系统性逆向分析，拆解 Anthropic 在 Agent Loop、工具系统、权限模型、沙盒安全、上下文工程等方面的设计决策与工程取舍。

![Harness Architecture](images/01_harness_architecture.png)

---

## 这个项目有什么

### 📖 主教程：Harness Engineering 完全指南

16 章 · ~50,000 字 · 147 段代码块 · 77 张图表 · 中英双语

从第一行 `#!/usr/bin/env node` 到最后一层沙盒隔离，**逐系统拆解**：

| 章节 | 内容 | 核心发现 |
|------|------|---------|
| 第 1 章 | Harness Engineering 概论 | 只改 Harness 就能让跑分从 52.8% 提升到 66.5% |
| 第 2 章 | Claude Code 架构全景 | 512K LOC 的模块分布与启动时序 |
| 第 3 章 | **Agent Loop** | 30 行 while(true) + 1800 行错误恢复 + 7 个 continue 站点 |
| 第 4 章 | **Tool System** | 43+ 工具的分区算法：读操作并行、写操作串行 |
| 第 5 章 | **Permission Model** | 6 层纵深防御，累计绕过概率 0.00000002% |
| 第 6 章 | **Hooks System** | 26 事件 × 4 类型的生命周期可扩展架构 |
| 第 7 章 | Sandbox & Security | 文件系统 + 网络 + 进程三维隔离 |
| 第 8 章 | Context Engineering | 180K → 45K 的四级压缩管道 |
| 第 9-12 章 | Settings / MCP / SubAgent / Skills | 7 级设置层级、多智能体编排、插件生态 |
| 第 13-14 章 | 实战指南 + 设计哲学 | 10 条可复用的 Harness 设计原则 |
| 第 15 章 | **Hands-on: Mini Harness** | 200 行 Python 从零实现一个可运行的 Harness |
| 第 16 章 | **竞品对比** | Claude Code vs Cursor vs Copilot 12 维对比 |

### 🔬 NEW: [Grove 系统 — Claude Code 中从未被报道的训练数据基础设施](docs/zh/grove-system.md)

**在源码中发现了 Anthropic 从用户键盘到 BigQuery 训练数据仓库的完整数据链路：**

- **Grove 系统** — UI 明确写着 "train and improve"，开启后数据保留从 30 天延长至 **5 年**
- **796 个 telemetry 事件** × 双路管道 — Datadog 拿脱敏数据，1P API 拿完整数据写入 **BigQuery 特权列**
- **Protobuf schema** — 865 行生成代码，外部 monorepo `go/cc-logging` 编译时强制
- **SWE-bench 嵌入每个 telemetry 事件** — eval 数据和用户数据走**同一条管道、同一个 BigQuery**
- **开发者注释直接写着 "training data"** — `messages.ts:245` + `sessionStorage.ts:4388`
- **Aider 竞品检测** — 追踪用户是否同时使用竞品工具

> 每一步都有精确的文件路径和行号。不是推测，不是类比。 **[👉 阅读完整分析](docs/zh/grove-system.md)**

### 🛡️ NEW: [Claude Code 是如何知道你在偷偷蒸馏的？— 机制分析](docs/zh/anti-distillation.md)

**从源码中拆解 Anthropic 防止模型被盗的 5 层工程实现：**

- **Native Client Attestation** — Bun/Zig 原生层注入认证 token，服务端验证客户端真实性
- **Fingerprint Attribution** — SHA256(salt + 消息特定字符 + 版本号)，每条训练数据可追溯来源
- **Fake Tools Injection** — 向 API 注入虚假工具定义，蒸馏模型暴露假工具 = 被抓
- **Signature-Bearing Blocks** — thinking + connector_text 绑定 API key，换 key 立即失效
- **Streamlined Mode** — 源码直接称为 "distillation-resistant output format"

> **[👉 阅读完整分析](docs/zh/anti-distillation.md)**

### 📊 77 张专业图表

AI 生成架构图、Mermaid 流程图、Matplotlib 数据可视化，覆盖每一章的核心概念。

---

## 在线阅读

👉 **[点击这里开始阅读](https://wanlanglin.github.io/-awesome-cc-harness/)**

---

## 项目结构

```
docs/
├── zh/
│   └── index.md                 # 主教程（16 章，~5000 行）
├── en/
│   └── index.html               # 英文版
└── _layouts/
    └── tutorial.html            # GitHub Pages 暗色主题模板
images/                          # 77 张图表
├── 01_harness_architecture.png  # AI 生成架构图
├── mermaid/                     # 16 张 Mermaid 渲染图
└── ch*_*.png                    # 各章数据图表
```

---

## 相关资源

| 资源 | 说明 |
|------|------|
| [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | 渐进式 12 节动手课程，适合从零构建 Harness |
| [claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) | 生产级 Plan→Work→Review 插件 |
| [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) | 三大支柱的概念框架 |
| [arXiv:2603.05344](https://arxiv.org/html/2603.05344v1) | 学术论文：scaffolding vs harness 架构 |

---

## 贡献

欢迎通过以下方式参与：

- ⭐ **Star** — 如果觉得有帮助，Star 是最大的鼓励
- 🐛 **Issue** — 纠错、补充、讨论
- 🔀 **Fork & PR** — 欢迎改进内容
- 📢 **分享** — 转发给做 AI Agent 的朋友

---

## 作者

**WanLanglin** · 微信: felixwll · Open to opportunities in AI Agent Infrastructure · 欢迎交流

---

## License

Educational and research purposes. Claude Code is property of Anthropic, Inc.
