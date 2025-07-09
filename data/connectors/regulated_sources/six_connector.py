import requests
import pandas as pd
from datetime import datetime, timedelta

class SixSwissExchangeAPI:
    """Official SIX Swiss Exchange API client for options data"""
    
    BASE_URL = "https://api.six-group.com/api/v1"
    
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        })
    
    def get_option_chain(self, isin: str, date: datetime = None) -> pd.DataFrame:
        """
        Retrieves options chain for Swiss underlyings
        ISIN formats: CH0038863350 (Rothschild), CH0012032048 (Nestlé)
        """
        date_str = date.strftime("%Y-%m-%d") if date else datetime.now().strftime("%Y-%m-%d")
        endpoint = f"{self.BASE_URL}/tradedOptions/v1/optionsChain"
        params = {
            "isin": isin,
            "date": date_str,
            "currency": "CHF"
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return self._parse_response(response.json())
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"SIX API failed: {str(e)}")
    
    def _parse_response(self, data: dict) -> pd.DataFrame:
        """Transforms SIX JSON response to analytics-ready DataFrame"""
        records = []
        for option in data['options']:
            records.append({
                "underlying": option['underlyingIsin'],
                "expiration": datetime.strptime(option['expirationDate'], "%Y-%m-%d"),
                "strike": option['strikePrice'],
                "option_type": "call" if option['optionRight'] == "C" else "put",
                "bid": option['bestBidPrice'],
                "ask": option['bestAskPrice'],
                "volume": option['tradedVolume'],
                "open_interest": option['openInterest'],
                "last_trade": datetime.strptime(option['lastTradeTime'], "%Y-%m-%dT%H:%M:%SZ")
            })
        return pd.DataFrame(records)

# Usage example
if __name__ == "__main__":
    # Get from Rothschild's SIX enterprise account
    api = SixSwissExchangeAPI(api_key="ROTHS_SIX_API_KEY")  
    rothschild_chain = api.get_option_chain("CH0038863350")  # Rothschild & Co AG
    rothschild_chain.to_parquet("data/raw/ROTH_options.parquet")