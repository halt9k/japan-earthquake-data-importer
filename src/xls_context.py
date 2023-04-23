import xlwings as xw

from errors import err_exit, debugger_is_active
from contextlib import contextmanager


def begin_excel(fpath, slowdown_import):
    wb = xw.Book(fpath)
    if not slowdown_import:
        wb.app.screen_updating = False
    return wb


def end_excel(wb):
    wb.app.screen_updating = True
    if debugger_is_active():
        wb.close()


@contextmanager
def open_excel(fpath, show_window):
    """
    @param fpath: path to file
    @param show_window: mostly debug use, introduces dramatic slowdown
    """

    try:
        wb = None
        # no point hiding background process
        # context creates buggy empty App, finally approach is better
        # with xw.App(add_book=False) as app:
        try:
            wb = begin_excel(fpath, show_window)
            yield wb
        finally:
            end_excel(wb)
    except:
        err_exit('Unexpected result during Excel initizlization. Ensure Excel 2013+ is installed.')
