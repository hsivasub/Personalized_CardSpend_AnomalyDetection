import pandas as pd
import numpy as np

def build_user_profiles(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Build user profiles containing behavioral aggregates from transaction data.
    Aggregates are calculated per client_id.
    
    Args:
        df_tx: A pandas DataFrame containing transaction data with columns like
               'client_id', 'amount', 'date', 'mcc', 'merchant_city'.
               
    Returns:
        pd.DataFrame: A DataFrame indexed by 'client_id' containing behavioral features.
    """
    # Ensure 'date' is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_tx['date']):
        df_tx['date'] = pd.to_datetime(df_tx['date'])

    # Create 'date_only' for daily aggregations
    df_tx['date_only'] = df_tx['date'].dt.date

    profiles = []
    
    # Group by client_id to calculate aggregates
    grouped = df_tx.groupby('client_id')
    
    for client_id, group in grouped:
        # Basic Amount Stats
        median_txn_amount = group['amount'].median()
        max_txn_amount = group['amount'].max()
        
        # Daily Stats
        daily_stats = group.groupby('date_only').agg(
            daily_spend=('amount', 'sum'),
            daily_txns=('id', 'count')
        )
        
        avg_daily_spend = daily_stats['daily_spend'].mean()
        std_daily_spend = daily_stats['daily_spend'].std() if len(daily_stats) > 1 else 0.0
        txn_freq_per_day = daily_stats['daily_txns'].mean()
        
        # Categorical Preferences (Top 3)
        top_mcc_codes = group['mcc'].value_counts().head(3).index.tolist() if 'mcc' in group.columns else []
        top_merchant_cities = group['merchant_city'].value_counts().head(3).index.tolist() if 'merchant_city' in group.columns else []
        
        profiles.append({
            'client_id': client_id,
            'median_txn_amount': median_txn_amount,
            'max_txn_amount': max_txn_amount,
            'avg_daily_spend': avg_daily_spend,
            'std_daily_spend': std_daily_spend,
            'txn_freq_per_day': txn_freq_per_day,
            'top_mcc_codes': top_mcc_codes,
            'top_merchant_cities': top_merchant_cities
        })
        
    df_profiles = pd.DataFrame(profiles).set_index('client_id')
    return df_profiles

if __name__ == '__main__':
    # Simple test run block
    print("User profiles module loaded.")
