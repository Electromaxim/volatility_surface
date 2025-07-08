# volatility_surface
Volatility Surface Generator & Options Pricing Engine

Description:
Built a scalable volatility surface constructor using real-time options data (from CBOE/ICE) to model implied volatility across strikes/maturities.
Implemented Heston/NN-based pricing models (PyTorch) for exotic options (Barriers, Asians) and calibrated to market data.
Deployed on AWS with Spark for batch processing of historical surfaces (10TB+ data).
Financial Relevance: Directly applicable to ***’s derivatives desks, risk management, and structured products.

Tech Stack: Python (QuantLib, PyTorch), AWS (S3, EC2), Monte Carlo Methods, Spark
