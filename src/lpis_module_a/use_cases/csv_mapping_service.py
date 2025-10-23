# src/lpis_module_a/use_cases/csv_mapping_service.py
# 依據 M1_CsvMapper.spec.md (3.1) 實現
# [TSDD 7] 實現 get_csv_headers

from typing import List, Dict, Any
from src.lpis_module_a.domain.mapping_profile import MappingProfile
from src.lpis_module_a.domain.vendor_order import VendorOrder
from src.lpis_module_a.interfaces.i_csv_reader import ICsvReader
from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository
from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository
from src.lpis_module_a.domain.exceptions import MappingValidationError


class CsvMappingService:
    """ (Spec 3.1) 實現 M1 核心業務邏輯 (Use Cases) """
    
    def __init__(self, csv_reader: ICsvReader, profile_repo: IProfileRepository, order_repo: IOrderRepository):
        self.csv_reader = csv_reader
        self.profile_repo = profile_repo
        self.order_repo = order_repo

    def apply_mapping_and_save(self, file_path: str, profile: MappingProfile):
        """ [TSDD 1 & 2] 已驗證通過 """
        raw_data: List[Dict[str, Any]] = self.csv_reader.read_data(file_path)
        vendor_orders: List[VendorOrder] = []
        mapping = profile.mapping
        
        for row in raw_data:
            try:
                order = VendorOrder(
                    order_id=row[mapping["order_id"]],
                    item_name=row[mapping["item_name"]],
                    tracking_number_t1=row[mapping["tracking_number_t1"]],
                    quantity=int(row[mapping["quantity"]]), 
                    total_amount=float(row[mapping["total_amount"]]),
                    order_placed_date=row[mapping["order_placed_date"]]
                )
                vendor_orders.append(order)
            except KeyError as e:
                raise MappingValidationError(
                    f"Mapping Error: Required CSV column '{e.args[0]}' not found in data row."
                ) from e
            except ValueError as e:
                raise MappingValidationError(
                    f"Type Conversion Error: {e}. Failed to convert data in row {row}."
                ) from e
        if vendor_orders:
            self.order_repo.save_batch(vendor_orders)

    # --- (Spec 3.1) 其他方法 ---

    def get_csv_headers(self, file_path: str) -> List[str]:
        """
        (Spec 3.1 get_csv_headers)
        [TSDD 7] 實現：依據 Scenario 3.1
        呼叫 ICsvReader 獲取標頭
        """
        # (PE 註記: 委派給 Adapter)
        return self.csv_reader.get_headers(file_path)

    def save_profile(self, name: str, mapping: Dict[str, str]) -> MappingProfile:
        """ [TSDD 3] 已驗證通過 """
        profile = MappingProfile(name=name, mapping=mapping)
        self.profile_repo.save(profile)
        return profile

    def load_profile(self, name: str) -> MappingProfile:
        # TDD: 尚未有測試，暫不實現
        pass

    def list_profiles(self) -> List[str]:
        # TDD: 尚未有測試，暫不實現
        pass