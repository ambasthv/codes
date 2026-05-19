import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime

# ====================== ADVANCED STEP 4 ======================
print("\n=== STEP 4: Advanced Visualization - Observation Count by RiskUnitName & Year/Month ===")

# Prepare data
step4_long = (df_filtered.groupby(['YearMonth', 'riskunitname'])['obligor_id']
              .count()
              .reset_index(name='Observation_Count'))

# Convert YearMonth to proper datetime for better plotting
step4_long['Date'] = pd.to_datetime(step4_long['YearMonth'] + '-01')

print(f"Total periods: {step4_long['YearMonth'].nunique()} (from {step4_long['YearMonth'].min()} to {step4_long['YearMonth'].max()})")

# ============== OPTION 1: Best for many years - Line Chart (Recommended) ==============
plt.figure(figsize=(16, 9))

sns.lineplot(data=step4_long, 
             x='Date', 
             y='Observation_Count', 
             hue='riskunitname',
             marker='o',
             markersize=4,
             linewidth=2.5,
             palette="Set2")

plt.title('Observation Count by RiskUnitName Over Time\n(Year-Month from 2006 to 2025)', fontsize=16, pad=20)
plt.xlabel('Grade Date (Year-Month)', fontsize=12)
plt.ylabel('Number of Observations', fontsize=12)

# Format x-axis nicely (show every 6 or 12 months)
plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))      # Major tick every year
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(6))     # Minor tick every 6 months
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)
plt.legend(title='Risk Unit Name', title_fontsize=12, fontsize=11, bbox_to_anchor=(1.02, 1), loc='upper left')

plt.tight_layout()
plt.savefig('temp_charts/step4_advanced_line.png', dpi=300, bbox_inches='tight')
plt.show()

# ============== OPTION 2: Stacked Area Chart (Also Very Good) ==============
plt.figure(figsize=(16, 9))
step4_pivot = step4_long.pivot(index='Date', columns='riskunitname', values='Observation_Count').fillna(0)

step4_pivot.plot(kind='area', stacked=True, figsize=(16,9), alpha=0.85, linewidth=0.5)
plt.title('Stacked Trend - Observation Count by RiskUnitName (2006-2025)', fontsize=16, pad=20)
plt.xlabel('Grade Date', fontsize=12)
plt.ylabel('Observation Count', fontsize=12)
plt.legend(title='Risk Unit Name', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temp_charts/step4_advanced_area.png', dpi=300, bbox_inches='tight')
plt.show()

# ============== OPTION 3: Facet (Small Multiples) - Cleanest for Comparison ==============
g = sns.relplot(data=step4_long, 
                x='Date', 
                y='Observation_Count',
                hue='riskunitname',
                col='riskunitname',
                kind='line',
                col_wrap=2,
                height=4,
                aspect=2.2,
                marker='o',
                facet_kws={'sharey': False})

g.set_axis_labels('Grade Date', 'Observation Count')
g.set_titles("{col_name}")
g.fig.suptitle('Observation Count by Risk Unit Name (Monthly Trend)', fontsize=16, y=1.02)

plt.tight_layout()
plt.savefig('temp_charts/step4_facet.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Step 4 Advanced Charts Generated Successfully!")
print("Three versions saved:")
print("   • step4_advanced_line.png   (Recommended)")
print("   • step4_advanced_area.png")
print("   • step4_facet.png")