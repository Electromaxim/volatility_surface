# infrastructure/utils/swiss_calendar.py
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday
import numpy as np

class SwissHolidayCalendar(AbstractHolidayCalendar):
    """Holiday calendar for Zurich Stock Exchange"""
    rules = [
        Holiday("New Year's Day", month=1, day=1),
        Holiday("Berchtold's Day", month=1, day=2),
        Holiday("Good Friday", month=1, day=1, offset=[pd.offsets.Easter(), pd.offsets.Day(-2)]),
        Holiday("Easter Monday", month=1, day=1, offset=[pd.offsets.Easter(), pd.offsets.Day(1)]),
        Holiday("Labour Day", month=5, day=1),
        Holiday("Ascension Day", month=1, day=1, offset=[pd.offsets.Easter(), pd.offsets.Day(39)]),
        Holiday("Whit Monday", month=1, day=1, offset=[pd.offsets.Easter(), pd.offsets.Day(50)]),
        Holiday("Swiss National Day", month=8, day=1),
        Holiday("Christmas Day", month=12, day=25),
        Holiday("St. Stephen's Day", month=12, day=26)
    ]

class SwissBankingCalendar:
    """Zurich financial calendar with tax deadlines for private banking"""
    
    def __init__(self):
        self.holiday_calendar = SwissHolidayCalendar()
        self.business_day = CustomBusinessDay(calendar=self.holiday_calendar)
        
        # Swiss tax deadlines (Cantonal Zurich)
        self.tax_deadlines = {
            "wealth_tax": "2025-03-31",
            "income_tax": "2025-09-30",
            "withholding_tax": "2025-01-31",
            "stamp_duty": "2025-12-31"
        }
    
    def is_business_day(self, date: pd.Timestamp) -> bool:
        """Check if date is a Zurich trading day"""
        return date in pd.date_range(start=date, end=date, freq=self.business_day)
    
    def get_tax_optimization_window(self, tax_type: str) -> tuple:
        """Get 30-day window before tax deadline"""
        deadline = pd.Timestamp(self.tax_deadlines[tax_type])
        return deadline - pd.DateOffset(days=30), deadline
    
    def next_rebalancing_date(self) -> pd.Timestamp:
        """Get next quarterly portfolio rebalancing date"""
        today = pd.Timestamp.today()
        quarter_ends = [
            pd.Timestamp(f"{today.year}-03-31"),
            pd.Timestamp(f"{today.year}-06-30"),
            pd.Timestamp(f"{today.year}-09-30"),
            pd.Timestamp(f"{today.year}-12-31")
        ]
        return min(d for d in quarter_ends if d > today)
    
    def get_banking_days(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
        """Get business days between two dates (Zurich calendar)"""
        return pd.date_range(start, end, freq=self.business_day)
    
    def days_until_deadline(self, tax_type: str) -> int:
        """Business days remaining until tax deadline"""
        deadline = pd.Timestamp(self.tax_deadlines[tax_type])
        today = pd.Timestamp.today()
        return len(self.get_banking_days(today, deadline))

# Example usage
if __name__ == "__main__":
    cal = SwissBankingCalendar()
    print("Next wealth tax optimization window:", cal.get_tax_optimization_window("wealth_tax"))
    print("Days until income tax deadline:", cal.days_until_deadline("income_tax"))
    print("Next rebalancing date:", cal.next_rebalancing_date())