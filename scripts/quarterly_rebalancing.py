from infrastructure.utils.swiss_calendar import SwissBankingCalendar

cal = SwissBankingCalendar()
if pd.Timestamp.today() == cal.next_rebalancing_date():
    execute_rebalancing()