# Content to create
from prefect import flow, task
from scripts.run_calibration import execute as run_calibration
from scripts.daily_frtb import run as daily_frtb
from reporting.compliance.pdf_generator import export as generate_compliance

@task(retries=3, retry_delay_seconds=60)
def calibration_task():
    run_calibration()

@task
def risk_task():
    daily_frtb()

@flow(name="Production Pipeline")
def main_flow():
    calibration_task() >> risk_task() >> generate_compliance()