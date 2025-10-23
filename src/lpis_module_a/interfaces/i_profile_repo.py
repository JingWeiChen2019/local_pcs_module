from abc import ABC, abstractmethod
from typing import List
from src.lpis_module_a.domain.mapping_profile import MappingProfile

class IProfileRepository(ABC):
    """
    [SPEC] 4.2: Profile 儲存庫介面 (IProfileRepository)
    """
    
    @abstractmethod
    def save(self, profile: MappingProfile):
        # TODO-CAA: Implement application logic.
        pass

    @abstractmethod
    def load(self, name: str) -> MappingProfile:
        # TODO-CAA: Implement application logic.
        pass

    @abstractmethod
    def list_profiles(self) -> List[str]:
        # TODO-CAA: Implement application logic.
        pass
