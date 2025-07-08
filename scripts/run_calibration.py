#!/usr/bin/env python3
import yaml
import pandas as pd
from data_ingestion.sample_loader import generate_mock_swiss_data
from surface_construction.heston_calibrator import HestonCalibrator
from risk.frtb import FRTBCalculator

# Load configuration
with open('config/params.yaml', 'r') as f:
    params = yaml.safe_load(f)

# Generate mock data for Roche
print("Generating mock market data for ROG:SW...")
rog_df = generate_mock_swiss_data("ROG:SW")

# Initialize calibrator with Swiss rates
calibrator = HestonCalibrator(
    S=100,  # Current spot price
    r=0.01,  # CHF SARON rate
    q=0.025  # Roche dividend yield
)

# Calibrate with FINMA compliance
print("Calibrating Heston model...")
try:
    result = calibrator.calibrate_with_checks(rog_df)
    print(f"Calibration successful: {result}")
except ValueError as e:
    print(f"Calibration failed FINMA checks: {str(e)}")
    exit(1)

# Calculate FRTB capital charge
print("Computing regulatory capital...")
portfolio = {
    'positions': [{'delta': -420000, 'risk_weight': 0.018}],
    'curvature_positions': [{
        'S': 100, 'K': 95, 'T': 0.75, 'r': 0.01,
        'sigma_base': 0.18, 'sigma_shocked': 0.27,
        'option_type': 'put'
    }]
}
charge = FRTBCalculator.calculate_total_charge(portfolio)
print(f"FRTB Capital Requirement: CHF {charge:,.2f}")

# Save results
rog_df.to_parquet("data/ROG_calibrated.parquet")
print("Results saved to data/ROG_calibrated.parquet")