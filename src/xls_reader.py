# TODO this is supposed to be different library
# which reads files directly instead of executing Excel
# current approach is less reliable for tests and more buggy, though simpler
import xlwings as xw

from errors import debugger_is_active
from xls_context import open_excel


def get_value(fpath, sheet_n, xls_range):
    with open_excel(fpath, debugger_is_active()) as wb:
        sheet = xw.Sheet(wb.sheets[sheet_n])
        return sheet.range(xls_range).value


def get_sheet_count(fpath):
    with open_excel(fpath, debugger_is_active()) as (app, wb):
        return wb.sheets.count
