from configparser import ConfigParser, NoOptionError
from enum import Enum

from pandas.io import json


class ImportModes:
    MULTIPLE_PAGES = 'multiple_pages'
    SINGLE_PAGE = 'single_page'
    ALL = [MULTIPLE_PAGES, SINGLE_PAGE]


DEFAULT_CONFIG = {
    'Data sources': {
        'ask_archive': False,
        'default_arc_paths': [],
        'ask_xls_template': False,
        'default_xls_template': ''
    },
    'Excel import': {
        'import_mode': ImportModes.MULTIPLE_PAGES,
        'header_final_order': ''
    },
    'UX': {
        'slow_paced_import': True
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

    @staticmethod
    def validate_enums(config):
        if config.has_option('Excel import', 'import_mode'):
            assert(config['Excel import']['import_mode'] in ImportModes.ALL)

    @staticmethod
    def ensure_correct_config_file(default_config, ini_config, conf_path):
        deafult_opts = AppConfig.all_options(default_config)
        ini_file_opts = AppConfig.all_options(ini_config)

        new_opts = set(ini_file_opts) - set(deafult_opts)
        old_opts = set(deafult_opts) - set(ini_file_opts)
        if len(new_opts) > 0:
            raise NoOptionError(str(new_opts) + '; probably intended : ' + str(old_opts), section=conf_path)

        AppConfig.validate_enums(ini_config)

    def read_config(self, conf_path):
        ini_config = ConfigParser(strict=True)
        ini_config.read(conf_path)

        default_config = AppConfig.get_default_config()
        AppConfig.ensure_correct_config_file(default_config, ini_config, conf_path)

        # all checked, read again to do override of defaults
        self.__config = default_config
        self.__config.read(conf_path)

    # TODO improve
    @staticmethod
    def get_list(config, section, entry):
        str_entry = config[section][entry]
        if '\n' in str_entry:
            return list(json.loads(str_entry))
        else:
            return list([str_entry])


APP = AppConfig()
