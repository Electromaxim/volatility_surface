# 📈 Volatility Surface Generator & Risk Engine 🇨🇭

**FINMA-aligned Swiss Derivatives Infrastructure**  
*A production-grade volatility surface and options pricing system built for regulated derivatives desks, UHNW client protection, and capital optimization.*

---

![Build](https://img.shields.io/github/actions/workflow/status/vol-surface/ci.yml)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-92%25-green)
![Python](https://img.shields.io/badge/python-3.11-blue)

---

## 🚀 Overview

This project delivers a **modular and scalable solution** for real-time implied volatility modeling, pricing exotic options, capital charge simulation, and Swiss regulatory compliance.  
Built with rigor, deployed with resilience — designed for **high-volume structured products, risk reporting, and regulatory alignment** in Switzerland’s financial ecosystem.

---

## 🔍 Description

A scalable **volatility surface constructor** using real-time options data (SIX/Bloomberg/CBOE/ICE) to model implied vol across strikes and maturities.  
Supports Heston/SVI/NN calibration with FINMA constraints and performs **GPU-accelerated pricing** for exotics (barriers, Asians).  
**Batch-processing enabled via Spark** on 10TB+ historical datasets in AWS.

> Financial Relevance: Directly applicable to derivatives desks, risk management, UHNW portfolio protection, and structured product issuance.

---

## 🧠 Key Features

- **Multi-model Volatility Calibration**
  - Models: `Heston`, `SVI`, `LSTM residual NN`
  - Convexity-preserving interpolation (`Gatheral constraints`)
- **Advanced Pricing & Risk Engine**
  - Basel IV FRTB-SA capital charge models
  - Real-time VaR/ES, scenario shocks (COVID, CHF floor, liquidity crisis)
- **Swiss Market-Specific Logic**
  - FINMA constraints (Art. 35b, 47 BA, FRTB_711)
  - Zurich cantonal tax optimization for UHNW tiers
- **Explainable AI & Drift Detection**
  - SHAP-based transparency for neural models
  - Statistical monitors (KS test, P&L attribution R²)
- **Data Ingestion & Failover**
  - SIX and Bloomberg adapters with latency-aware failover logic
  - Redis caching for 10ms latency on 20+ underlyings

---

## 🧾 Compliance-Centric Design

| Feature                          | Details                                                        |
|----------------------------------|----------------------------------------------------------------|
| FINMA-Ready                      | Built against FINMA Circular 2018/3 with Swiss-specific overrides |
| Audit Automation                 | Signature binding via SHA-256 config hash, 7-year retention      |
| Banking Secrecy Enforcement      | Art. 47 BA compliance with anomaly detection (Isolation Forest) |
| Regulatory Reporting             | XBRL submission, compliance PDF with e-signature block          |
| Tiered UHNW Protections          | Capital shielding logic by AUM thresholds, tax-aware hedging    |

---

## ⚙️ Architecture at a Glance

```bash
volatility-surface/
├── config/           # FINMA stress rules, tax brackets, model bounds
├── data/             # SIX/Bloomberg adapters, fidelity validation, caching
├── pricing/          # Heston, SVI, NN calibration, smile modeling
├── risk/             # FRTB-SA engine, UHNW breach detection, VaR/ES
├── reporting/        # PDF reports, PowerBI dashboards, XBRL exports
├── infrastructure/   # Terraform, Docker, AWS Lambda, EMR
├── scripts/          # End-to-end runners (calibration, daily FRTB)
├── tests/            # Unit, integration, scenario-based testing
└── main.py           # CLI entrypoint to orchestrate full pipeline


```
## ⚙️ Tech Stack

Quant & Pricing: Python, QuantLib, NumPy, SciPy, Monte Carlo

ML & Explainability: PyTorch, SHAP, LSTM, pandas

Infrastructure: AWS (S3, EC2, Lambda, EMR), Terraform, Docker

Compliance & Audit: cryptography, sentry_sdk, PDF/XBRL

Data Layer: Redis, DeltaLake, Avro, Spark


## ⚙️ 🧪 Testing & Validation
✅ 95% backtest scenario coverage (2011 CHF peg, COVID, internal crises)

✅ Arbitrage-free interpolation + FINMA-bound validation

✅ Automated breach escalation triggers (DQM_115, FRTB_711)

✅ Neural model explainability via SHAP visualizer

✅ Failover tests from SIX → Bloomberg (latency < 5s)



## 🧭 Example Workflows

```bash
# Run full volatility surface calibration
python scripts/run_calibration.py --underlying ZURN:SW

# Daily regulatory capital reporting
python scripts/daily_frtb.py --portfolio clients/uhnw_123.json

# Trigger compliance certification package
python reporting/compliance/pdf_generator.py

# Deploy cloud infrastructure
terraform apply -var-file=infrastructure.tfvars
```

## 📊 Dashboards (PowerBI)
| Dashboard Name:                  | Purpose:                                                       |
|----------------------------------|----------------------------------------------------------------|
|  Capital Charge Monitor       | Basel IV charge allocation |
| Volatility Explorer                 | Live visualization of smiles & skews      |
| UHNW Risk Heatmap      | Breach zones, tax efficiency projections |

I keep this project open to external contributions.
## 🔒 Security & Privacy
Encrypted client processing using FIPS 140-3 algorithms

Pseudonymized position aggregation with Laplace noise injection

Behavioral anomaly detection for data access (compliant with Art. 47 BA)


