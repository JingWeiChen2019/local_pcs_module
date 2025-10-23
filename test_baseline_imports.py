# test_baseline_imports.py
# PE DESIGN for [SETUP-GLOBAL] AC 

def test_import_core_dependencies():
    """
    驗證 [STRAT-R1] (V2) 基準線中定義的所有核心依賴均可被成功導入，
    以證明環境已正確配置且模組間無基礎衝突。
    [cite: 17564, 17567]
    """
    try:
        # 1. 應用程式框架 [cite: 17541, 17556]
        import PyQt6
        from PyQt6.QtWidgets import QApplication
        print("PyQt6 OK")

        # 2. 核心數據處理 [cite: 17543, 17557]
        import pandas
        print("pandas OK")

        # 3. XLSX 支援 [cite: 17544, 17558]
        import openpyxl
        print("openpyxl OK")

        # 4. PDF 處理 (PyMuPDF) [cite: 17545, 17559]
        import fitz # PyMuPDF's import name
        print("PyMuPDF (fitz) OK")

        # 5. TSDD 測試框架 [cite: 17547, 17560]
        import pytest
        print("pytest OK")

        # 6. TSDD UI 測試 [cite: 17548, 17561]
        import pytestqt
        print("pytest-qt OK")

    except ImportError as e:
        # 如果任何導入失敗，測試將失敗
        assert False, f"Failed to import a core dependency: {e}"

    assert True