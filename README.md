# Show all columns that contain 'bsd' (case-insensitive)
matches = [col for col in df.columns if 'bsd' in col.lower()]

print(f"Found {len(matches)} columns containing 'bsd':")
for col in matches:
   print(f"  → {col}")
