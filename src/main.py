import glob
import os
import subprocess

# TODO answer SO questions on deploy error if this line missing

from config import APP
from errors import err_exit, debugger_is_active
from jap_arc_parser import jap_arcs_to_xlsx, verify_file_exists
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


def get_config_paths(try_paths, is_silent, ask_filetypes, ask_title, allow_multiple):
    if not is_silent:
        for path in try_paths:
            verify_file_exists(path)
        return try_paths

    closest_valid_dir = os.path.commonpath(try_paths)
    if not os.path.isdir(closest_valid_dir):
        closest_valid_dir = os.path.dirname(closest_valid_dir)

    try_files = ' '.join(['"{}"'.format(os.path.basename(x)) for x in try_paths])

    paths = filedialog.askopenfilename(filetypes=ask_filetypes,
                                       initialdir=closest_valid_dir, initialfile=try_files,
                                       title=ask_title, multiple=allow_multiple)
    if not paths:
        err_exit('canceled')

    return paths


def get_config_path(try_path, is_silent, ask_filetypes, ask_title, allow_multiple):
    res = get_config_paths([try_path], is_silent, ask_filetypes, ask_title, allow_multiple)

    if res:
        if allow_multiple:
            assert(type(res) is list)
        else:
            assert (type(res) is str)
    return res


def get_archives(arc_path):
    path_mask = os.path.join(arc_path, ARC_MASK)
    arc_paths = glob.glob(path_mask)

    arcives_count = len(arc_paths)
    if not 2 <= arcives_count <= 10:
        err_exit('amount of earthquake arcives unexpected: ' + str(arcives_count))

    return arc_paths


def import_data(try_data_arc_paths, ask_data_paths, try_template_path, ask_tamplate_path):
    arc_paths = get_config_paths(try_data_arc_paths, ask_data_paths, [('Japan archives', ARC_MASK)],
                                 'Select source archive', allow_multiple=True)

    if type(arc_paths) is tuple and len(arc_paths) == 1:
        arc_info = os.path.basename(arc_paths[0])
    else:
        arc_info = ' count of ' + str(len(arc_paths))
    title = 'Select excel template for source archive ' + arc_info
    template_path = get_config_path(try_template_path, ask_tamplate_path, [('Excel files', XLS_MASK)], title,
                                    allow_multiple=False)

    if len(arc_paths) == 1 and os.path.isdir(arc_paths[0]):
        arc_paths = get_archives(arc_paths[0])

    xlsx_fname = jap_arcs_to_xlsx(arc_paths, template_path)

    return xlsx_fname


def process_dir():
    try_data_paths_text = APP.config()['Data sources']['default_arc_paths']
    ask_data_paths = APP.config()['Data sources'].getboolean('ask_archive')

    try_data_paths = try_data_paths_text.replace('\t', '').split('\n')
    try_data_paths = list(filter(None, try_data_paths))

    try_template_path = APP.config()['Data sources']['default_xls_template']
    ask_template = APP.config()['Data sources'].getboolean('ask_xls_template')

    xlsx_fname = import_data(try_data_paths, ask_data_paths, try_template_path, ask_template)

    if xlsx_fname and debugger_is_active():
        os_view_path(xlsx_fname)

    return


def main():
    APP.read_config(CONFIG_FILE)
    process_dir()


if __name__ == '__main__':
    main()