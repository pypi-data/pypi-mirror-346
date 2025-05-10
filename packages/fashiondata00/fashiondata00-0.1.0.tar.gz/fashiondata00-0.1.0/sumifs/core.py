import pandas as pd

def sumifs(df, sum_col, **conditions):
    cond = pd.Series([True] * len(df))
    for col, val in conditions.items():
        cond &= df[col] == val
    return df[cond][sum_col].sum()
