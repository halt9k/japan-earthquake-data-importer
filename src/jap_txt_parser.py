import pandas as pd

from src.pandas_utils import dataframe_from_text

HEADER_END = 'Memo.'
HEADER_SPLIT_INDENT = 17


def separate_header_and_data(text):
    header_word_pos = text.find(HEADER_END)
    if header_word_pos < 1:
        raise ValueError('No header end found ')

    header_end = text.find('\n', header_word_pos)
    header_text = text[: header_end]
    table_text = text[header_end:]
    return header_text, table_text


def jap_text_to_tables(text):
    header_text, table_text = separate_header_and_data(text)

    df_header = dataframe_from_text(header_text)
    if (df_header[0].str[HEADER_SPLIT_INDENT] != ' ').any():
        raise ValueError('Cannot split header ')
    df_header[1] = df_header[0].str[:HEADER_SPLIT_INDENT]
    df_header[2] = df_header[0].str[HEADER_SPLIT_INDENT:]
    df_header = df_header.drop(0, axis=1)

    # add empty row
    # df_header.loc[len(df_header)] = pd.NA

    df = dataframe_from_text(table_text, split_by_spaces=True)

    if df.shape[1] != 8:
        raise ValueError('Not 8 columns in text files ')
    flattened_row = df.to_numpy().flatten(order='C')
    df_column = pd.DataFrame(flattened_row)

    # named_column = pd.DataFrame(flattened_row, columns=[df_header.columns[0]])
    # pd.concat([df_header, named_column], axis=0, ignore_index=True)

    return df_header, df_column
