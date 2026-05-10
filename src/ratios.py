# ratios.py contains only calculation functions
# No database connections or external imports are needed here

def calcCAR(equity, rwa):
    # Capital Adequacy Ratio = Equity / Risk Weighted Assets
    return equity / rwa

def calcLCR(hqla, outflows):
    # Liquidity Coverage Ratio = High Quality Liquid Assets / Net Cash Outflows
    return hqla / outflows

def calcLeverage(equity, assets):
    # Leverage Ratio = Equity / Total Assets
    return equity / assets
