# tests/adapters/test_json_profile_repo.py
# 依據 M1_CsvMapper.spec.md (Spec 5.2) 
# 依據 M1_CsvMapper.spec.test.md (Scenario 2.1) 撰寫

import pytest
import os
import json # 導入 json 依賴
from src.lpis_module_a.adapters.json_profile_repo import JsonProfileRepository
from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository
from src.lpis_module_a.domain.mapping_profile import MappingProfile

@pytest.fixture
def temp_profile_dir(tmp_path):
    """
    (Given) 建立一個真實的 (暫時性) Profile 儲存目錄
    'tmp_path' 是 pytest 提供的內建 fixture
    """
    profile_dir = tmp_path / "profiles"
    profile_dir.mkdir()
    return str(profile_dir) # 回傳目錄路徑

@pytest.fixture
def repo(temp_profile_dir: str) -> JsonProfileRepository:
    """ 初始化我們的 Adapter 實體，並注入暫存目錄路徑 """
    # (Spec 5.2) ...儲存於 (e.g., data/profiles/*.json)
    return JsonProfileRepository(storage_path=temp_profile_dir)

@pytest.fixture
def walmart_profile() -> MappingProfile:
    """ (Scenario 2.1 Given) """
    return MappingProfile(
        name="Walmart",
        mapping={"order_id": "PO_NUMBER"}
    )

#
# ----------------------------------
# 測試 Spec 5.2 (Adapter) - [TSDD 5 - RED]
# ----------------------------------
#
def test_adapter_implements_interface(repo: JsonProfileRepository):
    """ 驗證 Adapter 確實遵循 Interface (Clean Architecture) """
    assert isinstance(repo, IProfileRepository)

def test_save_profile(repo: JsonProfileRepository, walmart_profile: MappingProfile, temp_profile_dir: str):
    """ (Spec 5.2 / Scenario 2.1) 測試 save 方法 """
    
    # When
    # PE 註記: JsonProfileRepository.save 目前是 'pass'
    # 預期: 此測試將 100% 失敗 (Red Light)。
    repo.save(walmart_profile)

    # Then (Scenario 2.1 - And: ...一個 "Walmart.json" 檔案必須被建立)
    expected_file = os.path.join(temp_profile_dir, "Walmart.json")
    assert os.path.exists(expected_file)
    
    # (And: ...且內容包含 "PO_NUMBER")
    with open(expected_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert data["name"] == "Walmart"
    assert data["mapping"]["order_id"] == "PO_NUMBER"

def test_load_profile(repo: JsonProfileRepository, walmart_profile: MappingProfile, temp_profile_dir: str):
    """ (Spec 5.2) 測試 load 方法 """
    
    # (Given) 先手動建立一個檔案
    test_file = os.path.join(temp_profile_dir, "Walmart.json")
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump({"name": "Walmart", "mapping": {"order_id": "PO_NUMBER"}}, f)

    # When
    # PE 註記: JsonProfileRepository.load 目前是 'pass'
    # 預期: 此測試將 100% 失敗 (Red Light)。
    profile = repo.load("Walmart")

    # Then
    assert isinstance(profile, MappingProfile)
    assert profile.name == "Walmart"
    assert profile.mapping["order_id"] == "PO_NUMBER"

def test_list_profiles(repo: JsonProfileRepository, temp_profile_dir: str):
    """ (Spec 5.2) 測試 list_profiles 方法 """
    
    # (Given) 建立兩個 .json 檔案和一個 .txt 檔案
    (open(os.path.join(temp_profile_dir, "Amazon.json"), 'w')).close()
    (open(os.path.join(temp_profile_dir, "Walmart.json"), 'w')).close()
    (open(os.path.join(temp_profile_dir, "readme.txt"), 'w')).close()

    # When
    # PE 註記: JsonProfileRepository.list_profiles 目前是 'pass'
    # 預期: 此測試將 100% 失敗 (Red Light)。
    profiles = repo.list_profiles()

    # Then (應只回傳 .json 檔案的名稱，不含副檔名)
    assert isinstance(profiles, list)
    assert len(profiles) == 2
    assert "Amazon" in profiles
    assert "Walmart" in profiles
    assert "readme.txt" not in profiles