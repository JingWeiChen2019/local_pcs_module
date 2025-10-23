from dataclasses import dataclass

@dataclass
class VendorOrder:
    """
    [SPEC] 2.1: 核心數據實體 (VendorOrder)
    代表 [AC-2.3] 中定義的「系統核心欄位」 [cite: 35]
    """
    order_id: str             # [cite: 36]
    item_name: str            # [cite: 37]
    tracking_number_t1: str   # [cite: 38]
    quantity: int             # [cite: 39]
    total_amount: float       # [cite: 40]
    order_placed_date: str    # [cite: 41]
