# Claude Code 源码中从未被报道的训练数据基础设施 — Grove 系统

**从用户键盘到 BigQuery 训练数据仓库：一条完整的、可源码验证的数据链路**

> 在逆向分析 Claude Code 512K 行源码的过程中，我发现了一套此前从未被公开报道的训练数据收集基础设施。它不是推测，不是类比——每一步都有精确的文件路径和行号。本文将这条链路完整呈现。

---

## 一句话总结

Anthropic 在 Claude Code 客户端中构建了一套名为 **"Grove"** 的系统，通过 UI 明确告知用户数据将用于 **"train and improve"** 模型，并将数据保留期从 30 天延长至 5 年。所有 analytics 事件通过 Protobuf schema 定义、双路管道传输，最终写入 BigQuery 特权列。同一套管道还嵌入了 SWE-bench 评估字段——意味着训练数据采集和 Agent 能力评估共享同一基础设施。

---

## 第一环：Grove — "Help Improve Claude"

在 Claude Code 的源码中，有一个名为 `Grove` 的组件（`src/components/grove/Grove.tsx`），它向用户展示一个开关：

```typescript
// src/components/grove/Grove.tsx
// Line 47:
<Text bold={true}>You can help improve Claude </Text>

// Line 56 — 关键文案:
"Allow the use of your chats and coding sessions to train and improve
 Anthropic AI models. Change anytime in your Privacy Settings."

// Line 63 — 数据保留变更通知:
"Updates to data retention — To help us improve our AI models and safety
 protections, we're extending data retention to 5 years."

// Line 116 — 保留期的具体影响:
"Turning ON the improve Claude setting extends data retention from
 30 days to 5 years. Turning it OFF keeps the default 30-day data
 retention. Delete data anytime."
```

这不是隐藏的后门。这是 Anthropic 正式的、面向用户的训练数据收集机制。但它的**工程实现**从未被公开分析过。

### Grove 的类型定义

```typescript
// src/services/api/grove.ts Lines 25-35:
export type AccountSettings = {
  grove_enabled: boolean | null       // 用户是否开启 "Help improve Claude"
  grove_notice_viewed_at: string | null
}

export type GroveConfig = {
  grove_enabled: boolean
  domain_excluded: boolean            // 某些组织/域名被排除
  notice_is_grace_period: boolean     // 宽限期内
  notice_reminder_frequency: number | null
}

// API 端点:
// GET  /api/oauth/account/settings
// POST /api/oauth/account/grove_notice_viewed
// PATCH /api/oauth/account/settings
// GET  /api/claude_code_grove
```

**关键细节**：`domain_excluded` 字段意味着某些企业客户的数据被自动排除在训练之外。`grove_enabled` 是一个布尔开关——开启后，你的数据保留期从 30 天变成 **5 年**。

> **为什么是 5 年？** 产品 analytics 通常保留 30-90 天就够了。5 年的保留期只有一个合理解释：这些数据要进入训练数据集，而训练数据集的生命周期远长于运维日志。

---

## 第二环：796 个 Telemetry 事件 × 双路管道

Grove 收集的不是粗粒度的使用统计。Claude Code 源码中包含 **796 个以 `tengu_` 为前缀的唯一 analytics 事件名**。每一次 API 调用、每一次工具执行、每一次权限决策、每一次 Bash 命令——全部被记录。

这些事件通过双路管道传输：

| 通道 | 端点 | 数据内容 | 用途 |
|------|------|---------|------|
| **Datadog** | `logs.us5.datadoghq.com` | 脱敏数据（`_PROTO_*` 字段被剥离） | 运维监控 |
| **1P（第一方）** | `/api/event_logging/batch` | **完整数据**（含特权字段） | 写入 BigQuery |

```typescript
// src/services/analytics/sink.ts Lines 48-71:
function logEventImpl(eventName: string, metadata: LogEventMetadata): void {
  const sampleResult = shouldSampleEvent(eventName)
  if (sampleResult === 0) return

  if (shouldTrackDatadog()) {
    // Datadog 只拿到脱敏数据
    void trackDatadogEvent(eventName, stripProtoFields(metadataWithSampleRate))
  }

  // 1P 拿到完整数据，含 _PROTO_* 特权字段
  logEventTo1P(eventName, metadataWithSampleRate)
}
```

```typescript
// src/services/analytics/firstPartyEventLoggingExporter.ts Lines 714-750:
// _PROTO_* keys are PII-tagged values meant only for privileged BQ
// columns. Hoist known keys to proto fields, then defensively strip any
// remaining _PROTO_* so an unrecognized future key can't silently land
// in the general-access additional_metadata blob.
```

