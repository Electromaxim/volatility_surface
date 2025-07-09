rothschild-vol-surface/
├── 📂 config/                  # Centralized configuration
│   ├── financial_params.yaml   # Underlyings, maturities, moneyness ranges
│   ├── model_params.yaml       # Heston/SVI bounds, NN hyperparameters
│   ├── risk_limits.yaml        # Desk-level exposure thresholds
│   └── stress_scenarios.yaml   # FRTB scenarios (CHF-specific)
│
├── 📂 data/                    # Data layer
│   ├── connectors/             # Market data integrations
│   │   ├── six_connector.py    # SIX Swiss Exchange API
│   │   ├── bloomberg_adapter.py# Bloomberg Terminal fallback
│   │   └── mock_generator.py   # Synthetic Swiss options data
│   │
│   ├── storage/                # Data persistence
│   │   ├── delta_lake_writer.py# Atomic writes to S3
│   │   └── redis_cache.py      # Low-latency surface caching
│   │
│   └── validation/             # Data quality
│       ├── schema_validator.py # Avro schemas for options data
│       └── drift_monitor.py    # Statistical data drift detection
│
├── 📂 pricing/                 # Core quant models
│   ├── analytic/               # Parametric models
│   │   ├── black_scholes.py    # With CHF dividend handling
│   │   ├── heston_calibrator.py# FINMA-compliant calibration
│   │   └── svi_model.py        # UBS-style surface parameterization
│   │
│   ├── ml_correction/          # AI enhancement
│   │   ├── nn_vol_corrector.py # LSTM residual model
│   │   ├── feature_engineer.py # Moneyness/volume/VIX features
│   │   └── shap_explainer.py   # Model explainability
│   │
│   └── surface_builder/        # Surface construction
│       ├── spline_interpolator.py # Arbitrage-free interpolation
│       └── variance_proxy.py   # Liquid instrument fusion
│
├── 📂 risk/                    # Banking compliance
│   ├── frtb_engine/            # Basel IV implementation
│   │   ├── capital_calculator.py# SA-CCR computations
│   │   ├── stress_applier.py   # Scenario application
│   │   └── finma_adapter.py    # Swiss regulatory adjustments
│   │
│   ├── exposure/               # Risk measurement
│   │   ├── greeks_calculator.py# Portfolio sensitivities
│   │   └── var_engine.py       # Historical/parametric VaR
│   │
│   └── validation/             # Model validation
│       ├── arbitrage_checks.py # Static/dynamic arbitrage tests
│       └── backtester.py       # Historical scenario testing
│
├── 📂 infrastructure/          # Cloud operations
│   ├── aws/                    # Infrastructure-as-Code
│   │   ├── lambda_calibration.tf # Serverless calibration
│   │   ├── emr_cluster.tf      # Spark processing
│   │   └── vpc_network.tf      # Zurich-optimized networking
│   │
│   ├── docker/                 # Containerization
│   │   ├── calibration.Dockerfile # GPU-enabled image
│   │   └── frtb.Dockerfile     # Lightweight risk engine
│   │
│   └── monitoring/             # Observability
│       ├── cloudwatch_setup.py # Metrics dashboard
│       └── alert_manager.py    # Threshold-based alerts
│
├── 📂 reporting/               # Business interfaces
│   ├── powerbi/                # Dashboards
│   │   ├── surface_dashboard.pbit # Live surface visualization
│   │   └── risk_exposure.pbit  # Capital charge analysis
│   │
│   ├── notebooks/              # Analysis
│   │   ├── surface_analysis.ipynb # Interactive exploration
│   │   └── frtb_validation.ipynb  # Compliance reporting
│   │
│   └── compliance/             # Regulatory output
│       ├── pdf_generator.py    # Audit-ready reports
│       └── finma_submitter.py  # FINMA submission format
│
├── 📂 scripts/                 # Operational workflows
│   ├── run_calibration.py      # End-to-end surface generation
│   ├── daily_frtb.py           # Regulatory capital calculation
│   └── deploy_infra.py         # Terraform/CDK deployment
│
├── 📂 tests/                   # Validation suite
│   ├── unit/                   # Isolated tests
│   │   ├── test_black_scholes.py
│   │   ├── test_heston.py
│   │   └── test_nn_corrector.py
│   │
│   └── integration/            # System tests
│       ├── test_calibration_pipeline.py
│       └── test_frtb_engine.py
│
├── 📜 main.py                  # CLI entry point
├── 📜 Makefile                 # Build automation
├── 📜 requirements.txt         # Python dependencies
├── 📜 infrastructure.tfvars    # Environment variables
└── 📜 README.md                # Project documentation