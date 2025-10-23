# tests/ui/test_mapper_widget.py
# 依據 M1_CsvMapper.spec.md (Spec 5.4) 
# 依據 M1_CsvMapper.spec.test.md (Scenario 3.1) 撰寫

import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication, QComboBox

# [TSDD 7] 導入被測 UI 元件
from src.lpis_module_a.ui.mapper_widget import PyQtMapperView
# [TSDD 7] 導入 Mock Service
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

# (PE 註記: pytest-qt 會自動提供 'qtbot' fixture)

@pytest.fixture
def mock_service() -> CsvMappingService:
    """ (Scenario 3.1 Given) Mock CsvMappingService """
    service = MagicMock(spec=CsvMappingService)
    
    # (Scenario 3.1 Given) Mock get_csv_headers() 
    # 回傳 ["col_A", "col_B"]
    service.get_csv_headers.return_value = ["col_A", "col_B"]
    return service

@pytest.fixture
def view(mock_service: CsvMappingService, qtbot):
    """ 
    (Given) 初始化主應用程式 (PyQtMapperView)
    並注入 Mock Service
    """
    # 確保 QApplication 存在 (pytest-qt 的要求)
    app = QApplication.instance() or QApplication([])

    # [TSDD 7] 實例化 UI
    # (PE 註記: PyQtMapperView 尚未實現)
    # 預期: 此處將 100% 失敗 (Red Light)。
    widget = PyQtMapperView(service=mock_service)
    
    # (PE 註記: qtbot.addWidget 是 pytest-qt 的標準做法，
    #  確保 widget 在測試結束時被清理)
    qtbot.addWidget(widget)
    
    return widget

#
# ----------------------------------
# 測試 Spec 5.4 / Scenario 3.1 (UI) - [TSDD 7 - RED]
# ----------------------------------
#
def test_scenario_3_1_ui_loads_headers_into_comboboxes(
    view: PyQtMapperView, 
    qtbot,
    mock_service: CsvMappingService
):
    """
    Spec 3.1: (AC-2.2) 
    Then: 介面上必須包含 6 個 QComboBox (下拉選單)。
    And: 每個 QComboBox 必須包含 "col_A" 和 "col_B" 選項。
    """
    
    # (Given) 模擬導入 CSV 檔案
    dummy_file_path = "dummy.csv"
    
    # (When) 
    # (PE 註記: 假設 UI 有一個方法叫 'load_csv' 
    #  來觸發 'get_csv_headers')
    # 
    # (PyQtMapperView.load_csv 尚未實現)
    view.load_csv(dummy_file_path)

    # Then (AC-2.2) - 驗證 Service 被呼叫
    mock_service.get_csv_headers.assert_called_with(dummy_file_path)

    # Then (AC-2.2) - 驗證 UI
    # 查找所有 QComboBox 元件
    combos = view.findChildren(QComboBox)
    
    # (And: 必須包含 6 個 QComboBox)
    # (PE 註記: 這是針對 AC-2.3 的 6 個核心欄位)
    assert len(combos) == 6, f"Expected 6 QComboBoxes, but found {len(combos)}"
    
    # (And: 每個 QComboBox 必須包含 "col_A" 和 "col_B")
    for i, combo in enumerate(combos):
        items = [combo.itemText(j) for j in range(combo.count())]
        assert "col_A" in items, f"ComboBox {i} missing 'col_A'"
        assert "col_B" in items, f"ComboBox {i} missing 'col_B'"