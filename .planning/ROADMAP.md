# Roadmap: Proxy Monitor Robustness & Testing

## Overview
本项目旨在将现有的单文件 Proxy Monitor 脚本演进为一个健壮、模块化且经过充分测试的 Windows 系统工具。通过重构解决逻辑耦合问题，引入自动化测试保障核心功能，并大幅提升用户在环境异常时的交互反馈。

## Phases

- [ ] **Phase 1: 架构重构与基础自检** - 拆分单文件代码，建立模块化结构，引入启动预测。
- [ ] **Phase 2: 自动化测试与逻辑加固** - 初始化测试框架，实现 Mock 测试，修复已知与潜在 Bug。
- [ ] **Phase 3: 用户反馈与异常处理增强** - 优化 GUI 反馈逻辑，增加详细的排错引导与环境自修。

## Phase Details

### Phase 1: 架构重构与基础自检
**Goal**: 实现代码逻辑与 UI 的完全解耦，为自动化测试打下基础。
**Depends on**: Nothing
**Requirements**: ARCH-01, ARCH-02, ARCH-03, ROB-03
**Success Criteria**:
  1. 代码库被拆分为至少 4 个独立的逻辑文件。
  2. 逻辑模块可以独立于 Tkinter 运行。
  3. 启动时具备 `Pre-flight` 环境自检能力。
**Plans**: 2 plans

Plans:
- [x] 01-01: 代码库逻辑拆分与解耦重构
- [x] 01-02: 实现单实例锁与配置管理模块化

### Phase 2: 自动化测试与逻辑加固
**Goal**: 建立全方位的测试覆盖，利用 Mock 技术验证关键/失败路径。
**Depends on**: Phase 1
**Requirements**: TEST-01, TEST-02, TEST-03, TEST-04, ROB-01, ROB-02
**Success Criteria**:
  1. `pytest` 环境搭建完成，具备有效的 Mock 配置文件。
  2. 注册表与 Socket 逻辑通过单元测试验证。
  3. 网络异常情况下的流量解析具备回归测试。
**Plans**: 2 plans

Plans:
- [x] 02-01: 测试环境构建与核心逻辑单元测试
- [ ] 02-02: 流量解析 Robustness 增强与异常 Mock

### Phase 3: 用户反馈与异常处理增强
**Goal**: 提升终端用户在遇到问题时的解决效率与软件交互感。
**Depends on**: Phase 2
**Requirements**: UX-01, UX-02, UX-03
**Success Criteria**:
  1. 配置修改后，托盘图标实现毫秒级 UI 刷新反馈。
  2. 针对网络/环境错误，显示具备具体排错建议的对话框。
**Plans**: 1 plan

Plans:
- [ ] 03-01: 错误反馈 UI 增强与环境排错手册集成

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. 架构重构与基础自检 | 0/2 | Not started | - |
| 2. 自动化测试与逻辑加固 | 0/2 | Not started | - |
| 3. 用户反馈与异常处理增强 | 0/1 | Not started | - |
