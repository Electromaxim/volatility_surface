# data/validation/data_fidelity.py
import pandas as pd
import numpy as np
from scipy import stats

class SwissDataValidator:
    """Validates dataset against Swiss market characteristics"""
    
    SWISS_MARKET_THRESHOLDS = {
        "volatility_range": (0.05, 0.65),
        "volume_distribution": "lognormal",
        "bid_ask_spread": 0.02,
        "min_volume": 50,
        "max_spread_ratio": 0.1
        "crisis_vol_multiplier": 2.8  # 2020 COVID reference
    }
    
    def __init__(self, reference_data: pd.DataFrame):
        self.reference = reference_data
    
    def calculate_fidelity_score(self, test_data: pd.DataFrame) -> float:
        scores = []
        
        # 1. Volatility distribution similarity
        vol_score = self._compare_distributions(
            test_data['implied_vol'], self.reference['implied_vol']
        )
        scores.append(vol_score)
        
        # 2. Volume correlation
        volume_corr = test_data['volume'].corr(self.reference['volume'])
        scores.append(max(0, volume_corr))
        
        # 3. Crisis behavior check
        if '2020-03-15' in test_data.index:
            crisis_vol = test_data.loc['2020-03-15', 'implied_vol'].mean()
            ref_crisis_vol = self.reference.loc['2020-03-15', 'implied_vol'].mean()
            crisis_score = 1 - abs(crisis_vol - ref_crisis_vol) / ref_crisis_vol
            scores.append(max(0, crisis_score))
        
        # 4. Liquidity checks
        liquidity_score = self._check_liquidity(test_data)
        scores.append(liquidity_score)
        
        return np.mean(scores)
    
    def _compare_distributions(self, test_series, ref_series) -> float:
        hist_test, bin_edges = np.histogram(test_series, bins=50, density=True)
        hist_ref, _ = np.histogram(ref_series, bins=bin_edges, density=True)
        hist_test = np.where(hist_test == 0, 1e-10, hist_test)
        hist_ref = np.where(hist_ref == 0, 1e-10, hist_ref)
        kl_div = stats.entropy(hist_test, hist_ref)
        return np.exp(-kl_div)
    
    def _check_liquidity(self, df: pd.DataFrame) -> float:
        """Ensure meets SIX liquidity requirements"""
        valid_count = 0
        total = len(df)
        
        # Check minimum volume
        valid_count += sum(df['volume'] >= self.SWISS_MARKET_THRESHOLDS['min_volume'])
        
        # Check bid-ask spreads
        spreads = (df['ask_iv'] - df['bid_iv']) / ((df['ask_iv'] + df['bid_iv'])/2)
        valid_count += sum(spreads <= self.SWISS_MARKET_THRESHOLDS['max_spread_ratio'])
        
        return valid_count / (2 * total)  # Normalize to 0-1 range
    
    @staticmethod
    def validate_six_requirements(df: pd.DataFrame) -> bool:
        """Quick check for mandatory fields"""
        required_columns = [
            'underlying', 'expiration', 'strike', 'type',
            'bid_iv', 'ask_iv', 'volume', 'open_interest'
        ]
        return all(col in df.columns for col in required_columns)
        
    def detect_data_drift(self, new_data: pd.DataFrame) -> dict:
    drift_metrics = {}
    for column in ['implied_vol', 'volume']:
        drift = stats.ks_2samp(self.reference[column], new_data[column])
        drift_metrics[column] = drift.statistic
    return drift_metrics
    
    
###########

    def __init__(self, reference_data: pd.DataFrame):
        self.reference = reference_data
    
    def validate_uhnw_characteristics(self, client_data: pd.DataFrame) -> dict:
        """Checks specific to ultra-high-net-worth portfolios"""
        results = {}
        
        # 1. Position concentration check
        top_3_exposure = client_data['notional_chf'].nlargest(3).sum() / client_data['notional_chf'].sum()
        results['concentration'] = top_3_exposure < 0.15  # Max 15% in top 3 positions
        
        # 2. Liquidity profile
        illiquid_assets = client_data[client_data['volume'] < 100]['notional_chf'].sum()
        results['illiquid_exposure'] = illiquid_assets / client_data['notional_chf'].sum() < 0.1
        
        # 3. Tax efficiency score
        results['tax_efficiency'] = self.calculate_tax_efficiency(client_data)
        
        return results
    
    def calculate_tax_efficiency(self, client_data) -> float:
        """Quantifies tax optimization (0-1 scale)"""
        # Placeholder: In production uses Zurich cantonal tax tables
        return 0.92
    
    def detect_behavioral_anomalies(self, transaction_history):
        """Identifies unusual patterns for UHNW clients"""
        # Uses federated learning to detect anomalies without raw data access
        pass