# Count of unique CIFs by lifestage_mapped
cif_by_lifestage = (
   df.groupby("lifestage_mapped")["cif"]
   .nunique()
   .sort_values(ascending=False)
   .reset_index()
)
cif_by_lifestage.columns = ["Lifestage", "Unique_CIF_Count"]

# Print in the format you asked for
for _, row in cif_by_lifestage.iterrows():
   print(f"{row['Lifestage']} = {row['Unique_CIF_Count']:,}")
