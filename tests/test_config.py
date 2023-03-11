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

