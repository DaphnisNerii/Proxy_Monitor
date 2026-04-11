# Requirements - v1.1 UX & Analytics

## Milestone v1.1
**Goal**: Elevate user experience through a modern UI overhaul and data-rich visualizations.

### 1. 现代化 UI 重构 (UI-MOD)
- [ ] **UI-01**: From Tkinter to **Flet** migration. Implement a modern Windows-native-like interface.
- [ ] **UI-02**: Sidebar navigation layout for easy access to different sections.
- [ ] **UI-03**: Interactive validation feedbacks for settings inputs.
- [ ] **UI-04**: Modern components (switches, sliders, card layouts) instead of legacy entries.

### 2. 流量看板 (STAT-ANL)
- [ ] **STAT-01**: Real-time traffic monitoring charts (Last 1 minute).
- [ ] **STAT-02**: Historical data persistence via SQLite database.
- [ ] **STAT-03**: Daily/Monthly usage summaries and visualization.

### 3. 架构优化 (ARCH-EXP)
- [ ] **ARCH-04**: MVP/Bridge pattern to separate UI framework from monitoring core.
- [ ] **ARCH-05**: Robust multi-threading management for UI and Tray integration.

## Future Requirements (Deferred)
- **NOTI-01**: Support Bark, PushDeer expansion.
- **UPDT-01**: Auto-update mechanism.

## Out of Scope
- Multi-platform support (Still Windows-only).
- Complete logic rewrite (Core monitoring logic will be reused).
