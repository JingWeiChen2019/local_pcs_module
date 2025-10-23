import json
from pathlib import Path
from typing import List
from src.lpis_module_a.domain.mapping_profile import MappingProfile
from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository

class JsonProfileRepository(IProfileRepository):
    """
    [SPEC] 5.2: Profile 儲存實現 (JsonProfileRepository)
    將 MappingProfile 序列化為 JSON 檔案
    """

    def __init__(self, storage_path: Path):
        self._storage_path = storage_path
        # TODO-CAA: Implement application logic.
        # (確保 self._storage_path 存在)

    def save(self, profile: MappingProfile):
        """
        實現 IProfileRepository.save
        """
        # TODO-CAA: Implement application logic.
        pass

    def load(self, name: str) -> MappingProfile:
        """
        實現 IProfileRepository.load
        """
        # TODO-CAA: Implement application logic.
        pass

    def list_profiles(self) -> List[str]:
        """
        實現 IProfileRepository.list_profiles
        """
        # TODO-CAA: Implement application logic.
        pass
