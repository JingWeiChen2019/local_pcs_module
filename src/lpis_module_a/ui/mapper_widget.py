# src/lpis_module_a/ui/mapper_widget.py
# 依據 M1_CsvMapper.spec.md (Spec 5.4) 
# [BUG-M1-001] 修正 (Green Light)

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

from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

class PyQtMapperView(QWidget):
    """
    (Spec 5.4) PyQtMapperView (UI 實現)
    """

    CORE_FIELDS = [
        "Order #",
        "Item Name",
        "Tracking Number (T1)",
        "Quantity",
        "Total Amount",
        "Order Placed Date"
    ]

    # [BUG-M1-001] (Green Light)
    # 修正 __init__ 簽章，使其匹配 main.py (UAT) 的呼叫
    #
    # 原 (TDD): def __init__(self, service: CsvMappingService, ...):
    # 新 (UAT):
    def __init__(self, mapping_service: CsvMappingService, parent: Optional[QWidget] = None):
        """
        [TSDD 7 修正] 實現 __init__ 並注入 Service
        """
        super().__init__(parent)
        
        # (PE 註記: 外部參數是 'mapping_service'，
        #  我們在類別內部的屬性名稱仍保持 'service'。)
        self.service = mapping_service
        
        self.combo_boxes: List[QComboBox] = []
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CSV 欄位映射器 [M1]")
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        for field_name in self.CORE_FIELDS:
            label = QLabel(field_name)
            combo = QComboBox()
            self.combo_boxes.append(combo)
            form_layout.addRow(label, combo)

        layout.addLayout(form_layout)
        self.save_button = QPushButton("儲存 Profile (Save Profile)")
        layout.addWidget(self.save_button)
        self.setGeometry(300, 300, 400, 300)

    def load_csv(self, file_path: str):
        headers = self.service.get_csv_headers(file_path)
        
        for combo in self.combo_boxes:
            combo.clear()
            combo.addItems(headers)