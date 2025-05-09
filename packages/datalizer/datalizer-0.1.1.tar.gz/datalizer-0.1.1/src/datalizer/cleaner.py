import pandas as pd
from typing import Literal
from datalizer.utils import *

__all__ = ["check_for_issues", "clean_basic"]

@requires_numeric_data
def check_for_issues(df: pd.DataFrame) -> None:
    """
    Check for common issues in a DataFrame.
    
    Parameters
    ----------
        df (pd.DataFrame)
            Input DataFrame
    """
    num_missing = df.isnull().sum().sum()
    num_duplicates = df.duplicated().sum()
    
    print(f"\nNumber of missing cells: {num_missing}")
    if num_missing > 0:
        print("\nRows with missing values:")
        print(df[df.isnull().any(axis=1)])
        
    print(f"\nNumber of duplicate rows: {num_duplicates}")
    if num_duplicates > 0:
        print("\nDuplicate rows:")
        print(df[df.duplicated()],)

@requires_numeric_data
def clean_basic(df: pd.DataFrame, strategy: Literal["mean", "median", "mode", "drop"] = "mode") -> pd.DataFrame:
    """
    Perform basic cleaning:
    - Remove duplicate rows
    - Handle missing values using a chosen strategy

    Parameters
    ----------
        df (pd.DataFrame)
            Input DataFrame
        strategy (str)
            Strategy to handle missing values ('mean', 'median', 'mode', or 'drop')
        
    Returns
    -------
        pd.DataFrame
            Cleaned DataFrame
    
    Raises
    ------
        ValueError
            If an invalid strategy is provided.
    """
    
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()

    if not df_clean.isnull().values.any():
        print("\nNo missing values found.")
        return df_clean
    
    print(f"\nMissing values detected. Cleaning with strategy: '{strategy}'.")
    
    if strategy == "mean":
        df_clean = df_clean.fillna(df_clean.mean())
    elif strategy == "median":
        df_clean = df_clean.fillna(df_clean.median())
    elif strategy == "mode":
        df_clean = df_clean.fillna(df_clean.mode().iloc[0])
    elif strategy == "drop":
        df_clean = df_clean.dropna()
        return df_clean
    else:
        raise ValueError(f"Invalid strategy '{strategy}'. Choose 'mean', 'median', 'mode', or 'drop'.")
    
    return df_clean