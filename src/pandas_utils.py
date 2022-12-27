from io import StringIO

import pandas as pd


def dataframe_from_text(text, split_by_spaces=False):
    stream = StringIO(text)
    if split_by_spaces:
        return pd.read_csv(stream, header=None, delimiter=r"\s+")
    else:
        return pd.read_csv(stream, header=None)