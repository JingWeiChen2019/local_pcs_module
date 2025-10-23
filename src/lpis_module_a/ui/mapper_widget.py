from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox, 
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

class PyQtMapperView(QWidget):
    """
    [SPEC] 5.4: UI 實現 (PyQtMapperView)
    實現 (AC-1.1, AC-2.2) [cite: 32, 34]
    """
    
    def __init__(self, mapping_service: CsvMappingService, parent=None):
        super().__init__(parent)
        self._service = mapping_service
        self._init_ui()

    def _init_ui(self):
        """
        初始化主 UI 控件
        """
        layout = QVBoxLayout(self)
        
        # (AC-1.1) "導入採購 CSV" 按鈕 [cite: 32]
        self._import_button = QPushButton("Import Purchase CSV")
        self._import_button.clicked.connect(self._on_import_clicked)
        
        layout.addWidget(self._import_button)
        
        # TODO-CAA: Implement application logic.
        # (添加其他 UI 元素, e.g., 一個 TableView 顯示導入的數據)
        
        self.setLayout(layout)

    def _on_import_clicked(self):
        """
        (AC-2.1) 處理導入按鈕點擊 [cite: 33]
        """
        # TODO-CAA: Implement application logic.
        # 1. 彈出 QFileDialog 選擇 CSV 檔案
        # 2. 獲取 file_path
        # 3. 彈出對話框詢問 "選擇現有 Profile" 或 "建立新 Profile" [cite: 33]
        # 4. if "建立新":
        #    headers = self._service.get_csv_headers(file_path)
        #    self._show_mapper_dialog(headers, file_path)
        # 5. if "選擇現有":
        #    profile_name = (顯示 Profile 選擇對話框)
        #    profile = self._service.load_profile(profile_name)
        #    self._service.apply_mapping_and_save(file_path, profile) [cite: 43]
        pass

    def _show_mapper_dialog(self, csv_headers: List[str], file_path: str):
        """
        (AC-2.2) 顯示「欄位映射器」UI [cite: 34]
        """
        # TODO-CAA: Implement application logic.
        # 1. 創建一個 QDialog
        # 2. (AC-2.3) 創建 6 個 QLabels (核心欄位) [cite: 35]
        # 3. (AC-2.3) 創建 6 個 QComboBox (下拉選單), 填充 csv_headers
        # 4. 創建 "Save Profile" 按鈕 (AC-3.1) [cite: 42]
        # 5. 點擊 "Save Profile" 時:
        #    mapping = (從 6 個 QComboBox 獲取)
        #    profile_name = (詢問使用者命名)
        #    profile = self._service.save_profile(profile_name, mapping)
        #    self._service.apply_mapping_and_save(file_path, profile)
        pass
