import configparser


def get_default_config():
    config_obj = configparser.ConfigParser()
    config_obj['Source files'] = {
        'ask_path': False,
        'default_path': ''
    }
    return  config_obj


def read_config(conf_path):
    config_obj = get_default_config()
    config_obj.read(conf_path)
    return config_obj
