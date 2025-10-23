# tests/ui/test_mapper_widget.py
# 依據 M1_CsvMapper.spec.md (Spec 5.4) 
# 依據 M1_CsvMapper.spec.test.md (Scenario 3.1) 撰寫
# [BUG-M1-001] 修正 (Red Light)

import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication, QComboBox

from src.lpis_module_a.ui.mapper_widget import PyQtMapperView
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

@pytest.fixture
def mock_service() -> CsvMappingService:
    service = MagicMock(spec=CsvMappingService)
    service.get_csv_headers.return_value = ["col_A", "col_B"]
    return service

@pytest.fixture
def view(mock_service: CsvMappingService, qtbot):
    app = QApplication.instance() or QApplication([])

    # [BUG-M1-001] (Red Light)
    # 修正呼叫簽章，使其與 main.py (UAT) 的呼叫方式一致。
    # 
    # 原 (TDD): widget = PyQtMapperView(service=mock_service)
    # 新 (UAT):
    widget = PyQtMapperView(mapping_service=mock_service)
    
    # 預期: 此處將 100% 失敗 (Red Light)，
    #       拋出 'unexpected keyword argument 'mapping_service''
    
    qtbot.addWidget(widget)
    return widget

def test_scenario_3_1_ui_loads_headers_into_comboboxes(
    view: PyQtMapperView, 
    qtbot,
    mock_service: CsvMappingService
):
    """ Spec 3.1: (AC-2.2) """
    
    dummy_file_path = "dummy.csv"
    
    # (When) 
    view.load_csv(dummy_file_path)

    # Then (AC-2.2) - 驗證 Service 被呼叫
    # (PE 註記: 'service' 是 UI 內部的屬性名稱)
    view.service.get_csv_headers.assert_called_with(dummy_file_path)

    # Then (AC-2.2) - 驗證 UI
    combos = view.findChildren(QComboBox)
    assert len(combos) == 6, f"Expected 6 QComboBoxes, but found {len(combos)}"
    
    for i, combo in enumerate(combos):
        items = [combo.itemText(j) for j in range(combo.count())]
        assert "col_A" in items, f"ComboBox {i} missing 'col_A'"
        assert "col_B" in items, f"ComboBox {i} missing 'col_B'"