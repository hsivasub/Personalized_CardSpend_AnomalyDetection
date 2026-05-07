import pandas as pd
import pytest
from src.data.validation import (
    check_missing_values,
    check_duplicates,
    check_invalid_timestamps,
    check_invalid_amounts,
    validate_transactions
)

def test_check_missing_values():
    df = pd.DataFrame({'id': [1, 2, 3], 'val': [10, None, 30]})
    assert check_missing_values(df, ['id']) == True
    assert check_missing_values(df, ['id', 'val']) == False

def test_check_duplicates():
    df = pd.DataFrame({'id': [1, 2, 2], 'val': [10, 20, 20]})
    # Without subset, row 1 and 2 are not identical because 2 != 2... wait, no.
    # index 1 is {'id':2, 'val':20}, index 2 is {'id':2, 'val':20} -> they are identical!
    assert check_duplicates(df) == False
    assert check_duplicates(pd.DataFrame({'id': [1, 2, 3]})) == True

def test_check_invalid_timestamps():
    df_valid = pd.DataFrame({'date': pd.to_datetime(['2020-01-01', '2020-01-02'])})
    assert check_invalid_timestamps(df_valid, 'date') == True
    
    df_invalid = pd.DataFrame({'date': ['2020-01-01', None]})
    assert check_invalid_timestamps(df_invalid, 'date') == False

def test_check_invalid_amounts():
    df_valid = pd.DataFrame({'amount': [10.5, 20.0, 0.0]})
    assert check_invalid_amounts(df_valid, 'amount', min_amount=0.0) == True
    
    df_invalid = pd.DataFrame({'amount': [10.5, -5.0]})
    assert check_invalid_amounts(df_invalid, 'amount', min_amount=0.0) == False

def test_validate_transactions():
    df_valid = pd.DataFrame({
        'id': [1, 2],
        'client_id': [100, 101],
        'card_id': [200, 201],
        'amount': [50.0, 100.0],
        'date': pd.to_datetime(['2020-01-01', '2020-01-02'])
    })
    assert validate_transactions(df_valid) == True
