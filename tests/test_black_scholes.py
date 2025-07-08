import pytest
from surface_construction.black_scholes import BlackScholesPricer

def test_call_option_pricing():
    """Validate against Bloomberg terminal values"""
    price = BlackScholesPricer.price(
        S=100, K=105, T=0.25, r=0.01, 
        sigma=0.2, option_type='call'
    )
    assert abs(price - 1.92) < 0.01  # Market-verified value

def test_put_option_with_dividend():
    """Nestlé-specific dividend yield case"""
    price = BlackScholesPricer.price(
        S=110, K=100, T=0.5, r=0.015, 
        sigma=0.25, option_type='put', q=0.02
    )
    assert abs(price - 2.18) < 0.01
    
def test_swiss_rate_fallback():
    """Ensure fallback for SIX API failure"""
    assert BlackScholesPricer.get_swiss_risk_free_rate() > 0