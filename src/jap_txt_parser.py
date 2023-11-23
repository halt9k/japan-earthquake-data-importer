from datetime import datetime

import pandas as pd

from pandas_utils import dataframe_from_text, insert_row

HEADER_SCALE = 'Scale Factor'
HEADER_SCALE_VAL = HEADER_SCALE + ' Value'
HEADER_FREQ = 'Sampling Freq(Hz)'
HEADER_FREQ_VAL = HEADER_FREQ + ' Value'
HEADER_DATE = 'Origin Time'
HEADER_SEPARATOR_INDENT = 17
HEADER_END = 'Memo.'


# TODO ensure all works?
class ExpectedDuplications:
    # same for ['.EW1', '.NS1', '.UD1', '.EW2', '.NS2', '.UD2']
    SAME_FOR_GEO_SITE = 1
    # same for ['.EW1', '.NS1', '.UD1'] and ['.EW2', '.NS2', '.UD2']
    SAME_FOR_SEISMOGRAPH_DIRECTIONS = 2
    EXPECTED_ANY = 3


ED = ExpectedDuplications
HEADER_INFO = [
    [HEADER_DATE, datetime, ED.SAME_FOR_GEO_SITE],
    ['Lat.', float, ED.SAME_FOR_GEO_SITE],
    ['Long.', float, ED.SAME_FOR_GEO_SITE],
    ['Depth. (km)', int, ED.SAME_FOR_GEO_SITE],
    ['Mag.', float, ED.SAME_FOR_GEO_SITE],
    ['Station Code', str, ED.SAME_FOR_GEO_SITE],
    ['Station Lat.', float, ED.SAME_FOR_GEO_SITE],
    ['Station Long.', float, ED.SAME_FOR_GEO_SITE],
    # TODO 4 critical: brokes support of previous imports; check commit history
    ['Station Height(m)', int, ED.SAME_FOR_GEO_SITE],
    ['Record Time', datetime, ED.SAME_FOR_GEO_SITE],
    [HEADER_FREQ, str, ED.SAME_FOR_GEO_SITE],
    ['Duration Time(s)', int, ED.SAME_FOR_GEO_SITE],
    ['Dir.', str, ED.EXPECTED_ANY],
    [HEADER_SCALE, str, ED.SAME_FOR_GEO_SITE],
    ['Max. Acc. (gal)', float, ED.EXPECTED_ANY],
    ['Last Correction', datetime, ED.EXPECTED_ANY],
    [HEADER_END, str, ED.EXPECTED_ANY],
]
# Header is preprocessed during import, after preprocess:
HEADER_INFO_AP = HEADER_INFO + \
                 [[HEADER_SCALE_VAL, float, ED.SAME_FOR_SEISMOGRAPH_DIRECTIONS]] + \
                 [[HEADER_FREQ_VAL, float, ED.SAME_FOR_GEO_SITE]]
DF_HEADER_INFO = pd.DataFrame(HEADER_INFO)

# header info after preprocess
DF_HEADER_IAP = pd.DataFrame(HEADER_INFO_AP)
VAL_EXPECTED_SAME_FOR_SITE = list(DF_HEADER_IAP.loc[DF_HEADER_IAP[2] == ED.SAME_FOR_GEO_SITE, 0])
VAL_EXPECTED_SAME_ON_SEISMOGRAPH = list(DF_HEADER_IAP.loc[DF_HEADER_IAP[2] == ED.SAME_FOR_SEISMOGRAPH_DIRECTIONS, 0])
VAL_EXPECTED_DIFFERENT = list(DF_HEADER_IAP.loc[DF_HEADER_IAP[2] == ED.EXPECTED_ANY, 0])


def separate_header_and_data(text):
    header_word_pos = text.find(HEADER_END)
    if header_word_pos < 1:
        raise ValueError('No header end found ')

    header_end = text.find('\n', header_word_pos)
    header_text = text[: header_end]
    table_text = text[header_end:]
    return header_text, table_text


def fix_header_values(df_header):
    type_table = DF_HEADER_INFO.loc[:, 0:1]

    numbers_mask = type_table[1].isin([int, float])
    df_header.loc[numbers_mask, 1] = df_header.loc[numbers_mask, 1].apply(pd.to_numeric)

    mask = type_table[1].isin([datetime])
    df_header.loc[mask, 1] = df_header.loc[mask, 1].apply(lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M:%S'))

    spec_row_1 = df_header.loc[df_header[0] == HEADER_SCALE]
    assert('(gal)/' in spec_row_1.values[0, 1])
    vals = spec_row_1.values[0, 1].split('(gal)/')

    spec_row_1.iat[0, 0] = HEADER_SCALE_VAL
    spec_row_1.iat[0, 1] = int(vals[0]) / int(vals[1])

    # df_header.loc[len(df_header)] = spec_row_1
    # pd.concat([spec_row_1, df_header])

    df_header_processed = insert_row(df_header, spec_row_1, spec_row_1.index[0] + 1)

    spec_row_2 = df_header_processed.loc[df_header_processed[0] == HEADER_FREQ]
    assert ('Hz' in spec_row_2.values[0, 1])
    val = spec_row_2.values[0, 1].rstrip('Hz')

    spec_row_2.iat[0, 0] = HEADER_FREQ_VAL
    spec_row_2.iat[0, 1] = int(val)

    df_header_processed = insert_row(df_header_processed, spec_row_2, spec_row_2.index[0] + 1)

    return df_header_processed


def process_header(header_text):
    df_header = dataframe_from_text(header_text)
    if (df_header[0].str[HEADER_SEPARATOR_INDENT] != ' ').any():
        raise ValueError('Cannot split header ')

    tmp = df_header[0]
    df_header[0] = tmp.str[:HEADER_SEPARATOR_INDENT].str.strip()
    df_header[1] = tmp.str[HEADER_SEPARATOR_INDENT:].str.strip()

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


def jap_text_to_tables(text, skip_data):
    header_text, table_text = separate_header_and_data(text)
    df_header = process_header(header_text)
    df_column = process_data_table(table_text) if not skip_data else None

    # named_column = pd.DataFrame(flattened_row, columns=[df_header.columns[0]])
    # pd.concat([df_header, named_column], axis=0, ignore_index=True)

    return df_header, df_column
