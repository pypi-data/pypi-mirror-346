import pandas as pd
from functools import wraps

def requires_numeric_data(func):
    """
    Decorator to ensure that a DataFrame contains only numeric data.
    
    Raises
    ------
        ValueError
            If non-numeric data is present.
    """
    @wraps(func)
    def wrapper(df: pd.DataFrame, *args, **kwargs):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"{func.__name__} expects a pandas DataFrame.")
        if not df.select_dtypes(exclude=["number"]).empty:
            raise ValueError(f"{func.__name__} only supports numerical datasets. Non-numeric data found.")
        return func(df, *args, **kwargs)
    return wrapper