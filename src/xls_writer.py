import os

import pandas as pd
import xlwings as xw

from errors import log_msg

IMPORT_XLS_ANCHOR_HEADER = "IMPORT_HEADER_"
IMPORT_XLS_ANCHOR_DATA = "IMPORT_DATA_"


def write_table_under_xls_ancor(sheet, anchor, table: pd.DataFrame):
    # df = sheet.Range(anchor).table.value
    # target_df = xw.Range('A7').options(pd.DataFrame, expand='table').value
    # df = pd.DataFrame(df)  # into Pandas DataFrame
    # df['sum'] = df.sum(axis=1)

    rng = None
    try:
        rng = xw.Range(anchor)
        print(rng.count)
    except:
        log_msg('ERROR: Failed to find ancor ' + anchor)
        raise

    try:
        rng.options(index=False, header=False).value = table
    except:
        log_msg('ERROR: Failure while import under anchor ' + anchor)
        raise


def modify_excel_shreadsheet(fname, eq_tables):
    log_msg('Writing xlsx from archive files \n' + str(eq_tables.keys()))

    # writer = pd.ExcelWriter(path=fname, engine='xlsxwriter')
    # for arc_fname, df in eq_tables.items():
    #    df.to_excel(writer, sheet_name=arc_fname, index=False)
    # writer.close()

    workbook = xw.Book(fname)
    try:
        sht = workbook.sheets[0]
        for arc_fname, data_frames in eq_tables.items():
            ext = os.path.splitext(arc_fname)[1]
            ext = ext.split('.')[1]
            write_table_under_xls_ancor(sht, IMPORT_XLS_ANCHOR_HEADER + ext, data_frames[0])
            write_table_under_xls_ancor(sht, IMPORT_XLS_ANCHOR_DATA + ext, data_frames[1])
        workbook.save()
    finally:
        app = xw.apps.active
        # workbook.close()
        app.quit()