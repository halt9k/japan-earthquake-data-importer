import configparser


class App:
    __config = None

    @staticmethod
    def config():
        return App.__config

    @staticmethod
    def get_default_config():
        config_obj = configparser.ConfigParser()
        config_obj['Source files'] = {
            'ask_path': False,
            'default_arc_paths': [],
            'ask_xls_template': False,
            'default_xls_template': '',

        }
        return config_obj

    @staticmethod
    def read_config(conf_path):
        App.__config = App.get_default_config()
        App.__config.read(conf_path)
