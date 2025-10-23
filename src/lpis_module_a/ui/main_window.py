# src/lpis_module_a/ui/main_window.py
# [BUG-M1-002] (Green Light)
# 實現 AC-1.1 (主視窗與按鈕)

import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QPushButton
)
from typing import Optional

from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService
from src.lpis_module_a.ui.mapper_widget import PyQtMapperView # 導入子視窗

class MainWindow(QMainWindow):
    """
    (AC-1.1) 應用程式主視窗
    """
    
    # [BUG-M1-001] (Fix) 
    # 確保 __init__ 簽章與 'main.py' (組合根) 一致
    def __init__(self, mapping_service: CsvMappingService, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # 依賴注入 (DI)
        self.mapping_service = mapping_service
        
        # [BUG-M1-002] (Fix)
        # 確保 'mapper_widget' (子視窗) 是 None，
        # 僅在按鈕點擊時才建立
        self.mapper_widget: Optional[PyQtMapperView] = None
        
        self.init_ui()

    def init_ui(self):
        """
        [BUG-M1-002] (Green Light)
        實現 test_ac_1_1_import_button_exists
        """
        self.setWindowTitle("LPIS 專案 (Project LPIS) [M1]")
        self.setGeometry(100, 100, 300, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # (AC-1.1) 實現「導入採購 CSV」按鈕
        self.import_button = QPushButton("導入採購 CSV (Import Purchase CSV)")
        
        # (AC-2.1 / AC-2.2) 
        # 將按鈕點擊連接到 'open_mapper' 函數
        self.import_button.clicked.connect(self.open_mapper)
        
        layout.addWidget(self.import_button)

    def open_mapper(self):
        """
        (AC-2.1) 當按鈕被點擊時，
        建立並顯示「欄位映射器」子視窗 (PyQtMapperView)
        """
        
        # (PE 註記: 這裡暫時只處理「建立 Profile」，
        #  完整的 AC-2.1 (選擇現有) 待後續 [MODIFY] 任務)
        
        # [BUG-M1-002] (Fix)
        # 僅在此時才建立 PyQtMapperView
        if self.mapper_widget is None:
            # [BUG-M1-001] (Fix) 
            # 傳遞 'mapping_service'
            self.mapper_widget = PyQtMapperView(mapping_service=self.mapping_service)
        
        # (PE 註記: 這裡暫時模擬 load_csv，
        #  真正的檔案選擇對話框待後續 [MODIFY] 任務)
        
        # 模擬 (Scenario 3.1) 觸發
        # self.mapper_widget.load_csv("dummy.csv") 
        
        self.mapper_widget.show()