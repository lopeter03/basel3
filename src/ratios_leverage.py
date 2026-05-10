# ============================
# ratios_leverage.py
# Basel III Leverage Ratio calculations
# ============================

def calc_leverage(equity, assets):
    """
    Baseline Leverage Ratio
    Formula: Equity / Assets * 100
    Basel III minimum threshold: 3%
    """
    return (equity / assets) * 100 if assets else 0


def calc_leverage_stress(equity, assets, stress_equity, stress_assets):
    """
    Stressed Leverage Ratio
    Apply stress multipliers to equity and assets, then recalculate.
    """
    stressed_equity = equity * stress_equity
    stressed_assets = assets * stress_assets
    return (stressed_equity / stressed_assets) * 100 if stressed_assets else 0


def classify_resilience(leverage_base, leverage_stress):
    """
    Resilience classification for leverage:
    - Resilient: baseline and stress both ≥ 3%
    - Fragile (Compliant Only): baseline ≥ 3% but stress < 3%
    - Non-Resilient: baseline < 3%
    """
    if leverage_base >= 3 and leverage_stress >= 3:
        return "Resilient"
    elif leverage_base >= 3 and leverage_stress < 3:
        return "Fragile (Compliant Only)"
    else:
        return "Non-Resilient"
