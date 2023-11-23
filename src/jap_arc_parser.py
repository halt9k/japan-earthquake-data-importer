import os
from pathlib import Path

import shutil
import time
from unittest.mock import inplace

import pandas as pd

from config import APP
from errors import err_exit, log_msg
from jap_txt_parser import jap_text_to_tables, HEADER_DATE, VAL_EXPECTED_SAME_FOR_SITE, \
    VAL_EXPECTED_SAME_ON_SEISMOGRAPH, VAL_EXPECTED_DIFFERENT
from tar_extract import extract_arcive_files
from xls_writer import modify_excel_shreadsheet

STANDARD = ['.EW', '.NS', '.UD']
LOW_SM = ['.EW1', '.NS1', '.UD1']
HIGH_SM = ['.EW2', '.NS2', '.UD2']
EXTRACT_ARC_EXT = STANDARD + LOW_SM + HIGH_SM


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


def extract_arc_data(src_arc_path, headers_only=False):
    eq_data = extract_arcive_files(src_arc_path, EXTRACT_ARC_EXT)

    modify_guide_dfs = {}
    for fname, fbytes in eq_data.items():
        try:
            text = str(fbytes, "utf-8")
            df_header, df_data = jap_text_to_tables(text, headers_only)
            earthquake_date = df_header.loc[df_header[0] == HEADER_DATE].values[0, 1]
            modify_guide_dfs[fname] = df_header, df_data, earthquake_date
        except ValueError:
            err_exit(str(ValueError) + fname)

    return modify_guide_dfs


# TODO
def ensure_headers_integrity(df_expected, df_parsed):
    if df_expected is None:
        return df_parsed

    if not df_expected.eq(df_parsed).all():
        err_msg = str(df_expected) + ' \n ' + str(df_parsed)
        err_exit('Unexpected data difference of values for same site:\n' + err_msg)

    return df_expected


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
        expected_same_for_sites = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_FOR_SITE)
        expected_same_for_heights = filter_header(ext, df_header, src_column, VAL_EXPECTED_SAME_ON_SEISMOGRAPH)
        update_data = filter_header(ext, df_header, src_column,
                                    VAL_EXPECTED_SAME_ON_SEISMOGRAPH + VAL_EXPECTED_DIFFERENT)

        # TODO extract integrity chack better
        if site_data_column is None:
            site_data_column = expected_same_for_sites
        common_data = ensure_headers_integrity(common_data, expected_same_for_sites)

        if ext.endswith('1'):
            common_low_data = ensure_headers_integrity(common_low_data, expected_same_for_heights)
        elif ext.endswith('2'):
            common_high_data = ensure_headers_integrity(common_high_data, expected_same_for_heights)
        else:
            assert False

        if col_names_mode:
            update_data += ext

        site_data_column = pd.concat((site_data_column, update_data))
    return site_data_column


def reorder_headers(df_aggregated, config):
    correct_order = APP.get_list(APP.config(), 'Excel import', 'header_final_order')
    # correct_order = ['Origin Time', 'Long.', 'Lat.', 'Station Height(m).EW1']

    if len(correct_order) < 1:
        return df_aggregated

    filter_mask = df_aggregated[0].isin(correct_order)
    skipped_rows = str(list(df_aggregated[0][~filter_mask]))
    log_msg('Skipping header data since it\'s not requred by configuration file entry: ' + skipped_rows)

    df_filtered = df_aggregated[filter_mask]
    if len(correct_order) != len(df_filtered):
        err_exit('Possibly incorrect header column names in configuration file. Total columns after reorder does not match expected count.')

    return df_filtered


def aggregate_headers(arc_data, config):
    df_aggregated = None

    for fname, eq_table in arc_data.items():
        if df_aggregated is None:
            col_names_row = aggregate_site_headers(eq_table, col_names_mode=True)
            df_aggregated = col_names_row

        eq_site_row = aggregate_site_headers(eq_table)
        df_aggregated = pd.concat((df_aggregated, eq_site_row), axis=1)
    df_aggregated.reset_index(drop=True, inplace=True)

    return reorder_headers(df_aggregated, config)


def jap_arcs_to_xlsx(src_arc_paths, xlsx_template_path, headers_only, config):
    tgt_xlsx_path = prepare_files(src_arc_paths, xlsx_template_path)

    arc_data = {}
    for path in src_arc_paths:
        log_msg('Processing archive  ' + path)
        arc_data[path] = extract_arc_data(path, headers_only=headers_only)

    # TODO not parsing op
    if headers_only:
        arc_data = aggregate_headers(arc_data, config).T

    log_msg('Writing table to ' + tgt_xlsx_path)
    modify_excel_shreadsheet(tgt_xlsx_path, arc_data, single_page_mode=headers_only)
    return tgt_xlsx_path
