import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk

class UIStyles:
    BG_DARK = "#0f172a"
    CARD_DARK = "#1e293b"
    TEXT_LIGHT = "#f8fafc"
    TEXT_MUTED = "#94a3b8"
    ACCENT = "#818cf8"
    SUCCESS = "#10b981"
    INPUT_BG = "#334155"

    @staticmethod
    def configure_styles():
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=UIStyles.BG_DARK)
        style.configure("Card.TFrame", background=UIStyles.CARD_DARK)
        style.configure("TLabel", background=UIStyles.CARD_DARK, foreground=UIStyles.TEXT_LIGHT, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=UIStyles.ACCENT, background=UIStyles.BG_DARK)
        style.configure("Sub.TLabel", font=("Segoe UI", 9), foreground=UIStyles.TEXT_MUTED, background=UIStyles.CARD_DARK)
        style.configure("Status.TLabel", font=("Segoe UI", 10, "bold"), foreground=UIStyles.SUCCESS, background=UIStyles.BG_DARK)
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=UIStyles.ACCENT, foreground="white", borderwidth=0)
        style.map("Primary.TButton", background=[('active', '#6366f1')])
        style.configure("TLabelframe", background=UIStyles.CARD_DARK, foreground=UIStyles.ACCENT, bordercolor=UIStyles.INPUT_BG)
        style.configure("TLabelframe.Label", background=UIStyles.CARD_DARK, foreground=UIStyles.ACCENT, font=("Segoe UI", 10, "bold"))

