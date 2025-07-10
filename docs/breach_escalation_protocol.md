# Breach Escalation Protocol  
*Version 1.0 - FINMA Compliant*

## Levels
1. **Level 1 (Desk Alert)**  
   - Threshold: 80% risk limit utilization  
   - Action: Trader notification + hedging recommendation  
   - Timeframe: 15 min response  

2. **Level 2 (Risk Officer)**  
   - Threshold: 95% limit utilization  
   - Action: Position freeze + manual override  
   - Timeframe: 5 min response  

3. **Level 3 (CRO/FINMA)**  
   - Threshold: Breach occurrence  
   - Action:  
     - Auto-submit FINMA incident report  
     - Activate UHNW client protection  
     - Initiate liquidity reserve  
   - Timeframe: Immediate  

## UHNW Client Protocol
| Client Tier | Escalation Path | Actions |
|-------------|-----------------|---------|
| Tier1 (>CHF 100M) | Trader ¡ú Family Office RM ¡ú CRO | 1. Freeze redemptions<br>2. Activate capital protection<br>3. Notify FINMA within 15 min |
| Tier2 (CHF 20-100M) | Trader ¡ú Risk Officer | 1. Tax-optimized hedging<br>2. Quarterly disclosure |

## FINMA Reporting Matrix
| Incident Type | FINMA Code | Report Deadline |
|---------------|------------|----------------|
| Capital Breach | FRTB_711 | 1 business day |
| Data Confidentiality | BA_47 | Immediately |
| Model Failure | ART_35b | 3 business days |