# tests/adapters/test_sqlite_order_repo.py
# 依據 M1_CsvMapper.spec.md (Spec 5.3) 
# 依據 M1_CsvMapper.spec.test.md (Scenario 2.2) 撰寫

import pytest
import os
import sqlite3 # 導入依賴
from src.lpis_module_a.adapters.sqlite_order_repo import SqliteOrderRepository
from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository
from src.lpis_module_a.domain.vendor_order import VendorOrder

@pytest.fixture
def temp_db_file(tmp_path):
    """
    (Given) 建立一個真實的 (暫時性) SQLite 資料庫檔案
    'tmp_path' 是 pytest 提供的內建 fixture
    """
    db_file = tmp_path / "test_lpis.db"
    return str(db_file) # 回傳檔案路徑

@pytest.fixture
def repo(temp_db_file: str) -> SqliteOrderRepository:
    """ 
    初始化我們的 Adapter 實體，並注入暫存 DB 路徑。
    (PE 註記: 每次測試都使用一個全新的、空白的資料庫)
    """
    return SqliteOrderRepository(db_path=temp_db_file)

@pytest.fixture
def sample_orders() -> list[VendorOrder]:
    """ (Scenario 2.2 Given) 提供一個 List[VendorOrder] """
    return [
        VendorOrder(
            order_id="123-ABC",
            item_name="Test Item 1",
            tracking_number_t1="TBA123", # (Scenario 2.2 關鍵)
            quantity=1,
            total_amount=19.99,
            order_placed_date="2025-10-01"
        ),
        VendorOrder(
            order_id="456-DEF",
            item_name="Test Item 2",
            tracking_number_t1="TBA456",
            quantity=2,
            total_amount=9.99,
            order_placed_date="2025-10-02"
        )
    ]

#
# ----------------------------------
# 測試 Spec 5.3 (Adapter) - [TSDD 6 - RED]
# ----------------------------------
#
def test_adapter_implements_interface(repo: SqliteOrderRepository):
    """ 驗證 Adapter 確實遵循 Interface (Clean Architecture) """
    assert isinstance(repo, IOrderRepository)

def test_init_table_creates_table(repo: SqliteOrderRepository, temp_db_file: str):
    """ (Spec 5.3 _init_table) 測試 _init_table 是否成功建表 """
    
    # (Given) 尚未呼叫 save_batch，表不應存在 (或由 __init__ 觸發)
    # (When) _init_table 應在 repo 初始化時被隱含呼叫
    
    # Then (AC-5.1) - 驗證 `vendor_orders` 表已存在
    # PE 註記: repo.save_batch 目前是 'pass'，且 __init__ 
    #         可能未呼叫 _init_table。
    # 預期: 此測試將 100% 失敗 (Red Light)。
    conn = sqlite3.connect(temp_db_file)
    cursor = conn.cursor()
    
    # 查詢 sqlite_master 表以確認 'vendor_orders' 表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vendor_orders'")
    table_exists = cursor.fetchone()
    conn.close()
    
    assert table_exists is not None, "Table 'vendor_orders' was not created by __init__"

def test_save_batch(repo: SqliteOrderRepository, sample_orders: list[VendorOrder], temp_db_file: str):
    """ (Spec 5.3 / Scenario 2.2) 測試 save_batch 方法 """
    
    # When
    # PE 註記: repo.save_batch 目前是 'pass'
    # 預期: 此測試將 100% 失敗 (Red Light)。
    repo.save_batch(sample_orders)

    # Then (Scenario 2.2 - And: ...資料庫必須包含 "TBA123" 紀錄)
    conn = sqlite3.connect(temp_db_file)
    conn.row_factory = sqlite3.Row # 讓我們可以通過欄位名訪問
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vendor_orders WHERE tracking_number_t1 = ?", ("TBA123",))
    row = cursor.fetchone()
    
    assert row is not None, "No record found with tracking_number_t1='TBA123'"
    assert row["order_id"] == "123-ABC"
    assert row["quantity"] == 1
    assert row["total_amount"] == 19.99
    
    cursor.execute("SELECT COUNT(*) FROM vendor_orders")
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count == 2, "save_batch did not insert all 2 records"