# Requirements: Proxy Monitor Robustness & Testing

**Defined:** 2026-04-11
**Core Value:** 为 Windows 用户提供一个零缺陷、高度可靠且具备极佳反馈机制的代理流量监控工具。

## v1 Requirements (当前迭代)

### ARCH: 架构重构 (模块化)
- [ ] **ARCH-01**: 将单文件 `proxy_monitor.pyw` 拆分为逻辑独立的模块（如 `config_manager.py`, `traffic_monitor.py`, `gui_window.py`, `tray_icon.py`）。
- [ ] **ARCH-02**: 消除全局变量，改用依赖注入或配置对象进行状态传递。
- [ ] **ARCH-03**: 实现 GUI 与逻辑层的完全解耦，确保逻辑层不导入 `tkinter` 或 `pystray`。

### TEST: 自动化测试
- [ ] **TEST-01**: 建立基于 `pytest` 的测试环境。
- [ ] **TEST-02**: 实现对 `winreg`（注册表）的 Mock 单元测试，验证开机自启逻辑。
- [ ] **TEST-03**: 实现对 `socket` 的 Mock 单元测试，验证单实例锁逻辑。
- [ ] **TEST-04**: 模拟多种网络异常（超时、404、Header 缺失），验证流量分析引擎的健壮性。

### UX: 用户反馈与体验
- [ ] **UX-01**: 增强配置更改后的实时刷新感知（如托盘图标闪烁或 Tooltip 立即更新）。
- [ ] **UX-02**: 实现关键错误（如依赖库缺失、网络持续失败）的友好弹窗提示，而非静默崩溃。
- [ ] **UX-03**: 优化启动时的静默检测，若检测到环境问题（如无 Python 环境、库未安装且自动安装失败），提供清晰的排错手册链接。

### ROB: 健壮性增强
- [ ] **ROB-01**: 改进 `subscription-userinfo` 正则解析，支持更多厂商的 Header 格式变体。
- [ ] **ROB-02**: 优化单实例检测逻辑，确保程序在非正常退出（如崩溃）后能通过清理残留 Socket 成功重启。
- [ ] **ROB-03**: 增加 `Pre-flight` 启动自检流程，在导入重型依赖前先验证环境。

## v2 Requirements (未来规划)
- **NOTI-01**: 支持更多推送平台（如 Bark, PushDeer）。
- **STAT-01**: 增加更详细的历史流量分析图表。
- **UPDT-01**: 引入自动检查更新功能。

## Out of Scope (不在本次范围内)
| 需求 | 原因 |
|---------|--------|
| 全新的 UI 视觉设计 | 本阶段重心在于稳定性和测试，维持现有 Indigo 风格。 |
| Linux/macOS 支持 | Windows API 深度集成是核心，暂不考虑跨平台。 |

## Traceability (追踪矩阵)

| Requirement | Phase | Status |
|-------------|-------|--------|
| ARCH-01 | Phase 1 | Pending |
| ARCH-02 | Phase 1 | Pending |
| ARCH-03 | Phase 1 | Pending |
| TEST-01 | Phase 1 | Pending |
| TEST-02 | Phase 2 | Pending |
| TEST-03 | Phase 2 | Pending |
| TEST-04 | Phase 2 | Pending |
| UX-01   | Phase 3 | Pending |
| UX-02   | Phase 3 | Pending |
| UX-03   | Phase 3 | Pending |
| ROB-01  | Phase 2 | Pending |
| ROB-02  | Phase 2 | Pending |
| ROB-03  | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-11*
*Last updated: 2026-04-11 after initial definition*
