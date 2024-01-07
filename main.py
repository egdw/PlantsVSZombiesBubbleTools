import sys
from PyQt5.QtWidgets import QApplication

from windows import WebWidows

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebWidows.WebWindows()
    sys.exit(app.exec())
