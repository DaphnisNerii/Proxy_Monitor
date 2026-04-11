import sqlite3
import threading
import os
import datetime
import json

class DataService:
    _instance = None
    _lock = threading.Lock()
    _local = threading.local()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DataService, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path="traffic.db"):
        if self._initialized:
            return
        self.db_path = db_path
        self._init_db()
        self._initialized = True

    def _get_conn(self):
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(self.db_path, timeout=30)
            # 开启 WAL 模式以支持并发读写
            self._local.conn.execute("PRAGMA journal_mode=WAL;")
            self._local.conn.execute("PRAGMA synchronous=NORMAL;")
        return self._local.conn

    def _init_db(self):
        conn = self._get_conn()
        with conn:
            # 明细记录表 (30天)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS traffic_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    delta_bytes INTEGER NOT NULL,
                    used_bytes INTEGER NOT NULL,
                    remaining_bytes INTEGER NOT NULL
                )
            """)
            # 每日汇总表 (30天)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_used INTEGER NOT NULL,
                    max_rate INTEGER NOT NULL,
                    warned BOOLEAN DEFAULT 0
                )
            """)
            # 索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_history_ts ON traffic_history(timestamp)")

    def record_traffic(self, delta, used, remaining):
        conn = self._get_conn()
        now = datetime.datetime.now()
        ts = now.isoformat()
        date_str = now.strftime("%Y-%m-%d")

        with conn:
            # 1. 存入明细
            conn.execute(
                "INSERT INTO traffic_history (timestamp, delta_bytes, used_bytes, remaining_bytes) VALUES (?, ?, ?, ?)",
                (ts, delta, used, remaining)
            )
            # 2. 更新每日汇总
            # 使用 UPSERT 语法 (SQLite 3.24+)
            conn.execute("""
                INSERT INTO daily_stats (date, total_used, max_rate)
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    total_used = excluded.total_used,
                    max_rate = MAX(daily_stats.max_rate, excluded.max_rate)
            """, (date_str, used, delta))
            
    def get_daily_usage(self, date_str):
        conn = self._get_conn()
        cursor = conn.execute("SELECT total_used FROM daily_stats WHERE date = ?", (date_str,))
        row = cursor.fetchone()
        return row[0] if row else 0

    def set_daily_warned(self, date_str, warned=True):
        conn = self._get_conn()
        with conn:
            conn.execute("UPDATE daily_stats SET warned = ? WHERE date = ?", (warned, date_str))

    def is_daily_warned(self, date_str):
        conn = self._get_conn()
        cursor = conn.execute("SELECT warned FROM daily_stats WHERE date = ?", (date_str,))
        row = cursor.fetchone()
        return bool(row[0]) if row else False

    def prune_old_data(self, days=30):
        conn = self._get_conn()
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        
        with conn:
            h = conn.execute("DELETE FROM traffic_history WHERE timestamp < ?", (cutoff,))
            d = conn.execute("DELETE FROM daily_stats WHERE date < ?", (cutoff_date,))
            print(f"[{datetime.datetime.now()}] 数据清理完成: 移除 {h.rowcount} 条明细, {d.rowcount} 条汇总")

    def migrate_from_json(self, json_path):
        if not os.path.exists(json_path):
            return False
            
        try:
            with open(json_path, 'r') as f:
                state = json.load(f)
            
            date_str = state.get("date")
            if date_str:
                conn = self._get_conn()
                with conn:
                    # 模拟一笔迁移数据
                    conn.execute("""
                        INSERT OR IGNORE INTO daily_stats (date, total_used, max_rate, warned)
                        VALUES (?, ?, ?, ?)
                    """, (date_str, state.get("last_total_used", 0), 0, state.get("daily_warned", False)))
            
            # 迁移成功后重命名文件
            bak_path = json_path + ".bak"
            if os.path.exists(bak_path):
                os.remove(bak_path)
            os.rename(json_path, bak_path)
            print(f"[{datetime.datetime.now()}] 已从 JSON 迁移数据并备份原始文件")
            return True
        except Exception as e:
            print(f"迁移失败: {e}")
            return False
