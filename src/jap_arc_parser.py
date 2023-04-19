import os
from pathlib import Path

import shutil
import time

import pandas as pd

from errors import err_exit, log_msg
from jap_txt_parser import jap_text_to_tables, HEADER_DATE, VAL_EXPECTED_SAME_FOR_SITE, \
    VAL_EXPECTED_SAME_ON_SEISMOGRAPH, VAL_EXPECTED_DIFFERENT
from tar_extract import extract_arcive_files
from xls_writer import modify_excel_shreadsheet

LOW_SM = ['.EW1', '.NS1', '.UD1']
HIGH_SM = ['.EW2', '.NS2', '.UD2']
EXTRACT_ARC_EXT = LOW_SM + HIGH_SM


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
    if not os.path.isdir(out_dir):
        out_dir = os.path.dirname(out_dir)

    _, xls_ext = os.path.splitext(xlsx_template_path)
    out_fname = 'Imported_' + time.strftime("%Y.%m.%d %H-%M") + xls_ext

    tgt_xlsx_path = os.path.join(out_dir, out_fname)
    try:
        copy_file_override(xlsx_template_path, tgt_xlsx_path)
    except PermissionError:
        err_exit('Close Excel before running script')

    verify_file_exists(tgt_xlsx_path)
    return tgt_xlsx_path


def extract_arc_data(src_arc_path, skip_data=False):
    eq_data = extract_arcive_files(src_arc_path, EXTRACT_ARC_EXT)

    modify_guide_dfs = {}
    for fname, fbytes in eq_data.items():
        try:
            text = str(fbytes, "utf-8")
            df_header, df_data = jap_text_to_tables(text, skip_data)
            earthquake_date = df_header.loc[df_header[0] == HEADER_DATE].values[0, 1]
            modify_guide_dfs[fname] = df_header, df_data, earthquake_date
        except ValueError:
            err_exit(str(ValueError) + fname)

    return modify_guide_dfs


# TODO
def ensure_headers_integrity(df_expected, df_parsed):
    if not df_expected.eq(df_parsed).all():
        err_msg = str(df_expected) + ' \n ' + str(df_parsed)
        err_exit('Unexpected data difference of values for same site:\n' + err_msg)


def filter_header(ext, df_header, src_column, column_set):
    mask = df_header[0].isin(column_set)

    # TODO
    # ensure_integrity(df_header, df_aggregated)
    # df_header[df_header[0] == 'Dir.'].iloc[0, 1]

    return df_header[src_column].loc[mask]


def aggregate_site_headers(eq_table, col_names_mode=False):
    site_data_column = None
    common_data, common_low_data, common_high_data = None, None, None

    for arc_fname, (df_header, _, earthquake_date) in eq_table.items():
        ext = Path(arc_fname).suffix

        src_column = 1 if not col_names_mode else 0
        if common_data is None:
            common_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_FOR_SITE)
            site_data_column = common_data
        else:
            cur_common_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_FOR_SITE)
            ensure_headers_integrity(common_data, cur_common_data)

        if ext.endswith('1'):
            if common_low_data is None:
                common_low_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_ON_SEISMOGRAPH)
            else:
                cur_low_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_ON_SEISMOGRAPH)
                ensure_headers_integrity(common_low_data, cur_low_data)

        if ext.endswith('2'):
            if common_high_data is None:
                common_high_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_ON_SEISMOGRAPH)
            else:
                cur_high_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_ON_SEISMOGRAPH)
                ensure_headers_integrity(common_high_data, cur_high_data)

        update_data = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_ON_SEISMOGRAPH + VAL_EXPECTED_DIFFERENT)
        if col_names_mode:
            update_data += ext

        site_data_column = pd.concat((site_data_column, update_data))
    return site_data_column


def aggregate_headers(arc_data):
    df_aggregated = None

    for fname, eq_table in arc_data.items():
        if df_aggregated is None:
            col_names_row = aggregate_site_headers(eq_table, col_names_mode=True)
            df_aggregated = col_names_row

        eq_site_row = aggregate_site_headers(eq_table)
        df_aggregated = pd.concat((df_aggregated, eq_site_row), axis=1)

    return df_aggregated


def jap_arcs_to_xlsx(src_arc_paths, xlsx_template_path, skip_data):
    tgt_xlsx_path = prepare_files(src_arc_paths, xlsx_template_path)

    arc_data = {}
    for path in src_arc_paths:
        log_msg('Processing archive  ' + path)
        arc_data[path] = extract_arc_data(path, skip_data=skip_data)

    # TODO not parsing op
    if skip_data:
        arc_data = aggregate_headers(arc_data).T

    log_msg('Writing table to ' + tgt_xlsx_path)
    modify_excel_shreadsheet(tgt_xlsx_path, arc_data, single_page_mode=skip_data)
    return tgt_xlsx_path
