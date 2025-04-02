from PyQt5.QtWidgets import QApplication
Qt5App = QApplication([])


from ConfiggerClass import Configger
from IconClass import IconClass
from MainWindow import MainWindow
from SetWindow import SetWindow
from ConfirmWindow import ConfirmWindow
from EditPadWindow import EditPadWindow
from ControllerClass import Controller


obj_configger = Configger()
obj_icons = IconClass()
main_window = MainWindow()
set_window = SetWindow()
confirm_window = ConfirmWindow()
editPad_window = EditPadWindow()
obj_controller = Controller()


obj_configger.setup()
obj_icons.setup()
main_window.setup(obj_icons, obj_configger, set_window, confirm_window, editPad_window)
set_window.setup(obj_icons, obj_configger, main_window, obj_controller)
confirm_window.setup(obj_icons, obj_configger, main_window, obj_controller)
editPad_window.setup(obj_icons, obj_configger, main_window, obj_controller)
obj_controller.setup(obj_configger, set_window)



Qt5App.exec()