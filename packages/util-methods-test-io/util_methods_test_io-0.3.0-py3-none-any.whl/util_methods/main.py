import pandas as pd

def find_max_timestamp(df: pd.DataFrame, column: str = 'timestamp') -> pd.Timestamp:
    """
    Find the maximum timestamp in a pandas DataFrame column.
    
    Args:
        df: Input DataFrame
        column: Name of the timestamp column (default: 'timestamp')
    
    Returns:
        pd.Timestamp: The maximum timestamp found
        
    Raises:
        ValueError: If column doesn't exist or contains non-timestamp data
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        raise ValueError(f"Column '{column}' must contain datetime values")
    
    return df[column].max()