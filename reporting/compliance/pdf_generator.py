from risk.validation import backtester
from .signer import ComplianceSigner

def generate_finma_documentation():
    with open('finma_documentation.md') as f:
        template = f.read()
    
    signer = ComplianceSigner()
    signature_block = signer.generate_signature_block()
    
    # Insert signature
    final_doc = template.replace("{{ SIGNATURE_BLOCK }}", signature_block)
    
    # Save with timestamp
    filename = f"finma_compliance_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, 'w') as f:
        f.write(final_doc)
    
    return filename



report = backtester.generate_crisis_report("2011_CHF_Peg")
pdf = create_finma_submission(report)