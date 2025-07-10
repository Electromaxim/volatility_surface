import numpy as np
from scipy.stats import norm
from typing import Dict

class UHNWPortfolioShield:
    """
    Capital protection engine for ultra-high-net-worth clients
    Returns: Dict with protection structure details
    """
    
    PROTECTION_LEVELS = {"tier1": 0.85, "tier2": 0.90}
    COST_MULTIPLIERS = {"tier1": 1.2, "tier2": 1.0}
    
    def __init__(self, notional_chf: float):
        """
        notional_chf: Total portfolio value in CHF
        """
        self.notional = notional_chf
        self.tier = "tier1" if notional_chf > 1e8 else "tier2"
    
    def generate_protection(self) -> Dict[str, object]:
        """
        Creates capital protection structure
        Returns: {
            "type": str - Option type,
            "protection_level": float - Capital protection percentage,
            "cost_bps": float - Cost in basis points,
            "tax_impact": Dict[str, str] - Tax treatment details
        }
        """
        protection_level = self.PROTECTION_LEVELS[self.tier]
        cost_bps = self._calculate_cost(protection_level) * 10000
        
        return {
            "type": "DownAndInPut",
            "protection_level": protection_level,
            "cost_bps": cost_bps,
            "tax_impact": self._get_tax_impact()
        }
    
    def _calculate_cost(self, protection_level: float) -> float:
        """Black-Scholes based pricing with Swiss adjustments"""
        S = self.notional  # Current portfolio value
        K = S * protection_level  # Strike price
        T = 1.0  # 1-year protection
        r = 0.01  # CHF risk-free rate
        sigma = 0.25  # Conservative volatility estimate
        
        # Black-Scholes put price
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        put_price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        # Apply tier-based multiplier
        return put_price * self.COST_MULTIPLIERS[self.tier]
    
    def _get_tax_impact(self) -> Dict[str, str]:
        """Swiss tax treatment characteristics"""
        return {
            "wealth_tax": "Deferred until barrier trigger",
            "income_tax": "Not applicable",
            "stamp_duty": "Exempt per Art. 13 Stamp Tax Act",
            "treatment": "Tax-advantaged derivative structure"
        }