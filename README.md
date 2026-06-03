col = "lifestage"

if col in df.columns:
   print(f"YES — '{col}' exists in the dataframe")
else:
   print(f"NO — '{col}' does not exist in the dataframe")
