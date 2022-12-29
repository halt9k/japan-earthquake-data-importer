
def print_clear(msg):
    if '\n' in msg:
        if not msg.startswith('\n'):
            msg = '\n' + msg
        if not msg.endswith('\n'):
            msg = msg + '\n'

    print(msg)


def err_exit(err_msg):
    print_clear(err_msg)
    raise


def log_msg(msg: str):
    print_clear(msg)