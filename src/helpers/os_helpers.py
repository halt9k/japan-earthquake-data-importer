from os import chdir
from pathlib import Path
from sys import path

"""
 This module is intended to be imported before all other src/* modules
 allows to keep sources organized with working dir . as root:
 ./README.md
 ./<main launch files>
 ./src/*.py
 ./data/*

 Import without warning:
 from helpers import os_helpers  # noqa: F401
"""


def ch_project_root_dir():
    this_file_path = Path(__file__).parent
    assert (this_file_path.name == 'helpers')

    new_working_dir = str(this_file_path.parent.parent)

    chdir(new_working_dir)
    # nessesary for imports
    path.append(new_working_dir)

    print(f'Working path is changed to {new_working_dir} \n')


ch_project_root_dir()
