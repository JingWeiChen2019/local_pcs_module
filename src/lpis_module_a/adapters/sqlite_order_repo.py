# src/lpis_module_a/adapters/sqlite_order_repo.py
# 依據 M1_CsvMapper.spec.md (Spec 5.3) 實現

import sqlite3
from typing import List
from dataclasses import astuple # 用於將 dataclass 轉為 tuple

from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository
from src.lpis_module_a.domain.vendor_order import VendorOrder

class SqliteOrderRepository(IOrderRepository):
    """
    (Spec 5.3) SqliteOrderRepository (訂單儲存實現)
    
    實現 IOrderRepository 介面，使用 SQLite 儲存 VendorOrder。
    """
    
    def __init__(self, db_path: str = "data/lpis_main.db"):
        """
        初始化儲存庫，並確保資料表存在。
        :param db_path: SQLite 資料庫檔案路徑
        """
        self.db_path = db_path
        # (Spec 5.3 _init_table) 
        # [TSDD 6 修正] 在初始化時立即呼叫 _init_table()
        self._init_table()

    def _get_connection(self):
        """ 輔助方法：獲取資料庫連接 """
        return sqlite3.connect(self.db_path)

    def _init_table(self):
        """
        (Spec 5.3 / AC-5.1) 
        確保 'vendor_orders' 資料表存在，並包含 [AC-2.3] 的 6 個欄位。
        [TSDD 6 修正] 實現此方法以通過 test_init_table_creates_table
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS vendor_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            item_name TEXT,
            tracking_number_t1 TEXT NOT NULL,
            quantity INTEGER,
            total_amount REAL,
            order_placed_date TEXT
        );
        """
        # (PE 註記: tracking_number_t1 設為 NOT NULL 
        #  是良好的防禦性設計，因為它是 Module-B 的關鍵)
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(create_table_sql)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table 'vendor_orders' in {self.db_path}: {e}")
            raise

    def save_batch(self, orders: List[VendorOrder]):
        """
        (Spec 5.3 / Scenario 2.2) 
        使用 executemany() 將 List[VendorOrder] 寫入 SQLite。
        [TSDD 6 修正] 實現此方法以通過 test_save_batch
        """
        
        # 1. (Spec 5.3 關鍵) 將 List[VendorOrder (Dataclass)] 
        #    轉換為 List[Tuple] 以便 executemany 使用。
        #    (注意: astuple 會依 dataclass 定義的順序轉換)
        data_tuples = [astuple(order) for order in orders]
        
        # [AC-2.3] 的 6 個欄位
        insert_sql = """
        INSERT INTO vendor_orders (
            order_id, item_name, tracking_number_t1, 
            quantity, total_amount, order_placed_date
        ) VALUES (?, ?, ?, ?, ?, ?);
        """
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # 2. (Spec 5.3 關鍵) 執行 'executemany'
                cursor.executemany(insert_sql, data_tuples)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving batch to 'vendor_orders': {e}")
            raise