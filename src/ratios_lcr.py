# ============================
# ratios_lcr.py
# Specialized for Liquidity Coverage Guideline (Basel III)
# ============================

def calculate_lcr(hqla, outflows, inflows, stress_outflows, stress_inflows):
    """
    Calculate both baseline and stressed LCR.
    Returns: (lcr_base, lcr_stress, resilience_flag)
    """

    # Step 1: Baseline net outflows
    net_outflows_base = outflows - inflows

    # Step 2: Baseline LCR (%)
    lcr_base = (hqla / net_outflows_base) * 100

    # Step 3: Apply stress multipliers
    outflows_stress = outflows * stress_outflows
    inflows_stress = inflows * stress_inflows

    # Step 4: Stressed net outflows
    net_outflows_stress = outflows_stress - inflows_stress

    # Step 5: Stressed LCR (%)
    lcr_stress = (hqla / net_outflows_stress) * 100

    # Step 6: Resilience classification
    if lcr_base >= 100 and lcr_stress >= 100:
        resilience = "Resilient"
    elif lcr_base >= 100 and lcr_stress < 100:
        resilience = "Fragile (Compliant Only)"
    else:
        resilience = "Non-Resilient"

    return lcr_base, lcr_stress, resilience
