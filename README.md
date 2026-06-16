import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("=== Separate Correlation Analysis: Original vs Winsorized ===\n")

# ====================== 1. Original Ratios ======================
original_ratios = ['grossmargin', 'netmargin', 'sales_to_assets']
available_orig = [col for col in original_ratios if col in df.columns]

if available_orig:
    corr_orig = df[available_orig].corr().round(4)
    
    print("CORRELATION MATRIX - ORIGINAL RATIOS")
    print(corr_orig)
    
    # Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_orig, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.3f')
    plt.title('Correlation - Original Ratios')
    plt.tight_layout()
    plt.show()
    
    corr_orig.to_excel(os.path.join(os.path.dirname(df_path), "Correlation_Original_Ratios.xlsx"))
    print("✅ Original correlation saved\n")

# ====================== 2. Winsorized Ratios ======================
winsor_ratios = ['grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']
available_win = [col for col in winsor_ratios if col in df.columns]

if available_win:
    corr_win = df[available_win].corr().round(4)
    
    print("CORRELATION MATRIX - WINSORIZED RATIOS")
    print(corr_win)
    
    # Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_win, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.3f')
    plt.title('Correlation - Winsorized Ratios')
    plt.tight_layout()
    plt.show()
    
    corr_win.to_excel(os.path.join(os.path.dirname(df_path), "Correlation_Winsorized_Ratios.xlsx"))
    print("✅ Winsorized correlation saved")

print("\n✅ Separate correlation analysis completed!")