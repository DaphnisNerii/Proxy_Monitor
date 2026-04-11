import os
import json
import pytest
import sys

# 临时将项目根目录加入 sys.path 以便导入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_manager import ConfigManager

@pytest.fixture
def temp_config(tmp_path):
    return os.path.join(tmp_path, "config.json")

def test_load_default_config(temp_config):
    mgr = ConfigManager(temp_config)
    assert mgr.get("check_interval") == 60
    assert mgr.get("auto_start") is False
    assert mgr.get("sub_url") == ""

def test_load_existing_config(temp_config):
    with open(temp_config, "w", encoding="utf-8") as f:
        json.dump({"check_interval": 120, "auto_start": True}, f)
    
    mgr = ConfigManager(temp_config)
    assert mgr.get("check_interval") == 120
    assert mgr.get("auto_start") is True

def test_save_config(temp_config, mocker):
    # Mock config_manager winreg to avoid touching real registry
    mocker.patch("config_manager.winreg", None)
    
    mgr = ConfigManager(temp_config)
    success = mgr.save_config({"check_interval": 300, "daily_limit_gb": 5.0})
    
    assert success is True
    with open(temp_config, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["check_interval"] == 300
    assert data["daily_limit_gb"] == 5.0

def test_sync_auto_start_winreg(temp_config, mocker):
    mock_reg = mocker.patch("config_manager.winreg")
    mock_key = mocker.Mock()
    mock_reg.OpenKey.return_value = mock_key
    mock_reg.HKEY_CURRENT_USER = "HKEY_CURRENT_USER"
    mock_reg.KEY_SET_VALUE = "KEY_SET_VALUE"
    
    mgr = ConfigManager(temp_config)
    
    # 启用
    mgr.save_config({"auto_start": True})
    mock_reg.OpenKey.assert_called_with("HKEY_CURRENT_USER", r"Software\Microsoft\Windows\CurrentVersion\Run", 0, "KEY_SET_VALUE")
    mock_reg.SetValueEx.assert_called()
    mock_reg.CloseKey.assert_called_with(mock_key)
    
    # 禁用
    mgr.save_config({"auto_start": False})
    mock_reg.DeleteValue.assert_called_with(mock_key, "ProxyTrafficMonitor")
