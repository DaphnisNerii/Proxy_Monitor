import os
import json
import time
import datetime
import re
import socket
import urllib.request
import urllib.parse
import urllib.error
import traceback

class TrafficMonitor:
    def __init__(self, config_manager, state_file):
        self.config = config_manager
        self.state_file = state_file
        self.keep_running = True
        self.refresh_event = None # 将由外部传入或初始化

    def format_bytes(self, b):
        if b < 1024: return f"{b} B"
        elif b < 1024**2: return f"{b/1024:.2f} KB"
        elif b < 1024**3: return f"{b/(1024**2):.2f} MB"
        else: return f"{b/(1024**3):.2f} GB"

    def send_serverchan(self, title, desp=""):
        sendkey = self.config.get("serverchan_sendkey")
        if not sendkey or "替换为你" in sendkey:
            return
            
        url = f"https://sctapi.ftqq.com/{sendkey}.send"
        data = urllib.parse.urlencode({'title': title, 'desp': desp}).encode('utf-8')
        req = urllib.request.Request(url, data=data)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"[{datetime.datetime.now()}] Server酱推送成功: {title}")
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Server酱推送异常: {e}")

    def get_traffic_info(self):
        sub_url = self.config.get("sub_url")
        if not sub_url:
            return None
            
        retries = 3
        backoff_sec = 2
        for attempt in range(retries):
            try:
                req = urllib.request.Request(sub_url, headers={'User-Agent': 'ClashforWindows/0.19.23'})
                with urllib.request.urlopen(req, timeout=10) as response:
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
            except (socket.timeout, urllib.error.URLError, Exception) as e:
                if attempt == retries - 1:
                    print(f"[{datetime.datetime.now()}] 请求订阅信息异常: {e}")
            if attempt < retries - 1:
                time.sleep(backoff_sec)
                backoff_sec *= 2
        return None

    def run_loop(self, icon_callback=None):
        print("代理流量监控已启动！开始后台轮询...")
        while self.keep_running:
            try:
                info = self.get_traffic_info()
                if info:
                    upload, download, total, expire = info
                    current_used = upload + download
                    remaining = max(0, total - current_used)
                    
                    state = {"date": "", "start_of_day_used": 0, "last_total_used": 0, "daily_warned": False}
                    if os.path.exists(self.state_file):
                        try:
                            with open(self.state_file, "r") as f: state.update(json.load(f))
                        except: pass
                    
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    if state["date"] != current_date:
                        state.update({"date": current_date, "start_of_day_used": current_used, "daily_warned": False})
                    
                    today_used = max(0, current_used - state["start_of_day_used"])
                    
                    if today_used > self.config.get("daily_limit_gb") * 1024**3 and not state["daily_warned"]:
                        self.send_serverchan(f"⚠️ 流量超限: {self.format_bytes(today_used)}", f"已达每日额度。剩余: {self.format_bytes(remaining)}")
                        state["daily_warned"] = True
                    
                    delta = max(0, current_used - state["last_total_used"]) if state["last_total_used"] > 0 else 0
                    if delta > self.config.get("rate_limit_mb") * 1024**2:
                        self.send_serverchan(f"🚨 速率过快: {self.format_bytes(delta)}/min")
                    
                    state["last_total_used"] = current_used
                    with open(self.state_file, "w") as f: json.dump(state, f, indent=4)
                    
                    if icon_callback:
                        icon_callback(delta, today_used, remaining, expire)
            except Exception:
                print(traceback.format_exc())
                
            if self.refresh_event:
                self.refresh_event.wait(timeout=self.config.get("check_interval"))
                self.refresh_event.clear()
            else:
                time.sleep(self.config.get("check_interval"))
