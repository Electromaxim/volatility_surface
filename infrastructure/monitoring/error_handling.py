import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

class FINMAErrorTracker:
    """Regulatory-compliant error monitoring"""
    
    def __init__(self, dsn: str):
        sentry_sdk.init(
            dsn=dsn,
            integrations=[AwsLambdaIntegration()],
            traces_sample_rate=1.0
        )
        self.client = sentry_sdk.Hub.current
        
    def capture_calibration_error(self, error: Exception, params: dict):
        """Log calibration failures with context"""
        with self.client.configure_scope() as scope:
            scope.set_tag("sector", "swiss_options")
            scope.set_context("calibration_params", params)
            self.client.capture_exception(error)
            
    def log_arbitrage_violation(self, surface_id: str):
        """Alert on arbitrage detection"""
        self.client.capture_message(
            f"Arbitrage violation in surface {surface_id}",
            level="error"
        )