import os
import pytest
from unittest.mock import MagicMock
import socket
import urllib.error
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor_service import TrafficMonitor
from config_manager import ConfigManager

@pytest.fixture
def mock_config(tmp_path):
    conf_path = tmp_path / "config.json"
    mgr = ConfigManager(str(conf_path))
    mgr.save_config({"sub_url": "http://test-sub.local/sub", "serverchan_sendkey": "", "daily_limit_gb": 10.0, "rate_limit_mb": 100.0, "check_interval": 60})
    return mgr

@pytest.fixture
def monitor(mock_config, tmp_path):
    return TrafficMonitor(mock_config, str(tmp_path / "state.json"))

def test_get_traffic_info_success(monitor, mocker):
    mock_urlopen = mocker.patch("urllib.request.urlopen")
    
    mock_resp = MagicMock()
    mock_resp.info.return_value = {
        "subscription-userinfo": "upload=1024; download=2048; total=10240; expire=1700000000"
    }
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    res = monitor.get_traffic_info()
    assert res == (1024, 2048, 10240, 1700000000)

def test_get_traffic_info_no_header(monitor, mocker):
    mock_urlopen = mocker.patch("urllib.request.urlopen")
    mock_resp = MagicMock()
    mock_resp.info.return_value = {"content-type": "text/html"}
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    res = monitor.get_traffic_info()
    assert res is None

def test_get_traffic_info_network_error_backoff(monitor, mocker):
    mock_urlopen = mocker.patch("urllib.request.urlopen")
    # 让它一直抛出 URLError
    mock_urlopen.side_effect = urllib.error.URLError("Failed to resolve")
    
    # 必须把 sleep mock 掉，不然测试会卡在那等 2秒 + 4秒
    mock_sleep = mocker.patch("time.sleep")
    
    res = monitor.get_traffic_info()
    assert res is None
    assert mock_urlopen.call_count == 3
    # 断言指数退避被调用，先按 2 秒睡，再按 4 秒睡
    mock_sleep.assert_any_call(2)
    mock_sleep.assert_any_call(4)
    assert mock_sleep.call_count == 2
