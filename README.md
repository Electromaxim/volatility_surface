# volatility_surface
Volatility Surface Generator & Options Pricing Engine

Description:
Built a scalable volatility surface constructor using real-time options data (from CBOE/ICE) to model implied volatility across strikes/maturities.
Implemented Heston/NN-based pricing models (PyTorch) for exotic options (Barriers, Asians) and calibrated to market data.
Deployed on AWS with Spark for batch processing of historical surfaces (10TB+ data).
Financial Relevance: Directly applicable to ***’s derivatives desks, risk management, and structured products.

Tech Stack: Python (QuantLib, PyTorch), AWS (S3, EC2), Monte Carlo Methods, Spark


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
