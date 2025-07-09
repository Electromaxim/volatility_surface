rothschild-vol-surface/
├── config/
│   ├── params.yaml                 # MUST-HAVE: Financial parameters
│   └── stress_scenarios.yaml       # FRTB-compliant scenarios
├── data_ingestion/
│   ├── sample_loader.py            # MUST-HAVE: Mock data generator
│   ├── api_connectors.py           # Real market data connectors
│   └── spark_ingest.scala          # Batch processing
├── surface_construction/
│   ├── black_scholes.py            # MUST-HAVE: Core pricing
│   ├── heston_calibrator.py        # MUST-HAVE: Stochastic model
│   └── nn_pricing/
│       ├── dataset.py              # Data processing
│       └── model.py                # PyTorch model
├── risk/
│   ├── frtb.py                     # MUST-HAVE: Capital charges
│   └── var_engine.py               # Value-at-Risk
├── tests/
│   ├── test_black_scholes.py       # MUST-HAVE: Validation
│   ├── test_heston.py
│   └── test_frtb.py
├── notebooks/
│   ├── surface_visualization.ipynb # Analysis
│   └── frtb_reporting.ipynb        # Compliance
├── infrastructure/
│   ├── main.tf                     # AWS Terraform
│   └── lambda_calibration.tf       # Serverless
├── scripts/
│   └── run_calibration.sh          # Execution script
└── README.md                       # Project overview