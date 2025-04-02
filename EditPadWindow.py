from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox
from PyQt5 import QtCore

class EditPadWindow:

    window : QWidget = QWidget()

    obj_icons = None
    obj_main_window = None
    obj_controller = None

    target_action = None
    target_pad = None

    combo_config = None
    field_name = None
    btn_action = None

    list_configs = []


    def setup(self, obj_icons, obj_configger, obj_main_window, obj_controller):
        self.obj_icons = obj_icons
        self.obj_configger = obj_configger
        self.obj_main_window = obj_main_window
        self.obj_controller = obj_controller
        self.create_window()
        self.window.hide()        

    def open_add(self):
        self.target_action = "add"
        self.window.setWindowTitle("Add Gamepad")
        self.field_name.setText("New Gamepad")
        self.btn_action.setText("Add")
        self.show()
    
    def open_edit(self, id_pad):
        self.target_pad = None
        if id_pad in self.obj_controller.gamepad_dict:
            self.target_pad = self.obj_controller.gamepad_dict[id_pad]
            self.target_action = "edit"
            self.window.setWindowTitle("Edit Gamepad")
            self.field_name.setText(self.target_pad.name)
            self.btn_action.setText("Apply")
            self.show()
            self.combo_config.setCurrentText(self.obj_configger.cfg[self.target_pad.id_config]["name"])



    def do_action(self):
        match self.target_action:
            case "add":
                if self.combo_config.currentIndex() != 0:
                    id_pad = self.obj_controller.add_gamepad(self.list_configs[self.combo_config.currentIndex() - 1], self.field_name.text())
                    if id_pad:
                        self.obj_main_window.add_active(self.field_name.text(), id_pad)
                    self.window.close()
            case "edit":
                self.target_pad.name = self.field_name.text()
                self.obj_main_window.dict_actives[self.target_pad.id_pad].setText(self.target_pad.name)
                self.obj_controller.change_pad_config(self.target_pad, self.list_configs[self.combo_config.currentIndex() - 1])
                self.window.close()


    def show(self):
        self.list_configs = []
        self.combo_config.clear()

        self.combo_config.addItem("--Select config--")
        self.combo_config.setCurrentIndex(0)
        
        for id_config in self.obj_configger.cfg.sections():
            self.list_configs.append(id_config)
            self.combo_config.addItem(self.obj_configger.cfg[id_config]["name"])
        
        self.window.move(self.obj_main_window.window.pos() + QtCore.QPoint(100,100))
        self.window.show()


    def create_window(self):
        vbox_layout = QVBoxLayout()
        vbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.window.setLayout(vbox_layout)
        self.window.setFixedSize(300, 145)
        self.window.setStyleSheet("background-color: #231f36; color: white;")
        
        text_name = QLabel("Name", self.window)
        text_name.move(50, 10)

        field_name = QLineEdit(self.window)
        field_name.setGeometry(100, 10, 160, 30)
        field_name.setStyleSheet("background-color: black;")
        self.field_name = field_name

        text_config = QLabel("Config", self.window)
        text_config.move(45, 50)

        self.combo_config = QComboBox(self.window)
        self.combo_config.setGeometry(100, 50, 160, 30)
        

        self.btn_action = QPushButton("Add Gamepad", self.window)
        self.btn_action.setGeometry(105, 100, 100, 30)
        self.btn_action.clicked.connect(self.do_action)