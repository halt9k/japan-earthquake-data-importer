from datetime import datetime

import pandas as pd

from src.pandas_utils import dataframe_from_text, insert_row

HEADER_SCALE = 'Scale Factor'
HEADER_SCALE_VAL = HEADER_SCALE + ' Val'
HEADER_DATE = 'Origin Time'
HEADER_SPLIT_INDENT = 17
HEADER_END = 'Memo.'

HEADER_FORMAT = {
    'Origin Time': datetime,
    'Lat.': float,
    'Long.': float,
    'Depth. (km)': int,
    'Mag.': float,
    'Station Code': str,
    'Station Lat.': float,
    'Station Long.': float,
    'Station Height(m)': int,
    'Record Time': datetime,
    'Sampling Freq(Hz)': str,
    'Duration Time(s)': int,
    'Dir.': int,
    'Scale Factor': str,
    'Max. Acc. (gal)': float,
    'Last Correction': datetime,
    'Memo.': str
}


def separate_header_and_data(text):
    header_word_pos = text.find(HEADER_END)
    if header_word_pos < 1:
        raise ValueError('No header end found ')

    header_end = text.find('\n', header_word_pos)
    header_text = text[: header_end]
    table_text = text[header_end:]
    return header_text, table_text


def fix_header_values(df_header):
    type_table = pd.DataFrame([HEADER_FORMAT.keys(), HEADER_FORMAT.values()]).T

    numbers_mask = type_table[1].isin([int, float])
    df_header.loc[numbers_mask, 1] = df_header.loc[numbers_mask, 1].apply(pd.to_numeric)

    mask = type_table[1].isin([datetime])
    df_header.loc[mask, 1] = df_header.loc[mask, 1].apply(lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M:%S'))

    spec_row_1 = df_header.loc[df_header[0] == HEADER_SCALE]
    vals = spec_row_1.values[0, 1].split('(gal)/')

    spec_row_1.iat[0, 0] = HEADER_SCALE_VAL
    spec_row_1.iat[0, 1] = int(vals[0]) / int(vals[1])

    # df_header.loc[len(df_header)] = spec_row_1
    # pd.concat([spec_row_1, df_header])
    return insert_row(df_header, spec_row_1, spec_row_1.index[0] + 1)


def process_header(header_text):
    df_header = dataframe_from_text(header_text)
    if (df_header[0].str[HEADER_SPLIT_INDENT] != ' ').any():
        raise ValueError('Cannot split header ')

    tmp = df_header[0]
    df_header[0] = tmp.str[:HEADER_SPLIT_INDENT].str.strip()
    df_header[1] = tmp.str[HEADER_SPLIT_INDENT:].str.strip()

    df_header = fix_header_values(df_header)

    # add empty row
    # df_header.loc[len(df_header)] = pd.NA

    return df_header


def process_data_table(table_text):
    df = dataframe_from_text(table_text, split_by_spaces=True)

    if df.shape[1] != 8:
        raise ValueError('Not 8 columns in text files ')

    flattened_row = df.to_numpy().flatten(order='C')
    df_column = pd.DataFrame(flattened_row)

    return df_column


def jap_text_to_tables(text):
    header_text, table_text = separate_header_and_data(text)
    df_header = process_header(header_text)
    df_column = process_data_table(table_text)

    # named_column = pd.DataFrame(flattened_row, columns=[df_header.columns[0]])
    # pd.concat([df_header, named_column], axis=0, ignore_index=True)

    return df_header, df_column
