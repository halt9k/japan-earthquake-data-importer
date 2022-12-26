import glob
import os
import pandas as pd
import sys
from io import BytesIO


from src.errors import err_exit
from src.tar_processing import extract_arcive_files

SOURCE_ARC_EXT = '*.gz'
EXTRACT_ARC_EXT = ['.EW1', '.EW2', '.NS1', '.NS2', '.UD1', '.UD2']
HEADER_END = 'Memo.'
HEADER_SPLIT_INDENT = 17
MAX_HEADER_SEARCH = 20

# from importlib import reload
# import src.data_processing
# reload(src.data_processing)


def split_line_at_pos(line, pos):
    assert (line[pos] == ' ')
    return [line[0: pos], line[pos + 1: -1]]


def process_text_files_to_tables(text):
    text_io = BytesIO(text)

    df_header = pd.DataFrame(columns=['A', 'B', 'C'])
    for n in range(MAX_HEADER_SEARCH):
        line = str(text_io.readline(), "utf-8")

        df_header.iloc[:, n] = [split_line_at_pos(line, HEADER_SPLIT_INDENT)]
        if str(line).startswith(HEADER_END):
            break

        if n == MAX_HEADER_SEARCH - 1:
            err_exit('Reached max header lines in text file, no header end')

    df = pd.read_csv(text_io, sep=" ")
    return pd.concat(df_header, df)


def create_excel_shreadsheet(eq_tables):

    return


def process_archive(arc_path):
    eq_data = extract_arcive_files(arc_path, EXTRACT_ARC_EXT)

    eq_pd_tables = {}
    for time_key in eq_data.keys():
        eq_pd_tables[time_key] = process_text_files_to_tables(eq_data[time_key])

    xls = create_excel_shreadsheet(eq_pd_tables)


def process_dir(config):
    working_path = config['Source files']['default_path']
    path_mask = os.path.join(working_path, SOURCE_ARC_EXT)
    arc_paths = glob.glob(path_mask)

    arcives_count = len(arc_paths)
    if not 4 <= arcives_count <= 6:
        err_exit('amount of earthquake arcives unexpected: ' + str(arcives_count))

    for arc_path in arc_paths:
        process_archive(arc_path)

    return
