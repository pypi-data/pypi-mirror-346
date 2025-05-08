import pytest
from PyThinkDesign import Application
import pythoncom

@pytest.fixture(autouse=True)
def com_cleanup():
    # 确保每个测试前初始化COM库
    #print('\n---com intialize by module:Application---')
    pythoncom.CoInitialize()
    yield
    # 测试后清理COM库
    #print('\n---com unintialize by module: Application---')
    pythoncom.CoUninitialize()

def test_GetOrCreateApplication():
    app = Application.GetOrCreateApplication()
    assert app is not None

