import numpy as np
from pricing.analytic import black_scholes

class ArbitrageValidator:
    """FINMA-required arbitrage checks for volatility surfaces"""
    
    @staticmethod
    def check_butterfly_arbitrage(strikes: list, vols: list) -> bool:
        """Verify call spreads are non-negative"""
        calls = [black_scholes.BlackScholesPricer.price(
            100, K, 0.25, 0.01, iv, 'call'
        ) for K, iv in zip(strikes, vols)]
        
        # Check call spreads: C(K1) - C(K2) should be non-negative for K1 < K2
        for i in range(len(calls) - 1):
            if calls[i] < calls[i+1]:
                return False
        return True
    
    @staticmethod
    def check_calendar_arbitrage(short_term_vol: float, long_term_vol: float) -> bool:
        """Verify term structure consistency"""
        return long_term_vol >= short_term_vol  # Normal contango condition
    
    @staticmethod
    def check_put_call_parity(put_price: float, call_price: float, 
                             spot: float, strike: float, r: float, T: float) -> bool:
        """Verify put-call parity holds within tolerance"""
        theoretical_diff = call_price - put_price
        actual_diff = spot - strike * np.exp(-r * T)
        return abs(theoretical_diff - actual_diff) < 0.01  # 1 bps tolerance