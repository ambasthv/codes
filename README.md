# load master db modeling dataset
master_db = pd.read_parquet(master_db_path)   # Use full path directly

# load variable cleaning excels
cleaning_excels = read_cleaning_xlsx(support_path)  # Use full path

print(f"Loaded master data shape: {master_db.shape}")
print("✅ Data and cleaning rules loaded successfully!")