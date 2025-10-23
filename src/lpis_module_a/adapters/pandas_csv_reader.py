# src/lpis_module_a/adapters/pandas_csv_reader.py
# 依據 M1_CsvMapper.spec.md (Spec 5.1) 實現

import pandas as pd
from typing import List, Dict, Any
from src.lpis_module_a.interfaces.i_csv_reader import ICsvReader

class PandasCsvReader(ICsvReader):
    """
    (Spec 5.1) PandasCsvReader (CSV 讀取實現)
    
    實現 ICsvReader 介面，使用 Pandas 處理 CSV。
    """

    def get_headers(self, file_path: str) -> List[str]:
        """
        (Spec 5.1) 實現 get_headers
        僅讀取 CSV 的標頭行。
        """
        try:
            # nrows=0 確保只讀標頭，不讀內容
            headers = pd.read_csv(file_path, nrows=0).columns.tolist()
            return headers
        except FileNotFoundError:
            # (PE 註記: 良好的防禦性程式設計)
            raise
        except Exception as e:
            print(f"Error reading headers from {file_path}: {e}")
            return []

    def read_data(self, file_path: str) -> List[Dict[str, Any]]:
        """
        (Spec 5.1) 實現 read_data
        
        1. 讀取整個 CSV。
        2. (關鍵) dtype=str: 強制所有欄位讀取為字串 (str)。
           型別轉換 (e.g., str -> int) 是 Use Case (CsvMappingService)
           的職責，Adapter 不應處理。
        3. (關鍵) to_dict('records'): 將 DataFrame 轉換為 Python 原生
           List[Dict] 格式，以滿足 Spec 5.1 的要求 (與 pandas 解耦)。
        """
        try:
            df = pd.read_csv(file_path, dtype=str)
            
            # (Spec 5.1 關鍵要求)
            data: List[Dict[str, Any]] = df.to_dict('records')
            return data
            
        except FileNotFoundError:
            raise
        except Exception as e:
            print(f"Error reading data from {file_path}: {e}")
            return []