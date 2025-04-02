from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QFrame,\
                            QVBoxLayout, QScrollArea, QWidget, QApplication
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
import sys

class MainWindow:

    window : QWidget = QWidget()
    
    obj_icons = None
    obj_configger = None
    obj_set_window = None
    obj_confirm_window = None
    obj_editPad_window = None

    input_list = []
    icon_list = []
    vbox_availables : QVBoxLayout = None
    vbox_actives : QVBoxLayout = None

    group_create : QFrame = None

    dict_availables = {}
    dict_actives = {}

    selected_available = None
    selected_active = None

    lbl_rmv_availables : QLabel
    lbl_rmv_actives : QLabel

    lbl_edit_active : QLabel

    field_newName = None
    combo_newType = None
    pad_type = "Playstation"

    cursor_pointer = QCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    key_names = ['reserved','esc','1','2','3','4','5','6','7','8','9','0','minus','equal','backspace','tab','q','w','e','r','t','y','u','i','o','p','l_brace','r_brace','enter','l_ctrl','a','s','d','f','g','h','j','k','l','semicolon','apostrophe','grave','l_shift','backslash','z','x','c','v','b','n','m','comma','dot','slash','r_shift','numpad_asterisk','l_alt','space','capslock','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','numlock','scrolllock','numpad_7','numpad_8','numpad_9','numpad_minus','numpad_4','numpad_5','numpad_6','numpad_plus','numpad_1','numpad_2','numpad_3','numpad_0','numpad_dot','unknown','zenkakuhankaku','102nd','f11','f12','ro','katakana','hiragana','henkan','katakanahiragana','muhenkan','numpad_jpcomma','numpad_enter','r_ctrl','numpad_slash','sysrq','r_alt','linefeed','home','up','pageup','l_','r_','end','down','pagedown','insert','delete','macro','mute','volumedown','volumeup','power','numpad_equal','numpad_plusminus','pause','scale','numpad_comma','hanguel','hanja','yen','l_meta','r_meta','compose','stop','again','props','undo','front','copy','open','paste','find','cut','help','menu','calc','setup','sleep','wakeup','file','sendfile','deletefile','xfer','prog1','prog2','www','msdos','screenlock','rotate_display','cyclewindows','mail','bookmarks','computer','back','forward','closecd','ejectcd','ejectclosecd','nextsong','playpause','previoussong','stopcd','record','rewind','phone','iso','config','homepage','refresh','exit','move','edit','scrollup','scrolldown','numpad_leftparen','numpad_rightparen','new','redo','f13','f14','f15','f16','f17','f18','f19','f20','f21','f22','f23','f24','unknown','unknown','unknown','unknown','unknown','playcd','pausecd','prog3','prog4','dashboard','suspend','close','play','fastforward','bassboost','print','hp','camera','sound','question','email','chat','search','connect','finance','sport','shop','alterase','cancel','brightnessdown','brightnessup','media','switchvideomode','kbdillumtoggle','kbdillumdown','kbdillumup','send','reply','forwardmail','save','documents','battery','bluetooth','wlan','uwb','unknown','video_next','video_prev',"mouse_south","mouse_west","mouse_north","mouse_east","wheel_down","wheel_up","mouse_1","mouse_2","mouse_3","mouse_x1","mouse_x2","mouse_x3","mouse_x4","mouse_x5","mouse_x6","mouse_x7","mouse_x8","mouse_x9","mouse_x10"]


    def setup(self, obj_icons, obj_configger, obj_set_window, obj_confirm_window, obj_editPad_window):
        self.obj_icons = obj_icons
        self.obj_configger = obj_configger
        self.obj_set_window = obj_set_window
        self.obj_confirm_window = obj_confirm_window
        self.obj_editPad_window = obj_editPad_window

        self.create_window()
        self.window.show()
        
    
    def create_window(self):        
        self.window.setFixedSize(870, 630)
        self.window.setWindowTitle("Padoca - Keyboard to Gamepad")
        self.window.setStyleSheet("background-color: #231f36; color: white;")
        self.window.closeEvent = lambda a: QApplication.quit()

        self.create_actives()
        self.create_available()
        self.create_create()

        self.populate_availables()

    def switch_input_icons(self, event):
        self.pad_type = event
        if self.selected_available and self.dict_availables.get(self.selected_available):
            self.obj_configger.update_config(self.selected_available, "pad_type", self.pad_type)
        for i in range(9):
           self.icon_list[i].setPixmap(self.obj_icons.console_dict[event][i])

    def populate_availables(self):
        for id_cfg in self.obj_configger.cfg.sections():
            self.dict_availables[id_cfg] = QLabel(f'{self.obj_configger.cfg[id_cfg]["name"]}')
            self.dict_availables[id_cfg].mousePressEvent = lambda a, id_cfg = id_cfg: self.click_available(id_cfg)
            self.vbox_availables.addWidget(self.dict_availables[id_cfg])

    def click_available(self, id_cfg):
        if self.dict_availables.get(self.selected_available):
            self.dict_availables[self.selected_available].setStyleSheet("background-color: transparent")
        self.selected_available = id_cfg
        self.lbl_rmv_availables.setDisabled(False)
        self.group_create.setDisabled(False)
        self.dict_availables[self.selected_available].setStyleSheet("background-color: rgba(20,255,20,0.3)")
        self.field_newName.setText(self.obj_configger.cfg[id_cfg]["name"])
        self.combo_newType.setCurrentText(self.obj_configger.cfg[id_cfg]["pad_type"])
        for i in range(24):
            if self.obj_configger.cfg.has_option(id_cfg , str(i)):
                if int(self.obj_configger.cfg[id_cfg][str(i)]) > len(self.key_names):
                    self.input_list[i].setText(f'KEY_ID_{self.obj_configger.cfg[id_cfg][str(i)]}')
                else:
                    self.input_list[i].setText(self.key_names[int(self.obj_configger.cfg[id_cfg][str(i)])])
            else:
                self.input_list[i].setText("--Click to Set--")

    def unclick_available(self):
        if self.dict_availables.get(self.selected_available):
            self.dict_availables[self.selected_available].setStyleSheet("background-color: transparent")
        self.selected_available = None
        self.lbl_rmv_availables.setDisabled(True)
        self.group_create.setDisabled(True)

    def add_available(self, event):
        new_id = self.obj_configger.add_config(self.pad_type)
        self.dict_availables[new_id] = QLabel("New Config")
        self.dict_availables[new_id].mousePressEvent = lambda a, id_cfg = new_id: self.click_available(id_cfg)
        self.vbox_availables.addWidget(self.dict_availables[new_id])
        self.click_available(new_id)

    def rmv_available(self, event):
        if self.selected_available and self.dict_availables.get(self.selected_available):
            self.vbox_availables.removeWidget(self.dict_availables[self.selected_available])
            self.dict_availables[self.selected_available].deleteLater()
            del self.dict_availables[self.selected_available]
            self.unclick_available()
    
    def alter_config_name(self, event):
        if self.selected_available and self.dict_availables.get(self.selected_available):
            self.obj_configger.update_config(self.selected_available, "name", event)
            self.dict_availables[self.selected_available].setText(event)

    def clear_button(self, btn_id):
        self.input_list[btn_id].setText("--Click to Set--")
        self.obj_configger.rmv_option(self.selected_available, btn_id)

    def add_active(self, name, id_pad):
        self.dict_actives[id_pad] = QLabel(name)
        self.dict_actives[id_pad].mousePressEvent = lambda a, id_pad = id_pad: self.click_active(id_pad)
        self.vbox_actives.addWidget(self.dict_actives[id_pad])
    
    def rmv_active(self):
        if self.selected_active and self.dict_actives.get(self.selected_active):
            self.vbox_actives.removeWidget(self.dict_actives[self.selected_active])
            self.dict_actives[self.selected_active].deleteLater()
            del self.dict_actives[self.selected_active]
            self.unclick_active()

    def click_active(self, id_pad):
        if self.dict_actives.get(self.selected_active):
            self.dict_actives[self.selected_active].setStyleSheet("background-color: transparent")
        self.selected_active = id_pad
        self.lbl_rmv_actives.setDisabled(False)
        self.lbl_edit_active.setDisabled(False)
        self.dict_actives[self.selected_active].setStyleSheet("background-color: rgba(20,255,20,0.3)")
    
    def unclick_active(self):
        if self.dict_actives.get(self.selected_active):
            self.dict_actives[self.selected_active].setStyleSheet("background-color: transparent")
        self.selected_active = None
        self.lbl_rmv_actives.setDisabled(True)
        self.lbl_edit_active.setDisabled(True)



    def create_actives(self):
        group_actives = QFrame(self.window)
        group_actives.setGeometry(0, 0, 250, 620)

        text_actives = QLabel("Active", group_actives)
        text_actives.setStyleSheet("font-weight: bold; font-size: 15px;")
        text_actives.move(15, 10)
        
        self.lbl_rmv_actives = QLabel(group_actives)
        self.lbl_rmv_actives.setPixmap(self.obj_icons.rmv_icon)
        self.lbl_rmv_actives.move(130, 10)
        self.lbl_rmv_actives.setCursor(self.cursor_pointer)
        self.lbl_rmv_actives.setDisabled(True)
        self.lbl_rmv_actives.mousePressEvent = lambda a: self.obj_confirm_window.open_rmv_active(self.selected_active, self.dict_actives[self.selected_active].text())

        self.lbl_edit_active = QLabel(group_actives)
        self.lbl_edit_active.setPixmap(self.obj_icons.edit_icon)
        self.lbl_edit_active.move(170, 10)
        self.lbl_edit_active.setCursor(self.cursor_pointer)
        self.lbl_edit_active.setDisabled(True)
        self.lbl_edit_active.mousePressEvent = lambda a : self.obj_editPad_window.open_edit(self.selected_active)

        add_active = QLabel(group_actives)
        add_active.setPixmap(self.obj_icons.add_icon)
        add_active.move(210, 10)
        add_active.setCursor(self.cursor_pointer)
        add_active.mousePressEvent = lambda a : self.obj_editPad_window.open_add()
        
        frame_gamepads = QFrame(group_actives)
        frame_gamepads.setStyleSheet("border: 1px solid grey; border-radius: 10px;")
        frame_gamepads.setGeometry(10, 35, 230, 580)

        widget_bcus = QWidget()
        self.vbox_actives = QVBoxLayout(widget_bcus)
        self.vbox_actives.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        scroll_actives = QScrollArea(group_actives)
        scroll_actives.setGeometry(20, 45, 210, 560)
        scroll_actives.setWidget(widget_bcus)
        scroll_actives.setWidgetResizable(True)
    
    def create_available(self):

        group_availables = QFrame(self.window)
        group_availables.setGeometry(250, 0, 250, 620)

        text_availables = QLabel("Available", group_availables)
        text_availables.setStyleSheet("font-weight: bold; font-size: 15px;")
        text_availables.move(15, 10)

        self.lbl_rmv_availables = QLabel(group_availables)
        self.lbl_rmv_availables.setPixmap(self.obj_icons.rmv_icon)
        self.lbl_rmv_availables.move(160, 10)
        self.lbl_rmv_availables.setCursor(self.cursor_pointer)
        self.lbl_rmv_availables.setDisabled(True)
        self.lbl_rmv_availables.mousePressEvent = lambda a: self.obj_confirm_window.open_rmv_available(self.selected_available)

        add_availables = QLabel(group_availables)
        add_availables.setPixmap(self.obj_icons.add_icon)
        add_availables.move(210, 10)
        add_availables.setCursor(self.cursor_pointer)
        add_availables.mousePressEvent = self.add_available

        frame_availables = QFrame(group_availables)
        frame_availables.setStyleSheet("border: 1px solid grey; border-radius: 10px;")
        frame_availables.setGeometry(10, 35, 230, 580)

        widget_bcus = QWidget()
        self.vbox_availables = QVBoxLayout(widget_bcus)
        self.vbox_availables.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        scroll_availables = QScrollArea(group_availables)
        scroll_availables.setGeometry(20, 45, 210, 560)
        scroll_availables.setWidget(widget_bcus)
        scroll_availables.setWidgetResizable(True)


    def create_create(self):
        group_create = QFrame(self.window)
        group_create.setGeometry(500, 0, 370, 620)
        group_create.setDisabled(True)
        self.group_create = group_create

        text_create= QLabel("Edit Configuration", group_create)
        text_create.setStyleSheet("font-weight: bold; font-size: 15px;")
        text_create.move(10, 10)

        frame_create = QFrame(group_create)
        frame_create.setStyleSheet("border: 1px solid grey; border-radius: 10px;")
        frame_create.setGeometry(10, 35, 350, 580)

        text_newType = QLabel("Pad Type", group_create)
        text_newType.move(20, 45)

        combo_newType = QComboBox(group_create)
        combo_newType.setGeometry(110, 40, 120, 30)
        combo_newType.addItems(["Playstation", "Xbox"])
        combo_newType.currentTextChanged.connect(self.switch_input_icons)
        self.combo_newType = combo_newType

        text_newName = QLabel("Config Name", group_create)
        text_newName.move(20, 75)

        field_newName = QLineEdit(group_create)
        field_newName.setGeometry(110, 70, 120, 30)
        field_newName.setStyleSheet("background-color: black;")
        field_newName.textChanged.connect(self.alter_config_name)
        self.field_newName = field_newName

        speed_set = QLabel(group_create)
        speed_set.setPixmap(self.obj_icons.speed_icon)
        speed_set.move(240, 60)
        speed_set.setCursor(self.cursor_pointer)
        speed_set.mousePressEvent = lambda a: self.obj_set_window.show(self.pad_type, 0, True)

        wipe_config = QLabel(group_create)
        wipe_config.setPixmap(self.obj_icons.wipe_icon)
        wipe_config.move(310, 60)
        wipe_config.setCursor(self.cursor_pointer)
        wipe_config.mousePressEvent = lambda a: self.obj_confirm_window.open_wipe_for_all_to_see(self.selected_available)

        group_icons_left = QFrame(group_create)
        group_icons_left.setGeometry(20, 110, 41, 500)
        group_icons_right = QFrame(group_create)
        group_icons_right.setGeometry(195, 110, 41, 500)

        group_inputs_left = QFrame(group_create)
        group_inputs_left.setGeometry(65, 110, 81, 500)
        group_inputs_right = QFrame(group_create)
        group_inputs_right.setGeometry(240, 110, 81, 500)


        group_clear_left = QFrame(group_create)
        group_clear_left.setGeometry(150, 110, 21, 500)
        group_clear_right = QFrame(group_create)
        group_clear_right.setGeometry(325, 110, 21, 500)


        for i in range(24):
            self.icon_list.append(None)
            self.input_list.append(None)

        for i in range(12):
            icon_holder = QLabel(group_icons_left)
            icon_holder.setPixmap(self.obj_icons.console_dict["Playstation"][i])
            icon_holder.setGeometry(1, i * 42, 40, 40)
            self.icon_list[i] = icon_holder
            icon_holder = QLabel(group_icons_right)
            icon_holder.setPixmap(self.obj_icons.console_dict["Playstation"][i + 12])
            icon_holder.setGeometry(1, i * 42, 40, 40)
            self.icon_list[i + 12] = icon_holder
            icon_holder = QLabel(group_clear_left)
            icon_holder.setPixmap(self.obj_icons.clear_icon)
            icon_holder.setGeometry(1, 10 + (i * 42), 21, 21)
            icon_holder.setCursor(self.cursor_pointer)
            icon_holder.mousePressEvent = lambda a, btn_id = i: self.clear_button(btn_id)
            icon_holder = QLabel(group_clear_right)
            icon_holder.setPixmap(self.obj_icons.clear_icon)
            icon_holder.setGeometry(1, 10 + (i * 42), 21, 21)
            icon_holder.setCursor(self.cursor_pointer)
            icon_holder.mousePressEvent = lambda a, btn_id = (i + 12): self.clear_button(btn_id)

            input_holder = QLabel("--Click to Set--", group_inputs_left)
            input_holder.setStyleSheet("background-color: black;")
            input_holder.setGeometry(1, 8 + (i * 42), 80, 25)
            input_holder.mousePressEvent = lambda a, btn_id = i: self.obj_set_window.show(self.pad_type, btn_id)
            self.input_list[i] = input_holder
            input_holder = QLabel("--Click to Set--", group_inputs_right)
            input_holder.setStyleSheet("background-color: black;")
            input_holder.setGeometry(1, 8 + (i * 42), 80, 25)
            input_holder.mousePressEvent = lambda a, btn_id = (i + 12): self.obj_set_window.show(self.pad_type, btn_id)
            self.input_list[i + 12] = input_holder
        