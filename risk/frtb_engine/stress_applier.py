# In risk/frtb_engine/stress_applier.py
class StressApplier:
    def __init__(self):
        with open('config/risk_limits.yaml') as f:
            self.scenarios = yaml.safe_load(f)['stress_scenarios']
    
    def apply_scenario(self, scenario_name: str, surface: VolSurface):
        scenario = next(s for s in self.scenarios if s['name'] == scenario_name)
        return surface.apply_shock(**scenario['parameters'])