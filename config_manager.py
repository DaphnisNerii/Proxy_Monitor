import os
import json
import sys
import datetime

try:
    import winreg
except ImportError:
    winreg = None

class ConfigManager:
    DEFAULT_CONFIG = {
        "sub_url": "",
        "serverchan_sendkey": "",
        "daily_limit_gb": 10.0,
        "rate_limit_mb": 500.0,
        "check_interval": 60,
        "auto_start": False
    }

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        config = self.DEFAULT_CONFIG.copy()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    config.update(loaded)
            except Exception as e:
                print(f"[{datetime.datetime.now()}] 读取配置文件失败: {e}")
        return config

    def save_config(self, new_config=None):
        if new_config:
            self.config.update(new_config)
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
            self.sync_auto_start()
            return True
        except Exception as e:
            print(f"[{datetime.datetime.now()}] 保存配置文件失败: {e}")
            return False

    def get(self, key):
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def sync_auto_start(self):
        """同步 Windows 开机自启设置"""
        if not winreg:
            return
            
        enable = self.config.get("auto_start", False)
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "ProxyTrafficMonitor"
        
        # 假设入口程序名为 main.pyw 或跟当前脚本同目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_app = os.path.join(base_dir, "main.pyw")
        if not os.path.exists(target_app):
            # 回退到当前执行的脚本 (重构期间过渡)
            target_app = os.path.abspath(sys.argv[0])

        cmd = f'"{sys.executable}" "{target_app}"'
        
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
