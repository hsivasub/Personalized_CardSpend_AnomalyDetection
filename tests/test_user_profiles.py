import pandas as pd
import numpy as np
import pytest
from src.features.user_profiles import build_user_profiles

def test_build_user_profiles():
    # Create dummy data
    data = {
        'id': [1, 2, 3, 4, 5, 6],
        'client_id': [100, 100, 100, 200, 200, 200],
        'date': [
            '2023-01-01 10:00:00',
            '2023-01-01 15:00:00',
            '2023-01-02 09:00:00',
            '2023-01-01 11:00:00',
            '2023-01-03 14:00:00',
            '2023-01-03 18:00:00'
        ],
        'amount': [10.0, 20.0, 30.0, 50.0, 100.0, 150.0],
        'mcc': ['5411', '5411', '5812', '5814', '5814', '5812'],
        'merchant_city': ['New York', 'New York', 'Boston', 'Chicago', 'Chicago', 'Chicago']
    }
    df = pd.DataFrame(data)
    
    # Run function
    profiles = build_user_profiles(df)
    
    # Assertions for Client 100
    assert 100 in profiles.index
    p100 = profiles.loc[100]
    assert p100['median_txn_amount'] == 20.0  # median of 10, 20, 30
    assert p100['max_txn_amount'] == 30.0
    # Client 100 days: Jan 1 (10+20=30, 2 txns), Jan 2 (30, 1 txn)
    assert p100['avg_daily_spend'] == 30.0 # (30+30)/2
    assert p100['txn_freq_per_day'] == 1.5 # (2+1)/2
    assert p100['top_mcc_codes'] == ['5411', '5812']
    assert p100['top_merchant_cities'] == ['New York', 'Boston']
    
    # Assertions for Client 200
    assert 200 in profiles.index
    p200 = profiles.loc[200]
    assert p200['median_txn_amount'] == 100.0 # median of 50, 100, 150
    assert p200['max_txn_amount'] == 150.0
    # Client 200 days: Jan 1 (50, 1 txn), Jan 3 (100+150=250, 2 txns)
    assert p200['avg_daily_spend'] == 150.0 # (50+250)/2
    assert p200['txn_freq_per_day'] == 1.5 # (1+2)/2
    assert p200['top_mcc_codes'] == ['5814', '5812']
    assert p200['top_merchant_cities'] == ['Chicago']

