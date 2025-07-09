from risk.validation import backtester
report = backtester.generate_crisis_report("2011_CHF_Peg")
pdf = create_finma_submission(report)