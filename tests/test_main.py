import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from contextlib import contextmanager

from main import main
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
        val = get_value('./data/Template_empty.xlsx', sheet_n='0', xls_range='H19')
        assert (abs(val - 0.000476478) < 0.01)

        main()
        new_file = list(Path().glob('./data/Imported_*.xlsx'))[0]
        val = get_value(new_file, sheet_n='2012.11.17_1713', xls_range='H19')
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

    # TODO extract scenario into dev
    @pytest.mark.parametrize('src_path', [Path('./test_import_headers_experiment')])
    def test_batch_headers(self, use_fixture_path, src_path):
        main()
        new_file = list(Path().glob('./data/sites/IBRH17/Imported_*.xlsx'))[0]
        assert(get_sheet_count(new_file) == 1)

    @pytest.mark.parametrize('src_path', [Path('./test_import_headers_experiment_data_fail')])
    def test_batch_headers_inconsistent_data(self, use_fixture_path, src_path):
        main()
        new_file = list(Path().glob('./data/sites/IBRH17/Imported_*.xlsx'))[0]
        assert(get_sheet_count(new_file) == 1)
