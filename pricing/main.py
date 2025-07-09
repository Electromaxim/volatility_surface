from data.connectors import six_connector
from pricing.analytic import svi_model

chain = six_connector.load("CH0038863350")
surface = svi_model.calibrate(chain).enhance_with_nn()


from infrastructure.monitoring.error_handling import FINMAErrorTracker

tracker = FINMAErrorTracker(
    dsn=os.getenv("SENTRY_DSN"),
    finma_api_key=os.getenv("FINMA_API_KEY")
)

try:
    # main application logic
except Exception as e:
    tracker.capture_calibration_error(e, calibration_params)