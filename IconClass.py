from PyQt5.QtGui import QPixmap

class IconClass:

    console_dict = {
        "Playstation": [],
        "Xbox": []
    }

    add_icon = QPixmap("./imgs/add.png").scaledToHeight(20)
    rmv_icon = QPixmap("./imgs/rmv.png").scaledToHeight(20)
    edit_icon = QPixmap("./imgs/edit.png").scaledToHeight(20)
    clear_icon = QPixmap("./imgs/clear.png").scaledToHeight(20)
    wipe_icon = QPixmap("./imgs/wipe.png").scaledToHeight(30)
    speed_icon = QPixmap("./imgs/speed.png").scaledToHeight(30)
    mouse_icon = QPixmap("./imgs/mouse.png").scaledToHeight(40)
    south_icon = QPixmap("./imgs/south.png").scaledToHeight(40)
    west_icon = QPixmap("./imgs/west.png").scaledToHeight(40)
    north_icon = QPixmap("./imgs/north.png").scaledToHeight(40)
    east_icon = QPixmap("./imgs/east.png").scaledToHeight(40)

    logo_ps = QPixmap("./imgs/logos/ps.png").scaledToHeight(30)
    logo_xb = QPixmap("./imgs/logos/xb.png").scaledToHeight(30)

    def setup(self):
        for i in range(9):
            self.console_dict["Playstation"].append(QPixmap(f'./imgs/pad_icons/ps/{i}.png').scaledToHeight(40))
            self.console_dict["Xbox"].append(QPixmap(f'./imgs/pad_icons/xb/{i}.png').scaledToHeight(40))
        for i in range(9, 24):
            self.console_dict["Playstation"].append(QPixmap(f'./imgs/pad_icons/common/{i}.png').scaledToHeight(40))
            self.console_dict["Xbox"].append(QPixmap(f'./imgs/pad_icons/common/{i}.png').scaledToHeight(40))