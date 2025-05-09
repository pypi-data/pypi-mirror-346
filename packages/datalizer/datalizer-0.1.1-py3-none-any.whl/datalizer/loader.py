import os
import pandas as pd

__all__ = ["load_data"]

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a dataset from a file into a pandas DataFrame.
    
    Parameters
    ----------
        file_path : str
            Path to the dataset file.
            Supported formats: .csv, .xlsx, .json
                 
    Returns
    -------
        pd.DataFrame
            Loaded DataFrame
        
    Raises
    ------
        FileNotFoundError
            If the file doesn't exist.
        ValueError
            If the file extension is unsupported or reading fails.
            If non-numeric data is present.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    elif file_path.endswith(".json"):
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}. Please use .csv, .xlsx, or .json.")
    
    if not df.select_dtypes(exclude=["number"]).empty:
        raise ValueError("load_data only supports numerical datasets. Non-numeric data found.")

    return df