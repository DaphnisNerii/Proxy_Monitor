import threading
import datetime

class UIBridge:
    def __init__(self, monitor, config_manager, data_service):
        self.monitor = monitor
        self.config_manager = config_manager
        self.data_service = data_service
        # 实时数据缓存
        self.latest_data = {
            "delta_s": "0 B/min",
            "today_s": "0 B",
            "remaining_s": "0 B",
            "expire_s": "N/A",
            "last_update": "从未更新"
        }
        self._on_data_callbacks = []

    def get_recent_history(self, hours=24):
        return self.data_service.get_recent_history(hours)

    def get_stats_summary(self, days=7):
        return self.data_service.get_stats_summary(days)

    def register_callback(self, callback):
        """注册 UI 更新回调"""
        self._on_data_callbacks.append(callback)

    def update_data(self, delta_s, today_s, remaining_s, expire_s):
        """由 MonitorService 调用同步数据"""
        self.latest_data.update({
            "delta_s": delta_s,
            "today_s": today_s,
            "remaining_s": remaining_s,
            "expire_s": expire_s or "N/A",
            "last_update": datetime.datetime.now().strftime("%H:%M:%S")
        })
        # 通知所有注册的 UI 组件
        for cb in self._on_data_callbacks:
            try:
                cb(self.latest_data)
            except:
                pass

    def get_config(self, key):
        return self.config_manager.get(key)

    def save_config(self, new_config):
        success = self.config_manager.save_config(new_config)
        if success and self.monitor.refresh_event:
            self.monitor.refresh_event.set()
        return success

    def request_refresh(self):
        """手动触发监控刷新"""
        if self.monitor.refresh_event:
            self.monitor.refresh_event.set()
