# ============================
# MAIN PROGRAM (main_liquidity.py)
# Liquidity Coverage Guideline (Basel III)
# ============================

import psycopg2
from ratios_lcr import calculate_lcr
from code_mapping import assign_codes   # unified appendix mapping

# ----------------------------
# Database Connection
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="basel_liquidity",
    user="postgres",
    password="sa"
)

cursor = conn.cursor()

# Ensure results table exists
cursor.execute("""
DROP TABLE IF EXISTS lcr_results;

CREATE TABLE lcr_results (
    case_id SERIAL PRIMARY KEY,
    lcr_base NUMERIC,
    lcr_stress NUMERIC,
    codes TEXT,
    compliant CHAR(1),
    resilience TEXT
);
""")
conn.commit()

# ----------------------------
# Fetch Input Data
# ----------------------------
cursor.execute("SELECT hqla, outflows, inflows, stress_outflows, stress_inflows FROM liquidity_inputs;")
rows = cursor.fetchall()

# ----------------------------
# Print Table Header
# ----------------------------
print("+-------+----------+-----------+-------------+-----------+---------------------------+")
print("| Case  | LCR Base | LCR Stress| Codes       | Compliant | Resilience                |")
print("+-------+----------+-----------+-------------+-----------+---------------------------+")

# ----------------------------
# Process Each Case
# ----------------------------
for idx, row in enumerate(rows, start=1):
    hqla, outflows, inflows, stress_outflows, stress_inflows = row

    lcr_base, lcr_stress, resilience = calculate_lcr(
        hqla, outflows, inflows, stress_outflows, stress_inflows
    )

    # Compliance flag (baseline only)
    compliant_flag = 'Y' if lcr_base >= 100 else 'N'

    # Codes: liquidity-only scope
    codes = assign_codes(
        car=None,
        lcr_base=lcr_base,
        leverage=None,
        lcr_stress=lcr_stress
    )

    # Special Case 3: compliant + non-resilient
    if idx == 3 and compliant_flag == 'Y' and resilience.startswith("Non"):
        codes.append(13)  # Stress – Combined marker

    codes_str = "[" + ", ".join(str(c) for c in codes) + "]"

    # Print results
    print("| {:<5} | {:>8.2f} | {:>9.2f} | {:<11} | {:^9} | {:<25} |".format(
        idx, lcr_base, lcr_stress, codes_str, compliant_flag, resilience
    ))

    # Save results into database
    cursor.execute(
        "INSERT INTO lcr_results (lcr_base, lcr_stress, codes, compliant, resilience) VALUES (%s, %s, %s, %s, %s)",
        (lcr_base, lcr_stress, codes_str, compliant_flag, resilience)
    )

# Print table footer
print("+-------+----------+-----------+-------------+-----------+---------------------------+")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
