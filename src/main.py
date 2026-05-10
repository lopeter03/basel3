# ============================
# MAIN PROGRAM (main.py)
# ============================

# Import calculation functions from ratios.py
from ratios import calcCAR, calcLCR, calcLeverage

# Import psycopg2 to connect Python with PostgreSQL
import psycopg2

# ----------------------------
# Function: classify_results
# ----------------------------
def classify_results(equity, rwa, hqla, outflows, assets):
    # Step 1: Calculate ratios using helper functions
    car = calcCAR(equity, rwa)              # Capital Adequacy Ratio
    lcr = calcLCR(hqla, outflows)           # Liquidity Coverage Ratio
    leverage = calcLeverage(equity, assets) # Leverage Ratio

    # Step 2: Assign category codes based on Basel III thresholds
    codes = []

    # --- Capital Adequacy ---
    if car >= 0.10:
        codes.append(1)   # High Capital Adequacy
    elif car >= 0.08:
        codes.append(2)   # Borderline Capital
    else:
        codes.append(3)   # Undercapitalized

    # --- Liquidity Coverage ---
    if lcr >= 1.20:
        codes.append(4)   # Liquidity Surplus
    elif lcr >= 1.00:
        codes.append(5)   # Balanced Liquidity
    else:
        codes.append(6)   # Liquidity Shortfall

    # --- Leverage ---
    if leverage >= 0.05:
        codes.append(7)   # Conservative Leverage
    elif leverage >= 0.03:
        codes.append(8)   # Moderate Leverage
    else:
        codes.append(9)   # Excessive Leverage

    # --- Stress Condition (combined breach) ---
    if car < 0.08 and lcr < 1.00:
        codes.append(13)  # Stress – Combined

    # Step 3: Compliance decision
    # Rule: If any breach codes (3,6,9,13) appear → Non-compliant (N)
    # Otherwise → Compliant (Y)
    if any(code in [3,6,9,13] for code in codes):
        compliant_flag = 'N'
    else:
        compliant_flag = 'Y'

    # Step 4: Return results
    return car, lcr, leverage, codes, compliant_flag

# ----------------------------
# Database Connection
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="basel_demo",   # Database name
    user="postgres",         # Username
    password="sa"            # Password
)

cursor = conn.cursor()

# Ensure results table exists with correct columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    case_id SERIAL PRIMARY KEY,
    car NUMERIC,
    lcr NUMERIC,
    leverage NUMERIC,
    codes TEXT,
    compliant CHAR(1)
);
""")
conn.commit()

# ----------------------------
# Fetch Input Data
# ----------------------------
# Pull demo cases from demo_inputs table
cursor.execute("SELECT equity, rwa, assets, hqla, outflows FROM demo_inputs;")
rows = cursor.fetchall()

# ----------------------------
# Print Table Header
# ----------------------------
print("+-------+--------+---------+-------------+----------------+-----------+")
print("| Case  | CAR %  | LCR %   | Leverage %  | Codes          | Compliant |")
print("+-------+--------+---------+-------------+----------------+-----------+")

# ----------------------------
# Process Each Case
# ----------------------------
for idx, row in enumerate(rows, start=1):
    equity, rwa, assets, hqla, outflows = row
    car, lcr, leverage, codes, compliant_flag = classify_results(
        equity, rwa, hqla, outflows, assets
    )

    # Print results in table row format
    print("| {:<5} | {:>6.2f} | {:>7.2f} | {:>11.2f} | {:<14} | {:^9} |".format(
        idx, car*100, lcr*100, leverage*100, str(codes), compliant_flag
    ))

    # Save results into database
    cursor.execute(
        "INSERT INTO results (car, lcr, leverage, codes, compliant) VALUES (%s, %s, %s, %s, %s)",
        (car, lcr, leverage, str(codes), compliant_flag)
    )

# Print table footer
print("+-------+--------+---------+-------------+----------------+-----------+")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
