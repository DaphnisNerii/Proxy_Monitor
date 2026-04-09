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

try:
    import pystray
    from PIL import Image, ImageDraw
    import winreg
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError as e:
    print(f"[{datetime.datetime.now()}] 缺少依赖模块 {e}，正在尝试自动安装...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "pillow"])
    import pystray
    from PIL import Image, ImageDraw
    import winreg
    import tkinter as tk
    from tkinter import ttk, messagebox

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
    # 使用 pythonw.exe 运行脚本
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

# 全局变量同步 (将在循环中直接读取 config 字典以支持动态更新)
def get_config_val(key):
    global config
    return config.get(key, DEFAULT_CONFIG.get(key))

# ================= ================= =================
# ================= 以下内容通常无需修改 =================
# ================= ================= =================
# 基础计算 (由函数动态派生)
def get_daily_limit_bytes():
    return get_config_val("daily_limit_gb") * 1024 * 1024 * 1024

def get_rate_limit_bytes():
    return get_config_val("rate_limit_mb") * 1024 * 1024

# 获取当前脚本所在目录，确保状态文件与脚本在同一目录下
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "traffic_state.json")

# 后台运行退出标志
keep_running = True

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
            res = response.read().decode('utf-8')
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
            # 增加超时到 30 秒
            with urllib.request.urlopen(req, timeout=30) as response:
                headers = response.info()
                
                # 使用更通用的方式寻找包含 subscription-userinfo 的键
                userinfo = None
                for k, v in headers.items():
                    if 'subscription-userinfo' in k.lower():
                        userinfo = v
                        break
                        
                if userinfo:
                    upload = 0
                    download = 0
                    total = 0
                    m_up = re.search(r'upload=(\d+)', userinfo)
                    if m_up: upload = int(m_up.group(1))
                    m_dl = re.search(r'download=(\d+)', userinfo)
                    if m_dl: download = int(m_dl.group(1))
                    m_total = re.search(r'total=(\d+)', userinfo)
                    if m_total: total = int(m_total.group(1))
                    return upload, download, total
                else:
                    print(f"[{datetime.datetime.now()}] 失败：未在响应头中找到流量信息字段。")
                    return None
                    
        except socket.timeout:
            error_msg = "连接超时 (30s)"
        except urllib.error.URLError as e:
            error_msg = f"网络错误: {e.reason}"
        except Exception as e:
            error_msg = f"未知异常: {e}"
            
        if attempt < retries - 1:
            print(f"[{datetime.datetime.now()}] 获取订阅信息失败 ({error_msg})，5秒后进行第 {attempt + 2} 次尝试...")
            time.sleep(5)
        else:
            print(f"[{datetime.datetime.now()}] 请求订阅信息异常: {error_msg}")
            
    return None

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[{datetime.datetime.now()}] 读取状态文件失败: {e}")
            
    return {
        "date": "",                 # 记录日期的字符串 YYYY-MM-DD
        "start_of_day_used": 0,     # 当日零点时的历史总流量(upload+download)
        "last_total_used": 0,       # 上一分钟计算的旧总流量
        "daily_warned": False       # 今日是否触发过每日警告
    }

def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 保存状态文件失败: {e}")

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
                upload, download, total = info
                current_used = upload + download
                
                state = load_state()
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                
                # 1. 跨越新的一天重置标志位和基准线
                if state["date"] != current_date:
                    print(f"\n--- [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 新的一天开始记录，重置统计。 ---")
                    state["date"] = current_date
                    state["start_of_day_used"] = current_used
                    state["daily_warned"] = False
                    
                # 计算今天已经用掉的流量
                today_used = current_used - state["start_of_day_used"]
                # 处理如果厂商在年中强行清空了你的总流量使用记录的情况
                if today_used < 0:
                    today_used = 0
                    state["start_of_day_used"] = current_used
                    
                # 2. 每日阈值警告 (每天只会提醒一次)
                daily_limit_bytes = get_daily_limit_bytes()
                if today_used > daily_limit_bytes and not state["daily_warned"]:
                    msg_title = f"⚠️ 每日流量超限警告: 已使用 {format_bytes(today_used)}"
                    msg_desc = f"您设定的每日警告阈值为 **{get_config_val('daily_limit_gb')} GB**。\n\n今日已使用量达到 **{format_bytes(today_used)}**！\n请注意控制使用量。\n\n**总剩余流量:** {format_bytes(total - current_used)}"
                    send_serverchan(msg_title, msg_desc)
                    state["daily_warned"] = True

                # 3. 流量高速消耗警告判定 
                # (需要有上一分钟记录数据才对比)
                delta = 0
                rate_limit_bytes = get_rate_limit_bytes()
                if state["last_total_used"] > 0:
                    delta = current_used - state["last_total_used"]
                    # 避免清零或其他异常情况导致的负数
                    if delta > rate_limit_bytes:
                        msg_title = f"🚨 流量消耗过快警告: {format_bytes(delta)} / 分钟"
                        msg_desc = f"您在过去一分钟内的流量消耗了 **{format_bytes(delta)}**。\n\n设定的警告阈值为 **{get_config_val('rate_limit_mb')} MB/分钟**。\n\n可能是后台正在下载大文件，或者代理网络遭到了异常消耗，请尽快检查！"
                        send_serverchan(msg_title, msg_desc)
                        
                # 记录本分钟为"上一分钟"以便下次循环使用
                state["last_total_used"] = current_used
                save_state(state)
                
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 检查完成 -> 今日已用: {format_bytes(today_used).ljust(10)} | 当前速率: {format_bytes(delta)} / min | 剩余: {format_bytes(total - current_used)}")
                
                # 更新任务栏图标的状态提示文本
                if icon:
                    today_str = format_bytes(today_used)
                    left_str = format_bytes(total - current_used)
                    delta_str = format_bytes(delta)
                    icon.title = f"速率: {delta_str}/min\n今日已用: {today_str}\n剩余流量: {left_str}"
                
        except Exception as e:
            print(f"[{datetime.datetime.now()}] 运行发生异常:\n{traceback.format_exc()}")
            
        # 休眠 CHECK_INTERVAL 秒，切片以实现快速退出机制
        check_interval = get_config_val("check_interval")
        for _ in range(check_interval):
            if not keep_running:
                break
            time.sleep(1)

