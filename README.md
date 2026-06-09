# Check if both columns exist
print("lifestage (original) exists?", 'lifestage' in df.columns)
print("lifestage_mapped exists?", 'lifestage_mapped' in df.columns)

print("\nSample data (Original vs Mapped):")
print(df[['lifestage', 'lifestage_mapped']].drop_duplicates().head(15))