✅ FIXED & EASY Code – I corrected both issues:
	•	Fixed the summary NameError (moved save inside the loop)
	•	Fixed blank charts (added plt.show() properly + tight_layout)

Copy & Run these corrected sections one by one in VS Code
1. First — Make sure imports and df_filt are ready
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Make sure these are already run from previous cells
print("df_filt shape:", df_filt.shape)
print("lifestage_mapped unique:", df_filt['lifestage_mapped'].unique())

2. Fixed Summary Statistics + Excel Save
ratios = ['grossmargin', 'netmargin', 'netsales', 'totalassets']

for ratio in ratios:
    print(f"\n=== Summary for {ratio} by Lifestage_Mapped ===")
    
    summary = df_filt.groupby('lifestage_mapped')[ratio].describe().round(4)
    print(summary)
    
    # FIXED: Save inside the loop
    save_path = os.path.join(os.path.dirname(df_path), f"{ratio}_summary_by_lifestage.xlsx")
    summary.to_excel(save_path)
    print(f"✅ Saved: {save_path}")

3. Fixed Charts (Box Plot + Histogram) – Now they will show
for ratio in ratios:
    print(f"\nCreating charts for {ratio}...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Box Plot
    sns.boxplot(data=df_filt, x='lifestage_mapped', y=ratio, ax=axes[0])
    axes[0].set_title(f"Box Plot - {ratio} by Lifestage\n(Shows spread, median, and outliers)")
    axes[0].tick_params(axis='x', rotation=45)
    
    # Histogram
    sns.histplot(data=df_filt, x=ratio, hue='lifestage_mapped', kde=True, ax=axes[1])
    axes[1].set_title(f"Distribution - {ratio}\n(Shows how values are spread)")
    
    plt.tight_layout()
    
    # Save chart
    chart_path = os.path.join(os.path.dirname(df_path), f"{ratio}_distribution.png")
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    print(f"✅ Chart saved: {chart_path}")
    
    plt.show()          # This should now show the chart in VS Code

Quick Fix Tips for VS Code:
	1	If charts still blank → Add this at the very top of your notebook: %matplotlib inline
	2	
	3	Run cell by cell — Don’t run the whole script at once.
	4	After running the fixed code above, check the folder where your .parquet file is — you should now see Excel files and PNG charts.

Would you like me to also give the fixed Cluster Analysis code with the same improvements?
Just reply “Yes” and I’ll give you the clean fixed version for cluster characteristics by lifestage_mapped.
