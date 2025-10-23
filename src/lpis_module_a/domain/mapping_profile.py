from dataclasses import dataclass
from typing import Dict

@dataclass
class MappingProfile:
    """
    [SPEC] 2.2: 映射設定檔 (MappingProfile)
    儲存外部 CSV 欄位與內部 VendorOrder 核心欄位的對應關係 [cite: 28]
    """
    name: str
    mapping: Dict[str, str]  # e.g., {"order_id": "CSV Column Name"}
