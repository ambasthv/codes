import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("=== Correlation Sanity Check Between Ratios ===\n")

# Select the ratios you want to check
ratio_columns = ['grossmargin', 'netmargin', 'sales_to_assets',
                 'grossmargin_winsor', 'netmargin_winsor', 'sales_to_assets_winsor']

# Keep only columns that exist
available_ratios = [col for col in ratio_columns if col in df.columns]

# Correlation Matrix
corr_matrix = df[available_ratios].corr().round(4)

print("Correlation Matrix:")
print(corr_matrix)

# Save to Excel
corr_matrix.to_excel(os.path.join(os.path.dirname(df_path), "Ratios_Correlation_Matrix.xlsx"))

# Heatmap Visualization
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='coolwarm', 
            vmin=-1, 
            vmax=1,
            center=0,
            fmt='.3f',
            linewidths=0.5)
plt.title('Correlation Between Financial Ratios (Sanity Check)')
plt.tight_layout()
plt.show()

print("\n✅ Correlation analysis completed and saved!")