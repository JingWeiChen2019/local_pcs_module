# [SPEC] M1_CsvMapper.spec.md
# 模組一：採購 CSV 數據映射器 - 技術規格

## 1. 總覽 (Overview)

此規格定義了 [Module-A] CSV 數據映射器的架構與核心組件。
本架構遵循「Clean Architecture」原則，將核心業務邏E輯 (Use Cases) 與外部實現 (Adapters) 嚴格分離。

## 2. 核心領域模型 (Domain Entities)

這些是代表業務核心的物件，不依賴任何框架。

### 2.1. `VendorOrder` (核心數據實體)
- **路徑:** `src/lpis_module_a/domain/vendor_order.py`
- **職責:** 代表 [AC-2.3] 中定義的「系統核心欄位」，作為模組間傳遞的標準數據結構。
- **屬性 (Dataclass):**
  - `order_id: str` (對應 "Order #")
  - `item_name: str` (對應 "Item Name")
  - `tracking_number_t1: str` (對應 "Tracking Number (T1)")
  - `quantity: int` (對應 "Quantity")
  - `total_amount: float` (對應 "Total Amount")
  - `order_placed_date: str` (對應 "Order Placed Date", 暫定為 str，待 C-Module 整合)

### 2.2. `MappingProfile` (映射設定檔)
- **路徑:** `src/lpis_module_a/domain/mapping_profile.py`
- **職責:** 儲存外部 CSV 欄位名稱與內部 `VendorOrder` 核心欄位的對應關係。
- **屬性 (Dataclass):**
  - `name: str` (Profile 名稱, e.g., "Amazon Profile")
  - `mapping: Dict[str, str]` (e.g., `{"order_id": "CSV Column Name"}`)

## 3. 核心用例 (Use Cases)

這是系統的核心業務邏輯，負責協調 Entities 和 Interfaces。

### 3.1. `CsvMappingService` (CSV 映射服務)
- **路徑:** `src/lpis_module_a/use_cases/csv_mapping_service.py`
- **職責:** 實現 [PLAN-LPIS-M1] 中的所有核心映射與儲存 AC。
- **依賴 (注入):**
  - `csv_reader: ICsvReader`
  - `profile_repo: IProfileRepository`
  - `order_repo: IOrderRepository`
- **核心方法:**
  - `get_csv_headers(file_path: str) -> List[str]`:
    - (AC-2.2 UI 輔助) 呼叫 `csv_reader` 獲取 CSV 標頭，供 UI 顯示。
  - `save_profile(name: str, mapping: Dict[str, str]) -> MappingProfile`:
    - (AC-3.1) 建立 `MappingProfile` 實體並呼叫 `profile_repo.save()`。
  - `load_profile(name: str) -> MappingProfile`:
    - (AC-2.1) 呼叫 `profile_repo.load()` 獲取現有 Profile。
  - `list_profiles() -> List[str]`:
    - (AC-2.1 UI 輔助) 呼叫 `profile_repo.list_profiles()` 供 UI 顯示。
  - `apply_mapping_and_save(file_path: str, profile: MappingProfile)`:
    - (AC-4.1, AC-5.1) 核心流程：
      1. 呼叫 `csv_reader.read_data(file_path)` 獲取原始數據 (List[dict])。
      2. 遍歷原始數據，根據 `profile` 中的 `mapping` 規則，將其轉換為 `List[VendorOrder]`。
      3. (驗證) 確保所有 [AC-2.3] 的核心欄位均被成功映射。若缺少 (e.g., `tracking_number_t1` 欄位找不到)，必須拋出 `MappingValidationError`。
      4. 呼叫 `order_repo.save_batch(List[VendorOrder])` 完成數據儲存 (AC-5.1)。

## 4. 介面 (Interfaces / Ports)

定義核心邏輯與外部世界的邊界 (Dependency Inversion)。

### 4.1. `ICsvReader`
- **路徑:** `src/lpis_module_a/interfaces/i_csv_reader.py`
- **方法:**
  - `get_headers(file_path: str) -> List[str]`
  - `read_data(file_path: str) -> List[Dict[str, Any]]`

### 4.2. `IProfileRepository`
- **路徑:** `src/lpis_module_a/interfaces/i_profile_repo.py`
- **方法:**
  - `save(profile: MappingProfile)`
  - `load(name: str) -> MappingProfile`
  - `list_profiles() -> List[str]`

### 4.3. `IOrderRepository`
- **路徑:** `src/lpis_module_a/interfaces/i_order_repo.py`
- **方法:**
  - `save_batch(orders: List[VendorOrder])`
  - `_init_table()`: (內部) 確保 `vendor_orders` 表存在。

## 5. 適配器 (Adapters / Implementations)

外部技術的具體實現 (e.g., Pandas, SQLite, PyQt)。

### 5.1. `PandasCsvReader` (CSV 讀取實現)
- **路徑:** `src/lpis_module_a/adapters/pandas_csv_reader.py`
- **實現:** `ICsvReader`
- **技術:** 使用 `pandas.read_csv()`。
- **注意:** `read_data` 必須將 Pandas DataFrame 轉換為 Python 原生的 `List[Dict]` 格式回傳，以保持核心邏輯 (Use Case) 對 `pandas` 的獨立性。

### 5.2. `JsonProfileRepository` (Profile 儲存實現)
- **路徑:** `src/lpis_module_a/adapters/json_profile_repo.py`
- **實現:** `IProfileRepository`
- **技術:** 將 `MappingProfile` 序列化為 JSON 檔案，儲存於 (e.g., `data/profiles/*.json`)。

### 5.3. `SqliteOrderRepository` (訂單儲存實現)
- **路徑:** `src/lpis_module_a/adapters/sqlite_order_repo.py`
- **實現:** `IOrderRepository`
- **技術:** 使用 `sqlite3` (Python 內建)。
- **職責 (AC-5.1):**
  - `_init_table()`: 建立 `vendor_orders` 表，包含 [AC-2.3] 定義的 6 個欄位。
  - `save_batch()`: 使用 `executemany()` 將 `List[VendorOrder]` 寫入 SQLite。

### 5.4. `PyQtMapperView` (UI 實現)
- **路徑:** `src/lpis_module_a/ui/mapper_widget.py`
- **職責 (AC-1.1, AC-2.2):**
  - 提供 "Import" 按鈕。
  - 提供「選擇 Profile」或「建立 Profile」的對話框 (AC-2.1)。
  - 顯示「欄位映射器」UI：
    - 左側：[AC-2.3] 的 6 個核心欄位 (QLabel)。
    - 右側：`CsvMappingService.get_csv_headers()` 回傳的 CSV 欄位 (QComboBox)。
  - "Save Profile" 按鈕，呼叫 `CsvMappingService.save_profile()` (AC-3.1)。