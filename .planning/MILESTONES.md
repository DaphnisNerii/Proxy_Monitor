# Milestones

## v1.0 Robustness MVP (Shipped: 2026-04-11)

**Phases completed:** 3 phases, 6 plans, 11 tasks

**Key accomplishments:**

1. **核心逻辑模块化** — 成功将单文件脚本拆分为 6 个高内聚模块。
2. **UI 线程死锁修复** — 解决 Tkinter 与 pystray 的线程冲突问题。
3. **健壮的单实例锁** — 引入基于 ctypes 的 NamedMutex 锁，稳定性优于 Socket。
4. **全自动化测试** — 覆盖核心配置与网络逻辑，Pytest 全绿通过。
5. **用户交互反馈** — 实现全局异常弹窗、配置气泡通知与启动环境自检。

---

