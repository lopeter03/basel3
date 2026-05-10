# ============================
# Basel III Dashboard Program
# ============================

import psycopg2

from ratios_car import calc_car, calc_car_stress
from ratios_leverage import calc_leverage, calc_leverage_stress
from ratios_liquidity import calc_lcr, calc_lcr_stress
from code_mapping import assign_codes

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

cursor.execute("""
SELECT equity, rwa, assets, hqla, outflows,
       stress_equity, stress_rwa, stress_assets,
       stress_outflows, stress_inflows
FROM forecast_inputs;
""")

rows = cursor.fetchall()

# ----------------------------
# Print Table Header
# ----------------------------
print("+-------+-------+----------+----------+----------+----------+----------+------------------+-----------+--------------------------+")
print("| Case  | CAR%  | CAR St%  | LCR%     | LCR St%  | Lev%     | Lev St%  | Codes            | Compliant | Resilience               |")
print("+-------+-------+----------+----------+----------+----------+----------+------------------+-----------+--------------------------+")

# ----------------------------
# Process Each Case
# ----------------------------
for idx, row in enumerate(rows, start=1):
    equity, rwa, assets, hqla, outflows, stress_equity, stress_rwa, stress_assets, stress_outflows, stress_inflows = row

    # Baseline ratios
    car = calc_car(equity, rwa)
    lcr = calc_lcr(hqla, outflows, 0)
    leverage = calc_leverage(equity, assets)

    # Stressed ratios
    car_stress = calc_car_stress(equity, rwa, stress_equity, stress_rwa)
    lcr_stress = calc_lcr_stress(hqla, stress_outflows, stress_inflows)
    leverage_stress = calc_leverage_stress(equity, assets, stress_equity, stress_assets)

    # ✅ Compliance based on baseline ratios
    compliant_flag = 'Y' if car >= 8 and lcr >= 100 and leverage >= 3 else 'N'

    # Codes
    codes = assign_codes(car=car, lcr_base=lcr, leverage=leverage, lcr_stress=lcr_stress)
    if compliant_flag == 'N':
        codes.append(13)
    codes_str = "[" + ",".join(str(c) for c in codes) + "]"

    # ✅ Resilience classification (three-tier logic)
    if car >= 8 and lcr >= 100 and leverage >= 3:
        # Baseline compliant
        if car_stress >= 8 and lcr_stress >= 100 and leverage_stress >= 3:
            resilience = "Resilient"
        else:
            resilience = "Fragile (Compliant Only)"
    else:
        # Baseline fails outright
        resilience = "Non-Resilient"

    # Print results
    print("| {:<5} | {:>5.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:<16} | {:^9} | {:<24} |".format(
        idx, car, car_stress, lcr, lcr_stress, leverage, leverage_stress, codes_str, compliant_flag, resilience
    ))

print("+-------+-------+----------+----------+----------+----------+----------+------------------+-----------+--------------------------+")

cursor.close()
conn.close()
