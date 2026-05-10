
Basel III Compliance Dashboard Automation 

Project Overview  
This repository consolidates Basel III compliance across Capital Adequacy Ratio (CAR), Liquidity Coverage Ratio (LCR), and Leverage Ratio (LR) into a unified dashboard. It provides compliance and resilience flags under both baseline and stress conditions, with standardized Basel III codes (1–14) for traceability.  

Quick View Path:  
If you want to understand the project fast, open **Basel III Dashboard Summary.pptx** in the root directory.  
This 4‑page slide deck gives a visual summary of compliance logic, resilience categories, and Basel III code mapping — perfect for executives or reviewers who need an overview first.  
**Note:** The PPTX is a summary only — for full reproducibility and technical detail, see the guideline docs in `/docs` and the Python modules in `/src`.  

Full Detail Path:  
For technical reproducibility and deeper analysis, explore the guideline docs in /docs and the Python modules in /src.  
These provide schema setup, ratio automation, and the full dashboard logic behind the visuals.  

------------------------------------------------------------

Folder Structure  

BaselIII-Demo/  
│  
├── docs/  
│   ├── PostgreSQL Installation Guideline (Basel III).docx  
│   ├── Schema Setup Guideline (Basel III).docx  
│   ├── Capital Adequacy & Leverage Guideline (Basel III).docx  
│   ├── Liquidity Coverage Guideline (Basel III).docx  
│   ├── Ratio Automation Guideline (Basel III).docx  
│   └── Dashboard Summary (Basel III).docx  
│  
├── src/  
│   ├── code_mapping.py  
│   ├── main.py  
│   ├── main_capital.py  
│   ├── main_dashboard.py  
│   ├── main_liquidity.py  
│   ├── ratios.py  
│   ├── ratios_car.py  
│   ├── ratios_lcr.py  
│   ├── ratios_leverage.py  
│   └── ratios_liquidity.py  
│  
├── README.md  
├── spec.md  
└── Basel III Dashboard Summary.pptx   ← Quick‑view file  

------------------------------------------------------------

Document List  

- PostgreSQL Installation Guideline (Basel III) → Setup instructions for PostgreSQL environment.  
- Schema Setup Guideline (Basel III) → Database schema creation and sample data insertion.  
- Capital Adequacy & Leverage Guideline (Basel III) → CAR and Leverage ratio calculations with stress testing.  
- Liquidity Coverage Guideline (Basel III) → LCR baseline and stress calculations.  
- Ratio Automation Guideline (Basel III) → Unified ratio automation and code mapping logic.  
- Dashboard Summary (Basel III) → Consolidated CFO‑ready dashboard with compliance/resilience flags and Basel III codes.  
- Basel III Dashboard Summary.pptx → Quick‑view slide deck for fast visual understanding of compliance logic and code mapping. (Placed at root for immediate access)  
  **Note:** This PPTX is a summary only — for full reproducibility and technical detail, see docs and code.  

------------------------------------------------------------

Quick Start  

1. Install PostgreSQL using the installation guideline.  
2. Create schema and tables using the schema setup guideline.  
3. Insert demo data as described in the Capital Adequacy, Liquidity, and Ratio Automation guideline docs.  
4. Navigate to the src/ folder:  
   cd src  
5. Run the consolidated dashboard program:  
   python main_dashboard.py  
6. The program will connect to PostgreSQL, calculate CAR, LCR, and Leverage ratios, apply compliance/resilience logic, and print the consolidated CFO‑ready table with Basel III codes.  

------------------------------------------------------------

Sample Output  

+-------+-------+----------+----------+----------+----------+----------+------------------+-----------+--------------------------+  
| Case  | CAR%  | CAR St%  | LCR%     | LCR St%  | Lev%     | Lev St%  | Codes            | Compliant | Resilience               |  
+-------+-------+----------+----------+----------+----------+----------+------------------+-----------+--------------------------+  
| 1     | 12.00 | 11.00    | 120.00   | 110.00   | 5.00     | 4.80     | [1,4,7]          | Y         | Resilient                |  
| 2     | 9.50  | 7.80     | 105.00   | 85.00    | 3.50     | 2.90     | [2,5,8,13]       | Y         | Fragile (Compliant Only) |  
| 3     | 7.00  | 6.00     | 95.00    | 70.00    | 2.80     | 2.20     | [3,6,9,13]       | N         | Non-Resilient            |  
+-------+-------+----------+----------+----------+----------+----------+------------------+-----------+--------------------------+  

------------------------------------------------------------

Key Insight  

- Resilient → Baseline and stress thresholds satisfied.  
- Fragile (Compliant Only) → Baseline thresholds satisfied but stress breaches occur.  
- Non‑Resilient → Fail compliance outright at baseline.  

Numeric Basel III codes (1–14) provide traceability across CAR, LCR, and Leverage, so executives can see not only whether compliance is met but also how resilience holds under stress.  

------------------------------------------------------------

Methodology  

This Basel III mini‑project was completed with the assistance of AI Copilot, which generated much of the coding and draft documentation. The AI provided:  
- Code modules for capital adequacy, liquidity coverage, leverage ratio, and unified dashboard consolidation.  
- Draft documentation across guideline docs, schema setup, and implementation phases.  

My contribution focused on:  
- Integration of components — code, documentation, and results — into a cohesive mini‑project that demonstrates both technical reproducibility and business clarity.  
- Final structuring and document quality checks to ensure the project is presented in a professional and reliable manner.  

------------------------------------------------------------

---