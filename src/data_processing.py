import glob
import os

from src.errors import err_exit
from src.tar_processing import process_arcive

SOURCE_ARC_EXT = '*.gz'
EXTRACT_ARC_EXT = ['.EW1', '.EW2', '.NS1', '.NS2', '.UD1', '.UD2']

# from importlib import reload
# import src.data_processing
# reload(src.data_processing)


def extract_file_data(arcives_path):
    path_mask = os.path.join(arcives_path, SOURCE_ARC_EXT)

    arc_paths = glob.glob(path_mask)

    arcives_count = len(arc_paths)
    if not 4 <= arcives_count <= 6:
        err_exit('amount of earthquake arcives unexpected: ' + str(arcives_count))

    extracted_data = {}
    for arc_path in arc_paths:
        arc_name = os.path.basename(arc_path)
        extracted_data[arc_name] = process_arcive(arc_path, EXTRACT_ARC_EXT)

    return extracted_data


def process_dir(config):
    working_path = config['Source files']['default_path']
    files_data = extract_file_data(working_path)


    return
