# Add to existing class
THRESHOLDS = {"tier1": 0.9, "tier2": 0.7}

def detect_breach(self, access_log) -> dict:
    score = self.model.predict([access_log])[0]
    if score > self.THRESHOLDS[access_log['tier']]:
        return {"action": "FREEZE_ACCESS", "level": "CRITICAL"}