**这段注释直接说明了架构意图**：`_PROTO_*` 字段被路由到 BigQuery 的"特权列"（privileged columns），与普通 analytics 数据**物理隔离**。这不是普通的产品日志——这是一个有意设计的、分级隔离的数据仓库。

---

## 第三环：Protobuf Schema — 生产级数据管道

这些事件不是随意的 JSON blob。它们通过 **Protobuf schema** 严格定义，由外部 monorepo 编译生成：

```typescript
// src/services/analytics/firstPartyEventLoggingExporter.ts:
// Adding a field? Update the monorepo proto first (go/cc-logging):
//   event_schemas/.../claude_code/v1/claude_code_internal_event.proto
// then run `bun run generate:proto` here.
//
//   claude_code_internal_event.ts — 865 行 proto 生成代码
```

生成的 schema 定义了 29 个字段：

```protobuf
message ClaudeCodeInternalEvent {
  string event_name = 1;
  Date   client_timestamp = 2;
  string model = 3;
  string session_id = 4;
  string user_type = 5;                // "ant" vs "external"
  EnvironmentMetadata env = 7;         // 平台、版本、CI 标志等 30+ 子字段
  string additional_metadata = 13;     // 事件特定数据（BASE64 JSON）
  string device_id = 17;

  // ⬇️ 注意这三个字段
  string swe_bench_run_id = 18;
  string swe_bench_instance_id = 19;
  string swe_bench_task_id = 20;

  // Swarm/团队 Agent 归属
  string agent_id = 22;
  string parent_session_id = 23;
  string agent_type = 24;

  // PII 特权列
  string skill_name = 27;
  string plugin_name = 28;
  string marketplace_name = 29;
}
```

**这告诉我们三件事**：

1. **这不是临时的 analytics hack** — Protobuf + 外部 monorepo（`go/cc-logging`）+ 编译时强制 = 生产级数据管道基础设施
2. **SWE-bench 字段嵌入在每个事件中** — 不是单独的 eval 系统，而是和用户数据走**同一条管道**
3. **有专门的 PII 特权列** — `skill_name`、`plugin_name` 被隔离存储，说明数据分级管理

---

## 第四环：SWE-bench — Eval 和训练数据共享管道

这是最让人意外的发现。SWE-bench 的三个 ID 不是在某个单独的 eval 脚本里——它们被嵌入到了**每一个 analytics 事件的 Proto schema 中**。

```typescript
// src/services/analytics/metadata.ts Lines 722-724:
sweBenchRunId:     process.env.SWE_BENCH_RUN_ID || '',
sweBenchInstanceId: process.env.SWE_BENCH_INSTANCE_ID || '',
sweBenchTaskId:    process.env.SWE_BENCH_TASK_ID || '',

// Lines 912-920 — 写入 Proto 事件:
if (coreFields.sweBenchRunId) {
  core.swe_bench_run_id = coreFields.sweBenchRunId
}
```

这意味着：当 Anthropic 内部跑 SWE-bench 时，所有 796 个 `tengu_` 事件都带上了 `swe_bench_run_id` + `swe_bench_instance_id` + `swe_bench_task_id`。在 BigQuery 里，他们可以对每一道 SWE-bench 题做**完整的 Agent 行为轨迹分析**——哪些工具被调用了、每次 API 花了多少 token、权限分类器做了什么决策、命令执行是否成功。

> **含义**：Claude Code 不只是一个产品。它同时是 Anthropic 的 **Agent 能力评估平台**。Eval 数据和用户交互数据通过同一套 Protobuf schema、同一条管道、同一个 BigQuery 数据仓库处理。

配合完整的评估 Harness 接口：

```typescript
// src/main.tsx — 评估相关 CLI 标志:
'-p, --print'              // 非交互模式，输出后退出
'--output-format <format>' // "text" | "json" | "stream-json"
'--max-turns <turns>'      // 最大 Agent 轮次
'--max-budget-usd <amount>'// 预算限制
'--json-schema <schema>'   // 结构化输出验证
```

这构成了一个**完整的评估闭环**：环境变量标识任务 → `--print` 模式非交互执行 → 流式 NDJSON 输出 → 退出码判断成功/失败 → 所有过程数据通过 telemetry 写入 BigQuery。

---

## 第五环：开发者注释 — "Training Data"

最后，两条开发者内部注释提供了最直接的证据：

