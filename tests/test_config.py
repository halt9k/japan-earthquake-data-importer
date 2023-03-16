import configparser
from pathlib import Path

import pytest

from config import APP


class Test:
    def test_empty_config(self):
        APP.read_config('./test_config_fixtures/settings_empty.ini')
        assert (APP.get_default_config() == APP.config())

    def test_outdated_config(self):
        with pytest.raises(configparser.NoOptionError):
            APP.read_config('./test_config_fixtures/settings_invalid.ini')

    def test_config_paths(self):
        APP.read_config('./test_config_fixtures/settings_path.ini')
        assert APP.config()['Data sources']['default_arc_paths'] == 'data/KYTH031211171713.tar.gz'
        assert APP.config()['Data sources']['default_xls_template'] == 'Template_empty.xlsx'
