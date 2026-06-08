# === 1. Check if df_filt exists ===
print("Does df_filt exist?", 'df_filt' in globals())

# === 2. Show shape and all column names ===
if 'df_filt' in globals():
    print(f"\nShape of df_filt: {df_filt.shape}")
    print("\n=== All Columns in df_filt ===")
    print(df_filt.columns.tolist())
    
    # === 3. Check specific important columns ===
    important_cols = ['lifestage_mapped', 'lifestage', 'totalassets', 
                     'netsales', 'cif', 'year', 'grade_year', 'model_routing']
    
    print("\n=== Check Important Columns ===")
    for col in important_cols:
        if col in df_filt.columns:
            print(f"✅ '{col}' exists | Unique values: {df_filt[col].nunique()}")
        else:
            print(f"❌ '{col}' is MISSING")
else:
    print("❌ df_filt is not defined yet!")