# tests/ui/test_main_window.py
# [BUG-M1-002] (Red Light)
# 依據 M1_CsvMapper.spec.test.md (Scenario 3.1)
# 依據 [PLAN-LPIS-M1] (AC-1.1) 補齊 TDD 測試

import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication, QPushButton

# [BUG-M1-002] (Red Light)
# 預期：此導入將 100% 失敗 (ImportError: no module named ...)
# 因為 src/lpis_module_a/ui/main_window.py 尚未建立
from src.lpis_module_a.ui.main_window import MainWindow 

from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

@pytest.fixture
def mock_service(qtbot) -> CsvMappingService:
    """ Mock Service (用於 DI) """
    return MagicMock(spec=CsvMappingService)

@pytest.fixture
def main_win(mock_service, qtbot) -> MainWindow:
    """ (Given) 初始化主視窗 """
    app = QApplication.instance() or QApplication([])
    
    # [BUG-M1-001] (Fix) 
    # 我們已知 main.py 將使用 'mapping_service' 作為參數
    win = MainWindow(mapping_service=mock_service) 
    qtbot.addWidget(win)
    return win

#
# ----------------------------------
# 測試 [BUG-M1-002] / (AC-1.1) - [TSDD 8 - RED]
# ----------------------------------
#
def test_ac_1_1_import_button_exists(main_win: MainWindow, qtbot):
    """
    Spec (AC-1.1): 主介面必須提供一個「導入採購 CSV」的按鈕。
    
    Given: 主視窗 (MainWindow) 已啟動
    Then: 介面上必須存在一個 QPushButton
    And: 其文字必須包含 "導入採購 CSV"
    """
    
    # 查找所有 QPushButton 元件
    buttons = main_win.findChildren(QPushButton)
    
    found = False
    for btn in buttons:
        if "導入採購 CSV" in btn.text():
            found = True
            break
            
    assert found, "AC-1.1 Failed: '導入採購 CSV' button not found in MainWindow"