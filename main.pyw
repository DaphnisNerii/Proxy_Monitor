import sys
import os
import threading
import datetime
import tkinter as tk
from config_manager import ConfigManager
from monitor_service import TrafficMonitor
from system_utils import NamedMutex, PreFlightCheck, setup_logging
from tray_app import ProxyTrayIcon
from ui_components import SettingsWindow

# ================= 基础环境初始化 =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "monitor.log")
STATE_FILE = os.path.join(BASE_DIR, "traffic_state.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# 1. 立即设置日志重定向
setup_logging(LOG_FILE)

# 2. 单实例锁定
mutex = NamedMutex("ProxyTrafficMonitor_SingleInstance")
if not mutex.acquire():
    print(f"[{datetime.datetime.now()}] 程序已在运行中，退出新进程。")
    sys.exit(0)

def main():
    # 3. 环境自检测 (Pre-flight)
    checker = PreFlightCheck(os.path.join(BASE_DIR, "requirements.txt"))
    if not checker.check_dependencies():
        if not checker.auto_repair():
            missing = checker.get_missing()
            msg = (
                "以下关键依赖缺失且自动修复失败：\n\n"
                + "\n".join(f"  • {m}" for m in missing) + "\n\n"
                "请尝试手动执行:\n"
                f"  pip install -r {os.path.join(BASE_DIR, 'requirements.txt')}\n\n"
                "如仍无法解决，请访问项目 GitHub Issues 提交反馈。"
            )
            try:
                from tkinter import messagebox as _mb
                _r = tk.Tk(); _r.withdraw()
                _mb.showerror("Proxy Monitor - 启动失败", msg)
                _r.destroy()
            except Exception:
                pass
            print(msg)
            sys.exit(1)

    # 4. 初始化核心服务
    config_mgr = ConfigManager(CONFIG_FILE)
    monitor = TrafficMonitor(config_mgr, STATE_FILE)
    monitor.refresh_event = threading.Event()
    
    # 5. 主线程隐式 Tkinter root
    root = tk.Tk()
    root.withdraw()
    
    tray = [None] # 用列表包装以便在闭包中访问

    def update_tray_status(delta, today, remaining, expire):
        if tray[0]:
            delta_s = monitor.format_bytes(delta) + "/min"
            today_s = monitor.format_bytes(today)
            remains_s = monitor.format_bytes(remaining)
            expire_s = datetime.datetime.fromtimestamp(expire).strftime("%Y-%m-%d") if expire else None
            tray[0].update_status(delta_s, today_s, remains_s, expire_s)

    def on_settings_save():
        monitor.refresh_event.set()
        if tray[0]:
            tray[0].notify("配置已保存", "正在刷新监控数据...")

    ui_instance = [None]

    def open_settings_ui():
        def _show():
            if not ui_instance[0]:
                ui_instance[0] = SettingsWindow(root, config_mgr, on_settings_save)
            ui_instance[0].show()
        # 确保在属于 root 的主线程执行
        root.after(0, _show)

    def on_exit():
        monitor.keep_running = False
        if monitor.refresh_event:
            monitor.refresh_event.set()
        if tray[0]:
            tray[0].stop()
        mutex.release()
        try:
            root.quit()
            root.destroy()
        except:
            pass
        os._exit(0)

    # 6. 启动后台 Thread (monitor)
    threading.Thread(target=monitor.run_loop, args=(update_tray_status,), daemon=True).start()

    # 7. 运行托盘在专用后台线程，保证其不阻塞主线程
    tray[0] = ProxyTrayIcon(monitor, on_settings_click=open_settings_ui, on_exit_click=lambda: root.after(0, on_exit))
    threading.Thread(target=tray[0].run, daemon=True).start()

    # 8. 主线程启动 tk 的 mainloop 接管所有的 UI 及安全回调
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        err_detail = traceback.format_exc()
        print(err_detail)
        try:
            from tkinter import messagebox as _mb
            _r = tk.Tk(); _r.withdraw()
            _mb.showerror(
                "Proxy Monitor - 未处理的异常",
                f"程序遇到了意外错误，即将退出。\n\n"
                f"错误摘要:\n{err_detail[:500]}\n\n"
                f"完整日志已写入:\n{LOG_FILE}"
            )
            _r.destroy()
        except Exception:
            pass
    finally:
        mutex.release()
