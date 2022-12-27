import os

import pandas as pd

from src.errors import err_exit, log_msg
from src.jap_txt_parser import jap_text_to_tables
from src.tar_extract import extract_arcive_files

EXTRACT_ARC_EXT = ['.EW1', '.EW2', '.NS1', '.NS2', '.UD1', '.UD2']


# from importlib import reload
# import data_processing
# reload(data_processing)


def split_line_at_pos(line, pos):
    assert (line[pos] == ' ')
    return [line[0: pos], line[pos + 1: -1]]


def create_excel_shreadsheet(fname, eq_tables):
    log_msg('Writing xlsx from archive files ' + str(eq_tables.keys()))
    writer = pd.ExcelWriter(path=fname, engine='xlsxwriter')

    for arc_fname, df in eq_tables.items():
        df.to_excel(writer, sheet_name=arc_fname, index=False)

    writer.close()


def jap_arc_to_xlsx(arc_path):
    log_msg('Processing archive ' + os.path.abspath(arc_path))
    eq_data = extract_arcive_files(arc_path, EXTRACT_ARC_EXT)

    eq_pd_tables = {}
    for time_key, file_bytes in eq_data.items():
        try:
            eq_pd_tables[time_key] = jap_text_to_tables(file_bytes)
        except ValueError:
            err_exit(str(ValueError) + time_key)

    arc_fname = os.path.splitext(arc_path)[0] + '.xlsx'
    arc_full_fname = os.path.abspath(arc_fname)
    create_excel_shreadsheet(arc_full_fname, eq_pd_tables)

    return arc_full_fname


