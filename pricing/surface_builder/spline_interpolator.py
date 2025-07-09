from scipy.interpolate import CubicSpline
import numpy as np

class FINMASplineInterpolator:
    """Cubic spline with Swiss arbitrage constraints"""
    
    def __init__(self, strikes: np.array, vols: np.array):
        self.strikes = strikes
        self.vols = vols
        self.spline = self._build_constrained_spline()
        
    def _build_constrained_spline(self) -> CubicSpline:
        """Build spline enforcing convexity (d²C/dK² > 0)"""
        # Sort inputs
        sort_idx = np.argsort(self.strikes)
        sorted_strikes = self.strikes[sort_idx]
        sorted_vols = self.vols[sort_idx]
        
        # First pass: Unconstrained spline
        spline = CubicSpline(sorted_strikes, sorted_vols)
        
        # Check convexity
        k_test = np.linspace(min(sorted_strikes), max(sorted_strikes), 100)
        second_deriv = spline(k_test, 2)
        
        if np.all(second_deriv > 0):
            return spline
        
        # Apply convexity adjustment
        # ... (Implementation using quadratic programming)
        # ...
        return adjusted_spline
    
    def __call__(self, strike: float) -> float:
        return self.spline(strike)
    
    def get_smile_curvature(self) -> float:
        """Quantifies smile convexity for FINMA reporting"""
        mid = (min(self.strikes) + max(self.strikes)) / 2
        return self.spline(mid, 2)  # Second derivative at ATM