from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5 import QtCore

class ConfirmWindow:

    window : QWidget = QWidget()

    obj_icons = None
    obj_configger = None
    obj_main_window = None
    obj_controller = None

    action_icon : QLabel

    text_main = None
    text_info = None
    target_id = None
    target_op = None

    def setup(self, obj_icons, obj_configger, obj_main_window, obj_controller):
        self.obj_icons = obj_icons
        self.obj_configger = obj_configger
        self.obj_main_window = obj_main_window
        self.obj_controller = obj_controller
        self.create_window()
        self.window.hide()
    

    def create_window(self):
        vbox_layout = QVBoxLayout()
        vbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.window.setLayout(vbox_layout)
        self.window.setFixedSize(300, 200)
        self.window.setStyleSheet("background-color: #231f36; color: white;")
        
        action_icon = QLabel()
        action_icon.setFixedSize(31, 31)
        vbox_layout.addWidget(action_icon, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.action_icon = action_icon

        self.text_main = QLabel("")
        vbox_layout.addWidget(self.text_main, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.text_info = QLabel()
        vbox_layout.addWidget(self.text_info, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        vbox_layout.addSpacing(30)

        group_btn = QFrame()
        hbox_layout = QHBoxLayout()
        group_btn.setLayout(hbox_layout)
        btn_proceed = QPushButton("Proceed")
        btn_cancel = QPushButton("Cancel")
        hbox_layout.addWidget(btn_cancel)
        hbox_layout.addSpacing(50)
        hbox_layout.addWidget(btn_proceed)
        vbox_layout.addWidget(group_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        btn_cancel.clicked.connect(self.action_cancel)
        btn_proceed.clicked.connect(self.action_proceed)
                
    

    def open_wipe_for_all_to_see(self, config_id):
        if self.obj_configger.cfg.has_section(config_id):
            self.action_icon.setPixmap(self.obj_icons.wipe_icon)
            self.target_id = config_id
            self.window.setWindowTitle("Wipe Config")
            self.text_main.setText("Confirm wipe all set buttons?")
            self.text_info.setText(f'Target configuration: {self.obj_configger.cfg[config_id]["name"]}')
            self.target_op = "wipe"
            self.show()
        
    def open_rmv_available(self, config_id):
        if self.obj_configger.cfg.has_section(config_id):
            self.action_icon.setPixmap(self.obj_icons.rmv_icon)
            self.target_id = config_id
            self.window.setWindowTitle("Delete Configuration")
            self.text_main.setText("Confirm delete configuration?")
            self.text_info.setText(f'Target configuration: {self.obj_configger.cfg[config_id]["name"]}')
            self.target_op = "available"
            self.show()
    
    def open_rmv_active(self, id_pad, name):
        self.action_icon.setPixmap(self.obj_icons.rmv_icon)
        self.target_id = id_pad
        self.window.setWindowTitle("Disconnect Gamepad")
        self.text_main.setText(f'Confirm disconnect of {name}')
        self.target_op = "active"
        self.show()

    def show(self):
        self.window.move(self.obj_main_window.window.pos() + QtCore.QPoint(100,100))
        self.window.show()


    def action_cancel(self):
        self.target_id = None
        self.window.close()
    
    def action_proceed(self):
        if self.target_id:
            match self.target_op:
                case "wipe":
                    self.obj_configger.wipe_config(self.target_id)
                    self.obj_main_window.click_available(self.target_id)
                case "available":
                    self.obj_configger.rmv_config(self.target_id)
                    self.obj_main_window.rmv_available("")
                case "active":
                    self.obj_controller.rmv_gamepad(self.target_id)
                    self.obj_main_window.rmv_active()
            self.window.close()