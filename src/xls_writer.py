import os

import pandas as pd
import xlwings as xw

from config import App
from errors import log_msg, err_exit, debugger_is_active

IMPORT_XLS_ANCHOR_HEADER = "IMPORT_HEADER_"
IMPORT_XLS_ANCHOR_DATA = "IMPORT_DATA_"


def write_table_under_xls_ancor(sheet, anchor, table: pd.DataFrame):
    # df = sheet.Range(anchor).table.value
    # target_df = xw.Range('A7').options(pd.DataFrame, expand='table').value
    # df = pd.DataFrame(df)  # into Pandas DataFrame
    # df['sum'] = df.sum(axis=1)

    rng = None
    try:
        sheet.activate()

        # table dims without index
        sx, sy = table.shape[0] - 1, table.shape[1] - 1

        range_top_left = xw.Range(anchor).offset(row_offset=1)
        range_bottom_right = range_top_left.offset(sx, sy)
        rng = xw.Range(range_top_left, range_bottom_right)
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


def import_to_sheet(sheet, eq_tables):
    eq_date = None

    for arc_fname, (df_header, df_data, earthquake_date) in eq_tables.items():
        ext = os.path.splitext(arc_fname)[1].removeprefix('.')
        write_table_under_xls_ancor(sheet, IMPORT_XLS_ANCHOR_HEADER + ext, df_header)
        write_table_under_xls_ancor(sheet, IMPORT_XLS_ANCHOR_DATA + ext, df_data)
        if eq_date:
            assert (eq_date == earthquake_date)
        else:
            eq_date = earthquake_date
    return eq_date


def get_workbook(fname):
    try:
        return xw.Book(fname)
    except:
        err_exit('Unexpected result during Excel initizlization. Ensure Excel 2013+ is installed.')


def modify_excel_shreadsheet(fname, arcives_data):
    log_msg('Writing xlsx from archive files \n')

    # writer = pd.ExcelWriter(path=fname, engine='xlsxwriter')
    # for arc_fname, df in eq_tables.items():
    #    df.to_excel(writer, sheet_name=arc_fname, index=False)
    # writer.close()

    slowdown_import = App.config()['UX'].getboolean('slow_paced_import')

    workbook = get_workbook(fname)
    try:
        if not slowdown_import:
            xw.apps.active.screen_updating = False

        template_sheet = xw.Sheet(workbook.sheets[0])
        for eq_tables in arcives_data.values():
            import_sheet = template_sheet.copy(after=template_sheet)
            eq_date = import_to_sheet(import_sheet, eq_tables)
            import_sheet.name = eq_date.strftime('%Y.%m.%d_%H%M')

        template_sheet.delete()
        workbook.save()
    finally:
        xw.apps.active.screen_updating = True
        app = xw.apps.active
        # workbook.close()
        if debugger_is_active():
            app.quit()