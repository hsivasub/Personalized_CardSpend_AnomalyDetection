import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_missing_values(df: pd.DataFrame, critical_columns: list) -> bool:
    """Check if critical columns have missing values."""
    is_valid = True
    for col in critical_columns:
        if col not in df.columns:
            logging.warning(f"Column {col} not found in dataframe.")
            is_valid = False
            continue
        missing = df[col].isnull().sum()
        if missing > 0:
            logging.warning(f"Missing values found in critical column '{col}': {missing}")
            is_valid = False
    return is_valid

def check_duplicates(df: pd.DataFrame, subset: list = None) -> bool:
    """Check for duplicate rows."""
    duplicates = df.duplicated(subset=subset).sum()
    if duplicates > 0:
        logging.warning(f"Found {duplicates} duplicate rows.")
        return False
    return True

def check_invalid_timestamps(df: pd.DataFrame, time_column: str) -> bool:
    """Check if timestamps are valid (not null, correct type)."""
    if time_column not in df.columns:
        logging.warning(f"Time column {time_column} not found.")
        return False
        
    if not pd.api.types.is_datetime64_any_dtype(df[time_column]):
        try:
            pd.to_datetime(df[time_column])
        except Exception as e:
            logging.warning(f"Invalid timestamp format in column {time_column}: {e}")
            return False
            
    if df[time_column].isnull().any():
        logging.warning(f"Null timestamps found in column {time_column}.")
        return False
    return True

def check_invalid_amounts(df: pd.DataFrame, amount_column: str, min_amount: float = None) -> bool:
    """Check for invalid amounts."""
    if amount_column not in df.columns:
        logging.warning(f"Amount column {amount_column} not found.")
        return False
        
    if not pd.api.types.is_numeric_dtype(df[amount_column]):
        logging.warning(f"Amount column {amount_column} is not numeric.")
        return False
        
    if min_amount is not None:
        invalid_amounts = df[df[amount_column] < min_amount].shape[0]
        if invalid_amounts > 0:
            logging.warning(f"Found {invalid_amounts} rows with amount < {min_amount}.")
            return False
    return True

def validate_transactions(df: pd.DataFrame) -> bool:
    """Run all validation checks on the transactions dataframe."""
    is_valid = True
    
    if not check_missing_values(df, ['id', 'client_id', 'card_id', 'amount', 'date']):
        is_valid = False
        
    if not check_duplicates(df, subset=['id']):
        is_valid = False
        
    if not check_invalid_timestamps(df, 'date'):
        is_valid = False
        
    if not check_invalid_amounts(df, 'amount', min_amount=0.0): 
        # Refunds in some datasets are negative. We'll strict check min_amount=0.0 unless there are refunds.
        # But for this anomaly detection, we want valid >=0 amounts for card spends typically.
        is_valid = False
        
    return is_valid
