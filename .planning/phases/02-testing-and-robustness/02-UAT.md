---
status: testing
phase: 02-testing-and-robustness
source: [02-01-SUMMARY.md, 02-02-SUMMARY.md]
started: "2026-04-11T09:29:00Z"
updated: "2026-04-11T09:29:00Z"
---

## Current Test

(Please run through these tests one by one and tell me the result. If a test fails, describe the issue.)

### Test 1: 自动化测试用例运行检查
**目的:** 验证程序各项核心逻辑（配置、多线程锁、网络请求异常退避等）的自动化测试已覆盖并全量通过。
**步骤:**
1. 你只需告诉我通过，如果想亲身验证可以在终端里执行 `pytest tests/`。
**期望:** 输出应显示类似于 `9 passed in 6.xx s`。

### Test 2: UI 异常卡死问题验证（之前卡主的 Bug 修复测试）
**目的:** 验收 Phase 1 遗留并在此次修补的 UI 在多线程环境中卡死的问题。
**步骤:**
1. 在终端运行 `python main.pyw`。
2. 找到系统托盘区出现的图标，右键点击，选择“修改首选项...”。
3. 检查弹出的设置窗口是否能够**正常修改输入框**（例如改变每日限额数字）。
4. 确认点击“取消”按钮或右上角的红叉能够正常关闭窗口（且不会导致托盘程序崩溃）。
**期望:** 界面响应迅速，完全可用，无冻结或无法输入的死板现象。

### Test 3: 重复开启与后台不崩溃测试
**目的:** 进一步巩固架构调整后的鲁棒性。
**步骤:**
1. 在保持上方程序**正常运行在托盘中**的情况下，不要退出它。
2. 再次在这个终端运行一次 `python main.pyw`。
**期望:** 终端应直接输出提示“程序已在运行中，退出新进程。” 随后结束执行，既不会扰乱原来在托盘跑着的实例，也不会弹出新窗口。

---

## Results
- **Test 1**: (Pending)
- **Test 2**: (Pending)
- **Test 3**: (Pending)
