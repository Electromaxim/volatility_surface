# scripts/generate_diagrams.py
import os
import sys
import yaml
import mermaid.cli as mmdc

def generate_compliance_diagram():
    diagram = """
    graph TD
        A[FINMA Compliance] --> B[Model Governance]
        A --> C[Risk Management]
        A --> D[Data Integrity]
        B --> B1[ART_35b]
        B --> B2[VAL_303]
        C --> C1[FRTB_711]
        D --> D1[DQM_115]
        D --> D2[BA_47]
    """
    mmdc.execute('-i', '-o', 'compliance_diagram.svg', diagram)

def generate_data_lineage():
    diagram = """
    flowchart LR
        Client[UHNW Client] -->|Encrypted| S(SIX API)
        S --> V[Validation]
        V -->|Anonymized| C[Calibration]
        C -->|Encrypted| R[Risk Engine]
        R -->|Secure| A[Audit Trail]
        A -->|XBRL| F[FINMA]
    """
    mmdc.execute('-i', '-o', 'data_lineage.svg', diagram)

def generate_all_diagrams():
    config = yaml.safe_load(open('../config/diagram_config.yaml'))
    if config.get('generate_compliance', True):
        generate_compliance_diagram()
    if config.get('generate_lineage', True):
        generate_data_lineage()

if __name__ == "__main__":
    generate_all_diagrams()

