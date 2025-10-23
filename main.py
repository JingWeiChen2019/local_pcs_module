# main.py
# 用於 BASELINE_RUN_COMMAND (基準運行/驗證指令) 的 UI 入口點 [cite: 17571]

import sys

try:
    # 依賴 PyQt6 [cite: 17541, 17556]
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
except ImportError:
    print("Error: PyQt6 is not found.")
    print("Please run 'pip install -r requirements.txt' first.")
    sys.exit(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LPIS Global Baseline (V2) [STRAT-R1]")
        self.setGeometry(100, 100, 400, 150)
        label = QLabel("BASELINE_RUN_COMMAND: Success ", self)
        label.adjustSize()
        # 將標籤置中
        label_width = label.frameGeometry().width()
        label_height = label.frameGeometry().height()
        self.move(
            (self.width() - label_width) // 2, 
            (self.height() - label_height) // 2
        )

def main():
    """
    啟動空白的 PyQt 主視窗以滿足 AC 
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()