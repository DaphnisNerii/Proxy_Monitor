# Phase 1: 架构重构与基础自检 - Context

**Gathered:** 2026-04-11
**Status:** Ready for planning

<domain>
## Phase Boundary

将现有的 `proxy_monitor.pyw` 单文件重构为模块化结构，并增加启动前的 `Pre-flight` 环境自检流程。目标是实现业务逻辑与 UI 层级的彻底解耦，支持后续的自动化测试。

</domain>

<decisions>
## Implementation Decisions

### 模块组织策略
- **D-01:** 采用**扁平化**的文件结构，不引入复杂的包/子目录。
- **D-02:** 拆分为以下模块（建议命名）：
  - `config_manager.py`: 配置读写、注册表操作。
  - `monitor_service.py`: 业务逻辑、流量抓取与解析。
  - `ui_components.py`: Tkinter 窗口和样式定义。
  - `tray_app.py`: Pystray 托盘逻辑与其生命周期。
  - `main.pyw`: 入口点，包含启动自检和单实例控制。

### 依赖与环境管理
- **D-03:** 引入 `requirements.txt` 作为标准依赖声明文件。
- **D-04:** 后续开发/测试环境将基于此文件进行初始化。

### 启动自检 (Pre-flight Check)
- **D-05:** 自检流程包含：
  - Python 版本验证。
  - 关键三方库（Pillow, pystray, requests 等）存在性验证。
  - 配置文件合法性验证。
- **D-06:** 失败反馈采取并行方案：
  - **弹窗**: 使用 `tkinter.messagebox` 显示人类可读的错误。
  - **报告**: 将详细 Traceback 写入 `monitor.log` 或 `startup_error.txt`。
  - **自动修复**: 在弹窗中提供“尝试自动修复”选项，点击后调用 `pip install -r requirements.txt`。

### 单实例运行逻辑 (Singleton)
- **D-07:** 将原本的 Socket 方案升级为 **Windows 命名互斥体 (Named Mutex)**，利用 `ctypes` 调用 Windows API 实现。
- **D-08:** 互斥体名称需具备唯一性（如 `ProxyMonitor_Unique_Instance_Lock`）。

### the agent's Discretion
- 具体互斥体实现的 `ctypes` 调用细节。
- `requirements.txt` 的具体版本约束（建议使用当前环境的主版本）。
- 代码拆分时的具体函数划分细节。

</decisions>

<specifics>
## Specific Ideas

- "保持扁平结构，项目预计不会过度扩展"
- "启动失败时不仅要弹窗，还要能尝试一键自动修复依赖"
- "逻辑层绝对不能导入 tkinter，确保 pytest 可以纯净运行"

</specifics>

<canonical_refs>
## Canonical References

### 核心需求与规划
- `.planning/PROJECT.md` — 愿景与核心价值
- `.planning/REQUIREMENTS.md` — ARCH-01, ARCH-02, ARCH-03, UX-02, ROB-03 的具体要求

### 技术指南
- `.planning/codebase/CONVENTIONS.md` — 错误处理与 UI 风格约定
- `.planning/codebase/STRUCTURE.md` — 原始代码结构参考

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `get_traffic_info`: 迁移至 `monitor_service.py`。
- `load_config` / `save_config`: 迁移至 `config_manager.py`。
- `ttk.Style` 及 indigo 风格代码: 迁移至 `ui_components.py`。

### Established Patterns
- **Threading**: 依然需要保持监控逻辑在独立线程运行，不阻塞 UI。
- **Registry handling**: 目前在 L67 附近，需封装后迁移。

</code_context>

<deferred>
## Deferred Ideas

- 自动化测试用例编写 — Phase 2
- 增强托盘图标视觉反馈 — Phase 3

</deferred>

---

*Phase: 01-architecture-refactoring*
*Context gathered: 2026-04-11*
