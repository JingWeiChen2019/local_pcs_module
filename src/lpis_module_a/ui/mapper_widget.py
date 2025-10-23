# src/lpis_module_a/ui/mapper_widget.py
# 依據 M1_CsvMapper.spec.md (Spec 5.4) 
# 依據 M1_CsvMapper.spec.test.md (Scenario 3.1) 實現

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QFormLayout, 
    QLabel, 
    QComboBox, 
    QPushButton, 
    QGridLayout
)
from typing import List, Optional

# [TSDD 7] 導入 Service 介面
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

class PyQtMapperView(QWidget):
    """
    (Spec 5.4) PyQtMapperView (UI 實現)
    (Spec 3.1 / AC-2.2) 顯示一個「欄位映射器」介面。
    """

    # (Spec 2.3) 系統核心欄位 (AC-2.3)
    CORE_FIELDS = [
        "Order #",
        "Item Name",
        "Tracking Number (T1)",
        "Quantity",
        "Total Amount",
        "Order Placed Date"
    ]

    def __init__(self, service: CsvMappingService, parent: Optional[QWidget] = None):
        """
        [TSDD 7 修正] 實現 __init__ 並注入 Service
        """
        super().__init__(parent)
        
        # (Spec 5.4) 依賴注入 (DI)
        self.service = service
        
        # (Spec 3.1 / AC-2.2) 
        # 用於儲存 6 個 QComboBox (Then: 必須包含 6 個 QComboBox)
        self.combo_boxes: List[QComboBox] = []
        
        self.init_ui()

    def init_ui(self):
        """
        初始化 UI 佈局 (AC-2.2, AC-2.3)
        """
        self.setWindowTitle("CSV 欄位映射器 [M1]")
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # (AC-2.3)
        # 左側：[AC-2.3] 的 6 個核心欄位 (QLabel)。
        # 右側：(QComboBox)。
        for field_name in self.CORE_FIELDS:
            label = QLabel(field_name)
            combo = QComboBox()
            
            # [TSDD 7 關鍵]
            # 將 combo 儲存起來，以便 test_scenario_3_1 
            # 能用 findChildren(QComboBox) 找到它們
            self.combo_boxes.append(combo)
            
            form_layout.addRow(label, combo)

        layout.addLayout(form_layout)
        
        # (AC-3.1)
        self.save_button = QPushButton("儲存 Profile (Save Profile)")
        layout.addWidget(self.save_button)
        
        self.setGeometry(300, 300, 400, 300)

    def load_csv(self, file_path: str):
        """
        [TSDD 7 實現] 
        實現 test_scenario_3_1 (When: view.load_csv)
        """
        
        # (When) 呼叫 Service 獲取標頭
        # (And: service.get_csv_headers 必須被呼叫)
        headers = self.service.get_csv_headers(file_path)
        
        # (Then) 
        # (And: 每個 QComboBox 必須包含 "col_A" 和 "col_B")
        for combo in self.combo_boxes:
            combo.clear()
            combo.addItems(headers) # 填入 CSV 標頭