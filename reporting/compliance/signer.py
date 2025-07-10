from datetime import datetime
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import yaml

class ComplianceSigner:
    """Generates FINMA-compliant electronic signatures for documentation"""
    
    def __init__(self, private_key_path: str = "config/compliance_key.pem"):
        self.private_key = self._load_private_key(private_key_path)
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        
    def _load_private_key(self, path: str):
        """Loads Rothschild's compliance private key"""
        from cryptography.hazmat.primitives import serialization
        
        try:
            with open(path, "rb") as key_file:
                return serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        except FileNotFoundError:
            # Fallback to generated key for development
            return rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=default_backend()
            )
    
    def generate_config_hash(self) -> str:
        """SHA-256 hash of risk configuration"""
        with open("config/risk_limits.yaml", "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def sign_documentation(self, markdown_content: str) -> bytes:
        """Creates cryptographic signature for compliance docs"""
        return self.private_key.sign(
            markdown_content.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    def generate_signature_block(self) -> str:
        """Formatted signature section for documentation"""
        config_hash = self.generate_config_hash()
        return f"""
## Electronic Certification

```python
# Generated at {self.timestamp}
config_hash = "{config_hash}"
validator = "Rothschild Compliance Engine v2.1"