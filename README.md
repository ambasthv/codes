import pandas as pd
import numpy as np

# =============================================================================
# CREATE MANUAL GROSS & NET MARGIN (with _MANUALcalc suffix)
# =============================================================================

def create_gross_margin_manual(df):
    """Calculate Gross Margin manually and name it grossmargin_MANUALcalc"""
    df = df.copy()
    
    numerator = df['netsales'] - df['costofgoodssold']
    
    df['grossmargin_MANUALcalc'] = np.where(
        df['netsales'] == 0, 
        np.nan,                                      # Handle divide by zero
        numerator / df['netsales']
    )
    
    print("✅ Gross Margin Manual created → grossmargin_MANUALcalc")
    return df


def create_net_margin_manual(df):
    """Calculate Net Margin manually and name it netmargin_MANUALcalc"""
    df = df.copy()
    
    df['netmargin_MANUALcalc'] = np.where(
        df['netsales'] == 0, 
        np.nan,                                      # Handle divide by zero
        df['netprofit'] / df['netsales']
    )
    
    print("✅ Net Margin Manual created → netmargin_MANUALcalc")
    return df


# ====================== RUN THE FUNCTIONS ======================
df = create_gross_margin_manual(df)
df = create_net_margin_manual(df)

# ====================== QUICK CHECK ======================
print("\n=== Summary of Manually Created Ratios ===")
print(df[['grossmargin_MANUALcalc', 'netmargin_MANUALcalc']].describe().round(4))

print("\nNew Columns Added:")
print("- grossmargin_MANUALcalc")
print("- netmargin_MANUALcalc")