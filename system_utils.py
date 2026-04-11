import sys
import os
import subprocess
import datetime
import socket

try:
    import ctypes
    from ctypes import wintypes
except ImportError:
    ctypes = None

class NamedMutex:
    """Windows 原生命名互斥体，用于单实例自锁"""
    def __init__(self, name):
        self.name = f"Global\\{name}"
        self.mutex = None
        self.last_error = 0

    def acquire(self):
        if not ctypes:
            return False
            
        # CreateMutexW: lpMutexAttributes, bInitialOwner, lpName
        self.mutex = ctypes.windll.kernel32.CreateMutexW(None, False, self.name)
        self.last_error = ctypes.windll.kernel32.GetLastError()
        
        # ERROR_ALREADY_EXISTS = 183
        if self.last_error == 183:
            return False
        return bool(self.mutex)

    def release(self):
        if self.mutex:
            ctypes.windll.kernel32.CloseHandle(self.mutex)
            self.mutex = None

class PreFlightCheck:
    """启动前环境检查与自修复"""
    def __init__(self, requirements_path="requirements.txt"):
        self.requirements_path = requirements_path

    def check_dependencies(self):
        try:
            import pystray
            from PIL import Image
            return True
        except ImportError:
            return False

    def auto_repair(self):
        print(f"[{datetime.datetime.now()}] 正在尝试自动修复依赖环境...")
        try:
            # 优先使用 requirements.txt
            if os.path.exists(self.requirements_path):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", self.requirements_path])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pystray", "pillow"])
            return True
        except Exception as e:
            error_log = os.path.join(os.path.dirname(__file__), "error_report.log")
            with open(error_log, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now()}] 自动修复失败: {str(e)}\n")
            return False

def setup_logging(log_path):
    """设置全局日志重定向"""
    try:
        sys.stdout = open(log_path, "a", encoding="utf-8", buffering=1)
        sys.stderr = sys.stdout
    except Exception as e:
        print(f"无法重定向日志: {e}")
