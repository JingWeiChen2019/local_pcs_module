# LPIS 專案 (Project LPIS)

## 全域基準線 (Global Baseline) [STRAT-R1]

### 核心驗證指令集 (Core Validation Command Set)

[cite_start]此指令集是用於驗收 PE [SETUP-GLOBAL] 任務的「黃金標準」 。

**1. BASELINE_BUILD_COMMAND (基準建置/檢查指令)**

* [cite_start]**用途:** 驗證 (1) 所有依賴均已安裝 (2) TSDD 測試環境已啟動 (3) 所有核心模組均可被 `pytest` 成功導入 [cite: 17567]。
* **指令:**
    ```bash
    pip install -r requirements.txt && pytest
    ```
* **預期結果:** `pytest` 成功執行，並通過 `test_baseline_imports.py` 測試，回報 `1 passed` 。

**2. BASELINE_RUN_COMMAND (基準運行/驗證指令)**

* [cite_start]**用途:** 驗證應用程式 UI 入口點 (`main.py`) 仍可被成功喚醒 [cite: 17571]。
* **指令:**
    ```bash
    python main.py
    ```
* [cite_start]**預期結果:** 成功啟動一個空白的 PyQt 主視窗 。