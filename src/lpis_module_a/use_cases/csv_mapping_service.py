from typing import List, Dict
from src.lpis_module_a.domain.vendor_order import VendorOrder
from src.lpis_module_a.domain.mapping_profile import MappingProfile
from src.lpis_module_a.domain.exceptions import MappingValidationError
from src.lpis_module_a.interfaces.i_csv_reader import ICsvReader
from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository
from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository

class CsvMappingService:
    """
    [SPEC] 3.1: 核心用例 (CsvMappingService)
    實現 [PLAN-LPIS-M1] 中的所有核心映射與儲存 AC
    """
    
    def __init__(
        self,
        csv_reader: ICsvReader,
        profile_repo: IProfileRepository,
        order_repo: IOrderRepository
    ):
        self._csv_reader = csv_reader
        self._profile_repo = profile_repo
        self._order_repo = order_repo

    def get_csv_headers(self, file_path: str) -> List[str]:
        """
        (AC-2.2 UI 輔助) 獲取 CSV 標頭，供 UI 顯示
        """
        # TODO-CAA: Implement application logic.
        pass

    def save_profile(self, name: str, mapping: Dict[str, str]) -> MappingProfile:
        """
        (AC-3.1) 建立 MappingProfile 實體並呼叫 profile_repo.save()
        """
        # TODO-CAA: Implement application logic.
        pass

    def load_profile(self, name: str) -> MappingProfile:
        """
        (AC-2.1) 呼叫 profile_repo.load() 獲取現有 Profile
        """
        # TODO-CAA: Implement application logic.
        pass

    def list_profiles(self) -> List[str]:
        """
        (AC-2.1 UI 輔助) 呼叫 profile_repo.list_profiles() 供 UI 顯示
        """
        # TODO-CAA: Implement application logic.
        pass

    def apply_mapping_and_save(self, file_path: str, profile: MappingProfile):
        """
        (AC-4.1, AC-5.1) 核心流程
        """
        # TODO-CAA: Implement application logic.
        # 1. 呼叫 self._csv_reader.read_data(file_path)
        # 2. 遍歷數據, 根據 profile.mapping 轉換為 List[VendorOrder]
        # 3. (驗證) 若缺少 [AC-2.3] 欄位, 拋出 MappingValidationError
        # 4. 呼叫 self._order_repo.save_batch(List[VendorOrder]) [cite: 44]
        pass
