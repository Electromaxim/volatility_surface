import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yaml

# Load configuration
with open('../config/params.yaml', 'r') as f:
    params = yaml.safe_load(f)

def generate_mock_swiss_data(underlying: str) -> pd.DataFrame:
    """Generates realistic options data for Rothschild underlyings"""
    np.random.seed(42)  # Reproducibility
    today = datetime.now()
    data = []
    
    for maturity in params['maturities']:
        # Convert to expiration date
        if 'd' in maturity:
            exp_date = today + timedelta(days=int(maturity[:-1]))
        elif 'm' in maturity:
            exp_date = today + timedelta(days=30*int(maturity[:-1]))
            
        for moneyness in params['moneyness']:
            # Realistic Swiss market behavior
            base_vol = 0.15 + np.random.uniform(-0.03, 0.05)
            skew = 0.05 if moneyness < 1.0 else -0.03  # Volatility smile
            iv = base_vol + skew * (1 - moneyness)
            
            # Generate mock quotes
            for option_type in ['call', 'put']:
                data.append({
                    'underlying': underlying,
                    'expiration': exp_date.strftime("%Y-%m-%d"),
                    'strike': 100 * moneyness,  # Assuming spot=100
                    'type': option_type,
                    'bid_iv': iv - 0.005,
                    'ask_iv': iv + 0.005,
                    'volume': np.random.randint(100, 1000)
                })
                
    return pd.DataFrame(data)

# Example usage
if __name__ == "__main__":
    rog_df = generate_mock_swiss_data("ROG:SW")
    rog_df.to_parquet("data/ROG_mock.parquet")