# main.py
# [BUG-M1-002] (Green Light)
# 修正組合根 (Composition Root)

import sys
from PyQt6.QtWidgets import QApplication

# 1. Import Adapters
from src.lpis_module_a.adapters.pandas_csv_reader import PandasCsvReader
from src.lpis_module_a.adapters.json_profile_repo import JsonProfileRepository
from src.lpis_module_a.adapters.sqlite_order_repo import SqliteOrderRepository

# 2. Import Use Case
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

# 3. Import UI
# [BUG-M1-002] (Fix)
# 導入 MainWindow (AC-1.1)，而非 PyQtMapperView
from src.lpis_module_a.ui.main_window import MainWindow 

def main():
    """
    (AC-1.1) 啟動 PyQt 主視窗
    """
    app = QApplication(sys.argv)

    # --- (Spec) Composition Root ---
    # 1. Init Adapters (Ports)
    csv_reader = PandasCsvReader()
    profile_repo = JsonProfileRepository(storage_path="data/profiles") # (Spec 5.2)
    order_repo = SqliteOrderRepository(db_path="data/lpis_main.db") # (Spec 5.3)

    # 2. Init Use Case (injecting Adapters)
    mapping_service = CsvMappingService(
        csv_reader=csv_reader,
        profile_repo=profile_repo,
        order_repo=order_repo
    )
    
    # 3. Init UI (injecting Use Case)
    # [BUG-M1-002] (Fix)
    # 啟動 MainWindow (AC-1.1)，並傳入 DI
    window = MainWindow(mapping_service=mapping_service)
    
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()