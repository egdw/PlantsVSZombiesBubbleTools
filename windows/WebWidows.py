import typing

from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
from PyQt5.uic.properties import QtGui

from windows.OpertionGridWidget import OperateGridWidget


class WebWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        self.grid_layout = None
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("植物大战僵尸互动弹幕辅助工具")
        self.grid_layout = OperateGridWidget()
        self.setCentralWidget(self.grid_layout)
        self.show()

    def keyPressEvent(self, event) -> None:
        # 按q退出
        if event.key() == 81:
            self.close()
        else:
            self.grid_layout.key_press(event.key())

    def keyReleaseEvent(self, event) -> None:
        self.grid_layout.key_release(event.key())
