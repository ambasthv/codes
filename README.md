this is good for lifestage, but now i want it by 1205_niche_desc.
so now you create this as attached, 
no need to do any changes in cell1 code, i will keep it as it is, just cell 2 update or re-write lke you did just above for lifestage.

i already have mapping done as below, 

cell 1 
# Niche Mapping
niche_mapping = {
    "SOFTWARE": "SOFTWARE",
    "LIFE SCIENCE": "LIFE SCIENCE",
    "HARDWARE": "HARDWARE",
    "NNO": "OTHER",
    "ERI": "OTHER",
    "ENERGY AND RESOURCE INNOVATION": "OTHER",
    "HEALTHCARE": "OTHER",
    "None": "OTHER",
    "RELIGIOUS": "OTHER",
    "REAL ESTATE": "OTHER",
    "NON-NICHE": "OTHER",
    "VENTURE CAPITAL": "OTHER",
    "PRIVATE BANK": "OTHER",
    "RELIGIOUS LENDING": "OTHER",
    "PREMIUM WINE": "OTHER",
    "PRIVATE EQUITY FUND": "OTHER"
}

# Apply mapping (replace '1205' with your actual column name if different)
df['niche_mapped'] = df['1205_niche_desc'].map(niche_mapping).fillna("OTHER")

print("Niche Mapping Applied Successfully!")
print(df['niche_mapped'].value_counts())

cell 2 (this creates the table i showed you earlier)
import os
import re

print("=== Count per Bin per Niche ===\n")

bin_cols = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

for bin_col in bin_cols:

    if bin_col not in df.columns:
        continue

    count_df = (
        df.groupby([bin_col, 'niche_mapped'])
          .size()
          .unstack(fill_value=0)
          .reset_index()
    )

    count_df.rename(columns={bin_col: 'Bin'}, inplace=True)

    ratio_name = bin_col.replace('_winsor_bin', '')

    count_df.insert(0, 'Ratio', ratio_name)

    print(f"\n{ratio_name} - Counts per Bin:")
    print(count_df)

    output_dir = os.path.dirname(df_path)
    os.makedirs(output_dir, exist_ok=True)

    # Make filename Windows-safe
    safe_ratio_name = re.sub(r'[<>:"/\\|?*]', '_', ratio_name)

    output_path = os.path.join(
        output_dir,
        f"Bin_Counts_{safe_ratio_name}.xlsx"
    )

    count_df.to_excel(output_path, index=False)

    print(f"Saved: {output_path}")

