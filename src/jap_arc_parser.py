import os

import shutil

from src.errors import err_exit, log_msg
from src.jap_txt_parser import jap_text_to_tables
from src.tar_extract import extract_arcive_files
from xls_writer import modify_excel_shreadsheet

EXTRACT_ARC_EXT = ['.EW1', '.EW2', '.NS1', '.NS2', '.UD1', '.UD2']


# from importlib import reload
# import data_processing
# reload(data_processing)


def verify_file_exists(path):
    if not os.path.exists(path):
        err_exit('Expected file missing: \n' + path)


def copy_file_override(src, dst):
    if os.path.exists(dst):
        log_msg('File will be overwritten: \n' + dst)

    shutil.copyfile(src, dst)


def prepare_files(src_arc_path, xlsx_template_path):
    verify_file_exists(src_arc_path)
    verify_file_exists(xlsx_template_path)

    name, ext = os.path.splitext(src_arc_path)
    _, xls_ext = os.path.splitext(xlsx_template_path)
    tgt_xlsx_path = name + '_imported' + xls_ext
    copy_file_override(xlsx_template_path, tgt_xlsx_path)

    verify_file_exists(tgt_xlsx_path)
    return tgt_xlsx_path


def jap_arc_to_xlsx(src_arc_path, xlsx_template_path):
    tgt_xlsx_path = prepare_files(src_arc_path, xlsx_template_path)

    log_msg('Processing archive \n' + os.path.abspath(src_arc_path) + '\nto \n' + tgt_xlsx_path)
    eq_data = extract_arcive_files(src_arc_path, EXTRACT_ARC_EXT)

    eq_pd_tables = {}
    for time_key, file_bytes in eq_data.items():
        try:
            text = str(file_bytes, "utf-8")
            eq_pd_tables[time_key] = jap_text_to_tables(text)
        except ValueError:
            err_exit(str(ValueError) + time_key)

    modify_excel_shreadsheet(tgt_xlsx_path, eq_pd_tables)

    return tgt_xlsx_path


