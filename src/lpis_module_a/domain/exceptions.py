class MappingValidationError(Exception):
    """
    [SPEC] 3.1: 映射驗證錯誤
    當核心欄位 (如 tracking_number_t1) 在 CSV 中找不到時拋出
    """
    pass
