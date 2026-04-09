import sys
import os

# 将日志重定向提前到最开头，为了能捕获到第三方包导入失败的报错
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "monitor.log")
sys.stdout = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
sys.stderr = sys.stdout

import urllib.request
import urllib.parse
import json
import time
import datetime
import re
import traceback
import threading
import subprocess
import socket
import urllib.error
import tkinter as tk
from tkinter import ttk, messagebox, font

try:
    import pystray
    from PIL import Image, ImageDraw
    import winreg
except ImportError as e:
    print(f"[{datetime.datetime.now()}] 缺少依赖模块 {e}，正在尝试自动安装...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "pillow"])
    import pystray
    from PIL import Image, ImageDraw
    import winreg

# ================= 配置区 =================
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# 默认配置
DEFAULT_CONFIG = {
    "sub_url": "",
    "serverchan_sendkey": "",
    "daily_limit_gb": 10.0,
    "rate_limit_mb": 500.0,
    "check_interval": 60,
    "auto_start": False
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # 确保所有默认键都存在
                for k, v in DEFAULT_CONFIG.items():
                    if k not in config:
                        config[k] = v
                return config
        except Exception as e:
            print(f"[{datetime.datetime.now()}] 读取配置文件失败: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        handle_auto_start(config.get("auto_start", False))
        return True
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 保存配置文件失败: {e}")
        return False

def handle_auto_start(enable):
    """设置或取消 Windows 开机自启"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "ProxyTrafficMonitor"
    cmd = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        if enable:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 设置自启动失败: {e}")

# 初始化配置
config = load_config()

def get_config_val(key):
    global config
    return config.get(key, DEFAULT_CONFIG.get(key))

# 后台运行退出与刷新信号
keep_running = True
refresh_event = threading.Event()
STATE_FILE = os.path.join(BASE_DIR, "traffic_state.json")

def send_serverchan(title, desp=""):
    """使用 Server酱 推送消息"""
    sendkey = get_config_val("serverchan_sendkey")
    if not sendkey or "替换为你" in sendkey:
        print(f"[{datetime.datetime.now()}] 推送被跳过: 未配置有效的 Server酱 SendKey")
        return
        
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    data = urllib.parse.urlencode({'title': title, 'desp': desp}).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"[{datetime.datetime.now()}] Server酱推送成功: {title}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Server酱推送异常: {e}")

def get_traffic_info():
    """获取订阅链接中的流量信息 (带重试和超时优化)"""
    sub_url = get_config_val("sub_url")
    if not sub_url:
        return None
        
    retries = 2
    for attempt in range(retries):
        try:
            req = urllib.request.Request(sub_url, headers={'User-Agent': 'ClashforWindows/0.19.23'})
            with urllib.request.urlopen(req, timeout=30) as response:
                headers = response.info()
                userinfo = None
                for k, v in headers.items():
                    if 'subscription-userinfo' in k.lower():
                        userinfo = v
                        break
                if userinfo:
                    m_up = re.search(r'upload=(\d+)', userinfo)
                    m_dl = re.search(r'download=(\d+)', userinfo)
                    m_total = re.search(r'total=(\d+)', userinfo)
                    m_expire = re.search(r'expire=(\d+)', userinfo)
                    return int(m_up.group(1)) if m_up else 0, \
                           int(m_dl.group(1)) if m_dl else 0, \
                           int(m_total.group(1)) if m_total else 0, \
                           int(m_expire.group(1)) if m_expire else None
                else:
                    print(f"[{datetime.datetime.now()}] 失败：未在响应头中找到流量数据。")
                    return None
        except socket.timeout:
            error_msg = "连接超时 (30s)"
        except urllib.error.URLError as e:
            error_msg = f"网络错误: {e.reason}"
        except Exception as e:
            error_msg = f"未知异常: {e}"
            
        if attempt < retries - 1:
            time.sleep(5)
        else:
            print(f"[{datetime.datetime.now()}] 请求订阅信息异常: {error_msg}")
    return None

def format_bytes(b):
    if b < 1024: return f"{b} B"
    elif b < 1024**2: return f"{b/1024:.2f} KB"
    elif b < 1024**3: return f"{b/(1024**2):.2f} MB"
    else: return f"{b/(1024**3):.2f} GB"

def monitor_loop(icon):
    global keep_running
    print("代理流量监控已启动！开始后台轮询...")
    while keep_running:
        try:
            info = get_traffic_info()
            if info:
                upload, download, total, expire = info
                current_used = upload + download
                remaining = max(0, total - current_used)
                
                # 状态持久化与计算
                state = {"date": "", "start_of_day_used": 0, "last_total_used": 0, "daily_warned": False}
                if os.path.exists(STATE_FILE):
                    with open(STATE_FILE, "r") as f: state.update(json.load(f))
                
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                if state["date"] != current_date:
                    state.update({"date": current_date, "start_of_day_used": current_used, "daily_warned": False})
                
                today_used = max(0, current_used - state["start_of_day_used"])
                
                # 预警判定
                if today_used > get_config_val("daily_limit_gb") * 1024**3 and not state["daily_warned"]:
                    send_serverchan(f"⚠️ 流量超限: {format_bytes(today_used)}", f"已达每日额度。剩余: {format_bytes(remaining)}")
                    state["daily_warned"] = True
                
                delta = max(0, current_used - state["last_total_used"]) if state["last_total_used"] > 0 else 0
                if delta > get_config_val("rate_limit_mb") * 1024**2:
                    send_serverchan(f"🚨 速率过快: {format_bytes(delta)}/min")
                
                state["last_total_used"] = current_used
                with open(STATE_FILE, "w") as f: json.dump(state, f, indent=4)
                
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 今日已用: {format_bytes(today_used)} | 速率: {format_bytes(delta)}/min")
                
                # 更新悬停浮窗内容
                title_lines = [
                    f"速率: {format_bytes(delta)}/min",
                    f"今日已用: {format_bytes(today_used)}",
                    f"总计剩余: {format_bytes(remaining)}"
                ]
                if expire:
                    expire_date = datetime.datetime.fromtimestamp(expire).strftime("%Y-%m-%d")
                    title_lines.append(f"到期时间: {expire_date}")
                
                if icon: icon.title = "\n".join(title_lines)
        except Exception:
            print(traceback.format_exc())
            
        refresh_event.wait(timeout=get_config_val("check_interval"))
        refresh_event.clear()

def create_image():
    """现代 Indigo 500 圆环图标"""
    width, height = 64, 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    main_color = (99, 102, 241)
    draw.ellipse([8, 8, 56, 56], outline=main_color, width=6)
    draw.ellipse([22, 22, 42, 42], fill=main_color)
    return image

def open_settings(icon=None, item=None):
    def _create_window():
        root = tk.Tk()
        root.title("Proxy Monitor - 设置")
        root.configure(bg="#f8fafc")
        
        # 居中与淡入
        w, h = 480, 540
        x, y = (root.winfo_screenwidth()-w)//2, (root.winfo_screenheight()-h)//2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.attributes("-alpha", 0.0)
        def fade():
            if root.attributes("-alpha") < 1.0:
                root.attributes("-alpha", root.attributes("-alpha")+0.1)
                root.after(20, fade)
        root.after(50, fade)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#f8fafc", foreground="#1e293b", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#6366f1", background="#f8fafc")
        style.configure("Sub.TLabel", font=("Segoe UI", 9), foreground="#64748b", background="#f8fafc")
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background="#6366f1", foreground="white")
        style.configure("TLabelframe", background="#f8fafc", foreground="#6366f1")
        style.configure("TLabelframe.Label", background="#f8fafc", font=("Segoe UI", 9, "bold"))

        main_frame = ttk.Frame(root, padding=30, style="TFrame")
        style.configure("TFrame", background="#f8fafc")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="首选项设置", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        entries = {}
        def add_field(label, key, help=""):
            f = ttk.Frame(main_frame, style="TFrame")
            f.pack(fill=tk.X, pady=8)
            ttk.Label(f, text=label).pack(anchor="w")
            e = ttk.Entry(f, font=("Segoe UI", 10))
            e.insert(0, str(get_config_val(key))); e.pack(fill=tk.X, pady=(4, 0))
            if help: ttk.Label(f, text=help, style="Sub.TLabel").pack(anchor="w")
            entries[key] = e

        add_field("订阅链接 (Subscription URL)", "sub_url")
        add_field("Server酱 SendKey", "serverchan_sendkey")
        
        grp = ttk.LabelFrame(main_frame, text=" 预警阈值 ", padding=15)
        grp.pack(fill=tk.X, pady=20)
        def add_grp_field(label, key):
            f = ttk.Frame(grp, style="TFrame")
            f.pack(fill=tk.X, pady=5)
            ttk.Label(f, text=label).pack(side=tk.LEFT)
            e = ttk.Entry(f, width=15); e.insert(0, str(get_config_val(key))); e.pack(side=tk.RIGHT)
            entries[key] = e
        add_grp_field("每日限额 (GB)", "daily_limit_gb")
        add_grp_field("突发速率 (MB/min)", "rate_limit_mb")

        add_field("检查间隔 (秒)", "check_interval", "建议 60s")
        
        start_var = tk.BooleanVar(value=get_config_val("auto_start"))
        ttk.Checkbutton(main_frame, text="随 Windows 启动 (开机自启)", variable=start_var).pack(anchor="w", pady=10)

        def save():
            try:
                new = {k: entries[k].get() for k in ["sub_url", "serverchan_sendkey"]}
                new.update({
                    "daily_limit_gb": float(entries["daily_limit_gb"].get()),
                    "rate_limit_mb": float(entries["rate_limit_mb"].get()),
                    "check_interval": int(entries["check_interval"].get()),
                    "auto_start": start_var.get()
                })
                if save_config(new):
                    global config
                    config = new; refresh_event.set()
                    messagebox.showinfo("成功", "设置已生效"); root.destroy()
            except Exception: messagebox.showerror("错误", "输入非法")

        btns = ttk.Frame(main_frame, style="TFrame")
        btns.pack(fill=tk.X, pady=10)
        ttk.Button(btns, text=" 取消 ", command=root.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btns, text=" 保存 ", style="Action.TButton", command=save).pack(side=tk.RIGHT)
        
        root.mainloop()

    threading.Thread(target=_create_window, daemon=True).start()

def main():
    icon_image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem("📊 Proxy Monitor", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("🔄 立即刷新数据", lambda: refresh_event.set()),
        pystray.MenuItem("⚙️ 修改首选项...", open_settings),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("🚪 安全退出程序", lambda icon, item: [setattr(sys.modules[__name__], 'keep_running', False), icon.stop()])
    )
    icon = pystray.Icon("proxy_monitor", icon_image, "Proxy Monitor 运行中", menu)
    threading.Thread(target=monitor_loop, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    main()
