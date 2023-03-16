from configparser import ConfigParser, NoOptionError
from pathlib import Path

DEFAULT_CONFIG = {
    'Data sources': {
        'ask_archive': False,
        'default_arc_paths': [],
        'ask_xls_template': False,
        'default_xls_template': ''
    },
    'UX': {
        'slow_paced_import': True,
        'create_control_histograms': False
    }
}


class AppConfig:
    @staticmethod
    def get_default_config():
        result = ConfigParser(strict=True)
        for section in DEFAULT_CONFIG:
            result[section] = DEFAULT_CONFIG[section]
        return result

    def __init__(self):
        self.__config = None

    def config(self):
        return self.__config

    @staticmethod
    def all_options(parser: ConfigParser):
        sections = parser.sections()
        opts = []
        for s in sections:
            opts += list(parser.options(s))
        return opts

    def read_config(self, conf_path):
        assert Path(conf_path).exists()

        ini_config = ConfigParser(strict=True)
        ini_config.read(conf_path)
        default_config = AppConfig.get_default_config()

        deafult_opts = AppConfig.all_options(default_config)
        ini_file_opts = AppConfig.all_options(ini_config)

        new_opts = set(ini_file_opts) - set(deafult_opts)
        old_opts = set(deafult_opts) - set(ini_file_opts)
        if len(new_opts) > 0:
            raise NoOptionError(str(new_opts) + '; probably intended : ' + str(old_opts), section=conf_path)

        # all checked, read again to do override of defaults
        self.__config = default_config
        self.__config.read(conf_path)


APP = AppConfig()
