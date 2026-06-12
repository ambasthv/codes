

# =============================================================================
#LOAD PARQUET
# =============================================================================
df_path = "C:\Vivek Ambastha\\02. Data\\01. Master Database\\outputs\\SVB"

# Read data
df_main = "Clean Data V1.parquet"
df_main = pd.read_parquet(os.path.join(df_path, df_main)) 
print(f"Original data shape: {df_main.shape}")

# Filter ID/BSD
df_filt = df_main[df_main['model_routing'] == 'ID / BSD']
print(f"Filtered df_filt shape: {df_filt.shape}")
