import sys
import os
import threading
import datetime
import flet as ft
from config_manager import ConfigManager
from monitor_service import TrafficMonitor
from system_utils import NamedMutex, PreFlightCheck, setup_logging
from tray_app import ProxyTrayIcon
from ui_bridge import UIBridge
from flet_ui import FletUI

# ================= 基础环境初始化 =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "monitor.log")
STATE_FILE = os.path.join(BASE_DIR, "traffic_state.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# 1. 立即设置日志重定向
setup_logging(LOG_FILE)

# 2. 单实例检查 (命名互斥量)
mutex = NamedMutex("ProxyMonitor_v1_1_Mutex")
if not mutex.acquire():
    print(f"[{datetime.datetime.now()}] 程序已在运行中，退出新进程。")
    sys.exit(0)

def main():
    # 3. 环境自检测 (Pre-flight)
    checker = PreFlightCheck(os.path.join(BASE_DIR, "requirements.txt"))
    if not checker.check_dependencies():
        if not checker.auto_repair():
            print("关键依赖缺失，程序无法启动。")
            sys.exit(1)

    # 4. 初始化核心服务
    config_mgr = ConfigManager(CONFIG_FILE)
    from data_service import DataService
    ds = DataService()
    ds.migrate_from_json(STATE_FILE) # 尝试从旧版 JSON 迁移
    
    monitor = TrafficMonitor(config_mgr, STATE_FILE)
    monitor.refresh_event = threading.Event()
    
    # 5. 初始化桥接器
    bridge = UIBridge(monitor, config_mgr, ds)
    
    # 6. 初始化 Flet UI 对象 (尚未启动)
    ui_app = FletUI(bridge)

    def on_exit():
        print("正在退出程序...")
        monitor.keep_running = False
        if monitor.refresh_event:
            monitor.refresh_event.set()
        if tray[0]:
            tray[0].stop()
        mutex.release()
        os._exit(0)

    def update_tray_status(delta, today, remaining, expire):
        if tray[0]:
            delta_s = monitor.format_bytes(delta) + "/min"
            today_s = monitor.format_bytes(today)
            remains_s = monitor.format_bytes(remaining)
            expire_s = datetime.datetime.fromtimestamp(expire).strftime("%Y-%m-%d") if expire else None
            tray[0].update_status(delta_s, today_s, remains_s, expire_s)

    # 7. 启动托盘线程
    tray = [None]
    tray[0] = ProxyTrayIcon(
        bridge, 
        on_settings_click=ui_app.show_window, 
        on_exit_click=on_exit
    )
    threading.Thread(target=tray[0].run, daemon=True).start()

    # 8. 启动后台监控线程
    threading.Thread(target=monitor.run_loop, args=(update_tray_status,), daemon=True).start()

    # 9. 启动 Flet 应用 (主线程)
    # 使用 hidden 启动，等待托盘唤起
    ft.app(target=ui_app.main)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        print(traceback.format_exc())
    finally:
        mutex.release()
