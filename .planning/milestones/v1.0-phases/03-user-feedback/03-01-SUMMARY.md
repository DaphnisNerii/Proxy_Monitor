# Plan 03-01 Summary: UX 增强与实时感知

## 已完成的工作
- **保存通知气泡**：在 `tray_app.py` 中新增 `notify()` 方法，通过 `pystray.Icon.notify()` 发送 Windows 系统级气泡通知。
- **配置保存联动**：在 `main.pyw` 的 `on_settings_save` 回调中，保存配置后立即触发托盘通知"配置已保存 - 正在刷新监控数据..."，同时通过 `refresh_event.set()` 立即唤醒后台轮询线程获取最新数据。

## 验证结论
用户保存设置后，桌面右下角将弹出系统级通知气泡，给予明确的操作反馈。
