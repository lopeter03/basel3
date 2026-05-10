# ============================
# ratios_car.py
# Basel III Capital Adequacy Ratio calculations
# ============================

def calc_car(equity, rwa):
    return (equity / rwa) * 100 if rwa else 0

def calc_car_stress(equity, rwa, stress_equity, stress_rwa):
    return ((equity * stress_equity) / (rwa * stress_rwa)) * 100 if rwa else 0

def classify_resilience(car_base, car_stress):
    """
    Resilience classification for capital adequacy:
    - Resilient: baseline and stress both ≥ 8%
    - Fragile (Compliant Only): baseline ≥ 8% but stress < 8%
    - Non-Resilient: baseline < 8%
    """
    if car_base >= 8 and car_stress >= 8:
        return "Resilient"
    elif car_base >= 8 and car_stress < 8:
        return "Fragile (Compliant Only)"
    else:
        return "Non-Resilient"
