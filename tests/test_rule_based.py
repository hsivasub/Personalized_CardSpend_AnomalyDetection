import pytest
from src.models.rule_based import RuleBasedScorer

def test_rule_based_scorer_normal():
    scorer = RuleBasedScorer()
    
    # Mock user profile
    user_profile = {
        'median_txn_amount': 20.0,
        'max_txn_amount': 150.0,
        'top_mcc_codes': ['5411', '5812', '5814'],
        'top_merchant_cities': ['New York', 'Boston']
    }
    
    # Normal transaction: amount=30, mcc in top, city in top
    tx_normal = {
        'amount': 30.0,
        'mcc': '5411',
        'merchant_city': 'New York'
    }
    
    score, flags = scorer.score_transaction(tx_normal, user_profile)
    assert score == 0.0
    assert len(flags) == 0

def test_rule_based_scorer_anomalous():
    scorer = RuleBasedScorer()
    
    user_profile = {
        'median_txn_amount': 20.0,
        'max_txn_amount': 150.0,
        'top_mcc_codes': ['5411', '5812', '5814'],
        'top_merchant_cities': ['New York', 'Boston']
    }
    
    # Anomalous transaction: High amount (vs median), new max, strange city, strange MCC
    tx_anomalous = {
        'amount': 200.0,           # > 3 * 20 (60) AND > 150
        'mcc': '1234',             # Not in top
        'merchant_city': 'Miami'   # Not in top
    }
    
    score, flags = scorer.score_transaction(tx_anomalous, user_profile)
    assert score == 100.0  # Max score
    assert 'HIGH_AMOUNT_VS_MEDIAN' in flags
    assert 'NEW_HISTORICAL_MAX_AMOUNT' in flags
    assert 'UNUSUAL_MCC' in flags
    assert 'UNUSUAL_CITY' in flags

def test_rule_based_scorer_partial_anomaly():
    scorer = RuleBasedScorer()
    
    user_profile = {
        'median_txn_amount': 20.0,
        'max_txn_amount': 150.0,
        'top_mcc_codes': ['5411'],
        'top_merchant_cities': ['New York']
    }
    
    # Partial anomaly: normal amount, but unusual city
    tx_partial = {
        'amount': 20.0,
        'mcc': '5411',
        'merchant_city': 'Los Angeles'
    }
    
    score, flags = scorer.score_transaction(tx_partial, user_profile)
    assert score == 25.0
    assert flags == ['UNUSUAL_CITY']
