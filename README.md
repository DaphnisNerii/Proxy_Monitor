# 🚀 Proxy Traffic Monitor | 代理流量监控小助手

一款专为 Windows 用户设计的极速、健壮、模块化的代理订阅流量监控工具。它驻留在系统托盘，实时显示流量消耗，并在异常情况下提供可靠的反馈。

---

## ✨ 功能特性

- **📂 核心模块化**：已由单文件脚本重构为解耦的模块化架构，逻辑与 UI 完全分离。
- **🎨 托盘交互**：简洁的系统托盘图标，悬停查看当前速率及今日用量。
- **⚖️ 极速健壮**：
  - **NamedMutex**: 采用 Windows 原生互斥锁防止多开，崩溃后自动重启无压力。
  - **Exponential Backoff**: 指数退避重试策略，应对网络波动更稳健。
- **🚨 智能预警**：支持每日限额与速率突发预警，通过 Server酱 推送。
- **🛠️ 启动自检**：`Pre-flight` 自检逻辑，在环境缺失时提供清晰的修复指引。
- **🧪 自动化测试**：内置 `pytest` 测试套件，核心逻辑覆盖率高，确保生产环境稳定。

## 🛠️ 安装与运行

### 1. 环境要求
- Windows 10/11
- Python 3.7+

### 2. 获取程序
```bash
git clone https://github.com/DaphnisNerii/Proxy_Monitor.git
cd Proxy_Monitor
```

### 3. 安装依赖
程序会在首次启动时尝试自动修复缺失依赖。手动安装：
```bash
pip install -r requirements.txt
```
若需运行测试，请输入：
```bash
pip install -r requirements-test.txt
```

### 4. 启动程序
推荐通过 `pythonw` 启动以实现纯托盘无窗口运行：
```bash
pythonw main.pyw
```

## 🧪 自动化测试
本项目使用 `pytest` 进行逻辑验证。运行所有测试：
```bash
pytest
```

## 📂 项目结构

```text
Proxy_Monitor/
├── main.pyw              # 程序入口 (启动自检与集成)
├── monitor_service.py    # 核心监控逻辑 (网络抓取与解析)
├── config_manager.py     # 配置管理 (注册表与 JSON)
├── tray_app.py           # 托盘交互实现
├── ui_components.py      # Tkinter UI 组件 (设置窗口等)
├── system_utils.py       # 系统工具 (锁、自检、Windows API)
├── tests/                # 自动化测试用例
├── .gitignore            # Git 忽略规则
└── README.md             # 项目说明文档
```

## 🤝 贡献与反馈
欢迎提交 Issue 或 Pull Request！

---
**如果这个工具对你有帮助，欢迎点个 Star ⭐️！**
