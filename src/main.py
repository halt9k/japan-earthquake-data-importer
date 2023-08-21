import csv
import glob
from pathlib import Path

import regex
import pandas as pd
import win32com.client as win32
from xlsxwriter import Workbook


def get_archives(arc_path):
    arc_paths = glob.glob(arc_path, recursive=True)

    return arc_paths


def get_containing_word(words, text):
    matches = [x for x in words if x in text]
    assert (len(matches) == 1)
    return matches[0]


def add_year(path):
    parent_dirs = ['Logger', 'Ground', 'Eddy']
    match = get_containing_word(parent_dirs, path)
    regex_match = match + '\\\\((19|20)\\d{2})'

    re_match = regex.search(regex_match, path)
    assert (re_match)
    year = re_match[1]

    old_path = Path(path)
    new_name = year + '_' + old_path.name
    new_path = old_path.parent.joinpath(new_name)

    return str(new_path)


def convert_xls_to_xlsx(xls_path, xlsx_path):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(xls_path)

    # FileFormat = 51 is for .xlsx extension
    # FileFormat = 56 is for .xls extension
    wb.SaveAs(xlsx_path, FileFormat=51)

    wb.Close()
    excel.Application.Quit()


def convert_csv_to_xlsx(csv_path, xlsx_path):
    workbook = Workbook(xlsx_path, {'strings_to_numbers': True, 'constant_memory': True})
    worksheet = workbook.add_worksheet()
    with open(csv_path, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()


def main():
    xls_files = get_archives('**/*.xls')
    csv_files = get_archives('**/*.csv')

    src_files = xls_files + csv_files
    conversion_errors = []

    for i, src_rel_file in enumerate(src_files):
        path = Path(src_rel_file)
        fixed_path = Path(path.parent).joinpath(path.name.lower())

        ext = fixed_path.suffix
        src_file = str(fixed_path.absolute())

        match = get_containing_word(['.xls', '.csv'], src_file)
        out_name = add_year(src_file).replace(match, '.xlsx')

        if Path(out_name).exists():
            print('Already converted, skipping: ' + src_file + ' -> ' + str(out_name))
            continue

        try:
            if match == '.xls':
                convert_xls_to_xlsx(src_file, out_name)
            elif match == '.csv':
                convert_csv_to_xlsx(src_file, out_name)
            else:
                assert False
        except:
            conversion_errors += [src_file]
            continue

        print('Done: {0} of {1}  {2} -> {3} '.format(i, len(src_files), src_file, out_name))

    if len(conversion_errors) > 0:
        print('\n ERRORS HAPPENED ON FILES: \n' + '\n'.join(conversion_errors))


if __name__ == '__main__':
    main()
