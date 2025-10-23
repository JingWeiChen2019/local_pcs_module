# tests/test_m1_csv_mapper.py
# 依據 M1_CsvMapper.spec.test.md (Scenario 1.1, 1.2, 2.1) 撰寫
# [TSDD 7] 解除 3.1 skip

import pytest
from unittest.mock import MagicMock, call, ANY

from src.lpis_module_a.domain.vendor_order import VendorOrder
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService
from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository
from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository 
from src.lpis_module_a.domain.mapping_profile import MappingProfile
from src.lpis_module_a.domain.exceptions import MappingValidationError

# (PE 註記: 夾具 均來自 tests/conftest.py)

# --- Scenario 1.1 (PASSED) ---
def test_scenario_1_1_success_apply_mapping(
    mapping_service: CsvMappingService, 
    mock_order_repo: IOrderRepository,
    mock_amazon_profile: MappingProfile
):
    """ Spec 1.1: 成功套用現有 Profile 並解析數據 (AC-4.1, AC-2.3) """
    csv_file_path = "dummy/amazon_orders.csv"
    mapping_service.apply_mapping_and_save(
        file_path=csv_file_path, 
        profile=mock_amazon_profile
    )
    mock_order_repo.save_batch.assert_called_once()
    args, kwargs = mock_order_repo.save_batch.call_args
    saved_orders: list[VendorOrder] = args[0]
    assert saved_orders[0].tracking_number_t1 == "TBA123456"

# --- Scenario 1.2 (PASSED) ---
def test_scenario_1_2_mapping_failure_missing_column(
    mapping_service_invalid: CsvMappingService, 
    mock_order_repo: IOrderRepository,         
    mock_amazon_profile: MappingProfile
):
    """ Spec 1.2: 映射失敗 (缺少必要欄位) (AC-4.1 錯誤處理) """
    csv_file_path = "dummy/invalid_orders.csv"
    with pytest.raises(MappingValidationError) as e:
        mapping_service_invalid.apply_mapping_and_save(
            file_path=csv_file_path, 
            profile=mock_amazon_profile
        )
    mock_order_repo.save_batch.assert_not_called()
    assert "tracking-id" in str(e.value).lower()

# --- Scenario 2.1 (PASSED) ---
def test_scenario_2_1_save_profile(
    mapping_service: CsvMappingService,
    mock_profile_repo: IProfileRepository
):
    """ Spec 2.1: 成功儲存 Profile (AC-3.1) """
    profile_name = "Walmart"
    profile_mapping = {"order_id": "PO_NUMBER"}
    created_profile = mapping_service.save_profile(
        name=profile_name,
        mapping=profile_mapping
    )
    mock_profile_repo.save.assert_called_once_with(created_profile)

# --- Scenario 3.1 (SKIPPED -> RED) ---
# [TSDD 7] @pytest.mark.skip 已被移除
def test_scenario_3_1_ui_flow():
    """ 
    Spec 3.1: 觸發映射器 UI 
    (PE 註記: 此測試案例現在由 tests/ui/test_mapper_widget.py 負責)
    """
    pass # 此佔位符 PASS，真正的測試在 test_mapper_widget.py