# src/lpis_module_a/adapters/json_profile_repo.py
# 依據 M1_CsvMapper.spec.md (Spec 5.2) 實現

import os
import json
from typing import List
from dataclasses import asdict

from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository
from src.lpis_module_a.domain.mapping_profile import MappingProfile

class JsonProfileRepository(IProfileRepository):
    """
    (Spec 5.2) JsonProfileRepository (Profile 儲存實現)
    
    實現 IProfileRepository 介面，使用 JSON 檔案儲存 Profile。
    """
    
    def __init__(self, storage_path: str = "data/profiles"):
        """
        初始化儲存庫
        :param storage_path: Profile JSON 檔案的儲存目錄
        """
        self.storage_path = storage_path
        # (Spec 5.2 隱含要求) 確保目錄存在
        os.makedirs(self.storage_path, exist_ok=True)

    def _get_file_path(self, name: str) -> str:
        """ 輔助方法：獲取 Profile 的完整檔案路徑 """
        return os.path.join(self.storage_path, f"{name}.json")

    def save(self, profile: MappingProfile):
        """
        (Spec 5.2 / Scenario 2.1) 實現 save
        將 MappingProfile 實體序列化為 JSON 並儲存
        """
        file_path = self._get_file_path(profile.name)
        
        try:
            # 使用 asdict 將 dataclass 轉為 dict 以便 json.dump
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(profile), f, indent=4)
        except IOError as e:
            print(f"Error saving profile {profile.name} to {file_path}: {e}")
            raise

    def load(self, name: str) -> MappingProfile:
        """
        (Spec 5.2) 實現 load
        從 JSON 檔案讀取數據並反序列化為 MappingProfile 實體
        """
        file_path = self._get_file_path(name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # (Spec 5.2 關鍵) 將 dict 轉回 dataclass
            return MappingProfile(**data)
        except FileNotFoundError:
            raise
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading profile {name} from {file_path}: {e}")
            raise

    def list_profiles(self) -> List[str]:
        """
        (Spec 5.2) 實現 list_profiles
        掃描目錄，僅回傳 .json 檔案的名稱 (不含副檔名)
        """
        profiles: List[str] = []
        try:
            for file_name in os.listdir(self.storage_path):
                if file_name.endswith(".json"):
                    profile_name = os.path.splitext(file_name)[0]
                    profiles.append(profile_name)
            return profiles
        except OSError as e:
            print(f"Error listing profiles in {self.storage_path}: {e}")
            return []