import pandas as pd
from pandas.errors import EmptyDataError


def read_csv_globs(paths_arr):
    df = None
    if paths_arr is None:
        raise ValueError("No files in glob!")
    for p in paths_arr:
        if df is None:
            df = pd.read_csv(p)
        else:
            try:
                df = pd.concat([df, pd.read_csv(p)])
            except EmptyDataError:
                print(f"WARN: {p} is empty")
    return df
