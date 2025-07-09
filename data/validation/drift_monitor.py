# In data/validation/drift_monitor.py
with open('../../config/risk_limits.yaml') as f:
    config = yaml.safe_load(f)

class DriftMonitor:
    def __init__(self):
        self.drift_threshold = config['monitoring']['drift_threshold']
    
    def check_drift(self, new_data):
        drift_score = self.calculate_drift(new_data)
        if drift_score > self.drift_threshold:
            tracker = FINMAErrorTracker()
            tracker.log_data_drift(drift_score)