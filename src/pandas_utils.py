from io import StringIO

import pandas as pd


def dataframe_from_text(text, split_by_spaces=False):
    stream = StringIO(text)
    if split_by_spaces:
        return pd.read_csv(stream, header=None, delimiter=r"\s+")
    else:
        return pd.read_csv(stream, header=None)


def insert_row(df, new_row, idx):
    df_a = df.iloc[:idx, ]
    df_b = df.iloc[idx:, ]

    return pd.concat([df_a, new_row, df_b]).reset_index(drop=True)
