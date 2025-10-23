from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ICsvReader(ABC):
    """
    [SPEC] 4.1: CSV 讀取器介面 (ICsvReader)
    """
    
    @abstractmethod
    def get_headers(self, file_path: str) -> List[str]:
        # TODO-CAA: Implement application logic.
        pass

    @abstractmethod
    def read_data(self, file_path: str) -> List[Dict[str, Any]]:
        # TODO-CAA: Implement application logic.
        pass
