from infrastructure.utils.swiss_calendar import SwissBankingCalendar
from typing import Dict, Tuple, List

class SwissTaxOptimizer:
    """
    Zurich cantonal tax-aware derivatives optimization for private banking clients
    Returns: Dict with tax optimization strategy details
    """
    
    ZURICH_TAX_RATES = {
        "wealth": [  # Progressive wealth tax brackets (CHF, rate)
            (0, 0.00), (50000, 0.001), (100000, 0.002), 
            (500000, 0.003), (1000000, 0.004)
        ],
        "income": 0.11,
        "stamp_duty": 0.0015
    }
    
    def __init__(self, client_tier: str, canton: str = "ZH"):
        """
        client_tier: 'tier1' (>CHF 100M), 'tier2' (CHF 20-100M)
        canton: Swiss canton code (ZH = Zurich, GE = Geneva)
        """
        self.client_tier = client_tier
        self.canton = canton
        self.calendar = SwissBankingCalendar()
    
    def optimize_hedge(self, portfolio_value: float) -> Dict[str, object]:
        """
        Generates tax-optimized hedging strategy
        Returns: {
            "instruments": List[str] - Recommended derivatives,
            "tax_savings_bps": float - Estimated savings in basis points,
            "execution_window": Tuple[str, str] - Optimal date range,
            "quarter_end_adjustment": float - Notional reduction percentage
        }
        """
        return {
            "instruments": self._select_instruments(),
            "tax_savings_bps": self._calculate_savings(portfolio_value),
            "execution_window": self.calendar.get_tax_optimization_window("wealth_tax"),
            "quarter_end_adjustment": self._calculate_quarter_end_adjustment()
        }
    
    def _select_instruments(self) -> List[str]:
        """Select tax-efficient instruments based on client tier"""
        if self.client_tier == "tier1":
            return ["Forward", "Total Return Swap", "CHF Cantonal Bond"]
        return ["Forward", "ETF Swap"]
    
    def _calculate_savings(self, portfolio_value: float) -> float:
        """Estimate tax savings in basis points"""
        base_tax = self._calculate_tax(portfolio_value, "wealth")
        optimized_tax = self._calculate_tax(portfolio_value * 0.85, "wealth")
        return (base_tax - optimized_tax) / portfolio_value * 10000
    
    def _calculate_tax(self, amount: float, tax_type: str) -> float:
        """Compute tax liability using progressive brackets"""
        tax = 0.0
        remaining = amount
        
        for max_amount, rate in sorted(self.ZURICH_TAX_RATES[tax_type]):
            if remaining <= 0:
                break
            bracket_size = min(remaining, max_amount) if max_amount > 0 else remaining
            tax += bracket_size * rate
            remaining -= bracket_size
        
        return tax
    
    def _calculate_quarter_end_adjustment(self) -> float:
        """Calculate optimal notional reduction before tax dates"""
        return -0.15 if self.client_tier == "tier1" else -0.10