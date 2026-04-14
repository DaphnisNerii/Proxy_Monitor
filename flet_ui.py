import flet as ft
import threading
import datetime

class FletUI:
    def __init__(self, bridge):
        self.bridge = bridge
        self.page = None
        self.content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
        
        # 实时数据组件
        self.status_delta = ft.Text("0 B/min", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        self.status_today = ft.Text("0 B", size=18, color=ft.Colors.SECONDARY)
        self.status_remaining = ft.Text("0 B", size=18, color=ft.Colors.SECONDARY)
        self.status_expire = ft.Text("N/A", size=14, color=ft.Colors.OUTLINE)
        self.status_last_update = ft.Text("从未更新", size=12, italic=True)

        # 历史趋势组件
        self.chart_series = ft.LineChartData(
            color=ft.Colors.BLUE,
            stroke_width=3,
            curved=True,
            data_points=[]
        )
        self.chart = ft.LineChart(
            data_series=[self.chart_series],
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.Colors.with_opacity(0.05, ft.Colors.ON_SURFACE)),
            vertical_grid_lines=ft.ChartGridLines(interval=3600, color=ft.Colors.with_opacity(0.05, ft.Colors.ON_SURFACE)),
            left_axis=ft.ChartAxis(labels_size=40),
            bottom_axis=ft.ChartAxis(labels_size=32),
            expand=True,
            interactive=True,
        )
        self.summary_row = ft.Row(wrap=True, spacing=10, run_spacing=10)

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Proxy Monitor"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 1000
        self.page.window.height = 950
        self.page.window.min_width = 800
        self.page.window.min_height = 700
        
        # 拦截关闭事件，改为隐藏
        self.page.window.prevent_close = True
        self.page.window.on_event = self._on_window_event
        
        # 初始化界面
        self._build_layout()
        
        # 注册数据更新回调
        self.bridge.register_callback(self._on_data_received)
        
        # 默认显示仪表盘
        self._show_dashboard()
        self.page.update()

    def _on_window_event(self, e):
        if e.data == "close":
            self.page.window.visible = False
            self.page.update()

    def show_window(self):
        if self.page:
            self.page.window.visible = True
            self.page.window.to_front()
            self.page.update()

    def _on_data_received(self, data):
        """处理来自 Bridge 的实时数据更新"""
        self.status_delta.value = data["delta_s"]
        self.status_today.value = data["today_s"]
        self.status_remaining.value = data["remaining_s"]
        self.status_expire.value = f"到期: {data['expire_s']}"
        self.status_last_update.value = f"最后同步: {data['last_update']}"
        
        if self.page:
            try:
                self._update_charts()
                self.page.update()
            except:
                pass

    def _update_charts(self):
        """刷新图表数据"""
        # 1. 更新 24h 速率图
        history = self.bridge.get_recent_history(24)
        if history:
            now = datetime.datetime.now()
            now_ts = now.timestamp()
            # 2. 构造数据点
            data_points = []
            for item in history:
                ts_str, delta_bytes = item
                ts = datetime.datetime.fromisoformat(ts_str).timestamp()
                x_val = 86400 - (now_ts - ts)
                y_val = delta_bytes / (1024 * 1024) # MB/min
                data_points.append(ft.LineChartDataPoint(x_val, y_val))
            
            self.chart_series.data_points = data_points
            
            # 3. 设置坐标轴与标签 (每4小时一个刻度)
            self.chart.min_x = 0
            self.chart.max_x = 86400
            self.chart.max_y = max(p.y for p in data_points) * 1.2 or 1
            
            labels = []
            for i in range(0, 25, 4): # 从 -24h 到 0h，每 4 小时
                ts = now - datetime.timedelta(hours=24-i)
                labels.append(
                    ft.ChartAxisLabel(
                        value=i * 3600,
                        label=ft.Text(ts.strftime("%H:%M"), size=10, color=ft.Colors.OUTLINE)
                    )
                )
            self.chart.bottom_axis.labels = labels
        
        # 2. 更新 7d 汇总卡片
        summaries = self.bridge.get_stats_summary(7)
        if summaries:
            cards = []
            for date_str, total in summaries:
                gb = total / (1024 * 1024 * 1024)
                cards.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(date_str[5:], size=12, weight=ft.FontWeight.W_500), # 只显示 MM-DD
                            ft.Text(f"{gb:.2f} GB", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        padding=10,
                        border_radius=8,
                        bgcolor=ft.Colors.SURFACE,
                        width=80,
                    )
                )
            self.summary_row.controls = cards

    def _build_layout(self):
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="仪表盘",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="首选项",
                ),
            ],
            on_change=self._on_rail_change,
        )

        self.page.add(
            ft.Row(
                [
                    self.rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=self.content_area,
                        expand=True,
                        padding=20,
                    ),
                ],
                expand=True,
            )
        )

    def _on_rail_change(self, e):
        if e.control.selected_index == 0:
            self._show_dashboard()
        elif e.control.selected_index == 1:
            self._show_settings()
        self.page.update()

    def _show_dashboard(self):
        self.content_area.controls = [
            ft.Text("系统状态", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    ft.Text("当前实时速率", size=14, color=ft.Colors.OUTLINE),
                    self.status_delta,
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=16),
                        ft.Text("今日已消耗:"),
                        self.status_today,
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.STORAGE, size=16),
                        ft.Text("套餐剩余:"),
                        self.status_remaining,
                    ]),
                    ft.Divider(),
                    ft.Row([
                        self.status_expire,
                        ft.Container(expand=True),
                        self.status_last_update,
                    ]),
                ]),
                padding=20,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
                bgcolor=ft.Colors.SURFACE,
            ),
            ft.Container(height=20),
            ft.Text("24小时流量速率 (MB/min)", size=18, weight=ft.FontWeight.W_500),
            ft.Container(
                content=self.chart,
                height=250,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLACK12,
            ),
            ft.Container(height=20),
            ft.Text("最近 7 天统计", size=18, weight=ft.FontWeight.W_500),
            self.summary_row,
            ft.Container(height=20),
        ]
        # 初次加载数据
        self._update_charts()

    def _show_settings(self):
        # 从 Bridge 获取当前的配置
        fields = {
            "sub_url": self.bridge.get_config("sub_url"),
            "serverchan_sendkey": self.bridge.get_config("serverchan_sendkey"),
            "daily_limit_gb": self.bridge.get_config("daily_limit_gb"),
            "rate_limit_mb": self.bridge.get_config("rate_limit_mb"),
            "check_interval": self.bridge.get_config("check_interval"),
            "auto_start": self.bridge.get_config("auto_start"),
        }

        # 创建输入控件
        self.inputs = {}
        for key, val in fields.items():
            if isinstance(val, bool):
                self.inputs[key] = ft.Switch(label="开机自启", value=val)
            else:
                self.inputs[key] = ft.TextField(
                    label=key.replace("_", " ").title(),
                    value=str(val),
                    width=400,
                    border_color=ft.Colors.OUTLINE,
                )

        self.content_area.controls = [
            ft.Text("首选项设置", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("连接与推送", size=16, weight=ft.FontWeight.W_500),
            self.inputs["sub_url"],
            self.inputs["serverchan_sendkey"],
            ft.Divider(),
            ft.Text("监控阈值", size=16, weight=ft.FontWeight.W_500),
            ft.Row([self.inputs["daily_limit_gb"], ft.Text("GB")]),
            ft.Row([self.inputs["rate_limit_mb"], ft.Text("MB/min")]),
            self.inputs["check_interval"],
            ft.Divider(),
            self.inputs["auto_start"],
            ft.Container(height=20),
            ft.ElevatedButton(
                "保存配置", 
                icon=ft.Icons.SAVE, 
                on_click=self._on_save_settings,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE, 
                    color=ft.Colors.WHITE
                )
            )
        ]

    def _on_save_settings(self, e):
        try:
            new_conf = {
                "sub_url": self.inputs["sub_url"].value,
                "serverchan_sendkey": self.inputs["serverchan_sendkey"].value,
                "daily_limit_gb": float(self.inputs["daily_limit_gb"].value),
                "rate_limit_mb": float(self.inputs["rate_limit_mb"].value),
                "check_interval": int(self.inputs["check_interval"].value),
                "auto_start": self.inputs["auto_start"].value,
            }
            if self.bridge.save_config(new_conf):
                self.page.snack_bar = ft.SnackBar(ft.Text("设置已保存并生效"))
                self.page.snack_bar.open = True
            else:
                raise Exception("保存失败")
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"保存失败: {str(ex)}"), bgcolor=ft.Colors.ERROR)
            self.page.snack_bar.open = True
        
        self.page.update()
