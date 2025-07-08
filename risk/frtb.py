import numpy as np
from scipy.stats import norm

class FRTBCalculator:
    """Implements Basel IV FRTB-SA capital requirements"""
    
    @staticmethod
    def delta_risk_charge(delta: float, risk_weight: float) -> float:
        """Delta charge for market risk"""
        return abs(delta) * risk_weight
    
    @staticmethod
    def curvature_risk(S: float, K: float, T: float, r: float, 
                      sigma_base: float, sigma_shocked: float, 
                      option_type: str) -> float:
        """Curvature risk under stressed conditions"""
        from surface_construction.black_scholes import BlackScholesPricer
        base_price = BlackScholesPricer.price(S, K, T, r, sigma_base, option_type)
        shocked_price = BlackScholesPricer.price(S, K, T, r, sigma_shocked, option_type)
        return max(0, base_price - shocked_price)
    
    @staticmethod
    def calculate_total_charge(portfolio_exposure: dict) -> float:
        """Aggregates capital charge for Rothschild portfolios"""
        delta_charge = sum(
            FRTBCalculator.delta_risk_charge(pos['delta'], pos['risk_weight']) 
            for pos in portfolio_exposure['positions']
        )
        
        curvature_charge = sum(
            FRTBCalculator.curvature_risk(**pos)
            for pos in portfolio_exposure['curvature_positions']
        )
        
        return delta_charge + curvature_charge