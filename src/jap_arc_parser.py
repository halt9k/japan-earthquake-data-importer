import os

import shutil
import time

from src.errors import err_exit, log_msg
from src.jap_txt_parser import jap_text_to_tables, HEADER_DATE
from src.tar_extract import extract_arcive_files
from xls_writer import modify_excel_shreadsheet

EXTRACT_ARC_EXT = ['.EW1', '.EW2', '.NS1', '.NS2', '.UD1', '.UD2']


def verify_file_exists(path):
    if not os.path.exists(path):
        err_exit('Expected file missing: \n' + path)


def copy_file_override(src, dst):
    if os.path.exists(dst):
        log_msg('File will be overwritten: \n' + dst)

    shutil.copyfile(src, dst)


def prepare_files(src_arc_paths, xlsx_template_path):
    verify_file_exists(xlsx_template_path)

    out_dir = os.path.commonpath(src_arc_paths)
    _, xls_ext = os.path.splitext(xlsx_template_path)
    out_fname = 'Imported_' + time.strftime("%Y.%m.%d %H-%M") + xls_ext

    tgt_xlsx_path = os.path.join(out_dir, out_fname)
    try:
        copy_file_override(xlsx_template_path, tgt_xlsx_path)
    except PermissionError:
        err_exit('Close Excel before running script')

    verify_file_exists(tgt_xlsx_path)
    return tgt_xlsx_path


def extract_arc_data(src_arc_path):
    eq_data = extract_arcive_files(src_arc_path, EXTRACT_ARC_EXT)

    modify_guide_dfs = {}
    for fname, fbytes in eq_data.items():
        try:
            text = str(fbytes, "utf-8")
            df_header, df_data = jap_text_to_tables(text)
            earthquake_date = df_header.loc[df_header[0] == HEADER_DATE].values[0, 1]
            modify_guide_dfs[fname] = df_header, df_data, earthquake_date
        except ValueError:
            err_exit(str(ValueError) + fname)

    return modify_guide_dfs


def jap_arcs_to_xlsx(src_arc_paths, xlsx_template_path, slowdown_import):
    tgt_xlsx_path = prepare_files(src_arc_paths, xlsx_template_path)

    arc_data = {}
    for path in src_arc_paths:
        log_msg('Processing archive  ' + path)
        arc_data[path] = extract_arc_data(path)

    log_msg('Writing table to ' + tgt_xlsx_path)
    modify_excel_shreadsheet(tgt_xlsx_path, arc_data)
    return tgt_xlsx_path
