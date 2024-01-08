from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QPushButton, QCheckBox

from api import Api


def dance_zombie_click():
    Api.send_bubble("太酷啦")


def small_zombie_click():
    Api.send_bubble("666")


def normal_zombie_click():
    Api.send_bubble("冲冲冲")


def box_zombie_click():
    Api.send_bubble("疯狂点赞")


class OperateGridWidget(QWidget):
    def __init__(self):
        super(OperateGridWidget, self).__init__()
        self.rocket_layout = None
        self.replace_checkbox = None
        self.rocket_pressing_key = None
        self.grid_layout = None
        self.operate_layout = None
        self.plants_layout = None
        self.layout = None
        self.function_layout = None

        self.plant_pressing_key = None  # 记录当前按下的植物
        self.plants_label_dict = {}
        self.plants_label = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "Z", "P", "L", "T"]
        self.plants_press_label = ["A按下", "B按下", "C按下", "D按下", "E按下", "F按下", "G按下", "H按下", "I按下",
                                   "J按下", "Z按下", "P按下", "L按下", "T按下"]

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

        # 替换模式
        self.replace_checkbox = QCheckBox("植物替换模式")
        self.plants_layout.addWidget(self.replace_checkbox)
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

        zombies_button1 = QPushButton("伴舞僵尸")
        zombies_button1.clicked.connect(dance_zombie_click)  # 太酷啦

        zombies_button2 = QPushButton("出小鬼")
        zombies_button2.clicked.connect(small_zombie_click)  # 666

        zombies_button3 = QPushButton("普通僵尸")
        zombies_button3.clicked.connect(normal_zombie_click)  # 冲冲冲

        zombies_button4 = QPushButton("僵尸小盲盒")
        zombies_button4.clicked.connect(box_zombie_click)  # 疯狂点赞

        self.function_layout.addWidget(anything_button)
        self.function_layout.addWidget(top_button)
        self.function_layout.addWidget(bottem_button)
        self.function_layout.addWidget(water_button)
        self.function_layout.addWidget(zombies_button1)
        self.function_layout.addWidget(zombies_button2)
        self.function_layout.addWidget(zombies_button3)
        self.function_layout.addWidget(zombies_button4)

        self.operate_layout.addLayout(self.function_layout)

        self.layout.addLayout(self.operate_layout)
        # layout.addStretch(1)
        self.plants_label = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "Z", "P", "L", "T"]

        self.layout.addWidget(QLabel("A\tB\tC\tD\tE\tF\tG\tH\tI\tJ\tZ\tP\tL\tT"))
        self.layout.addWidget(
            QLabel(
                "A植物\tB植物\tC植物\tD植物\tE植物\tF植物\tG植物\tH植物\tI植物\tJ植物\tZ铲子\tP加农炮\tL搭梯子\tT切换替换模式"))

        self.layout.addWidget(QLabel("1\t2\t3\t4\t5\t6\t7\t8\t9"))
        self.layout.addWidget(
            QLabel("炮1\t炮2\t炮3\t炮4\t炮5\t炮6\t炮7\t炮8\t炮9"))
        self.setLayout(self.layout)

    def key_press(self, key):
        if key == 32:
            # 表示长按输入
            self.multi_send = True

        if key == ord('T') or key == ord('t'):
            self.replace_checkbox.setChecked(not self.replace_checkbox.isChecked())

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
                            # print(self.plant_pressing_key + widget.text())  # 获取用户的输入。
                            if not self.multi_send:
                                if self.replace_checkbox.isChecked():
                                    Api.send_bubble("T" + self.plant_pressing_key + widget.text())
                                else:
                                    Api.send_bubble(self.plant_pressing_key + widget.text())
                            else:
                                if self.replace_checkbox.isChecked():
                                    # 判断是否为替换模式，如果是替换模式则在原始指令之前加上T
                                    self.multi_send_list.append("T" + self.plant_pressing_key + widget.text())
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
            for i in range(9):
                for j in range(6):
                    if self.replace_checkbox.isChecked():
                        # 判断是否为替换模式，如果是替换模式则在原始指令之前加上T
                        lists.append("T" + self.plant_pressing_key + str(i) + str(j))
                    else:
                        lists.append(self.plant_pressing_key + str(i) + str(j))
            Api.send_multi_bubble(lists)

    def put_top_location_clicked(self):
        # 放置到所有区域
        if self.plant_pressing_key is not None:
            lists = ["05", "15", "06", "16", "07", "17", "08", "18"]
            sends = []
            for l in lists:
                if self.replace_checkbox.isChecked():
                    # 判断是否为替换模式，如果是替换模式则在原始指令之前加上T
                    sends.append("T" + self.plant_pressing_key + l)
                else:
                    sends.append(self.plant_pressing_key + l)
            Api.send_multi_bubble(sends)

    def put_bottem_location_clicked(self):
        if self.plant_pressing_key is not None:
            lists = ["45", "55", "46", "56", "47", "57", "48", "58"]
            sends = []
            for l in lists:
                if self.replace_checkbox.isChecked():
                    # 判断是否为替换模式，如果是替换模式则在原始指令之前加上T
                    sends.append("T" + self.plant_pressing_key + l)
                else:
                    sends.append(self.plant_pressing_key + l)
            Api.send_multi_bubble(sends)

    def put_water_location_clicked(self):
        if self.plant_pressing_key is not None:
            lists = ["20", "21", "22", "23", "24", "30", "31", "32", "33", "25", "26", "27", "28", "34", "35", "36",
                     "37",
                     "38"]
            sends = []
            for l in lists:
                if self.replace_checkbox.isChecked():
                    # 判断是否为替换模式，如果是替换模式则在原始指令之前加上T
                    sends.append("T" + self.plant_pressing_key + l)
                else:
                    sends.append(self.plant_pressing_key + l)
            Api.send_multi_bubble(sends)
