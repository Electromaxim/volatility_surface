# In risk/exposure/var_engine.py
with open('../config/risk_limits.yaml') as f:
    limits = yaml.safe_load(f)

def check_var_breach(desk: str, var_value: float):
    desk_limit = limits['desk_limits'][desk]['var_95_1d']
    if var_value > desk_limit:
        tracker = FINMAErrorTracker()
        tracker.log_capital_breach(var_value, desk_limit)