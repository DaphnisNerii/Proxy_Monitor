# Plan 03-02 Summary: 全局异常拦截与启动守护

## 已完成的工作
- **全局异常弹窗**：在 `main.pyw` 的顶层 `try/except` 中，捕获未处理异常后通过 `tkinter.messagebox.showerror()` 弹出错误对话框，展示异常摘要和日志文件路径，不再静默崩溃。
- **Pre-flight 友好提示**：当 `PreFlightCheck.auto_repair()` 失败时，弹出信息窗口列出缺失的依赖项名称，并提供手动修复命令和 GitHub Issues 链接。
- **get_missing() 方法**：在 `system_utils.py` 的 `PreFlightCheck` 类中新增方法，能够精确识别哪些包缺失（pystray / Pillow）。

## 验证结论
- 所有 9 个自动化测试用例继续通过，无回归。
- 致命异常不再导致程序"无声消失"，用户将看到清晰的错误窗口。
