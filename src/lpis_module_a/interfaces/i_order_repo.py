from abc import ABC, abstractmethod
from typing import List
from src.lpis_module_a.domain.vendor_order import VendorOrder

class IOrderRepository(ABC):
    """
    [SPEC] 4.3: 訂單儲存庫介面 (IOrderRepository)
    """
    
    @abstractmethod
    def save_batch(self, orders: List[VendorOrder]):
        # TODO-CAA: Implement application logic.
        pass

    @abstractmethod
    def _init_table(self):
        # TODO-CAA: Implement application logic.
        pass
