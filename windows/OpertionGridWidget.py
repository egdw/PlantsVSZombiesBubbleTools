import typing

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QPushButton
from PyQt5.uic.properties import QtGui
from PyQt5.QtCore import pyqtSignal

from api import Api


class OperateGridWidget(QWidget):
    def __init__(self):
        super(OperateGridWidget, self).__init__()
        self.rocket_pressing_key = None
        self.grid_layout = None
        self.operate_layout = None
        self.plants_layout = None
        self.layout = None
        self.function_layout = None

        self.plant_pressing_key = None  # 记录当前按下的植物
        self.plants_label_dict = {}
        self.plants_label = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "Z", "P"]
        self.plants_press_label = ["A按下", "B按下", "C按下", "D按下", "E按下", "F按下", "G按下", "H按下", "I按下",
                                   "J按下", "Z按下", "P按下"]

        self.rocket_label = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.rocket_press_label = ["1按下", "2按下", "3按下", "4按下", "5按下", "6按下", "7按下", "8按下", "9按下"]
        self.rocket_label_dict = {}

        self.multi_send = False
        self.multi_send_list = []
        self.init_layout()

    def init_layout(self):
        # 定义一个横向的布局，显示0，,1，,2，,3，,4
        self.layout = QVBoxLayout()
        # 定义选择植物区域
        self.plants_layout = QHBoxLayout()

        for plant in self.plants_label:
            label = QLabel(plant)
            self.plants_label_dict[plant] = label
            self.plants_layout.addWidget(label)
        self.layout.addLayout(self.plants_layout)
        self.layout.addStretch(0)
        # 定义炮操作区
        self.rocket_layout = QHBoxLayout()
        for rocket in self.rocket_label:
            label = QLabel(rocket)
            self.rocket_label_dict[rocket] = label
            self.rocket_layout.addWidget(label)
        self.layout.addLayout(self.rocket_layout)
        self.layout.addStretch(0)
        # 定义可操作的区域
        self.operate_layout = QHBoxLayout()
        self.grid_layout = QGridLayout()
        for i in range(6):
            for j in range(9):
                label = QPushButton(self)
                label.setText(str(i) + str(j))
                label.pressed.connect(self.label_click)
                self.grid_layout.addWidget(label, i, j, 1, 1)
        self.grid_layout.setHorizontalSpacing(1)
        self.grid_layout.setVerticalSpacing(1)
        self.grid_layout.setContentsMargins(1, 1, 1, 1)
        self.operate_layout.addLayout(self.grid_layout)

        # 设置功能区
        self.function_layout = QVBoxLayout()
        anything_button = QPushButton("放置所有区域")
        anything_button.clicked.connect(self.put_any_location_clicked)

        top_button = QPushButton("放置上方前线")
        top_button.clicked.connect(self.put_top_location_clicked)

        bottem_button = QPushButton("放置下方前线")
        bottem_button.clicked.connect(self.put_bottem_location_clicked)

        water_button = QPushButton("放置水池")
        water_button.clicked.connect(self.put_water_location_clicked)

        self.function_layout.addWidget(anything_button)
        self.function_layout.addWidget(top_button)
        self.function_layout.addWidget(bottem_button)
        self.function_layout.addWidget(water_button)
        # self.function_layout.addWidget(QPushButton("123"))
        # self.function_layout.addWidget(QPushButton("123"))
        self.operate_layout.addLayout(self.function_layout)

        self.layout.addLayout(self.operate_layout)
        # layout.addStretch(1)
        self.setLayout(self.layout)

    def key_press(self, key):
        if key == 32:
            # 表示长按输入
            self.multi_send = True
        for index, k in enumerate(self.plants_label):
            if key == ord(k.lower()) or key == ord(k):
                self.plant_pressing_key = k  # 设置当前按下的按键
                label = self.plants_label_dict[k]
                label.setText(self.plants_press_label[index])

        # 检测炮按下
        for index, k in enumerate(self.rocket_label):
            if key == ord(k):
                self.rocket_pressing_key = k  # 设置当前按下的按键
                label = self.rocket_label_dict[k]
                label.setText(self.rocket_press_label[index])

    def key_release(self, key):
        if key == 32:
            # 表示长按输入
            self.multi_send = False
            # 批量执行数据
            Api.send_multi_bubble(self.multi_send_list)
            self.multi_send_list = []
        for k in self.plants_label:
            if key == ord(k.lower()) or key == ord(k):
                self.plants_label_dict[k].setText(k)
                self.plant_pressing_key = None  # 设置当前按下的按键

        for k in self.rocket_label:
            if key == ord(k):
                self.rocket_label_dict[k].setText(k)
                self.rocket_pressing_key = None  # 设置当前按下的按键

    def label_click(self):
        if self.plant_pressing_key is not None:
            for row in range(self.grid_layout.rowCount()):
                for column in range(self.grid_layout.columnCount()):
                    item = self.grid_layout.itemAtPosition(row, column)
                    if item and item.widget():  # 检查是否为控件
                        widget = item.widget()
                        if widget.isDown():
                            print(self.plant_pressing_key + widget.text())  # 获取用户的输入。
                            if not self.multi_send:
                                Api.send_bubble(self.plant_pressing_key + widget.text())
                            else:
                                self.multi_send_list.append(self.plant_pressing_key + widget.text())
        if self.rocket_pressing_key is not None:
            for row in range(self.grid_layout.rowCount()):
                for column in range(self.grid_layout.columnCount()):
                    item = self.grid_layout.itemAtPosition(row, column)
                    if item and item.widget():  # 检查是否为控件
                        widget = item.widget()
                        if widget.isDown():
                            Api.send_bubble("P" + widget.text() + str(int(self.rocket_pressing_key) - 1))

    def put_any_location_clicked(self):
        # 放置到所有区域
        if self.plant_pressing_key is not None:
            lists = []
            for i in range(6):
                for j in range(9):
                    lists.append(self.plant_pressing_key + str(i) + str(j))
            Api.send_multi_bubble(lists)

    def put_top_location_clicked(self):
        # 放置到所有区域
        if self.plant_pressing_key is not None:
            lists = ["05", "15", "06", "07", "08", "16", "17", "18"]
            sends = []
            for l in lists:
                sends.append(self.plant_pressing_key + l)
            Api.send_multi_bubble(sends)

    def put_bottem_location_clicked(self):
        if self.plant_pressing_key is not None:
            lists = ["55", "56", "57", "58", "45", "46", "47", "48"]
            sends = []
            for l in lists:
                sends.append(self.plant_pressing_key + l)
            Api.send_multi_bubble(sends)

    def put_water_location_clicked(self):
        if self.plant_pressing_key is not None:
            lists = ["24", "25", "26", "27", "28", "34", "35", "36","37","38"]
            sends = []
            for l in lists:
                sends.append(self.plant_pressing_key + l)
            Api.send_multi_bubble(sends)
