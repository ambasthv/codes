import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
from scipy.stats import mstats
import warnings
import os
import plotly.express as px
from pathlib import Path



sns.set_theme(style="whitegrid", palette="Set2", font_scale=1.05)

warnings.filterwarnings("ignore")

df_path = "C:\Vivek Ambastha\\s\\B"

# Read data
df_main = "lean Data V1.parquet"
df_main = pd.read_parquet(os.path.join(df_path, df_main)) 
print(f"Original data shape: {df_main.shape}")

# Filter ID/BSD
df_filt = df_main[df_main['model_routing'] == 'ID / BSD']
print(f"Filtered df_filt shape: {df_filt.shape}")
### Check required columns
required_cols = [
    "cif",
    "grade_date",
    "totalassets",
    "netsales",
    "grossprofit",
    "netprofit",
    "lifestage",
    "balance",
    "rbs",
    "commitment"
]

missing_cols = [c for c in required_cols if c not in df_filt.columns]

print("Missing columns:", missing_cols)
print("All required columns present:", len(missing_cols) == 0)

# LIFESTAGE MAPPING (Updated)
lifestage_mapping = {
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Mid stage": "Mid Stage",
    "Non-Niche": "Other",
    "Non-niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other",
    "None": "None"
}

#  Apply Mapping 
df = df_filt.copy()        

# Clean original column first
df['lifestage_original'] = df['lifestage'].astype(str)
df['lifestage_clean'] = df['lifestage'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

# Apply mapping
df['lifestage_mapped'] = df['lifestage_clean'].map(lifestage_mapping)

# Fill unmapped values with "Other"
df['lifestage_mapped'] = df['lifestage_mapped'].fillna("Other")

print("Lifestage Mapping Applied Successfully!")
print("\nDistribution of lifestage_mapped:")
print(df['lifestage_mapped'].value_counts())
