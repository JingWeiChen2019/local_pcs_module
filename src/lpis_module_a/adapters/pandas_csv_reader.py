import pandas as pd
from typing import List, Dict, Any
from src.lpis_module_a.interfaces.i_csv_reader import ICsvReader

class PandasCsvReader(ICsvReader):
    """
    [SPEC] 5.1: CSV 讀取實現 (PandasCsvReader)
    使用 pandas 實現 ICsvReader 
    """

    def get_headers(self, file_path: str) -> List[str]:
        """
        實現 ICsvReader.get_headers
        """
        # TODO-CAA: Implement application logic.
        pass

    def read_data(self, file_path: str) -> List[Dict[str, Any]]:
        """
        實現 ICsvReader.read_data
        注意：必須轉換為 List[Dict]，保持 Use Case 對 pandas 的獨立性
        """
        # TODO-CAA: Implement application logic.
        pass
