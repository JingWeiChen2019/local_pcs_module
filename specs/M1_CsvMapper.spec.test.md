# [SPEC-TEST] M1_CsvMapper.spec.test.md
# 模組一：採購 CSV 數據映射器 - 測試規格

本文件依據 [PLAN-LPIS-M1] 的驗收標準 (AC) 編寫。

## 1. 核心映射邏輯 (Use Case 測試)

### Scenario 1.1: 成功套用現有 Profile 並解析數據 (AC-4.1, AC-2.3)
- **Given:** 一個 "amazon_orders.csv" 檔案，其欄位包含 "order-id" 和 "tracking-id"。
- **And:** 一個已儲存的 `MappingProfile` ("Amazon")，其映射規則為：
  - `order_id` (核心) -> "order-id" (CSV)
  - `tracking_number_t1` (核心) -> "tracking-id" (CSV)
  - (以及其他 4 個核心欄位的映射)
- **When:** `CsvMappingService` 使用 "Amazon" Profile 處理 "amazon_orders.csv"。
- **Then:** 服務應回傳 `List[VendorOrder]`。
- **And:** 列表中的第一筆 `VendorOrder` 實體，其 `order_id` 屬性必須等於 CSV 中的 "order-id" 值。
- **And:** 其 `tracking_number_t1` 屬性必須等於 CSV 中的 "tracking-id" 值。

### Scenario 1.2: 映射失敗 (缺少必要欄位) (AC-4.1 錯誤處理)
- **Given:** 一個 "invalid_orders.csv" 檔案，其欄位**不包含** "tracking-id"。
- **And:** 一個 "Amazon" Profile，它要求 `tracking_number_t1` 必須映射到 "tracking-id"。
- **When:** `CsvMappingService` 嘗試套用此 Profile 處理 "invalid_orders.csv"。
- **Then:** 系統必須拋出 `MappingValidationError` (或 `KeyError`)。
- **And:** (參見 Scenario 2.2) `IOrderRepository` 的 `save_batch` 方法**絕對不能**被呼叫。

## 2. 儲存庫 (Adapters 測試)

### Scenario 2.1: 成功儲存 Profile (AC-3.1)
- **Given:** `JsonProfileRepository` (或 `IProfileRepository` 的 Mock)。
- **And:** `CsvMappingService` 服務。
- **When:** 呼叫 `CsvMappingService.save_profile()`，名稱為 "Walmart"，映射為 `{"order_id": "PO_NUMBER"}`。
- **Then:** `IProfileRepository.save()` 必須被呼叫。
- **And:** (若測試 `JsonProfileRepository` 實體) 一個 "Walmart.json" 檔案必須被建立，且內容包含 "PO_NUMBER"。

### Scenario 2.2: 成功儲存訂單數據 (AC-5.1, AC-5.2)
- **Given:** `SqliteOrderRepository` (或 `IOrderRepository` 的 Mock)。
- **And:** 一個 `List[VendorOrder]`，其中包含 `tracking_number_t1="TBA123"` 的訂單。
- **When:** `CsvMappingService` 呼叫 `IOrderRepository.save_batch()`。
- **Then:** `save_batch` 方法必須被呼叫。
- **And:** (若測試 `SqliteOrderRepository` 實體) SQLite `vendor_orders` 表中必須包含一筆 `tracking_number_t1` 欄位為 "TBA123" 的紀錄。

## 3. UI 驅動的流程 (E2E / PyQt 測試)

### Scenario 3.1: 觸發映射器 UI (AC-1.1, AC-2.1, AC-2.2)
- **Given:** 主應用程式已啟動 (Mock `CsvMappingService`)。
- **And:** `CsvMappingService.get_csv_headers()` 被 Mock 為回傳 `["col_A", "col_B"]`。
- **When:** 使用者點擊 "Import Purchase CSV" 按鈕。
- **And:** 在跳出的對話框中選擇 "建立新 Profile"。
- **Then:** `PyQtMapperView` (欄位映射器) 必須顯示。
- **And:** 介面上必須包含 6 個 QComboBox (下拉選單)。
- **And:** 每個 QComboBox 必須包含 "col_A" 和 "col_B" 選項。