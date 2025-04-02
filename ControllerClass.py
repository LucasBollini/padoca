import gc, libevdev, evdev, threading
from PyQt5.QtCore import QTimer

class Controller:

    id_counter = 0
    flag_running = 0
    flag_grab = False

    obj_configger = None
    obj_set_window = None

    current_mouse_posi = [0, 0]

    gamepad_dict = {}
    press_dict = {}
    release_dict = {}
    held_dict = {}

    async_QTimer = None
    async_counter = 0
    async_time = {}
    async_held = {}

    btn_dict = {
        "0": libevdev.EV_KEY.BTN_SOUTH,
        "1": libevdev.EV_KEY.BTN_WEST,
        "2": libevdev.EV_KEY.BTN_NORTH,
        "3": libevdev.EV_KEY.BTN_EAST,
        "4": libevdev.EV_KEY.BTN_TR,
        "5": libevdev.EV_KEY.BTN_TL,
        "6": libevdev.EV_ABS.ABS_RZ,
        "7": libevdev.EV_ABS.ABS_Z,
        "8": libevdev.EV_KEY.BTN_SELECT,
        "9": libevdev.EV_KEY.BTN_START,
        "22": libevdev.EV_KEY.BTN_THUMBL,
        "23": libevdev.EV_KEY.BTN_THUMBR,
    }
    
    axes_dict = {
        "10" : [libevdev.EV_ABS.ABS_HAT0Y, 0, 1, 1],
        "11" : [libevdev.EV_ABS.ABS_HAT0X, 0, 0, -1],
        "12" : [libevdev.EV_ABS.ABS_HAT0Y, 0, 1, -1],
        "13" : [libevdev.EV_ABS.ABS_HAT0X, 0, 0, 1],
        "14" : [libevdev.EV_ABS.ABS_Y, 1, 1, 1],
        "15" : [libevdev.EV_ABS.ABS_X, 1, 0, -1],
        "16" : [libevdev.EV_ABS.ABS_Y, 1, 1, -1],
        "17" : [libevdev.EV_ABS.ABS_X, 1, 0, 1],
        "18" : [libevdev.EV_ABS.ABS_RY, 2, 1, 1],
        "19" : [libevdev.EV_ABS.ABS_RX, 2, 0, -1],
        "20" : [libevdev.EV_ABS.ABS_RY, 2, 1, -1],
        "21" : [libevdev.EV_ABS.ABS_RX, 2, 0, 1],
    }


    def keyboard_listener(self):
        target_device = None
        for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
                if ("kb" in device.name.lower()) or ("keyboard" in device.name.lower()) or ("keyboard" in device.phys.lower()):
                    if "input0" in device.phys.lower():
                        target_device = device

        while True: #While and toggle_grab compose the most horrible gambiarra ever produced by mankind, though it is the only way possible
            for event in target_device.read_loop():
                if event.value != 2:
                    if event.type == evdev.ecodes.EV_KEY:
                        if (str(event.code) == '70') and (event.value == 0):
                            break
                        if event.value == 1:
                            self.handle_input(event.code)
                        else:
                            if event.value == 0:
                                self.handle_release(event.code)
            self.toggle_grab(target_device)
    

    def toggle_grab(self, keyboard_obj):
        self.flag_grab = not self.flag_grab
        if self.flag_grab:
            keyboard_obj.grab()
        else:
            keyboard_obj.ungrab()
    
    
    def mouse_listener(self):
        target_device = None
        for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
                if ("mouse" in device.name.lower()) or ("mouse" in device.phys.lower()):
                    if "input0" in device.phys.lower():
                        target_device = device

        for event in target_device.read_loop():
            if event.type:
                if event.code < 2:
                    if event.code == 0:
                        self.start_async("246" if event.value == 1 else "244", 60)
                    else:
                        self.start_async("243" if event.value == 1 else "245", 60)
                else:
                    if event.code == 8:
                        self.start_async('248' if event.value == 1 else '247', 150)
                    else:
                        if event.code > 271:
                            if event.value == 1:
                                self.handle_input(event.code - 23)
                            else:
                                if event.value == 0:
                                    self.handle_release(event.code - 23)


    def setup(self, obj_configger, obj_set_window):
        self.obj_configger = obj_configger
        self.obj_set_window = obj_set_window

        threading.Thread(target=self.keyboard_listener, daemon=True).start()
        threading.Thread(target=self.mouse_listener, daemon=True).start()

        self.async_QTimer = QTimer()
        self.async_QTimer.timeout.connect(self.step_async)
        self.async_QTimer.start(30)


    def start_async(self, id_input, sleep_time):
        self.async_time[id_input] = sleep_time
        if not self.async_held.get(id_input):
            self.async_held[id_input] = True
            self.async_counter += 1
            self.handle_input(id_input)

    def step_async(self):
        if self.async_counter:
            for key in self.async_held.keys():
                if self.async_held[key]:
                    if self.async_time[key] > 50:
                        self.async_time[key] -= 50
                    else:
                        self.async_held[key] = False
                        self.async_time[key] = 0
                        self.handle_release(key)
                        self.async_counter -= 1

    def handle_input(self, key):
        key = str(key)
        if self.obj_set_window.window.isVisible():
            if str(key) not in ["243", "244", "245", "246"]:
                self.obj_set_window.set_button(key)

        if not self.held_dict.get(key, True):
            for action in self.press_dict.get(key, []):
                action[1]()
                action[0].apply_changes()
            self.held_dict[key] = True
        
    def handle_release(self, key):
        key = str(key)
        for action in self.release_dict.get(key, []):
            action[1]()
            action[0].apply_changes()
        if key in self.held_dict:
            self.held_dict[key] = False
    


    def add_gamepad(self, id_config, name):
        if self.obj_configger.cfg.has_section(id_config):
            self.id_counter += 1
            new_gamepad = self.Gamepad(str(self.id_counter), id_config, name, self.btn_dict, self.axes_dict)
            self.gamepad_dict[new_gamepad.id_pad] = new_gamepad
            self.map_btns(new_gamepad.id_pad)
            return new_gamepad.id_pad
        
    def rmv_gamepad(self, id_pad):
        if id_pad in self.gamepad_dict:
            self.unmap_btns(id_pad)            
            del self.gamepad_dict[id_pad]
            gc.collect() # Without forcing the garbage collector, gamepad won't disconnect. Definitely not something I did wrong 
        


    def map_btns(self, id_pad):
        new_presses = []
        new_releases = []
        
        if (id_pad in self.gamepad_dict):
            gamepad = self.gamepad_dict[id_pad]

            if not self.obj_configger.cfg.has_section(gamepad.id_config):
                return
            
            pad_config = self.obj_configger.cfg[gamepad.id_config]

            for elem in self.btn_dict.keys():
                if self.obj_configger.cfg.has_option(gamepad.id_config, str(elem)):
                    new_presses.append([pad_config[str(elem)], lambda ev_key = self.btn_dict[str(elem)]: gamepad.change_btn(ev_key, 1)])
                    new_releases.append([pad_config[str(elem)], lambda ev_key = self.btn_dict[str(elem)]: gamepad.change_btn(ev_key, 0)])

            for elem in self.axes_dict.keys():
                if self.obj_configger.cfg.has_option(gamepad.id_config, str(elem)):
                    new_presses.append([pad_config[str(elem)], lambda ev_info = self.axes_dict[str(elem)]: gamepad.change_axis(ev_info[0], ev_info[1], ev_info[2], ev_info[3])])
                    new_releases.append([pad_config[str(elem)], lambda ev_info = self.axes_dict[str(elem)]: gamepad.change_axis(ev_info[0], ev_info[1], ev_info[2], -ev_info[3])])

            for group in [[new_presses, self.press_dict], [new_releases, self.release_dict]]:
                for new_action in group[0]:
                    if new_action[0] not in group[1]:
                        group[1][new_action[0]] = []
                        self.held_dict[new_action[0]] = False
                    group[1][new_action[0]].append([gamepad, new_action[1]])

    def unmap_btns(self, id_pad):
        key_list = list(self.held_dict.keys())

        for group in [self.press_dict, self.release_dict]:
            for key in key_list:
                for index in reversed(range(len(group[key]))):
                    if group[key][index][0].id_pad == id_pad:
                        group[key].pop(index)
                if not group[key]:
                    del group[key]
        for key in key_list:
            if (key not in self.press_dict) and (key not in self.release_dict):
                del self.held_dict[key]

    def change_pad_config(self, target_pad, new_config):
        target_pad.id_config = new_config
        self.unmap_btns(target_pad.id_pad)
        self.map_btns(target_pad.id_pad)

    def remap_changed(self, id_changed_config):
        for gamepad in self.gamepad_dict.values():
            if gamepad.id_config == id_changed_config:
                self.unmap_btns(gamepad.id_pad)
                self.map_btns(gamepad.id_pad)


    class Gamepad:

        def __init__(self, id_pad, id_config, name, btn_dict, axes_dict):
            super().__init__()
            self.id_pad = id_pad
            self.id_config = id_config
            self.name = name

            self.change_list = []

            self.axes_values = [
                [0,0],
                [0,0],
                [0,0]
            ]

            self.device = libevdev.Device()
            self.device.name = name

            for ev_key in btn_dict.values():
                if (ev_key == libevdev.EV_ABS.ABS_RZ) or (ev_key == libevdev.EV_ABS.ABS_Z):
                    self.device.enable(ev_key, libevdev.InputAbsInfo(minimum=0, maximum=1, value=0))
                else:
                    self.device.enable(ev_key)
            
            for ev_key in axes_dict.values():
                self.device.enable(ev_key[0], libevdev.InputAbsInfo(minimum=-1, maximum=1, value=0))

            self.uinput = self.device.create_uinput_device()


        def change_btn(self, ev_key, new_value):
            self.change_list.append(libevdev.InputEvent(ev_key, value=new_value))
        
        def change_axis(self, ev_key, id_axis, dir_axis, new_value):
            self.axes_values[id_axis][dir_axis] += new_value
            #print(self.axes_values[id_axis])
            self.change_list.append(libevdev.InputEvent(ev_key, value=self.axes_values[id_axis][dir_axis]))
        
        def apply_changes(self):
            if self.change_list:
                self.change_list.append(libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0))
                self.uinput.send_events(self.change_list)
                self.change_list = []