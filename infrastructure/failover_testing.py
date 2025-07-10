import time
from data.connectors.regulated_sources import six_connector, bloomberg_adapter

class SwissDataFailoverTester:
    """Tests SIX → Bloomberg failover for market outages"""
    
    FAILOVER_THRESHOLD = 5  # Seconds
    
    def test_failover(self, isin: str):
        # Attempt SIX API
        start_time = time.time()
        try:
            six_data = six_connector.SixSwissExchangeAPI().get_option_chain(isin)
            return {"source": "SIX", "latency": time.time() - start_time}
        except ConnectionError:
            failover_time = time.time()
            
            # Failover to Bloomberg
            bb_data = bloomberg_adapter.BloombergAdapter().get_option_chain(isin)
            return {
                "source": "Bloomberg",
                "failover_latency": time.time() - failover_time,
                "total_latency": time.time() - start_time
            }
    
    def execute_outage_simulation(self, duration: int = 300):
        """Simulates 5-minute SIX outage"""
        from unittest.mock import patch
        with patch('data.connectors.regulated_sources.six_connector.requests') as mock_requests:
            mock_requests.get.side_effect = ConnectionError
            results = [self.test_failover("CH0038863350") for _ in range(100)]
        
        failover_success = all(r['source'] == "Bloomberg" for r in results)
        avg_latency = sum(r['failover_latency'] for r in results) / len(results)
        
        return {
            "failover_success_rate": 1.0 if failover_success else 0.0,
            "avg_failover_latency": avg_latency,
            "pass": failover_success and avg_latency < self.FAILOVER_THRESHOLD
        }