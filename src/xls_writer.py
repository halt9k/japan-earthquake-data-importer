import os

import pandas as pd
import xlwings as xw

from config import APP
from errors import log_msg, err_exit
from xls_context import open_excel

IMPORT_XLS_ANCHOR_HEADERS = "IMPORT_HEADERS"
IMPORT_XLS_ANCHOR_HEADER = "IMPORT_HEADER_"
IMPORT_XLS_ANCHOR_DATA = "IMPORT_DATA_"


def write_table_under_anchor(sheet, anchor, table: pd.DataFrame):
    # df = sheet.range(anchor).table.value
    # target_df = sheet.range('A7').options(pd.DataFrame, expand='table').value
    # df = pd.DataFrame(df)  # into Pandas DataFrame
    # df['sum'] = df.sum(axis=1)

    rng = None
    try:
        sheet.activate()

        # table dims without index
        sx, sy = table.shape[0] - 1, table.shape[1] - 1
        # TODO verify works in both modes

        # useful in row append mode
        # range_top_left = sheet.range(anchor).expand().rows(0).offset(row_offset=1)

        range_top_left = sheet.range(anchor).offset(row_offset=1)
        range_bottom_right = range_top_left.offset(sx, sy)
        rng = sheet.range(range_top_left, range_bottom_right)
        if not rng.number_format:
            err_exit('Data format in xlsx template must be all general, incorrect cell in ' + rng.address)

    except ValueError:
        log_msg('ERROR: Failed to find anchor ' + anchor)
        raise

    try:
        rng.options(pd.DataFrame, index=False, header=False).value = table
    except ValueError:
        log_msg('ERROR: Failure while writing below anchor ' + anchor)
        raise


def import_to_sheet(sheet, eq_table):
    write_table_under_anchor(sheet, IMPORT_XLS_ANCHOR_HEADERS, eq_table)


# TODO verify works in both modes
def import_to_sheets(sheet, eq_tables):
    eq_date = None

    for arc_fname, (df_header, df_data, earthquake_date) in eq_tables.items():
        ext = os.path.splitext(arc_fname)[1].removeprefix('.')
        write_table_under_anchor(sheet, IMPORT_XLS_ANCHOR_HEADER + ext, df_header)
        write_table_under_anchor(sheet, IMPORT_XLS_ANCHOR_DATA + ext, df_data)
        if eq_date:
            assert (eq_date == earthquake_date)
        else:
            eq_date = earthquake_date
    return eq_date


def modify_excel_shreadsheet(fpath, arcives_data, single_page_mode):
    log_msg('Writing xlsx from archive files \n')

    # writer = pd.ExcelWriter(path=fname, engine='xlsxwriter')
    # for arc_fname, df in eq_tables.items():
    #    df.to_excel(writer, sheet_name=arc_fname, index=False)
    # writer.close()

    slowdown_import = APP.config()['UX'].getboolean('slow_paced_import')
    with open_excel(fpath, slowdown_import) as wb:
        if single_page_mode:
            sheet = xw.Sheet(wb.sheets[0])
            # TODO
            # for eq_tables in arcives_data.values():
            import_to_sheet(sheet, arcives_data)
            if wb.app.visible:
                sheet.activate()
        else:
            template_sheet = xw.Sheet(wb.sheets[0])
            for eq_tables in arcives_data.values():
                sheet = template_sheet.copy(after=template_sheet)
                eq_date = import_to_sheets(sheet, eq_tables)
                sheet.name = eq_date.strftime('%Y.%m.%d_%H%M')

                if wb.app.visible:
                    sheet.activate()

            template_sheet.delete()

        wb.save()
