from typing import Dict, Any, Tuple

class RuleBasedScorer:
    """
    A rule-based scoring engine for card spend anomaly detection.
    Evaluates a transaction against a user's behavioral profile.
    """
    
    def __init__(self):
        # Weights for the scoring mechanism (total max = 100)
        self.weights = {
            'amount_vs_median': 20,    # > 3x median
            'amount_vs_max': 30,       # > historical max
            'unusual_mcc': 25,         # MCC not in top MCCs
            'unusual_city': 25         # City not in top Cities
        }

    def score_transaction(self, tx: Dict[str, Any], user_profile: Dict[str, Any]) -> Tuple[float, list]:
        """
        Score a single transaction against the user profile.
        
        Args:
            tx: Dictionary containing transaction data 
                (e.g., {'amount': 150.0, 'mcc': '5411', 'merchant_city': 'New York'})
            user_profile: Dictionary containing user profile aggregates
                (e.g., {'median_txn_amount': 20.0, 'max_txn_amount': 100.0, ...})
                
        Returns:
            Tuple containing:
            - The normalized risk score (0 to 100, where 100 is highest risk)
            - A list of triggered risk flags
        """
        score = 0.0
        flags = []
        
        # Check amount vs median
        if 'amount' in tx and 'median_txn_amount' in user_profile:
            if tx['amount'] > 3 * user_profile['median_txn_amount']:
                score += self.weights['amount_vs_median']
                flags.append('HIGH_AMOUNT_VS_MEDIAN')
                
        # Check amount vs absolute historical max
        if 'amount' in tx and 'max_txn_amount' in user_profile:
            if tx['amount'] > user_profile['max_txn_amount']:
                score += self.weights['amount_vs_max']
                flags.append('NEW_HISTORICAL_MAX_AMOUNT')
                
        # Check MCC familiarity
        if 'mcc' in tx and 'top_mcc_codes' in user_profile:
            if tx['mcc'] not in user_profile['top_mcc_codes']:
                score += self.weights['unusual_mcc']
                flags.append('UNUSUAL_MCC')
                
        # Check City familiarity
        if 'merchant_city' in tx and 'top_merchant_cities' in user_profile:
            if tx['merchant_city'] not in user_profile['top_merchant_cities']:
                score += self.weights['unusual_city']
                flags.append('UNUSUAL_CITY')
                
        # Cap score at 100.0
        score = min(score, 100.0)
        
        return score, flags

if __name__ == '__main__':
    # Test logic
    scorer = RuleBasedScorer()
    print("RuleBasedScorer loaded.")
