# awesome-cc-harness

> The most comprehensive reverse engineering of Claude Code's Harness architecture. 16 chapters, 4922 lines, 34 diagrams, real source code analysis.

## What's Inside

- **16-chapter textbook** dissecting every subsystem of Claude Code (512K LOC)
- **280 real code blocks** with exact file:line references
- **34 diagrams** (AI-generated schematics + matplotlib charts + Mermaid)
- **200-line Python Mini Harness** you can run in 5 minutes
- **Competitor analysis** (Claude Code vs Cursor vs Copilot)
- **Chinese + English** versions with GitHub Pages site

## Quick Start

- [Chinese version (complete)](docs/zh/)
- [English version](docs/en/)
- [GitHub Pages site](https://wanlanglin.github.io/-awesome-cc-harness/)

## Chapters

| # | Title | Depth |
|---|-------|-------|
| 1 | What is Harness Engineering? | Theory + ROI data |
| 2 | Claude Code Architecture | 512K LOC mapped |
| 3 | **The Agent Loop** | queryLoop() with 7 continue sites |
| 4 | **Tool System** | 43+ tools, partition algorithm |
| 5 | **Permission Model** | 6-layer defense-in-depth |
| 6 | **Hooks System** | 26 events × 4 types |
| 7 | Sandbox & Security | FS/network/process isolation |
| 8 | Context Engineering | Memory + 4-level compaction |
| 9-12 | Settings, MCP, Agents, Skills | Deep implementation analysis |
| 13-14 | Practical Guide + Philosophy | 10 design principles |
| 15 | **Hands-on: Mini Harness** | 200-line Python from scratch |
| 16 | **Competitor Analysis** | 12-dimension comparison |

## Related Resources

- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) — Progressive 12-session hands-on course, great for building a harness from scratch step by step
- [claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) — Production-ready Plan→Work→Review plugin for Claude Code
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — Concise conceptual framework on the three pillars
- [arXiv:2603.05344](https://arxiv.org/html/2603.05344v1) — Academic paper on scaffolding vs harness architecture

## License

Educational and research purposes. Claude Code is property of Anthropic, Inc.
