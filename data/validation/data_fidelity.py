import numpy as np
from scipy import stats
from sklearn.metrics import mean_absolute_error

class SwissDataValidator:
    """Validates dataset against Swiss market characteristics"""
    
    SWISS_MARKET_THRESHOLDS = {
        "volatility_range": (0.05, 0.65),  # Min/Max expected IV
        "volume_distribution": "lognormal",  # Expected volume distribution
        "bid_ask_spread": 0.02  # Max average spread for liquid options
    }
    
    def __init__(self, reference_data: pd.DataFrame):
        self.reference = reference_data
    
    def calculate_fidelity_score(self, test_data: pd.DataFrame) -> float:
        """Quantifies similarity to real Swiss markets (0-1 scale)"""
        scores = []
        
        # 1. Volatility distribution similarity
        vol_score = self._compare_distributions(
            test_data['implied_vol'], self.reference['implied_vol']
        )
        scores.append(vol_score)
        
        # 2. Volume correlation
        volume_corr = test_data['volume'].corr(self.reference['volume'])
        scores.append(max(0, volume_corr))  # Negative corr = 0
        
        # 3. Crisis behavior check (vol spike magnitude)
        if '2020-03-15' in test_data.index:
            crisis_vol = test_data.loc['2020-03-15', 'implied_vol'].mean()
            ref_crisis_vol = self.reference.loc['2020-03-15', 'implied_vol'].mean()
            crisis_score = 1 - abs(crisis_vol - ref_crisis_vol) / ref_crisis_vol
            scores.append(max(0, crisis_score))
        
        return np.mean(scores)
    
    def _compare_distributions(self, test_series, ref_series) -> float:
        """KL divergence scaled to 0-1 range"""
        hist_test, bin_edges = np.histogram(test_series, bins=50, density=True)
        hist_ref, _ = np.histogram(ref_series, bins=bin_edges, density=True)
        
        # Avoid zero bins
        hist_test = np.where(hist_test == 0, 1e-10, hist_test)
        hist_ref = np.where(hist_ref == 0, 1e-10, hist_ref)
        
        kl_div = stats.entropy(hist_test, hist_ref)
        return np.exp(-kl_div)  # Convert to similarity score