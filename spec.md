
# Basel III Compliance Dashboard Automation - Project Specification  

## 📑 Scope  
- **Capital Adequacy Ratio (CAR)** → Must be ≥ 8%  
- **Liquidity Coverage Ratio (LCR)** → Must be ≥ 100%  
- **Leverage Ratio (LR)** → Must be ≥ 3%  
- **Stress Scenarios** → Market Downturn, Credit Shock, Funding Squeeze, Combined Stress  
- **Recovery/Resolution** → Ratios restored ≥ thresholds  

---

## ⚙️ Program Modules  
- `main_dashboard.py` → Consolidates CAR, LCR, LR into one CFO‑ready table  
- `ratios_car.py` → CAR baseline + stress calculations  
- `ratios_liquidity.py` → LCR baseline + stress calculations  
- `ratios_leverage.py` → LR baseline + stress calculations  
- `code_mapping.py` → Basel III codes (1–14) assignment logic  

---

## 📊 Outputs  
- **Compliance Flag** → Y/N based on baseline thresholds  
- **Resilience Classification** →  
  - Resilient → Baseline and stress both pass  
  - Fragile (Compliant Only) → Baseline passes but stress fails  
  - Non‑Resilient → Baseline fails outright  
- **Basel III Codes [1–14]** → Numeric identifiers for CAR, LCR, LR, stress, and recovery outcomes  
- **CFO‑Ready Table** → Consolidated output for executive clarity  

---

## 🗂 References  
For detailed explanations, see documents in `/docs`:  
- PostgreSQL Installation Guideline (Basel III)  
- Schema Setup Guideline (Basel III)  
- Capital Adequacy & Leverage Guideline (Basel III)  
- Liquidity Coverage Guideline (Basel III)  
- Ratio Automation Guideline (Basel III)  
- Dashboard Summary (Basel III)  

---
