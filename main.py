from src.config import read_config
from src.data_processing import process_dir

SETTINGS_FILE = 'settings.ini'

if __name__ == '__main__':
    config = read_config(SETTINGS_FILE)
    process_dir(config)