import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from contextlib import contextmanager

from config import APP
from main import main, process_dir, CONFIG_FILE
from xls_writer import get_value, get_sheet_count


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


def os_view_path_patched(_):
    return


def err_exit_patched(self, err_msg):
    raise Exception(err_msg)


# @pytest.mark.usefixtures('use_fixture_path')
@patch('main.os_view_path', os_view_path_patched)
@patch('xls_writer.err_exit', err_exit_patched)
class Test:
    @pytest.mark.parametrize('src_path', [Path('./test_main_fixtures/basic')])
    def test_full_basic(self, use_fixture_path, src_path):
        val = get_value('./data/Template_empty.xlsx', sheet_n='0', xls_range='H18')
        assert (val == '3920(gal)/6170801')

        main()
        new_file = list(Path().glob('./data/Imported_*.xlsx'))[0]
        val = get_value(new_file, sheet_n='2012.11.17_1713', xls_range='H18')
        assert(val == '2940(gal)/6170270')

    @pytest.mark.parametrize('src_path', [Path('./test_main_fixtures/empty_xls')])
    def test_full_empty_xls(self, use_fixture_path, src_path):
        main()
        new_file = list(Path().glob('Imported_*.xlsx'))[0]
        val = get_value(new_file, sheet_n='2012.11.17_1713', xls_range='P7105')
        assert(val == -30638.0)

    @pytest.mark.parametrize('src_path', [Path('./test_main_fixtures/batch')])
    def test_full_batch(self, use_fixture_path, src_path):
        input_arcs = list(Path().glob('./batch/*.tar.gz'))
        main()
        new_file = list(Path().glob('./batch/Imported_*.xlsx'))[0]
        assert(get_sheet_count(new_file) == len(input_arcs) > 0)

    @pytest.mark.parametrize('src_path', [Path('./test_main_fixtures/broken_xls')])
    def test_full_broken_xls(self, use_fixture_path, src_path):
        with pytest.raises(Exception):
            main()

    @pytest.mark.parametrize('src_path', [Path('./test_main_fixtures/empty_xls')])
    def test_control_historgams(self, use_fixture_path, src_path):
        APP.read_config(CONFIG_FILE)
        APP.config()['UX']['create_control_histograms'] = True
        process_dir()