```typescript
// src/utils/messages.ts Line 245:
"content is fake, which poisons training data if submitted"

// src/utils/sessionStorage.ts Line 4388:
"Ant transcripts keep the wrapper so /share training data sees REPL usage"
```

第一条说某些内容"会毒化训练数据"——开发者**已知**消息内容会进入训练管道。

第二条说 `/share` 的数据被视为 "training data"——这是**最直接的文字证据**。

---

## 第六环：五层性能测量

除了功能数据，Anthropic 还在 Claude Code 中嵌入了五层性能测量系统：

| 层级 | 实现 | 采样率 | 输出目标 |
|------|------|--------|---------|
| Headless Latency Profiler | `headlessProfiler.ts` | 100% 内部 / 5% 外部 | `tengu_headless_latency` 事件 |
| Frame Timing | `interactiveHelpers.tsx` | 按需启用 | JSONL 本地文件 |
| FPS Tracker | `fpsTracker.ts` | 持续 | avgFps + P99 帧时间 |
| Perfetto Chrome Trace | `perfettoTracing.ts` | **仅内部** | `~/.claude/traces/` |
| OpenTelemetry | `instrumentation.ts` | 持续 | OTLP / Prometheus / **BigQuery** |

注意最后一层：OpenTelemetry 的导出器列表中包含 **BigQuery**。性能数据也流入了同一个数据仓库。

---

## 第七环：竞品检测

一个有趣的小发现：

```typescript
// src/utils/codeIndexing.ts Line 52, 82:
// 检测 aider CLI 和 MCP 服务器
// CLI: 'aider'
// MCP: /^aider$/i
// 用途: analytics 中跟踪 Claude Code 与竞品的共存使用模式
```

Anthropic 在 telemetry 中追踪用户是否同时使用竞品工具（Aider）。这些数据同样流入 BigQuery。

---

## 完整链路图

```
用户交互（每次工具调用、API 请求、Bash 命令）
  │
  ├─ grove_enabled = true → 数据保留 5 年
  │
  ▼
796 个 tengu_* 事件 × 40+ 元数据字段
  │
  ├─→ Datadog（脱敏，_PROTO_* 剥离）→ 运维监控
  │
  └─→ 1P API /api/event_logging/batch（完整数据）
       │
       ├─ Protobuf schema 严格定义（865 行生成代码）
       ├─ _PROTO_* 字段 → BigQuery 特权列（隔离存储）
       ├─ SWE-bench ID 嵌入 → eval 数据同管道
       │
       ▼
     BigQuery 数据仓库
       │
       ├─ 反馈文本 "approved for BQ"（PII 脱敏后）
       ├─ 转录共享 → POST /api/claude_code_shared_session_transcripts
       ├─ OpenTelemetry 性能数据
       ├─ 竞品使用检测
       │
       ▼
     开发者注释确认："training data"
       │
       ▼
     ???? （后端训练过程，客户端不可见）
```

---

## 这条链路为什么重要

1. **它是完整的**：从 UI 开关到 BigQuery 特权列，每一环都有源码行号
2. **它是分级的**：Datadog 拿脱敏数据，1P 拿完整数据，BigQuery 有特权列隔离
3. **它是复用的**：eval（SWE-bench）和用户数据走同一条管道，同一个 schema
4. **它不是推测**：Grove UI 明确写着 "train and improve"，开发者注释明确说 "training data"
5. **它从未被报道**：截至本文发布，没有任何公开分析提到过 "Grove 系统"、BigQuery 特权列、或 SWE-bench 与 telemetry 共管道这些发现

---

## 我们不知道的

诚实地说，以下内容**无法从客户端源码确认**：

- Anthropic 具体用什么方法训练（RLHF？DPO？GRPO？）
- BigQuery 中的数据如何被预处理和过滤
- SWE-bench eval 数据是否直接用于训练，还是仅用于评估
- 偏好对是如何在后端组装的（客户端没有 preference pair 构建代码）

但这些"不知道"并不影响核心结论：**从用户键盘到 BigQuery 训练数据仓库的完整数据链路，在客户端源码中是可验证的。**

---

## 后续

目前正在分析潜在可能支撑 Anthropic 收集训练数据的更多基础设施，包括疑似 reward 工程、YOLO 分类器的安全信息隔离设计等。持续更新中。

---

*本文所有代码引用来自 Claude Code 源码（2026-03-31 snapshot）。文件路径和行号均为实际源码位置。*

*完整教程（16 章 · ~50,000 字）：[GitHub](https://github.com/WanLanglin/-awesome-cc-harness)*

*作者：WanLanglin · 微信: felixwll*
