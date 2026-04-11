import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from system_utils import NamedMutex

def test_named_mutex_success(mocker):
    mock_ctypes = mocker.patch("system_utils.ctypes")
    
    # 模拟第一次获取
    mock_ctypes.windll.kernel32.CreateMutexW.return_value = 12345
    mock_ctypes.windll.kernel32.GetLastError.return_value = 0 # 没有发生 ERROR_ALREADY_EXISTS

    mutex = NamedMutex("TestMutex1")
    assert mutex.acquire() is True
    
    # 手动 release 应该调用 CloseHandle
    mutex.release()
    mock_ctypes.windll.kernel32.CloseHandle.assert_called_with(12345)

def test_named_mutex_already_exists(mocker):
    mock_ctypes = mocker.patch("system_utils.ctypes")
    
    # 模拟第二次获取
    mock_ctypes.windll.kernel32.CreateMutexW.return_value = 54321
    mock_ctypes.windll.kernel32.GetLastError.return_value = 183 # ERROR_ALREADY_EXISTS

    mutex2 = NamedMutex("TestMutex2")
    assert mutex2.acquire() is False
