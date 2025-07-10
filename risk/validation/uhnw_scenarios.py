class UHNWScenarioTester:
    """Validates Tier1 client-specific scenarios"""
    
    FAMILY_OFFICE_SCENARIOS = {
        "liquidity_crisis": {
            "trigger": "Large redemption request (>30% AUM)",
            "parameters": {
                "redemption_pressure": 0.35,
                "collateral_haircut": 0.25,
                "market_impact": 0.18
            },
            "acceptance_criteria": "Capital protection remains ≥85%"
        },
        "confidentiality_breach": {
            "trigger": "Suspected data leak",
            "parameters": {
                "position_covering": 1.0,
                "volatility_spike": 0.40
            },
            "acceptance_criteria": "Anonymization intact, zero PII exposure"
        }
    }
    
    def execute_family_office_test(self, scenario_name: str, portfolio):
        scenario = self.FAMILY_OFFICE_SCENARIOS[scenario_name]
        
        # Apply scenario parameters
        from risk.uhnw_shield import UHNWPortfolioShield
        shield = UHNWPortfolioShield(portfolio.value)
        protection = shield.generate_protection()
        
        # Run stress test
        from risk.frtb_engine.stress_applier import apply_scenario
        stressed_portfolio = apply_scenario(portfolio, scenario_name)
        
        return {
            "protection_effectiveness": protection['protection_level'] - stressed_portfolio.loss_percentage,
            "tax_impact": protection['tax_impact'],
            "pass": protection['protection_level'] - stressed_portfolio.loss_percentage >= 0.85
        }