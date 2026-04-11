import os
import sys
import time
import datetime
from data_service import DataService

def test_db():
    print("开始测试 DataService...")
    db_name = "test_traffic.db"
    if os.path.exists(db_name):
        os.remove(db_name)
        
    ds = DataService(db_name)
    
    # 1. 测试记录
    print("正在插入模拟数据...")
    ds.record_traffic(1024*1024, 10*1024*1024*1024, 5*1024*1024*1024)
    
    # 2. 测试读取今日状态
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    used = ds.get_daily_usage(today)
    print(f"今日已用 (DB): {used / 1024**3:.2f} GB")
    assert used > 0
    
    # 3. 测试告警状态
    ds.set_daily_warned(today, True)
    assert ds.is_daily_warned(today) == True
    print("告警状态测试通过")
    
    # 4. 测试清理 (注入一条老数据)
    old_date = (datetime.datetime.now() - datetime.timedelta(days=40)).strftime("%Y-%m-%d")
    conn = ds._get_conn()
    with conn:
        conn.execute("INSERT INTO daily_stats (date, total_used, max_rate) VALUES (?, ?, ?)", (old_date, 100, 10))
    
    print("执行清理前查询老数据...")
    cursor = conn.execute("SELECT COUNT(*) FROM daily_stats WHERE date = ?", (old_date,))
    assert cursor.fetchone()[0] == 1
    
    ds.prune_old_data(30)
    
    cursor = conn.execute("SELECT COUNT(*) FROM daily_stats WHERE date = ?", (old_date,))
    assert cursor.fetchone()[0] == 0
    print("数据清理测试通过")
    
    os.remove(db_name)
    print("🎉 所有持久化测试通过！")

if __name__ == "__main__":
    test_db()
