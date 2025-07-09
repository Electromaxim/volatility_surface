# finma_adapter.py
class FINMAAdjuster:
    SWISS_RISK_MULTIPLIER = 1.18  # FINMA 2023 coefficient
    
    def adjust_charge(self, base_charge: float) -> float:
        return base_charge * self.SWISS_RISK_MULTIPLIER