def create_image():
    # 生成一个简单的运行中图标（圆点）
    image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    # 画一个蓝底绿心圆图标
    d.ellipse((8, 8, 56, 56), fill=(40, 160, 240, 255))
    d.ellipse((16, 16, 48, 48), fill=(240, 240, 240, 255))
    d.ellipse((22, 22, 42, 42), fill=(30, 200, 30, 255))
    return image

def open_settings(icon, item):
    """在独立线程中打开设置窗口"""
    def _create_window():
        root = tk.Tk()
        root.title("Proxy Monitor - 设置")
        root.geometry("450x420")
        # 居中显示
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - 450) / 2
        y = (sh - 420) / 2
        root.geometry("+%d+%d" % (x, y))
        
        # 样式设置
        style = ttk.Style()
        style.configure("TLabel", font=("Microsoft YaHei", 9))
        style.configure("TButton", font=("Microsoft YaHei", 9))
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 辅助函数：创建输入行
        def create_entry(parent, label_text, key, row):
            ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(parent, width=40)
            entry.grid(row=row, column=1, sticky=tk.EW, pady=5)
            val = get_config_val(key)
            entry.insert(0, str(val))
            return entry

        entry_sub = create_entry(main_frame, "订阅链接:", "sub_url", 0)
        entry_key = create_entry(main_frame, "Server酱 Key:", "serverchan_sendkey", 1)
        entry_daily = create_entry(main_frame, "每日限额(GB):", "daily_limit_gb", 2)
        entry_rate = create_entry(main_frame, "速率阈值(MB/m):", "rate_limit_mb", 3)
        entry_interval = create_entry(main_frame, "检查间隔(s):", "check_interval", 4)
        
        var_autostart = tk.BooleanVar(value=get_config_val("auto_start"))
        ttk.Checkbutton(main_frame, text="开机自启动", variable=var_autostart).grid(row=5, column=1, sticky=tk.W, pady=10)

        def on_save():
            global config
            try:
                new_config = {
                    "sub_url": entry_sub.get().strip(),
                    "serverchan_sendkey": entry_key.get().strip(),
                    "daily_limit_gb": float(entry_daily.get()),
                    "rate_limit_mb": float(entry_rate.get()),
                    "check_interval": int(entry_interval.get()),
                    "auto_start": var_autostart.get()
                }
                if new_config["check_interval"] < 5:
                    messagebox.showwarning("警告", "检查间隔不能小于 5 秒")
                    return
                
                if save_config(new_config):
                    config = new_config
                    messagebox.showinfo("成功", "配置已保存并立即生效")
                    root.destroy()
            except ValueError:
                messagebox.showerror("错误", "请在数字项中输入有效的数值")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="保存", command=on_save).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=root.destroy).pack(side=tk.LEFT, padx=10)

        root.mainloop()

    # 在新线程里运行，防止阻塞托盘
    threading.Thread(target=_create_window, daemon=True).start()

def on_exit_clicked(icon, item):
    global keep_running
    keep_running = False
    icon.stop()

def main():
    # 初始化托盘图标
    icon_image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem("✅ 流量监控运行中", lambda: None, enabled=False),
        pystray.MenuItem("⚙️ 设置", open_settings),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("🚪 退出", on_exit_clicked)
    )
    icon = pystray.Icon("proxy_traffic_monitor", icon_image, "Proxy Monitor 正在启动...", menu)
    
    # 启动后台工作线程
    worker_thread = threading.Thread(target=monitor_loop, args=(icon,), daemon=True)
    worker_thread.start()
    
    # 阻塞主线程以显示系统托盘图标
    icon.run()

if __name__ == "__main__":
    main()
