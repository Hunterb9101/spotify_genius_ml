import pandas as pd
import numpy as np
import json


def str_to_list(x):
    return x[1:-1].replace("'", "").split(',')


def agg_uniq_list(x):
    return list(set(x.tolist()))


def to_json(x):
    x = x.replace("'", '"')
    x = x.replace("False", "false")
    x = x.replace("True", 'true')
    try:
        x_fin = json.loads(x)
    except Exception:
        x_fin = {'name': 'ERROR_UNENCODABLE'}
    return x_fin


def flatten_count_list_col(df, col):
    """Flatten a dataframe list column, and count unique instances of all elements"""
    arr = []
    if isinstance(df[col].tolist()[0], list):
        flattened = [arr.extend(x) for x in df[col].tolist()]
    else:
        flattened = [arr.extend(x) for x in df[col].apply(lambda x: tu.str_to_list(x)).tolist()]

    arr = [x.lstrip() for x in arr]

    unique, cnts = np.unique(np.array(arr), return_counts=True)
    counts = dict(zip(unique, cnts))
    counts = pd.DataFrame([{"col_val": x, "count": int(counts[x])} for x in counts.keys()])
    counts.sort_values('count', ascending=False, inplace=True)
    counts.reset_index(inplace=True, drop=True)
    return counts