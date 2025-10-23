# tests/conftest.py
# 用於 M1 模組的 Pytest 共享夾具

import pytest
import os
from unittest.mock import MagicMock, mock_open

from src.lpis_module_a.domain.mapping_profile import MappingProfile
from src.lpis_module_a.interfaces.i_csv_reader import ICsvReader
from src.lpis_module_a.interfaces.i_profile_repo import IProfileRepository
from src.lpis_module_a.interfaces.i_order_repo import IOrderRepository
from src.lpis_module_a.use_cases.csv_mapping_service import CsvMappingService

# --- 模擬數據定義 ---

MOCK_AMAZON_CSV_CONTENT = """order-id,item,tracking-id,qty,price,order-date
123-ABC,Test Item 1,TBA123456,1,19.99,2025-10-01
456-DEF,Test Item 2,TBA654321,2,9.99,2025-10-02
"""

@pytest.fixture
def mock_amazon_profile() -> MappingProfile:
    """ (Scenario 1.1 Given) 提供一個 'Amazon' 映射 Profile """
    return MappingProfile(
        name="Amazon",
        mapping={
            # 核心欄位 (Key) -> CSV 欄位 (Value)
            "order_id": "order-id",
            "item_name": "item",
            "tracking_number_t1": "tracking-id",
            "quantity": "qty",
            "total_amount": "price",
            "order_placed_date": "order-date",
        }
    )

@pytest.fixture
def mock_csv_data() -> list[dict[str, str]]:
    """ (Scenario 1.1 Given) 提供 'amazon_orders.csv' 的模擬內容 """
    return [
        {"order-id": "123-ABC", "item": "Test Item 1", "tracking-id": "TBA123456", "qty": "1", "price": "19.99", "order-date": "2025-10-01"},
        {"order-id": "456-DEF", "item": "Test Item 2", "tracking-id": "TBA654321", "qty": "2", "price": "9.99", "order-date": "2025-10-02"},
    ]

# --- 模擬 Clean Architecture 依賴 ---

@pytest.fixture
def mock_csv_reader(mock_csv_data) -> ICsvReader:
    """ Mock ICsvReader (Adapters) """
    reader = MagicMock(spec=ICsvReader)
    reader.read_data.return_value = mock_csv_data
    reader.get_headers.return_value = ["order-id", "item", "tracking-id", "qty", "price", "order-date"]
    return reader

@pytest.fixture
def mock_profile_repo(mock_amazon_profile) -> IProfileRepository:
    """ Mock IProfileRepository (Adapters) """
    repo = MagicMock(spec=IProfileRepository)
    repo.load.return_value = mock_amazon_profile
    return repo

@pytest.fixture
def mock_order_repo() -> IOrderRepository:
    """ Mock IOrderRepository (Adapters) """
    repo = MagicMock(spec=IOrderRepository)
    return repo


@pytest.fixture
def mapping_service(mock_csv_reader, mock_profile_repo, mock_order_repo) -> CsvMappingService:
    """ 
    初始化 CsvMappingService (Use Case) 
    並注入所有 Mock 的 Adapters。
    """
    return CsvMappingService(
        csv_reader=mock_csv_reader,
        profile_repo=mock_profile_repo,
        order_repo=mock_order_repo
    )

# (PE 註記: 貼在 conftest.py 檔案末尾)

@pytest.fixture
def mock_invalid_csv_data() -> list[dict[str, str]]:
    """ (Scenario 1.2 Given) 提供 'invalid_orders.csv' 的模擬內容 (缺少 'tracking-id') """
    return [
        {"order-id": "789-GHI", "item": "Test Item 3", "qty": "1", "price": "19.99", "order-date": "2025-10-03"},
    ]

@pytest.fixture
def mock_csv_reader_invalid(mock_invalid_csv_data) -> ICsvReader:
    """ Mock ICsvReader for Scenario 1.2 """
    reader = MagicMock(spec=ICsvReader)
    reader.read_data.return_value = mock_invalid_csv_data
    # 標頭中故意缺少 "tracking-id"
    reader.get_headers.return_value = ["order-id", "item", "qty", "price", "order-date"]
    return reader

@pytest.fixture
def mapping_service_invalid(mock_csv_reader_invalid, mock_profile_repo, mock_order_repo) -> CsvMappingService:
    """
    初始化 CsvMappingService (Use Case) 
    並注入 *無效的* CSV Reader (用於 Scenario 1.2)。
    """
    return CsvMappingService(
        csv_reader=mock_csv_reader_invalid,
        profile_repo=mock_profile_repo,
        order_repo=mock_order_repo
    )