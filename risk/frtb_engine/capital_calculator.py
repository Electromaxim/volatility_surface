import numpy as np
from pricing.analytic import black_scholes


class CapitalCalculator:
    """Basel IV FRTB-SA implementation for Swiss portfolios"""
    
    def compute_charge(self, portfolio: Portfolio) -> float:
        delta_charge = sum(
            abs(pos.delta) * self._get_risk_weight(pos) 
            for pos in portfolio
        )
        curvature_charge = sum(
            self._curvature_risk(pos) 
            for pos in portfolio.options
        )
        return delta_charge + curvature_charge
    
    def _get_risk_weight(self, position) -> float:
        # Higher weights for CHF instruments
        if position.currency == "CHF":
            return BASE_WEIGHTS[position.asset_class] * 1.25
        return BASE_WEIGHTS[position.asset_class]
        

class FRTBCalculator:
    """Basel IV FRTB-SA implementation for Swiss options portfolios"""
    
    # FINMA-prescribed risk weights (2023)
    RISK_WEIGHTS = {
        "equity": 0.32,
        "rates": 0.015,
        "fx": 0.30,
        "commodity": 0.40
    }
    SWISS_MULTIPLIER = 1.18  # Country risk factor
    
    def compute_delta_charge(self, position: dict) -> float:
        """Delta component of capital charge"""
        delta = position['delta']
        risk_class = position['risk_class']
        weight = self.RISK_WEIGHTS[risk_class] * self.SWISS_MULTIPLIER
        return abs(delta) * weight
    
    def compute_curvature_charge(self, position: dict) -> float:
        """Curvature risk under stress scenario"""
        S = position['spot']
        K = position['strike']
        T = position['maturity']
        r = position['risk_free_rate']
        q = position.get('dividend_yield', 0.0)
        sigma_base = position['base_vol']
        sigma_stressed = position['stressed_vol']
        option_type = position['option_type']
        
        base_price = black_scholes.BlackScholesPricer.price(
            S, K, T, r, sigma_base, option_type, q
        )
        stressed_price = black_scholes.BlackScholesPricer.price(
            S, K, T, r, sigma_stressed, option_type, q
        )
        return max(0, base_price - stressed_price)  # Worst-case loss
    
    def aggregate_charge(self, portfolio: list) -> float:
        """Total capital requirement for portfolio"""
        total = 0.0
        for position in portfolio:
            total += self.compute_delta_charge(position)
            total += self.compute_curvature_charge(position)
        return total
        
        
surface = pricing.get_latest_surface()
stress_vol = surface.apply_stress("2020_COVID")
charge = compute_curvature_charge(stress_vol)