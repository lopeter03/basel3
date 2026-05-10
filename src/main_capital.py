# ============================
# main_capital.py
# Basel III Capital Adequacy & Leverage Guideline
# ============================

import psycopg2
from ratios_car import calc_car, calc_car_stress
from ratios_leverage import calc_leverage, calc_leverage_stress
from code_mapping import assign_codes   # unified appendix mapping

# ----------------------------
# Database Connection
# ----------------------------
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="basel_capital",
    user="postgres",
    password="sa"
)

cursor = conn.cursor()

# Ensure results table exists
cursor.execute("""
DROP TABLE IF EXISTS capital_results;

CREATE TABLE capital_results (
    case_id SERIAL PRIMARY KEY,
    car NUMERIC,
    car_stress NUMERIC,
    leverage NUMERIC,
    leverage_stress NUMERIC,
    codes TEXT,
    compliant CHAR(1),
    resilience TEXT
);
""")
conn.commit()

# ----------------------------
# Fetch Input Data
# ----------------------------
cursor.execute("SELECT equity, rwa, assets, stress_equity, stress_rwa, stress_assets FROM capital_inputs;")
rows = cursor.fetchall()

# ----------------------------
# Print Table Header
# ----------------------------
print("+-------+--------+--------+-----------+-----------+-------------+-----------+---------------------------+")
print("| Case  | CAR %  | CAR St | Lev %     | Lev St    | Codes       | Compliant | Resilience                |")
print("+-------+--------+--------+-----------+-----------+-------------+-----------+---------------------------+")

# ----------------------------
# Process Each Case
# ----------------------------
for idx, row in enumerate(rows, start=1):
    equity, rwa, assets, stress_equity, stress_rwa, stress_assets = row

    car = calc_car(equity, rwa)
    car_stress = calc_car_stress(equity, rwa, stress_equity, stress_rwa)

    leverage = calc_leverage(equity, assets)
    leverage_stress = calc_leverage_stress(equity, assets, stress_equity, stress_assets)

    # Compliance baseline
    compliant_flag = 'Y' if car >= 8 and leverage >= 3 else 'N'

    # Codes
    codes = assign_codes(car=car, lcr_base=None, leverage=leverage, lcr_stress=None)

    # Stress overlays
    if car_stress < 8 or leverage_stress < 3:
        codes.append(13)  # Stress – Combined

    codes_str = "[" + ", ".join(str(c) for c in codes) + "]"

    # Resilience classification
    if car >= 8 and leverage >= 3 and car_stress >= 8 and leverage_stress >= 3:
        resilience = "Resilient"
    elif car >= 8 and leverage >= 3 and (car_stress < 8 or leverage_stress < 3):
        resilience = "Fragile (Compliant Only)"
    else:
        resilience = "Non-Resilient"

    # Print results
    print("| {:<5} | {:>6.2f} | {:>6.2f} | {:>9.2f} | {:>9.2f} | {:<11} | {:^9} | {:<25} |".format(
        idx, car, car_stress, leverage, leverage_stress, codes_str, compliant_flag, resilience
    ))

    # Save results into database
    cursor.execute(
        "INSERT INTO capital_results (car, car_stress, leverage, leverage_stress, codes, compliant, resilience) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (car, car_stress, leverage, leverage_stress, codes_str, compliant_flag, resilience)
    )

# Print table footer
print("+-------+--------+--------+-----------+-----------+-------------+-----------+---------------------------+")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
