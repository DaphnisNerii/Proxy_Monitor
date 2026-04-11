# Roadmap: Proxy Monitor UX & Analytics

## Overview
v1.1 里程碑专注于提升 Proxy Monitor 的用户体验。我们将弃用传统的 Tkinter 框架，采用现代化的 Flet 框架重新构建界面，并引入基于 SQLite 的历史流量看板。

## Milestones
- ✅ **v1.0 Robustness MVP** — Phases 1-3 (Shipped: 2026-04-11)
- 📋 **v1.1 UX & Analytics** — (Next Up)

## Phases

<details>
<summary>✅ v1.0 Robustness MVP (Phases 1-3) — SHIPPED 2026-04-11</summary>

- [x] **Phase 1: 架构重构与基础自检** — Completed 2026-04-11
- [x] **Phase 2: 自动化测试与逻辑加固** — Completed 2026-04-11
- [x] **Phase 3: 用户反馈与异常处理增强** — Completed 2026-04-11

</details>

### 📋 v1.1 UX & Analytics (Planned)

- [ ] **Phase 4: UI 框架迁移与系统桥接** (UI-MOD-01, ARCH-EXP-04/05)
  - 目标: 引入 Flet，实现 UI 与核心监控逻辑的解耦及托盘通信。
  - 指标: Flet 窗口与托盘共存，基本设置可读取。
- [ ] **Phase 5: 数据持久化与历史统计** (STAT-02, STAT-03)
  - 目标: 引入 SQLite，实现流量数据的历史采集与日/月报统计。
  - 指标: 数据库持久化正常，日志记录无损。
- [ ] **Phase 6: 数据看板与交互打磨** (STAT-01, UI-02, UI-03)
  - 目标: 实现实时流量折线图及侧边栏布局，美化设置反馈。
  - 指标: UI 流畅度提升，数据看板直观。

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. 架构重构与基础自检 | v1.0 | 2/2 | Complete | 2026-04-11 |
| 2. 自动化测试与逻辑加固 | v1.0 | 2/2 | Complete | 2026-04-11 |
| 3. 用户反馈与异常处理增强 | v1.0 | 2/2 | Complete | 2026-04-11 |
| 4. UI 框架迁移与重构 | v1.1 | 0/1 | Not started | - |
| 5. 数据持久化与历史统计 | v1.1 | 0/1 | Not started | - |
| 6. 数据看板与交互打磨 | v1.1 | 0/1 | Not started | - |

---
*Roadmap updated at milestones/v1.1-START.md*
