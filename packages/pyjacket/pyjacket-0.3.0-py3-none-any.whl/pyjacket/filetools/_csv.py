import pandas as pd

def read_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """Read csv data into a pandas dataframe"""
    kwargs.setdefault('index_col', 0)
    return pd.read_csv(filepath, **kwargs)

def write_csv(filepath: str, data: pd.DataFrame, **kwargs):
    kwargs.setdefault('float_format', '%.5f') 
    data.to_csv(filepath, **kwargs)