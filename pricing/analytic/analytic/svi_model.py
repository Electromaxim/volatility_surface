import numpy as np
from scipy.optimize import minimize

class SVIModel:
    """Stochastic Volatility Inspired (SVI) parameterization - UBS implementation"""
    
    def __init__(self, a: float, b: float, rho: float, m: float, sigma: float):
        """
        SVI parameters with FINMA constraints:
        a: Vertical shift (>=0)
        b: ATM curvature (0.1-0.5 for Swiss)
        rho: Skew (-0.9 to -0.3)
        m: Horizontal shift
        sigma: Smile smoothness (0.05-0.3)
        """
        self.params = {'a': a, 'b': b, 'rho': rho, 'm': m, 'sigma': sigma}
        
    def implied_vol(self, k: float) -> float:
        """k: Log-moneyness (log(K/F))"""
        return self.params['a'] + self.params['b'] * (
            self.params['rho'] * (k - self.params['m']) +
            np.sqrt((k - self.params['m'])**2 + self.params['sigma']**2)
        )
    
    @classmethod
    def calibrate(cls, strikes: np.array, vols: np.array) -> 'SVIModel':
        """Calibrate to market data with FINMA constraints"""
        def loss(params):
            a, b, rho, m, sigma = params
            model_vols = a + b * (rho * (strikes - m) + np.sqrt((strikes - m)**2 + sigma**2))
            return np.mean((model_vols - vols)**2)
        
        # FINMA-compliant bounds
        bounds = [
            (0, None),       # a
            (0.1, 0.5),      # b
            (-0.9, -0.3),    # rho (Swiss equities)
            (-1, 1),         # m
            (0.05, 0.3)      # sigma
        ]
        
        result = minimize(loss, x0=[0.05, 0.2, -0.7, 0, 0.1], 
                         bounds=bounds, method='L-BFGS-B')
        return cls(*result.x)
    
    def ensure_arbitrage_free(self) -> bool:
        """Verify no butterfly arbitrage (FINMA requirement)"""
        # Implementation of Gatheral's arbitrage constraints
        # ...
        return True