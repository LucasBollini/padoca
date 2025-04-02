import configparser, time, os

class Configger:

    cfg = None
    file_path = "./padoca_configs.cfg"

    def setup(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.file_path)


    def save_file(self):
        with open(self.file_path, "w") as file:
            self.cfg.write(file)
        try:
            os.chown(self.file_path, int(os.environ.get('SUDO_UID')), int(os.environ.get('SUDO_GID')))
        except:
            pass
    

    def add_config(self, pad_type):
        new_id = f'{time.time()}'
        self.cfg.add_section(new_id)
        self.cfg[new_id]["name"] = "New Config"
        self.cfg[new_id]["pad_type"] = pad_type
        self.save_file()
        return new_id
    
    def update_config(self, id_cfg, target, new_value):
        if self.cfg.has_section(id_cfg):
            self.cfg[id_cfg][str(target)] = str(new_value)
            self.save_file()

    def rmv_option(self, id_cfg, target):
        if self.cfg.has_section(id_cfg):
            self.cfg.remove_option(id_cfg, str(target))
            self.save_file()
    
    def wipe_config(self, id_cfg):
        if self.cfg.has_section(id_cfg):
            for i in range(24):
                self.cfg.remove_option(id_cfg, str(i))
            self.save_file()

    def rmv_config(self, id_cfg):
        if self.cfg.has_section(id_cfg):
            self.cfg.remove_section(id_cfg)
            self.save_file()