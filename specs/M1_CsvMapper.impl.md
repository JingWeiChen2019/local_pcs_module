# [IMPL] M1_CsvMapper.impl.md
# 模組一：採購 CSV 數據映射器 - 實現規格書

本文檔由 PE (CAA) 於 TSDD 循環完成後自動生成，用於確認 [SPEC] M1_CsvMapper.spec.md 已被完整實現。

## 1. 總覽 (Overview)
- **狀態:** ✅ 已實現
- **架構:** 遵循 [Clean Architecture] 原則，`src/lpis_module_a/` 目錄結構已實現 Domain, Use Cases, Interfaces, Adapters, 和 UI 的分離。

## 2. 核心領域模型 (Domain Entities)
- **狀態:** ✅ 已實現
- **實現檔案:**
  - `src/lpis_module_a/domain/vendor_order.py`:
    - ✅ (Spec 2.1) `VendorOrder` Dataclass 已實現。
  - `src/lpis_module_a/domain/mapping_profile.py`:
    - ✅ (Spec 2.2) `MappingProfile` Dataclass 已實現。
  - `src/lpis_module_a/domain/exceptions.py`:
    - ✅ (New) `MappingValidationError` (Spec 1.2 TDD 產物) 已實現。

## 3. 核心用例 (Use Cases)
- **狀態:** ✅ 已實現 (TDD 覆蓋範圍內)
- **實現檔案:**
  - `src/lpis_module_a/use_cases/csv_mapping_service.py`:
    - ✅ (DI) `__init__` 已實現依賴注入。
    - ✅ (Spec 1.1, 1.2) `apply_mapping_and_save()`: TDD 驗證通過 (含錯誤處理)。
    - ✅ (Spec 2.1) `save_profile()`: TDD 驗證通過。
    - ✅ (Spec 3.1) `get_csv_headers()`: TDD 驗證通過 (委派給 ICsvReader)。
    - ⚠️ `load_profile()`: (Not Implemented - TDD Skipped)
    - ⚠️ `list_profiles()`: (Not Implemented - TDD Skipped)

## 4. 介面 (Interfaces / Ports)
- **狀態:** ✅ 已實現
- **實現檔案:**
  - `src/lpis_module_a/interfaces/i_csv_reader.py`: ✅ `ICsvReader` (ABC)
  - `src/lpis_module_a/interfaces/i_profile_repo.py`: ✅ `IProfileRepository` (ABC)
  - `src/lpis_module_a/interfaces/i_order_repo.py`: ✅ `IOrderRepository` (ABC)

## 5. 適配器 (Adapters / Implementations)
- **狀態:** ✅ 已實現
- **實現檔案:**
  - `src/lpis_module_a/adapters/pandas_csv_reader.py`:
    - ✅ (Spec 5.1) `PandasCsvReader` TDD 驗證通過 (使用 `pandas`)。
  - `src/lpis_module_a/adapters/json_profile_repo.py`:
    - ✅ (Spec 5.2) `JsonProfileRepository` TDD 驗證通過 (使用 `json`, `os`)。
  - `src/lpis_module_a/adapters/sqlite_order_repo.py`:
    - ✅ (Spec 5.3) `SqliteOrderRepository` TDD 驗證通過 (使用 `sqlite3`)。

## 6. UI (Adapters / Implementations)
- **狀態:** ✅ 已實現
- **實現檔案:**
  - `src/lpis_module_a/ui/mapper_widget.py`:
    - ✅ (Spec 5.4 / Scenario 3.1) `PyQtMapperView` TDD 驗證通過 (使用 `PyQt6` 注入 Service 並填充 `QComboBox`)。