class SettingsWindow:
    def __init__(self, parent_root, config_manager, on_save_callback=None):
        self.parent_root = parent_root
        self.config_manager = config_manager
        self.on_save_callback = on_save_callback
        self.root = None
        self.entries = {}
        self.icons = {}

    def generate_icon(self, icon_type, color=(129, 140, 248)):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        c = color
        if icon_type == "link":
            d.rectangle([8, 14, 24, 18], outline=c, width=2)
            d.rectangle([12, 10, 20, 22], outline=c, width=2)
        elif icon_type == "key":
            d.ellipse([8, 8, 18, 18], outline=c, width=2)
            d.line([18, 13, 26, 13], fill=c, width=2)
            d.line([22, 13, 22, 17], fill=c, width=2)
        elif icon_type == "limit":
            d.polygon([(16, 6), (26, 26), (6, 26)], outline=c, width=2)
        elif icon_type == "clock":
            d.ellipse([6, 6, 26, 26], outline=c, width=2)
            d.line([16, 16, 16, 10], fill=c, width=2)
        elif icon_type == "power":
            d.arc([8, 8, 24, 24], start=300, end=240, fill=c, width=2)
            d.line([16, 6, 16, 16], fill=c, width=2)
        return ImageTk.PhotoImage(img.resize((20, 20), Image.Resampling.LANCZOS))

    def show(self):
        if self.root is not None and self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()
            return

        self.root = tk.Toplevel(self.parent_root)
        self.root.title("Proxy Monitor - 设置")
        self.root.configure(bg=UIStyles.BG_DARK)
        
        w, h = 540, 680
        x, y = (self.root.winfo_screenwidth()-w)//2, (self.root.winfo_screenheight()-h)//2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        UIStyles.configure_styles()
        self.icons = {
            "link": self.generate_icon("link"),
            "key": self.generate_icon("key"),
            "limit": self.generate_icon("limit", (244, 63, 94)),
            "clock": self.generate_icon("clock"),
            "power": self.generate_icon("power")
        }

        # Header
        header = tk.Frame(self.root, bg=UIStyles.BG_DARK, padx=30, pady=25)
        header.pack(fill=tk.X)
        ttk.Label(header, text="首选项设置", style="Header.TLabel").pack(side=tk.LEFT)

        main_frame = ttk.Frame(self.root, style="Card.TFrame", padding=25)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        self._add_field(main_frame, "订阅链接 (Subscription URL)", "sub_url", "link")
        self._add_field(main_frame, "Server酱 SendKey", "serverchan_sendkey", "key")
        
        # Thresholds
        grp = ttk.LabelFrame(main_frame, text=" 预警阈值警告 ", padding=15)
        grp.pack(fill=tk.X, pady=20)
        self._add_grp_field(grp, "每日限额 (GB)", "daily_limit_gb", "limit")
        self._add_grp_field(grp, "突发速率 (MB/min)", "rate_limit_mb", "limit")

        self._add_field(main_frame, "检查间隔 (秒)", "check_interval", "clock", "建议 60s")
        
        # Auto start
        p_f = ttk.Frame(main_frame, style="Card.TFrame")
        p_f.pack(fill=tk.X, pady=10)
        tk.Label(p_f, image=self.icons["power"], bg=UIStyles.CARD_DARK).pack(side=tk.LEFT, padx=(0, 8))
        self.start_var = tk.BooleanVar(value=self.config_manager.get("auto_start"))
        tk.Checkbutton(p_f, text="随 Windows 启动 (开机自启)", variable=self.start_var, 
                       bg=UIStyles.CARD_DARK, fg=UIStyles.TEXT_LIGHT, activebackground=UIStyles.CARD_DARK, 
                       selectcolor=UIStyles.INPUT_BG).pack(side=tk.LEFT)

        # Footer
        footer = tk.Frame(self.root, bg=UIStyles.BG_DARK, pady=20)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        btns = ttk.Frame(footer, style="TFrame")
        btns.pack(anchor="center")
        ttk.Button(btns, text=" 确定 ", style="Primary.TButton", command=self._save).pack(side=tk.LEFT, padx=10)
        ttk.Button(btns, text=" 取消 ", style="Primary.TButton", command=self.root.destroy).pack(side=tk.LEFT, padx=10)

    def _add_field(self, parent, label, key, icon_key, help_text=""):
        f = ttk.Frame(parent, style="Card.TFrame")
        f.pack(fill=tk.X, pady=12)
        lbl_f = ttk.Frame(f, style="Card.TFrame")
        lbl_f.pack(fill=tk.X)
        tk.Label(lbl_f, image=self.icons[icon_key], bg=UIStyles.CARD_DARK).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Label(lbl_f, text=label).pack(side=tk.LEFT)
        e = tk.Entry(f, font=("Segoe UI", 11), bg=UIStyles.INPUT_BG, fg=UIStyles.TEXT_LIGHT, relief=tk.FLAT, borderwidth=8)
        e.insert(0, str(self.config_manager.get(key))); e.pack(fill=tk.X, pady=(6, 0))
        if help_text: ttk.Label(f, text=help_text, style="Sub.TLabel").pack(anchor="w", padx=(28, 0))
        self.entries[key] = e

    def _add_grp_field(self, parent, label, key, icon_key):
        f = ttk.Frame(parent, style="Card.TFrame")
        f.pack(fill=tk.X, pady=6)
        tk.Label(f, image=self.icons[icon_key], bg=UIStyles.CARD_DARK).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Label(f, text=label).pack(side=tk.LEFT)
        e = tk.Entry(f, width=15, font=("Segoe UI", 10), bg=UIStyles.INPUT_BG, fg=UIStyles.TEXT_LIGHT, relief=tk.FLAT, borderwidth=5)
        e.insert(0, str(self.config_manager.get(key))); e.pack(side=tk.RIGHT)
        self.entries[key] = e

    def _save(self):
        try:
            new_conf = {
                "sub_url": self.entries["sub_url"].get(),
                "serverchan_sendkey": self.entries["serverchan_sendkey"].get(),
                "daily_limit_gb": float(self.entries["daily_limit_gb"].get()),
                "rate_limit_mb": float(self.entries["rate_limit_mb"].get()),
                "check_interval": int(self.entries["check_interval"].get()),
                "auto_start": self.start_var.get()
            }
            if self.config_manager.save_config(new_conf):
                if self.on_save_callback:
                    self.on_save_callback()
                self.root.destroy()
        except:
            messagebox.showerror("错误", "输入非法，请检查格式")
