import os
import shutil
from pathlib import Path

import pytest
from contextlib import contextmanager

from main import main


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


@pytest.mark.usefixtures('tmp_path')
@pytest.fixture
def use_fixture_path(tmp_path: Path, src_path: Path):
    assert(src_path.exists())

    shutil.copytree(src_path, tmp_path, dirs_exist_ok=True)
    print('Path before test',  Path().resolve())
    with cwd(tmp_path):
        print('Path during test', Path().resolve())
        yield tmp_path


# @pytest.mark.usefixtures('use_fixture_path')
class Test:
    @pytest.mark.parametrize('src_path', [Path('./test_main_fixtures/')])
    def test_process_dir(self, use_fixture_path, src_path):
        main()

        self.fail()
