✅ Here’s clean, robust Python code to handle your Lifestage mapping with proper cleaning.
1. Lifestage Mapping Code
import pandas as pd
import numpy as np

# ====================== LIFESTAGE MAPPING ======================
lifestage_mapping = {
    # Original variations → Clean Mapped Name
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "ET": "Emerging Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "Emerging Tech or ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Non-Niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",     # Typo in original
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other"
}

# Add lowercase + stripped versions for robustness
clean_mapping = {}
for k, v in lifestage_mapping.items():
    cleaned_key = str(k).strip().lower()
    clean_mapping[cleaned_key] = v

print("Mapping Dictionary Created (with cleaning support)")

2. Clean & Map Lifestage in `df_filt`
# ------------------- Clean and Map Lifestage -------------------
def clean_and_map_lifestage(df_filt):
    print("\n=== Cleaning and Mapping Lifestage ===")
    
    # Step 1: Make a copy of original column
    df_filt = df_filt.copy()
    df_filt['lifestage_original'] = df_filt['lifestage'].astype(str)
    
    # Step 2: Clean the column
    df_filt['lifestage_clean'] = (
        df_filt['lifestage']
        .astype(str)
        .str.strip()                    # Remove leading/trailing spaces
        .str.replace(r'\s+', ' ', regex=True)   # Replace multiple spaces with single
        .str.replace(r'["\']', '', regex=True)  # Remove quotes if any
    )
    
    # Step 3: Map using cleaned values (case insensitive)
    df_filt['lifestage_mapped'] = df_filt['lifestage_clean'].str.lower().map(clean_mapping)
    
    # Step 4: Handle unmapped values
    unmapped = df_filt[df_filt['lifestage_mapped'].isna()]['lifestage_clean'].unique()
    if len(unmapped) > 0:
        print(f"⚠️  Unmapped values found ({len(unmapped)} unique):")
        print(unmapped)
        # Optional: Map unknown to 'Other'
        df_filt['lifestage_mapped'] = df_filt['lifestage_mapped'].fillna("Other")
    else:
        print("✅ All values successfully mapped!")
    
    # Final summary
    print("\nMapped Lifestage Distribution:")
    summary = df_filt['lifestage_mapped'].value_counts().sort_values(ascending=False)
    print(summary)
    
    return df_filt

# Run the function
df_filt = clean_and_map_lifestage(df_filt)

3. Verify the Mapping
# ------------------- Verification -------------------
print("\n=== Verification: Sample of Original vs Mapped ===")
verification = df_filt[['lifestage_original', 'lifestage_clean', 'lifestage_mapped']].drop_duplicates().head(20)
print(verification)

# Save verification table
verification.to_excel(f"{output_folder}/Lifestage_Mapping_Verification.xlsx", index=False)

4. Updated Cluster Analysis (Using New Mapped Lifestage)
Since lifestage is the key parameter, let’s re-run cluster profile using the new clean mapped column:
# ------------------- Updated Cluster Profile with Mapped Lifestage -------------------
def updated_cluster_profile(df_filt):
    print("\n=== Updated Cluster Profile by Mapped Lifestage ===")
    
    profile = df_filt.groupby(['lifestage_mapped', 'Cluster']).agg({
        'cif': ['count', 'nunique'],
        'grossmargin': 'mean',
        'netmargin': 'mean',
        'balance': ['mean', 'sum'],
        'netsales': 'mean',
        'totalassets': 'mean'
    }).round(4)
    
    profile.columns = ['_'.join(col).strip() for col in profile.columns.values]
    profile = profile.reset_index()
    
    print(profile.head(15))
    profile.to_excel(f"{output_folder}/Cluster_Profile_by_Mapped_Lifestage.xlsx", index=False)
    
    # Bar plot
    plt.figure(figsize=(14, 8))
    sns.barplot(data=df_filt, x='lifestage_mapped', y='netmargin', hue='Cluster')
    plt.title('Net Margin by Mapped Lifestage and Cluster')
    plt.xticks(rotation=45)
    plt.legend(title='Cluster')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/NetMargin_by_MappedLifestage_Cluster.png", dpi=300)
    plt.show()

updated_cluster_profile(df_filt)

Key Improvements Made:
	•	Handles extra spaces, multiple spaces, quotes
	•	Case-insensitive matching
	•	Preserves original column
	•	Creates clean version + mapped version
	•	Safe fallback to "Other" for unknown values
	•	Full verification table saved

Would you like me to:
	1	Save the updated df_filt as a new parquet file?
	2	Add more columns to the mapping if you found new variations?
	3	Re-run full analysis using lifestage_mapped as the main segment?
Just paste the output of df_filt['lifestage'].unique() if you see any unmapped values, and I’ll refine the mapping.
