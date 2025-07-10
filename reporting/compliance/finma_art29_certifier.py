from cryptography.hazmat.primitives import serialization
from reporting.compliance.signer import ComplianceSigner
import requests

class FINMAArt29Certifier:
    """Handles FINMA Article 29 pre-submission certification"""
    
    FINMA_API_URL = "https://api.finma.ch/v1/certification"
    
    def __init__(self, private_key_path: str):
        self.signer = ComplianceSigner(private_key_path)
    
    def generate_certification_package(self) -> dict:
        """Compiles FINMA submission package"""
        return {
            "system_overview": self._generate_system_overview(),
            "validation_results": self._load_validation_records(),
            "attestation": self._generate_attestation()
        }
    
    def _generate_system_overview(self) -> str:
        with open('reporting/compliance/finma_documentation.md') as f:
            return f.read()
    
    def _load_validation_records(self) -> dict:
        from risk.validation.backtester import get_validation_results
        return get_validation_results()
    
    def _generate_attestation(self) -> str:
        config_hash = self.signer.generate_config_hash()
        return f"""
        FINMA ART. 29 CERTIFICATION
        System: Rothschild Volatility Engine
        Version: 2.1
        Config Hash: {config_hash}
        Valid Through: 2026-12-31
        """
    
    def submit_to_finma(self, package: dict) -> str:
        """Submits via FINMA API with Zurich IP restriction"""
        headers = {"X-Zurich-Origin": "true", "Content-Type": "application/xbrl"}
        response = requests.post(
            self.FINMA_API_URL,
            json=package,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()['submission_id']