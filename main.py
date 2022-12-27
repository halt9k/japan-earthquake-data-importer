import glob
import os
import subprocess
import sys

# TODO answer SO questions on deploy error if this line missing
# TODO create public git portable
sys.path.append(os.path.dirname(__file__))

from src.config import read_config
from src.errors import err_exit, log_msg
from src.jap_arc_parser import jap_arc_to_xlsx
from tkinter import filedialog

CONFIG_FILE = 'settings.ini'
ARC_EXTENSION = '*.tar.gz'


def os_view_path(path):
    # subprocess.Popen(r'explorer /select,"' + name + '"')
    dir_path = os.path.abspath(path)
    full_path = r'explorer /select,"' + dir_path + '"'
    subprocess.Popen(full_path)


def process_dir(a_config):
    arc_path, arc_paths = None, None
    default_path = a_config['Source files']['default_path']

    default_valid_path = os.path.commonpath([default_path])
    if not os.path.samefile(default_valid_path, default_path):
        log_msg('Warning: default_path in settings incorrect')
        default_path = default_valid_path

    if not a_config['Source files']['ask_path']:
        path_mask = os.path.join(default_path, ARC_EXTENSION)
        arc_paths = glob.glob(path_mask)

        arcives_count = len(arc_paths)
        if not 4 <= arcives_count <= 6:
            err_exit('amount of earthquake arcives unexpected: ' + str(arcives_count))
    else:
        path = os.path.abspath(default_path)
        arc_path = filedialog.askopenfilename(filetypes=[('Japan archives', ARC_EXTENSION)], initialdir=path)
        if not arc_path:
            err_exit('canceled')
        arc_paths = [arc_path]

    xlsx_fname = None

    for path in arc_paths:
        xlsx_fname = jap_arc_to_xlsx(path)

    if xlsx_fname:
        os_view_path(xlsx_fname)

    return


if __name__ == '__main__':
    config = read_config(CONFIG_FILE)
    process_dir(config)
