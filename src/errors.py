
def print_clear(msg, is_err):
    if is_err or '\n' in msg:
        if not msg.startswith('\n'):
            msg = '\n' + msg
        if not msg.endswith('\n'):
            msg = msg + '\n'

    print(msg)


def err_exit(err_msg):
    print_clear(err_msg, is_err=True)
    raise


def log_msg(msg: str):
    print_clear(msg, is_err=False)