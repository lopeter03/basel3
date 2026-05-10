# ============================
# Basel III Code Mapping (Appendix Standard)
# ============================

def assign_codes(car=None, lcr_base=None, leverage=None, lcr_stress=None):
    """
    Assign Basel III codes (1–14) based on CAR, LCR baseline, LCR stress, and Leverage.
    Returns a list of codes.
    """

    codes = []

    # --- Capital Adequacy ---
    if car is not None:
        if car >= 10:
            codes.append(1)   # High Capital Adequacy
        elif 8 <= car < 10:
            codes.append(2)   # Borderline Capital
        else:
            codes.append(3)   # Undercapitalized

    # --- Liquidity Coverage (Baseline) ---
    if lcr_base is not None:
        if lcr_base >= 120:
            codes.append(4)   # Liquidity Surplus
        elif 100 <= lcr_base < 120:
            codes.append(5)   # Balanced Liquidity
        else:
            codes.append(6)   # Liquidity Shortfall

    # --- Leverage Ratio ---
    if leverage is not None:
        if leverage >= 5:
            codes.append(7)   # Conservative Leverage
        elif 3 <= leverage < 5:
            codes.append(8)   # Moderate Leverage
        else:
            codes.append(9)   # Excessive Leverage

    # --- Stress Conditions ---
    if car is not None and lcr_base is not None:
        if car < 8 and lcr_base < 100:
            codes.append(13)  # Stress – Combined

    if lcr_stress is not None and lcr_base is not None:
        if lcr_base - lcr_stress >= 20:
            codes.append(10)  # Stress – Market Downturn
        if lcr_stress < 100 and lcr_base >= 100:
            codes.append(12)  # Stress – Funding Squeeze

    # --- Recovery ---
    if car is not None and lcr_base is not None:
        if car >= 8 and lcr_base >= 100 and (lcr_stress is not None and lcr_stress >= 100):
            codes.append(14)  # Recovery/Resolution

    return codes
