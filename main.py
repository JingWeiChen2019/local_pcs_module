import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow

# 依賴注入 (Dependency Injection) - 實例化 Adapters
from src.lpis_module_a.adapters.pandas_csv_reader import PandasCsvReader
from src.lpis_module_a.adapters.json_profile_repo import JsonProfileRepository
from src.lpis_module_a.adapters.sqlite_order_repo import SqliteOrderRepository
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService
from src.lpis_module_a.ui.mapper_widget import PyQtMapperView

# 確保 'data' 目錄存在 (用於 SQLite 和 Profiles)
Path("data/profiles").mkdir(parents=True, exist_ok=True)

def main():
    """
    應用程式主入口點 (Application Entry Point)
    滿足 BASELINE_RUN_COMMAND  啟動視窗的需求 [cite: 71]
    """
    
    # 1. 設置 Adapters (具體實現)
    db_path = "data/lpis_main.db"
    profiles_dir = Path("data/profiles")
    
    csv_reader = PandasCsvReader()
    profile_repo = JsonProfileRepository(storage_path=profiles_dir)
    order_repo = SqliteOrderRepository(db_path=db_path)
    
    # 2. 設置 Use Case (核心服務)
    mapping_service = CsvMappingService(
        csv_reader=csv_reader,
        profile_repo=profile_repo,
        order_repo=order_repo
    )
    
    # 3. 設置 UI (PyQt) [cite: 59]
    app = QApplication(sys.argv)
    
    main_window = QMainWindow()
    main_window.setWindowTitle("LPIS - Module A (CSV Mapper)")
    main_window.setGeometry(100, 100, 800, 600)
    
    # 將 [SPEC] 5.4 中定義的 UI 控件作為中央控件
    mapper_view_widget = PyQtMapperView(mapping_service=mapping_service)
    main_window.setCentralWidget(mapper_view_widget)
    
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
