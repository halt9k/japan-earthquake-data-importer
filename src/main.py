import glob
import os
import subprocess
import sys

# TODO answer SO questions on deploy error if this line missing
# TODO create public git portable

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config import read_config
from src.errors import err_exit, log_msg
from src.jap_arc_parser import jap_arc_to_xlsx, verify_file_exists, copy_file_override
from tkinter import filedialog

CONFIG_FILE = 'settings.ini'
ARC_EXT = '.tar.gz'
ARC_MASK = '*' + ARC_EXT
XLS_EXT = '.xlsx'
XLS_MASK = '*' + XLS_EXT


def os_view_path(path):
    # subprocess.Popen(r'explorer /select,"' + name + '"')
    dir_path = os.path.abspath(path)
    full_path = r'explorer /select,"' + dir_path + '"'
    subprocess.Popen(full_path)


def get_config_path(supposed_path, ask, ask_filetypes, ask_title):
    if not ask:
        verify_file_exists(supposed_path)
        return  supposed_path

    closest_valid = os.path.commonpath([supposed_path])

    path = filedialog.askopenfilename(filetypes=ask_filetypes, initialdir=closest_valid, title=ask_title)
    if not path:
        err_exit('canceled')

    return path


def batch_import(arc_path, template_path):
    path_mask = os.path.join(arc_path, ARC_MASK)
    arc_paths = glob.glob(path_mask)

    arcives_count = len(arc_paths)
    if not 2 <= arcives_count <= 10:
        err_exit('amount of earthquake arcives unexpected: ' + str(arcives_count))

    xlsx_fname = None
    for path in arc_paths:
        xlsx_fname = jap_arc_to_xlsx(path, template_path)

    return xlsx_fname


def import_data(try_src_arc, ask_src, try_dest_xls, ask_dest):
    arc_path = get_config_path(try_src_arc, ask_src, [('Japan archives', ARC_MASK)], 'Select source archive')
    title = 'Select excel template for source archive ' + os.path.basename(arc_path)
    template_path = get_config_path(try_dest_xls, ask_dest, [('Excel files', XLS_MASK)], title)

    if os.path.isdir(arc_path):
        xlsx_fname = batch_import(arc_path, template_path)
    else:
        xlsx_fname = jap_arc_to_xlsx(arc_path, template_path)

    return xlsx_fname


def process_dir(a_config):
    ask_arc_path = a_config['Data sources'].getboolean('ask_archive')
    default_arc = a_config['Data sources']['default_arc_path']
    ask_dest = a_config['Data sources'].getboolean('ask_xls_template')
    default_dest = a_config['Data sources']['default_xls_template']

    xlsx_fname = import_data(default_arc, ask_arc_path, default_dest, ask_dest)

    if xlsx_fname:
        os_view_path(xlsx_fname)

    return


if __name__ == '__main__':
    config = read_config(CONFIG_FILE)
    process_dir(config)
