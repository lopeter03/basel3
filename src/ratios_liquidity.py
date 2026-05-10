# ============================
# ratios_liquidity.py
# Basel III Liquidity Coverage Ratio calculations
# ============================

def calc_lcr(hqla, outflows, inflows):
    """
    Baseline Liquidity Coverage Ratio (LCR)
    Formula: HQLA / (Outflows - Inflows) * 100
    Basel III minimum threshold: 100%
    """
    net_outflows = outflows - inflows
    return (hqla / net_outflows) * 100 if net_outflows else 0


def calc_lcr_stress(hqla, stress_outflows, stress_inflows):
    """
    Stressed Liquidity Coverage Ratio (LCR)
    Apply stress scenario outflows and inflows, then recalculate.
    """
    net_stress_outflows = stress_outflows - stress_inflows
    return (hqla / net_stress_outflows) * 100 if net_stress_outflows else 0


def classify_resilience(lcr_base, lcr_stress):
    """
    Resilience classification for liquidity:
    - Resilient: baseline and stress both ≥ 100%
    - Fragile (Compliant Only): baseline ≥ 100% but stress < 100%
    - Non-Resilient: baseline < 100%
    """
    if lcr_base >= 100 and lcr_stress >= 100:
        return "Resilient"
    elif lcr_base >= 100 and lcr_stress < 100:
        return "Fragile (Compliant Only)"
    else:
        return "Non-Resilient"
