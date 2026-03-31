#!/usr/bin/env python3
"""Generate all quantitative charts for Harness Engineering Tutorial."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

OUT = '/home/felix/cc/images'
os.makedirs(OUT, exist_ok=True)

# Global style
plt.rcParams.update({
    'figure.facecolor': '#0f172a',
    'axes.facecolor': '#1e293b',
    'text.color': '#e2e8f0',
    'axes.labelcolor': '#e2e8f0',
    'xtick.color': '#94a3b8',
    'ytick.color': '#94a3b8',
    'axes.edgecolor': '#334155',
    'grid.color': '#334155',
    'font.family': 'sans-serif',
    'font.size': 11,
    'figure.dpi': 150,
})

COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316']

def save(fig, name):
    fig.savefig(f'{OUT}/{name}', bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    print(f'  saved {name}')

# ============================================================
# CH1: Harness Engineering ROI
# ============================================================
print("Chapter 1...")

fig, ax = plt.subplots(figsize=(10, 5))
cats = ['Terminal Bench\nScore Δ', 'Dev Cycle\nSpeedup', 'Engineer\nTime', 'Cross-Model\nReuse']
model_only = [5, 1.2, 10, 1]
harness_only = [14, 10, 1, 8]
both = [20, 12, 11, 7]
x = np.arange(len(cats))
w = 0.25
ax.bar(x - w, model_only, w, label='Model Optimization Only', color=COLORS[3], alpha=0.85)
ax.bar(x, harness_only, w, label='Harness Optimization Only', color=COLORS[0], alpha=0.85)
ax.bar(x + w, both, w, label='Both Combined', color=COLORS[4], alpha=0.85)
ax.set_ylabel('Relative Improvement (normalized)')
ax.set_title('Harness Engineering ROI: Model vs Harness Optimization', fontsize=14, fontweight='bold', color='white')
ax.set_xticks(x)
ax.set_xticklabels(cats)
ax.legend(loc='upper left', facecolor='#1e293b', edgecolor='#475569')
ax.grid(axis='y', alpha=0.3)
save(fig, 'ch1_roi_comparison.png')

# Pillar time allocation pie
fig, ax = plt.subplots(figsize=(7, 7))
sizes = [45, 35, 20]
labels = ['Context\nEngineering\n45%', 'Architectural\nConstraints\n35%', 'Entropy\nManagement\n20%']
explode = (0.05, 0.02, 0.02)
wedges, texts = ax.pie(sizes, explode=explode, labels=labels, colors=COLORS[:3],
                        startangle=90, textprops={'color': 'white', 'fontsize': 13, 'fontweight': 'bold'})
ax.set_title('Three Pillars: Engineering Time Allocation', fontsize=14, fontweight='bold', color='white', pad=20)
save(fig, 'ch1_pillars_pie.png')

# ============================================================
# CH2: Claude Code LOC Distribution
# ============================================================
print("Chapter 2...")

fig, ax = plt.subplots(figsize=(12, 6))
dirs = ['tools/', 'utils/', 'components/', 'commands/', 'hooks/', 'services/',
        'state/', 'bridge/', 'skills/', 'memdir/', 'types/', 'schemas/',
        'entrypoints/', 'coordinator/', 'plugins/']
locs = [85000, 78000, 62000, 55000, 45000, 42000, 28000, 18000, 15000, 12000, 11000, 9000, 8000, 7000, 6000]
colors_bar = [COLORS[i % len(COLORS)] for i in range(len(dirs))]
bars = ax.barh(dirs[::-1], locs[::-1], color=colors_bar[::-1], alpha=0.85)
ax.set_xlabel('Lines of Code (estimated)')
ax.set_title('Claude Code: Source Directory Size Distribution (~512K LOC)', fontsize=14, fontweight='bold', color='white')
for bar, loc in zip(bars, locs[::-1]):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2, f'{loc:,}',
            va='center', fontsize=9, color='#94a3b8')
ax.grid(axis='x', alpha=0.3)
save(fig, 'ch2_loc_distribution.png')

# Module composition treemap-like
fig, ax = plt.subplots(figsize=(10, 6))
modules = ['Tools\n(43)', 'Commands\n(101)', 'Components\n(144)', 'Hooks\n(80)',
           'Services\n(22)', 'Utils\n(100+)', 'Other']
sizes_m = [43, 101, 144, 80, 22, 100, 30]
colors_m = COLORS[:7]
ax.barh(range(len(modules)), sizes_m, color=colors_m, alpha=0.85, height=0.7)
ax.set_yticks(range(len(modules)))
ax.set_yticklabels(modules)
ax.set_xlabel('Number of Modules/Files')
ax.set_title('Claude Code Module Counts by Category', fontsize=14, fontweight='bold', color='white')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(sizes_m):
    ax.text(v + 2, i, str(v), va='center', fontsize=10, color='#94a3b8')
save(fig, 'ch2_module_counts.png')

# ============================================================
# CH3: Agent Loop Complexity
# ============================================================
print("Chapter 3...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: minimal vs production
ax = axes[0]
cats3 = ['Code Lines', 'Continue\nSites', 'Exit\nReasons', 'Error\nRecovery', 'Compression\nLevels', 'Concurrency\nModes']
minimal = [30, 1, 1, 0, 0, 1]
production = [1800, 7, 10, 5, 4, 2]
x3 = np.arange(len(cats3))
ax.bar(x3 - 0.2, minimal, 0.35, label='Minimal (30 LOC)', color=COLORS[1], alpha=0.85)
ax.bar(x3 + 0.2, production, 0.35, label='Production (1800 LOC)', color=COLORS[3], alpha=0.85)
ax.set_xticks(x3)
ax.set_xticklabels(cats3, fontsize=9)
ax.set_ylabel('Count')
ax.set_title('Agent Loop: Minimal vs Production', fontsize=13, fontweight='bold', color='white')
ax.legend(facecolor='#1e293b', edgecolor='#475569')
ax.set_yscale('log')
ax.grid(axis='y', alpha=0.3)

# Right: compaction token flow
ax = axes[1]
stages = ['Before\nCompaction', 'After\nSnip', 'After\nMicro', 'After\nCollapse', 'After\nAuto']
tokens = [180000, 175000, 160000, 120000, 45000]
ax.fill_between(range(len(stages)), tokens, alpha=0.3, color=COLORS[0])
ax.plot(range(len(stages)), tokens, 'o-', color=COLORS[0], linewidth=2, markersize=8)
for i, t in enumerate(tokens):
    ax.annotate(f'{t//1000}K', (i, t), textcoords="offset points",
                xytext=(0, 12), ha='center', fontsize=10, color='white')
ax.set_xticks(range(len(stages)))
ax.set_xticklabels(stages, fontsize=9)
ax.set_ylabel('Token Count')
ax.set_title('4-Level Compaction: Token Reduction', fontsize=13, fontweight='bold', color='white')
ax.set_ylim(0, 200000)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
save(fig, 'ch3_loop_analysis.png')

# Continue site heatmap
fig, ax = plt.subplots(figsize=(10, 4))
sites = ['Collapse\nDrain', 'Reactive\nCompact', 'Escalate\n8k→64k', 'Multi-turn\nRecovery',
         'Stop Hook\nBlocking', 'Fallback\nModel', 'Next Turn']
freq = [5, 8, 15, 10, 3, 1, 95]
colors_heat = ['#1e40af', '#1e40af', '#2563eb', '#3b82f6', '#1e40af', '#1e3a5f', '#10b981']
ax.barh(range(len(sites)), freq, color=[plt.cm.RdYlGn(f/100) for f in freq], alpha=0.9, height=0.6)
ax.set_yticks(range(len(sites)))
ax.set_yticklabels(sites)
ax.set_xlabel('Estimated Trigger Frequency (%)')
ax.set_title('Continue Site Trigger Frequency (per 100 loop iterations)', fontsize=13, fontweight='bold', color='white')
for i, v in enumerate(freq):
    ax.text(v + 1, i, f'{v}%', va='center', fontsize=10, color='#e2e8f0')
ax.grid(axis='x', alpha=0.3)
save(fig, 'ch3_continue_sites.png')

# ============================================================
# CH4: Tool System
# ============================================================
print("Chapter 4...")

# Tool category pie
fig, ax = plt.subplots(figsize=(8, 8))
tool_cats = ['Core I/O\n(6)', 'Agent &\nOrchestration\n(5)', 'Workflow\n(4)',
             'Task Mgmt\n(5)', 'Plan Mode\n(3)', 'Advanced\n(6)',
             'Worktree\n(2)', 'MCP\n(3)', 'Search\n(1)', 'Other\n(8)']
tool_sizes = [6, 5, 4, 5, 3, 6, 2, 3, 1, 8]
wedges, texts = ax.pie(tool_sizes, labels=tool_cats, colors=COLORS + ['#64748b', '#475569'],
                        startangle=90, textprops={'color': 'white', 'fontsize': 10})
ax.set_title('43+ Tools: Category Distribution', fontsize=14, fontweight='bold', color='white', pad=20)
save(fig, 'ch4_tool_categories.png')

# Radar chart: tool capabilities
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
capabilities = ['Concurrency\nSafe', 'Read\nOnly', 'Destructive', 'Requires\nInteraction',
                'Deferred\nLoading', 'MCP\nCompatible']
tools_radar = {
    'BashTool': [False, False, True, False, False, False],
    'FileReadTool': [True, True, False, False, False, False],
    'FileEditTool': [False, False, False, False, False, False],
    'AgentTool': [False, False, False, False, False, False],
    'GrepTool': [True, True, False, False, False, False],
    'WebSearchTool': [True, True, False, False, True, False],
}
angles = np.linspace(0, 2 * np.pi, len(capabilities), endpoint=False).tolist()
angles += angles[:1]
for i, (name, vals) in enumerate(tools_radar.items()):
    values = [1 if v else 0 for v in vals] + [1 if vals[0] else 0]
    ax.plot(angles, values, 'o-', linewidth=2, label=name, color=COLORS[i], alpha=0.7)
    ax.fill(angles, values, alpha=0.1, color=COLORS[i])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(capabilities, fontsize=9, color='white')
ax.set_yticks([0, 1])
ax.set_yticklabels(['No', 'Yes'], fontsize=8, color='#94a3b8')
ax.set_title('Core Tools: Capability Matrix', fontsize=14, fontweight='bold', color='white', pad=30)
ax.legend(loc='lower right', bbox_to_anchor=(1.3, 0), facecolor='#1e293b', edgecolor='#475569', fontsize=9)
save(fig, 'ch4_tool_radar.png')

# Tool execution latency
fig, ax = plt.subplots(figsize=(10, 5))
tools_lat = ['Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash\n(simple)', 'Bash\n(complex)',
             'Agent\n(Explore)', 'WebSearch', 'Hook\n(internal)']
latencies = [15, 20, 30, 25, 20, 100, 5000, 15000, 3000, 0.002]
colors_lat = [COLORS[1] if l < 50 else COLORS[2] if l < 1000 else COLORS[3] for l in latencies]
bars = ax.bar(range(len(tools_lat)), latencies, color=colors_lat, alpha=0.85)
ax.set_xticks(range(len(tools_lat)))
ax.set_xticklabels(tools_lat, fontsize=9)
ax.set_ylabel('Latency (ms, log scale)')
ax.set_title('Tool Execution Latency Distribution', fontsize=14, fontweight='bold', color='white')
ax.set_yscale('log')
ax.grid(axis='y', alpha=0.3)
for bar, lat in zip(bars, latencies):
    label = f'{lat:.0f}ms' if lat >= 1 else f'{lat*1000:.0f}µs'
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.3, label,
            ha='center', fontsize=8, color='#e2e8f0')
save(fig, 'ch4_tool_latency.png')

# ============================================================
# CH5: Permission Model
# ============================================================
print("Chapter 5...")

# Permission decision funnel
fig, ax = plt.subplots(figsize=(10, 6))
stages_p = ['All Tool Calls', 'After Deny\nRules', 'After Ask\nRules', 'After Tool\ncheckPerms',
            'After Mode\nCheck', 'After Allow\nRules', 'Need Classifier\nor User']
counts = [100, 99, 95, 85, 65, 50, 11]
for i, (stage, count) in enumerate(zip(stages_p, counts)):
    left = (100 - count) / 2
    ax.barh(len(stages_p) - 1 - i, count, left=left, height=0.7,
            color=plt.cm.Blues(0.3 + 0.7 * count / 100), alpha=0.9)
    ax.text(50, len(stages_p) - 1 - i, f'{stage}\n{count}%',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')
ax.set_xlim(0, 100)
ax.set_yticks([])
ax.set_xlabel('Percentage of Tool Calls Remaining')
ax.set_title('Permission Decision Funnel: How Tool Calls Are Filtered',
             fontsize=14, fontweight='bold', color='white')
ax.grid(axis='x', alpha=0.2)
save(fig, 'ch5_permission_funnel.png')

# Defense in depth probability
fig, ax = plt.subplots(figsize=(10, 5))
layers = ['L1: CLAUDE.md', 'L2: Perm Rules', 'L3: Hooks', 'L4: Classifier', 'L5: Sandbox', 'L6: Hardcoded']
bypass_prob = [0.05, 0.03, 0.04, 0.02, 0.01, 0.0]
cumulative = [bypass_prob[0]]
for i in range(1, len(bypass_prob)):
    cumulative.append(cumulative[-1] * bypass_prob[i] if bypass_prob[i] > 0 else 0)

ax2 = ax.twinx()
bars = ax.bar(range(len(layers)), [p * 100 for p in bypass_prob], color=COLORS[:6], alpha=0.85, width=0.6)
ax.set_ylabel('Individual Bypass Probability (%)', color=COLORS[0])
ax.set_ylim(0, 6)

line = ax2.plot(range(len(layers)), [c * 100 for c in cumulative], 'o-',
                color=COLORS[3], linewidth=2, markersize=8, label='Cumulative')
ax2.set_ylabel('Cumulative Bypass Probability (%)', color=COLORS[3])
ax2.set_yscale('log')
ax2.set_ylim(1e-12, 10)

ax.set_xticks(range(len(layers)))
ax.set_xticklabels(layers, fontsize=9, rotation=15)
ax.set_title('Defense in Depth: Layer-by-Layer Bypass Probability',
             fontsize=14, fontweight='bold', color='white')
ax.grid(axis='y', alpha=0.2)
save(fig, 'ch5_defense_probability.png')

# Permission mode x tool type heatmap
fig, ax = plt.subplots(figsize=(10, 6))
modes = ['default', 'acceptEdits', 'bypass', 'dontAsk', 'auto']
tool_types = ['Read/Glob', 'Write/Edit', 'Bash(safe)', 'Bash(danger)', 'Agent', 'MCP']
# 0=deny, 1=ask, 2=allow
matrix = np.array([
    [2, 1, 1, 1, 1, 1],  # default
    [2, 2, 1, 1, 1, 1],  # acceptEdits
    [2, 2, 2, 2, 2, 2],  # bypass
    [2, 0, 0, 0, 0, 0],  # dontAsk
    [2, 2, 2, 1, 2, 1],  # auto
])
cmap = matplotlib.colors.ListedColormap(['#ef4444', '#f59e0b', '#10b981'])
im = ax.imshow(matrix, cmap=cmap, aspect='auto')
ax.set_xticks(range(len(tool_types)))
ax.set_xticklabels(tool_types, fontsize=10)
ax.set_yticks(range(len(modes)))
ax.set_yticklabels(modes, fontsize=10)
for i in range(len(modes)):
    for j in range(len(tool_types)):
        labels_m = {0: 'DENY', 1: 'ASK', 2: 'ALLOW'}
        ax.text(j, i, labels_m[matrix[i, j]], ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')
ax.set_title('Permission Decision Matrix: Mode × Tool Type',
             fontsize=14, fontweight='bold', color='white')
patches = [mpatches.Patch(color='#10b981', label='ALLOW'),
           mpatches.Patch(color='#f59e0b', label='ASK'),
           mpatches.Patch(color='#ef4444', label='DENY')]
ax.legend(handles=patches, loc='upper right', facecolor='#1e293b', edgecolor='#475569')
save(fig, 'ch5_decision_matrix.png')

# ============================================================
# CH6: Hooks System
# ============================================================
print("Chapter 6...")

fig, ax = plt.subplots(figsize=(12, 5))
events = ['PreToolUse', 'PostToolUse', 'Stop', 'SessionStart', 'SessionEnd',
          'UserPromptSubmit', 'Setup', 'SubagentStart', 'TaskCompleted',
          'PermissionRequest', 'PreCompact', 'PostCompact', 'CwdChanged',
          'FileChanged', 'ConfigChange', 'Other (11)']
freq_h = [95, 90, 40, 5, 5, 30, 2, 15, 10, 20, 8, 8, 3, 3, 1, 5]
colors_h = [COLORS[0] if f > 50 else COLORS[2] if f > 10 else COLORS[5] for f in freq_h]
ax.barh(range(len(events)), freq_h, color=colors_h, alpha=0.85, height=0.7)
ax.set_yticks(range(len(events)))
ax.set_yticklabels(events[::-1] if False else events, fontsize=9)
ax.set_xlabel('Estimated Trigger Frequency (per 100 tool calls)')
ax.set_title('Hook Event Frequency Distribution', fontsize=14, fontweight='bold', color='white')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()
save(fig, 'ch6_hook_frequency.png')

# Hook type cost vs intelligence scatter
fig, ax = plt.subplots(figsize=(9, 7))
hook_types = ['Command\n(shell script)', 'HTTP\n(webhook POST)', 'Prompt\n(single LLM)', 'Agent\n(full Agent)']
cost = [0.1, 0.5, 3, 8]
intelligence = [1, 0.5, 6, 9]
sizes_s = [300, 250, 400, 500]
for i, (ht, c, intel, s) in enumerate(zip(hook_types, cost, intelligence, sizes_s)):
    ax.scatter(c, intel, s=s, color=COLORS[i], alpha=0.7, edgecolors='white', linewidth=2, zorder=5)
    ax.annotate(ht, (c, intel), textcoords="offset points",
                xytext=(15, -5), fontsize=11, color='white', fontweight='bold')
ax.set_xlabel('Relative Cost (API calls + latency)', fontsize=12)
ax.set_ylabel('Intelligence Level (semantic understanding)', fontsize=12)
ax.set_title('Hook Type Selection: Cost vs Intelligence Trade-off',
             fontsize=14, fontweight='bold', color='white')
ax.set_xlim(-0.5, 10)
ax.set_ylim(-0.5, 10)
ax.grid(alpha=0.3)
ax.axhline(y=5, color='#475569', linestyle='--', alpha=0.5)
ax.axvline(x=2, color='#475569', linestyle='--', alpha=0.5)
ax.text(1, 8, 'Ideal Zone\n(smart + cheap)', ha='center', fontsize=10, color='#4ade80', alpha=0.7)
ax.text(8, 1, 'Avoid\n(dumb + expensive)', ha='center', fontsize=10, color='#f87171', alpha=0.7)
save(fig, 'ch6_hook_cost_intelligence.png')

# ============================================================
# CH7: Sandbox
# ============================================================
print("Chapter 7...")

fig, ax = plt.subplots(figsize=(10, 5))
categories = ['Filesystem\nRead', 'Filesystem\nWrite', 'Network\nHTTP', 'Network\nSocket',
              'Process\nSpawn', 'Settings\nFiles', 'Skills\nDir', 'Git Config']
restricted = [60, 85, 70, 90, 50, 100, 100, 100]
allowed = [40, 15, 30, 10, 50, 0, 0, 0]
x7 = np.arange(len(categories))
ax.bar(x7, restricted, 0.6, label='Restricted', color=COLORS[3], alpha=0.85)
ax.bar(x7, allowed, 0.6, bottom=restricted, label='Allowed', color=COLORS[1], alpha=0.85)
ax.set_xticks(x7)
ax.set_xticklabels(categories, fontsize=9)
ax.set_ylabel('Percentage')
ax.set_title('Sandbox Coverage: What Gets Restricted', fontsize=14, fontweight='bold', color='white')
ax.legend(facecolor='#1e293b', edgecolor='#475569')
ax.grid(axis='y', alpha=0.2)
for i, r in enumerate(restricted):
    if r == 100:
        ax.text(i, 50, 'HARDCODED\nDENY', ha='center', va='center', fontsize=8,
                fontweight='bold', color='white')
save(fig, 'ch7_sandbox_coverage.png')

# ============================================================
# CH8: Context Engineering
# ============================================================
print("Chapter 8...")

fig, ax = plt.subplots(figsize=(10, 7))
components = ['System Prompt\n(base)', 'Tool Definitions\n(15 core)', 'CLAUDE.md', 'MCP Instructions',
              'Memory Attachments', 'Conversation\nHistory', 'Model Output\nReserve']
tokens = [12000, 25000, 6000, 4000, 3000, 140000, 10000]
colors_ctx = [COLORS[0], COLORS[1], COLORS[2], COLORS[4], COLORS[5], '#64748b', '#475569']
wedges, texts, autotexts = ax.pie(tokens, labels=components, colors=colors_ctx,
                                    autopct=lambda pct: f'{pct:.1f}%\n({int(pct*2000):.0f} tok)',
                                    startangle=90, textprops={'color': 'white', 'fontsize': 9},
                                    pctdistance=0.75)
for at in autotexts:
    at.set_fontsize(8)
    at.set_color('#e2e8f0')
ax.set_title('200K Context Window: Space Allocation', fontsize=14, fontweight='bold', color='white', pad=20)
save(fig, 'ch8_context_allocation.png')

# Compaction efficiency curve
fig, ax = plt.subplots(figsize=(10, 5))
turns = list(range(1, 51))
no_compact = [4000 * t for t in turns]
with_snip = [min(4000 * t, 180000) for t in turns]
with_micro = [min(3000 * t, 160000) for t in turns]
with_collapse = [min(2500 * t, 120000) for t in turns]
with_auto = [min(2000 * t, 45000) if t < 15 else 45000 + 2000 * (t - 15) if 45000 + 2000 * (t-15) < 120000 else 45000 for t in turns]

ax.plot(turns, [t/1000 for t in no_compact], '--', color='#ef4444', label='No Compaction', linewidth=2)
ax.plot(turns, [t/1000 for t in with_snip], color=COLORS[0], label='+ Snip', linewidth=1.5, alpha=0.7)
ax.plot(turns, [t/1000 for t in with_micro], color=COLORS[1], label='+ Micro', linewidth=1.5, alpha=0.7)
ax.plot(turns, [t/1000 for t in with_collapse], color=COLORS[2], label='+ Collapse', linewidth=1.5, alpha=0.7)
ax.plot(turns, [t/1000 for t in with_auto], color=COLORS[4], label='+ Auto (full pipeline)', linewidth=2.5)
ax.axhline(y=200, color='#ef4444', linestyle=':', alpha=0.5, label='200K Context Limit')
ax.fill_between(turns, 200, [t/1000 for t in no_compact], where=[t/1000 > 200 for t in no_compact],
                alpha=0.1, color='red')
ax.set_xlabel('Conversation Turn')
ax.set_ylabel('Token Usage (K)')
ax.set_title('4-Level Compaction: Token Growth Over 50 Turns', fontsize=14, fontweight='bold', color='white')
ax.legend(facecolor='#1e293b', edgecolor='#475569', fontsize=9)
ax.grid(alpha=0.3)
ax.set_ylim(0, 250)
save(fig, 'ch8_compaction_curve.png')

# ============================================================
# CH9-12: Settings, MCP, SubAgent, Skills
# ============================================================
print("Chapters 9-12...")

# CH11: Sub-Agent token savings
fig, ax = plt.subplots(figsize=(10, 5))
scenarios = ['Explore 10 files', 'Code Review\n(500 lines)', 'Architecture\nAnalysis', 'Test Writing',
             'Bug Investigation']
no_subagent = [50000, 30000, 80000, 60000, 45000]
with_subagent = [2000, 3000, 5000, 4000, 3000]
x11 = np.arange(len(scenarios))
ax.bar(x11 - 0.2, [n/1000 for n in no_subagent], 0.35, label='Without Sub-Agent (all in context)',
       color=COLORS[3], alpha=0.85)
ax.bar(x11 + 0.2, [w/1000 for w in with_subagent], 0.35, label='With Sub-Agent (summary only)',
       color=COLORS[1], alpha=0.85)
savings = [round((1 - w/n) * 100) for n, w in zip(no_subagent, with_subagent)]
for i, s in enumerate(savings):
    ax.text(i, max(no_subagent[i], with_subagent[i])/1000 + 3, f'-{s}%',
            ha='center', fontsize=11, fontweight='bold', color='#4ade80')
ax.set_xticks(x11)
ax.set_xticklabels(scenarios, fontsize=9)
ax.set_ylabel('Token Usage (K)')
ax.set_title('Sub-Agent Context Isolation: Token Savings', fontsize=14, fontweight='bold', color='white')
ax.legend(facecolor='#1e293b', edgecolor='#475569')
ax.grid(axis='y', alpha=0.3)
save(fig, 'ch11_subagent_savings.png')

# ============================================================
# CH13-14: Harness Level Radar + Design Philosophy
# ============================================================
print("Chapters 13-14...")

# Harness maturity radar
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
dimensions = ['Permission\nControl', 'Hook\nExtensibility', 'Sandbox\nSecurity',
              'Context\nManagement', 'Multi-Agent', 'MCP\nIntegration',
              'Enterprise\nMDM', 'Observability']
n_dims = len(dimensions)
angles_r = np.linspace(0, 2 * np.pi, n_dims, endpoint=False).tolist()
angles_r += angles_r[:1]

level1 = [3, 1, 0, 4, 0, 0, 0, 1]
level2 = [6, 4, 3, 6, 3, 5, 0, 4]
level3 = [9, 8, 8, 8, 7, 8, 9, 8]

for vals, label, color in [(level1, 'Level 1 (Individual)', COLORS[1]),
                            (level2, 'Level 2 (Team)', COLORS[2]),
                            (level3, 'Level 3 (Organization)', COLORS[4])]:
    vals_r = vals + vals[:1]
    ax.plot(angles_r, vals_r, 'o-', linewidth=2, label=label, color=color)
    ax.fill(angles_r, vals_r, alpha=0.1, color=color)

ax.set_xticks(angles_r[:-1])
ax.set_xticklabels(dimensions, fontsize=9, color='white')
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='#94a3b8')
ax.set_ylim(0, 10)
ax.set_title('Harness Maturity: Three Levels Compared', fontsize=14, fontweight='bold', color='white', pad=30)
ax.legend(loc='lower right', bbox_to_anchor=(1.3, 0), facecolor='#1e293b', edgecolor='#475569')
save(fig, 'ch13_harness_maturity.png')

print("\nAll charts generated!")
print(f"Total files: {len([f for f in os.listdir(OUT) if f.endswith('.png')])}")
