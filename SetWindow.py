from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
import time

class SetWindow:

    window : QWidget = QWidget()

    obj_icons = None
    obj_configger = None
    obj_main_window = None
    obj_controller = None

    button_icon : QLabel
    button_id : None

    current_console = "Playstation"
    speed_set = False

    cursor_pointer = QCursor(QtCore.Qt.CursorShape.PointingHandCursor)

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
        self.window.setFixedSize(300, 350)
        self.window.setWindowTitle("Set Button")
        self.window.setStyleSheet("background-color: #231f36; color: white;")

        button_icon = QLabel()
        button_icon.setFixedSize(41,41)
        vbox_layout.addWidget(button_icon, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.button_icon = button_icon
        
        vbox_layout.addWidget(QLabel("Press a keyboard key"), alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        vbox_layout.addWidget(QLabel("or a mouse button"), alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        vbox_layout.addWidget(QLabel("or scroll up/down"), alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        vbox_layout.addWidget(QLabel("or click on a mouse movement direction"), alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        vbox_layout.addSpacing(20)

        
        mouse_directions = [self.obj_icons.south_icon, self.obj_icons.west_icon, self.obj_icons.north_icon, self.obj_icons.east_icon]
        mouse_labels = []
        for i in range(4):
            mouse_labels.append(QLabel())
            mouse_labels[i].setFixedSize(41,41)
            mouse_labels[i].setPixmap(mouse_directions[i])
            mouse_labels[i].setCursor(self.cursor_pointer)
            mouse_labels[i].mousePressEvent = lambda a, id_btn=(i+243) : self.set_mouse_mov(id_btn)


        vbox_layout.addWidget(mouse_labels[2], alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        hbox_layout = QHBoxLayout()
        hbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        mouse_center_frame = QFrame()
        mouse_center_frame.setLayout(hbox_layout)
        vbox_layout.addWidget(mouse_center_frame, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        hbox_layout.addWidget(mouse_labels[1], alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        mouse = QLabel()
        mouse.setFixedSize(41,41)
        mouse.setPixmap(self.obj_icons.mouse_icon)
        hbox_layout.addWidget(mouse, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        hbox_layout.addWidget(mouse_labels[3], alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        vbox_layout.addWidget(mouse_labels[0], alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)



    
    def show(self, console, button_id, is_speed = False):
        self.speed_set = is_speed
        self.button_icon.setPixmap(self.obj_icons.console_dict[console][button_id])
        self.current_console = console
        self.button_id = button_id
        self.window.move(self.obj_main_window.window.pos() + QtCore.QPoint(210,130))
        time.sleep(0.1)
        self.window.show()
    


    def set_mouse_mov(self, new_key):
        time.sleep(0.1)
        self.window.show()
        self.set_button(new_key)

    def set_button(self, new_key):
        if self.window.isVisible():
            self.obj_configger.update_config(self.obj_main_window.selected_available, self.button_id, new_key)
            #self.obj_controller.remap_changed(self.obj_main_window.selected_available)

            if int(new_key) > len(self.obj_main_window.key_names):
                self.obj_main_window.input_list[self.button_id].setText(f'KEY_ID_{new_key}')
            else:
                self.obj_main_window.input_list[self.button_id].setText(self.obj_main_window.key_names[int(new_key)])

            if self.speed_set and self.button_id != 23:
                self.button_id += 1
                self.button_icon.setPixmap(self.obj_icons.console_dict[self.current_console][self.button_id])
            else:
                self.window.close()