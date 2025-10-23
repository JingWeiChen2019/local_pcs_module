# tests/adapters/test_pandas_csv_reader.py
# 依據 M1_CsvMapper.spec.md (Spec 5.1) 撰寫

import pytest
import os
import pandas # 導入依賴
from src.lpis_module_a.adapters.pandas_csv_reader import PandasCsvReader
from src.lpis_module_a.interfaces.i_csv_reader import ICsvReader

# 測試用的 CSV 內容 (與 conftest.py 相同，但用於真實檔案)
MOCK_CSV_CONTENT = """order-id,item,tracking-id,qty,price,order-date
123-ABC,Test Item 1,TBA123456,1,19.99,2025-10-01
456-DEF,Test Item 2,TBA654321,2,9.99,2025-10-02
"""

@pytest.fixture
def temp_csv_file(tmp_path):
    """
    (Given) 建立一個真實的 (暫時性) CSV 檔案
    'tmp_path' 是 pytest 提供的內建 fixture，用於建立暫存目錄
    """
    csv_file = tmp_path / "test_orders.csv"
    csv_file.write_text(MOCK_CSV_CONTENT)
    return str(csv_file) # 回傳檔案路徑

@pytest.fixture
def reader() -> PandasCsvReader:
    """ 初始化我們的 Adapter 實體 """
    return PandasCsvReader()

#
# ----------------------------------
# 測試 Spec 5.1 (Adapter) - [TSDD 4 - RED]
# ----------------------------------
#
def test_adapter_implements_interface(reader: PandasCsvReader):
    """ 驗證 Adapter 確實遵循 Interface (Clean Architecture) """
    assert isinstance(reader, ICsvReader)

def test_get_headers(reader: PandasCsvReader, temp_csv_file: str):
    """ (Spec 5.1) 測試 get_headers 方法 """
    
    # When
    # PE 註記: PandasCsvReader.get_headers 目前是 'pass'
    # 預期: 此測試將 100% 失敗 (Red Light)。
    headers = reader.get_headers(temp_csv_file)

    # Then
    expected = ["order-id", "item", "tracking-id", "qty", "price", "order-date"]
    assert headers == expected

def test_read_data(reader: PandasCsvReader, temp_csv_file: str):
    """ (Spec 5.1 關鍵) 測試 read_data 方法 """
    
    # When
    # PE 註記: PandasCsvReader.read_data 目前是 'pass'
    # 預期: 此測試將 100% 失敗 (Red Light)。
    data = reader.read_data(temp_csv_file)

    # Then (Spec 5.1 要求) - 必須回傳 List[Dict]，而非 DataFrame
    assert isinstance(data, list)
    assert len(data) == 2
    assert isinstance(data[0], dict)
    
    # 驗證內容 (Pandas 讀取 CSV 時預設會全轉為 str)
    assert data[0]["order-id"] == "123-ABC"
    assert data[0]["qty"] == "1" # 注意：此階段應為 '1' (str)
    assert data[1]["tracking-id"] == "TBA654321"