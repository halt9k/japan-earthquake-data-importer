import os
import sys


src_path = os.path.dirname(__file__)
app_root_path = os.path.dirname(src_path)
sys.path.append(app_root_path)

if os.path.abspath(os.curdir) == src_path:
    os.chdir(app_root_path)
    print(f'Root path is set to {app_root_path}')
