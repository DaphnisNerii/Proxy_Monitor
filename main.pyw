import sys
import os
import threading
import datetime
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
            # 这里原本应该用弹窗，但由于重构期简化，暂回退到日志
            print("关键依赖缺失且修复失败。")
            sys.exit(1)

    # 4. 初始化核心服务
    config_mgr = ConfigManager(CONFIG_FILE)
    monitor = TrafficMonitor(config_mgr, STATE_FILE)
    monitor.refresh_event = threading.Event()
    
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

    def open_settings_ui():
        # 如果已经打开了，这里的逻辑由 SettingsWindow 内部控制（待完善为单例或检查）
        ui = SettingsWindow(config_mgr, on_settings_save)
        ui.show()

    def on_exit():
        monitor.keep_running = False
        if monitor.refresh_event:
            monitor.refresh_event.set()
        if tray[0]:
            tray[0].stop()
        mutex.release()
        sys.exit(0)

    # 5. 启动后台 Thread
    threading.Thread(target=monitor.run_loop, args=(update_tray_status,), daemon=True).start()

    # 6. 运行托盘 (主线程)
    tray[0] = ProxyTrayIcon(monitor, on_settings_click=open_settings_ui, on_exit_click=on_exit)
    tray[0].run()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        print(traceback.format_exc())
    finally:
        mutex.release()
