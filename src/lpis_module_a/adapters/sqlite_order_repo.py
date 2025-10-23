import sqlite3
from typing import List
from src.lpis_module_a.domain.vendor_order import VendorOrder
from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository

class SqliteOrderRepository(IOrderRepository):
    """
    [SPEC] 5.3: 訂單儲存實現 (SqliteOrderRepository)
    使用 sqlite3 將 VendorOrder 寫入 'vendor_orders' 表 [cite: 44]
    """
    
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._init_table()

    def _init_table(self):
        """
        (AC-5.1) 建立 vendor_orders 表，包含 [AC-2.3] 的 6 個欄位
        """
        # TODO-CAA: Implement application logic.
        pass

    def save_batch(self, orders: List[VendorOrder]):
        """
        (AC-5.1) 使用 executemany() 將 List[VendorOrder] 寫入 SQLite
        """
        # TODO-CAA: Implement application logic.
        pass
