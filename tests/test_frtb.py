import pytest
from risk.frtb import FRTBCalculator

def test_delta_risk_charge():
    charge = FRTBCalculator.delta_risk_charge(delta=-500000, risk_weight=0.015)
    assert abs(charge - 7500) < 0.01  # |-500k| * 1.5% = 7,500 CHF

def test_curvature_risk():
    from surface_construction.black_scholes import BlackScholesPricer
    # Base scenario
    base_price = BlackScholesPricer.price(100, 110, 0.5, 0.01, 0.25, 'call')
    # Shock scenario: vol increases by 50%
    shocked_price = BlackScholesPricer.price(100, 110, 0.5, 0.01, 0.375, 'call')
    expected_curvature = max(0, base_price - shocked_price)
    
    curvature = FRTBCalculator.curvature_risk(
        S=100, K=110, T=0.5, r=0.01,
        sigma_base=0.25, sigma_shocked=0.375,
        option_type='call'
    )
    assert abs(curvature - expected_curvature) < 0.01

def test_total_charge():
    portfolio = {
        'positions': [
            {'delta': -300000, 'risk_weight': 0.02},
            {'delta': 200000, 'risk_weight': 0.015}
        ],
        'curvature_positions': [
            {'S': 100, 'K': 105, 'T': 0.3, 'r': 0.01, 
             'sigma_base': 0.22, 'sigma_shocked': 0.33, 'option_type': 'call'}
        ]
    }
    charge = FRTBCalculator.calculate_total_charge(portfolio)
    assert charge > 0