# Project Retrospective: Proxy Monitor

## Milestone: v1.0 — Robustness MVP

**Shipped:** 2026-04-11
**Phases:** 3 | **Plans:** 6

### What Was Built
- 核心代码重构为模块化结构 (MVC/MVP 雏形)。
- 建立 Pytest 自动化测试套件。
- 增强启动自检与全局异常拦截 UX。

### What Worked
- **NamedMutex 为基础的锁机制**：解决了 Windows 下文件/Socket 锁在程序崩溃后难以释放的问题。
- **Mock 网络请求测试**：非常有效地验证了弱网下的 Exponential Backoff 逻辑。
- **UI 线程拆分**：主线程运行 Tkinter，子线程运行 Pystray 的分工模式解决了多窗口交互卡死。

### What Was Inefficient
- **Traceability Table 更新滞后**：在 Phase 期间没有实时勾选 REQUIREMENTS.md，导致结束时需要大量追溯。
- **Monolith 迁移初期的复杂性**：从单文件迁移到 6 个文件时，由于循环导入 (Circular Import) 出现过几次调试开销，后续可以使用更严格的依赖注入结构。

### Patterns Established
- **PreFlightCheck 模式**：在程序导入 UI 库前先行检查运行环境，极大减少了由于依赖缺失导致的静默失败。

### Key Lessons
- Windows API (ctypes) 的稳定性在底层操作（如锁、注册表）上远超纯 Python 的 hack 手段。
- 在 GUI 开发中，尽早确定谁是主线程 (Main Thread) 对于防止后续死锁至关重要。

---
## Cross-Milestone Trends
| Milestone | Status | Plans | Days | Efficiency |
|-----------|--------|-------|------|------------|
| v1.0 | ✅ | 6 | 3 | High |
