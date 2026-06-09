# ====================== LIFESTAGE MAPPING (Updated) ======================
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

# ====================== Apply Mapping ======================
df = df_filt.copy()                     # Create new df from df_filt

# Clean original column first
df['lifestage_original'] = df['lifestage'].astype(str)
df['lifestage_clean'] = df['lifestage'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

# Apply mapping
df['lifestage_mapped'] = df['lifestage_clean'].map(lifestage_mapping)

# Fill unmapped values with "Other"
df['lifestage_mapped'] = df['lifestage_mapped'].fillna("Other")

print("✅ Lifestage Mapping Applied Successfully!")
print("\nDistribution of lifestage_mapped:")
print(df['lifestage_mapped'].value_counts())