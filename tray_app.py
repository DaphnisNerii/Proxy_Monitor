import pystray
import threading
import datetime
from PIL import Image, ImageDraw

class ProxyTrayIcon:
    def __init__(self, monitor_service, on_settings_click=None, on_exit_click=None):
        self.monitor = monitor_service
        self.on_settings_click = on_settings_click
        self.on_exit_click = on_exit_click
        self.icon = None

    def create_image(self):
        width, height = 64, 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        main_color = (129, 140, 248) # Indigo 400
        draw.ellipse([8, 8, 56, 56], outline=main_color, width=6)
        draw.ellipse([22, 22, 42, 42], fill=main_color)
        return image

    def update_status(self, delta_str, today_str, remaining_str, expire_str=None):
        if not self.icon: return
        title = f"速率: {delta_str}\n今日已用: {today_str}\n总计剩余: {remaining_str}"
        if expire_str:
            title += f"\n到期时间: {expire_str}"
        self.icon.title = title

    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem("📊 Proxy Monitor", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🔄 立即刷新数据", lambda: self.monitor.refresh_event.set() if self.monitor.refresh_event else None),
            pystray.MenuItem("⚙️ 修改首选项...", self.on_settings_click),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🚪 安全退出程序", self.on_exit_click)
        )
        self.icon = pystray.Icon("proxy_monitor", self.create_image(), "Proxy Monitor 运行中", menu)
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()
