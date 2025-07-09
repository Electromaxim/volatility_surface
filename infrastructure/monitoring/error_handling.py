# infrastructure/monitoring/error_handling.py
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
import requests

class FINMAErrorTracker:
    """Regulatory-compliant error monitoring"""
    FINMA_INCIDENT_CODES = {
        "CALIBRATION_FAILURE": "ART_35b",
        "ARBITRAGE_VIOLATION": "MRM_202",
        "CAPITAL_BREACH": "FRTB_711",
        "DATA_FIDELITY_BREACH": "DQM_115",
        "MODEL_DRIFT": "VAL_303"
    }
    
    # Then modify the notify_finma method:
    def notify_finma(self, event_code: str, description: str):
        """Report regulatory incidents to FINMA"""
        finma_code = self.FINMA_INCIDENT_CODES.get(event_code, "GEN_001")
        
        payload = {
            "event_code": finma_code,  # Use FINMA regulatory code
            "internal_code": event_code,
            "description": description,
            "severity": "HIGH",
            "origin": "volatility_surface_engine"
        }
    FINMA_API_URL = "https://reporting.finma.ch/api/v1/incidents"
    
    def __init__(self, dsn: str, finma_api_key: str):
        sentry_sdk.init(
            dsn=dsn,
            integrations=[AwsLambdaIntegration()],
            traces_sample_rate=1.0
        )
        self.client = sentry_sdk.Hub.current
        self.finma_api_key = finma_api_key
    
    def capture_calibration_error(self, error: Exception, params: dict):
        with self.client.configure_scope() as scope:
            scope.set_tag("sector", "swiss_options")
            scope.set_context("calibration_params", params)
            self.client.capture_exception(error)
            self.notify_finma("CALIBRATION_FAILURE", str(error))
    
    def log_arbitrage_violation(self, surface_id: str):
        self.client.capture_message(
            f"Arbitrage violation in surface {surface_id}",
            level="error"
        )
        self.notify_finma("ARBITRAGE_VIOLATION", surface_id)
    
    def notify_finma(self, event_code: str, description: str):
        """Report regulatory incidents to FINMA"""
        payload = {
            "event_code": event_code,
            "description": description,
            "severity": "HIGH",
            "origin": "volatility_surface_engine"
        }
        
        try:
            response = requests.post(
                self.FINMA_API_URL,
                json=payload,
                headers={"Authorization": f"Bearer {self.finma_api_key}"},
                timeout=5
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.client.capture_exception(e)
    
    def log_data_fidelity_alert(self, score: float, threshold=0.85):
        if score < threshold:
            self.client.capture_message(
                f"Low data fidelity score: {score:.2f}",
                level="warning"
            )
    
    def log_capital_breach(self, charge: float, limit: float):
        if charge > limit:
            self.client.capture_message(
                f"Capital breach: {charge:.2f} CHF > {limit:.2f} CHF",
                level="error"
            )
            self.notify_finma("CAPITAL_BREACH", 
                             f"Charge: {charge:.2f}, Limit: {limit:.2f}")
                             
                             
    