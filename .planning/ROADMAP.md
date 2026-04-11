# Roadmap: Proxy Monitor UX & Analytics

## Overview
v1.1 里程碑专注于提升 Proxy Monitor 的用户体验。我们将弃用传统的 Tkinter 框架，采用现代化的 Flet 框架重新构建界面，并引入基于 SQLite 的历史流量看板。

## Milestones
- ✅ **v1.0 Robustness MVP** — Phases 1-3 (Shipped: 2026-04-11)
- ✅ **v1.1 UX & Analytics** — (Shipped: 2026-04-11)

## Phases

<details>
<summary>✅ v1.0 Robustness MVP (Phases 1-3) — SHIPPED 2026-04-11</summary>

- [x] **Phase 1: 架构重构与基础自检** — Completed 2026-04-11
- [x] **Phase 2: 自动化测试与逻辑加固** — Completed 2026-04-11
- [x] **Phase 3: 用户反馈与异常处理增强** — Completed 2026-04-11

</details>

<details open>
<summary>✅ v1.1 UX & Analytics (Phases 4-6) — SHIPPED 2026-04-11</summary>

- [x] **Phase 4: UI 框架迁移与系统桥接** — Completed 2026-04-11
- [x] **Phase 5: 数据持久化与历史统计** — Completed 2026-04-11
- [x] **Phase 6: 数据看板与交互打磨** — Completed 2026-04-11

</details>

### Phase 4: UI 框架迁移与系统桥接
- **Goal**: 引入 Flet，实现 UI 与核心监控逻辑的解耦及托盘通信。
- **Requirements**: UI-MOD-01, ARCH-EXP-04, ARCH-EXP-05
- **Downstream**: Phase 5, Phase 6

### Phase 5: 数据持久化与历史统计
- **Goal**: 引入 SQLite，实现流量数据的历史采集与日/月报统计。
- **Requirements**: STAT-02, STAT-03
- **Downstream**: Phase 6

### Phase 6: 数据看板与交互打磨
- **Goal**: 实现实时流量折线图及侧边栏布局，美化设置反馈。
- **Requirements**: STAT-01, UI-02, UI-03

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. 架构重构与基础自检 | v1.0 | 2/2 | Complete | 2026-04-11 |
| 2. 自动化测试与逻辑加固 | v1.0 | 2/2 | Complete | 2026-04-11 |
| 3. 用户反馈与异常处理增强 | v1.0 | 2/2 | Complete | 2026-04-11 |
| 4. UI 框架迁移与系统桥接 | v1.1 | 1/1 | Complete | 2026-04-11 |
| 5. 数据持久化与历史统计 | v1.1 | 1/1 | Complete | 2026-04-11 |
| 6. 数据看板与交互打磨 | v1.1 | 1/1 | Complete | 2026-04-11 |

---
*Roadmap updated at milestones/v1.1-START.md*
