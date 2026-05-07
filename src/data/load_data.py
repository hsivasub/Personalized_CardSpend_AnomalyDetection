import pandas as pd
import numpy as np
from pathlib import Path
import gc

def load_data(file_path: str, nrows=None) -> pd.DataFrame:
    """Load dataset from raw data directory."""
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path, nrows=nrows)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize columns, parse dates, handle missing values."""
    print("Cleaning data...")
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Parse timestamps if 'date' column exists
    if 'date' in df.columns:
        print("Parsing timestamps...")
        df['date'] = pd.to_datetime(df['date'])
        
    # Clean money columns (remove '$' and convert to float)
    for col in ['amount', 'per_capita_income', 'yearly_income', 'total_debt', 'credit_limit']:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)
            
    # Handle missing values
    if 'errors' in df.columns:
        df['errors'] = df['errors'].fillna('None')
    if 'zip' in df.columns:
        df['zip'] = df['zip'].fillna(-1).astype(int)
    if 'merchant_state' in df.columns:
        df['merchant_state'] = df['merchant_state'].fillna('Unknown')
    if 'merchant_city' in df.columns:
        df['merchant_city'] = df['merchant_city'].fillna('Unknown')
        
    return df

def save_data(df: pd.DataFrame, file_path: str):
    """Save cleaned dataset to processed directory."""
    print(f"Saving data to {file_path}...")
    df.to_csv(file_path, index=False)
    print("Saved successfully.")

def main():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Process cards data
    cards_file = raw_dir / "cards_data.csv"
    if cards_file.exists():
        df_cards = load_data(cards_file)
        df_cards = clean_data(df_cards)
        save_data(df_cards, processed_dir / "cards_data_cleaned.csv")
        del df_cards
        gc.collect()

    # Process users data
    users_file = raw_dir / "users_data.csv"
    if users_file.exists():
        df_users = load_data(users_file)
        df_users = clean_data(df_users)
        save_data(df_users, processed_dir / "users_data_cleaned.csv")
        del df_users
        gc.collect()

    # Process transactions data
    tx_file = raw_dir / "transactions_data.csv"
    if tx_file.exists():
        print("Processing transactions data... This may take a few minutes for 1.2GB.")
        # Load the whole file or sample. For production, load whole file.
        df_tx = load_data(tx_file)
        df_tx = clean_data(df_tx)
        save_data(df_tx, processed_dir / "transactions_data_cleaned.csv")
        del df_tx
        gc.collect()

if __name__ == "__main__":
    main()
