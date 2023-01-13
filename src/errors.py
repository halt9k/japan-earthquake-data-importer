# edit and continue
# from importlib import reload
# import data_processing
# reload(data_processing)

import sys


def print_clear(msg, is_err):
    if is_err or '\n' in msg:
        if not msg.startswith('\n'):
            msg = '\n' + msg
        if not msg.endswith('\n'):
            msg = msg + '\n'

    print(msg)


def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


def err_exit(err_msg):
    print_clear(err_msg, is_err=True)
    if debugger_is_active():
        raise


def log_msg(msg: str):
    print_clear(msg, is_err=False)