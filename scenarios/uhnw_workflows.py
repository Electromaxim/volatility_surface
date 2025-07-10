# Content to create
from risk.uhnw_shield import UHNWPortfolioShield
from pricing.tax_optimizer import SwissTaxOptimizer
from reporting.compliance import generate_uhnw_report

def run_full_uhnw_simulation(tier: str, portfolio_value: float):
    shield = UHNWPortfolioShield(portfolio_value)
    protection = shield.generate_protection()
    
    optimizer = SwissTaxOptimizer(tier)
    optimized = optimizer.optimize_hedge(protection)
    
    report = generate_uhnw_report(optimized)
    return report